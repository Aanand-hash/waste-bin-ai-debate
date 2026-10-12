import json
import os
import sys
from datetime import datetime, timezone


def trace_enabled() -> bool:
    value = os.getenv("ENABLE_TRACE", os.getenv("TRACE_ENABLED", "false")).strip().lower()
    return value in {"1", "true", "yes", "on"}


def log_trace(message: str, **context) -> None:
    if not trace_enabled():
        return
    payload = {
        "time": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "context": context,
    }
    print(f"[TRACE] {json.dumps(payload, default=str)}", file=sys.stderr, flush=True)
