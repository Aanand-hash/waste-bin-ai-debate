import json
import time
from typing import Iterable, Iterator

import requests

from app.config import AppConfig
from app.tracing import log_trace


def stream_model_response(prompt: str, model_name: str, system_prompt: str, ollama_host: str) -> Iterator[str]:
    url = f"{ollama_host.rstrip('/')}/api/chat"
    payload = {
        "model": model_name,
        "stream": True,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }

    log_trace("Starting Ollama chat stream", model=model_name, url=url)
    try:
        response = requests.post(url, json=payload, stream=True, timeout=180)
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            if not line.startswith("data:"):
                continue
            payload_data = line[5:].strip()
            if payload_data == "[DONE]":
                break
            try:
                event = json.loads(payload_data)
            except json.JSONDecodeError:
                log_trace("Skipping malformed JSON chunk", chunk=payload_data)
                continue
            delta = event.get("message", {}).get("content", "")
            if delta:
                yield delta
    except requests.RequestException as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc


def generate_completion(prompt: str, system_prompt: str, config: AppConfig) -> str:
    pieces: list[str] = []
    start = time.perf_counter()
    try:
        for chunk in stream_model_response(prompt, config.model_name, system_prompt, config.ollama_host):
            pieces.append(chunk)
    except RuntimeError:
        raise
    elapsed = time.perf_counter() - start
    log_trace("Ollama completion finished", elapsed_seconds=round(elapsed, 3), model=config.model_name)
    return "".join(pieces)
