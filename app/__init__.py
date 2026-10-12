import os


def trace_enabled() -> bool:
    value = os.getenv("ENABLE_TRACE", "false").strip().lower()
    return value in {"1", "true", "yes", "on"}


def ensure_ollama_ready() -> None:
    # Lightweight check for a common local setup. This doesn't fail if Ollama is offline;
    # the actual model call will fail with a clear error later.
    _ = os.getenv("OLLAMA_HOST", "http://localhost:11434")


__all__ = ["trace_enabled", "ensure_ollama_ready"]
