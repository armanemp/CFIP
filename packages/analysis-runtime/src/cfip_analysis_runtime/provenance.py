"""Deterministic provenance identities for analysis execution.

The identity is intentionally content-derived and uses only standard-library
serialization. It is a correlation/integrity identifier, not a replacement
for durable dataset identity or PIT evidence.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime
from typing import Any

from .models import EngineExecutionContext


def _canonical(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.astimezone().isoformat()
    if isinstance(value, dict):
        return {str(key): _canonical(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value


def execution_fingerprint(context: EngineExecutionContext, engine_id: str, version: str) -> str:
    """Return a stable SHA-256 fingerprint for one engine execution request."""
    payload = {
        "engine_id": engine_id,
        "engine_version": version,
        "instrument": context.instrument,
        "timeframe": context.timeframe,
        "as_of": context.as_of.isoformat(),
        "data_revision": context.data_revision,
        "observations": _canonical(list(context.observations)),
        "correlation_id": context.correlation_id,
    }
    encoded = json.dumps(_canonical(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()
