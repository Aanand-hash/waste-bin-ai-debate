import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    model_name: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    s3_bucket: str | None = os.getenv("S3_BUCKET")
    enable_s3: bool = os.getenv("ENABLE_S3", "false").strip().lower() in {"1", "true", "yes", "on"}
    enable_trace: bool = os.getenv("ENABLE_TRACE", "false").strip().lower() in {"1", "true", "yes", "on"}


def load_config() -> AppConfig:
    return AppConfig()
