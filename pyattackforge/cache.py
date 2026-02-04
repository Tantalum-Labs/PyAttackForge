"""Small TTL cache used by the SDK to reduce API calls."""

from dataclasses import dataclass
from typing import Any, Dict, Optional
import time


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class TTLCache:
    def __init__(self, default_ttl: float = 300.0) -> None:
        self._default_ttl = default_ttl
        self._data: Dict[str, CacheEntry] = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._data.get(key)
        if not entry:
            return None
        if entry.expires_at < time.monotonic():
            self._data.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        ttl_value = self._default_ttl if ttl is None else ttl
        self._data[key] = CacheEntry(value=value, expires_at=time.monotonic() + ttl_value)

    def clear(self) -> None:
        self._data.clear()
