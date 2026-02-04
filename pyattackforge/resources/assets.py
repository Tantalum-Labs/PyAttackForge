"""Resource: assets."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..cache import TTLCache
from .base import BaseResource


class AssetsResource(BaseResource):
    """Assets API resource wrapper."""

    def __init__(self, transport) -> None:  # type: ignore[override]
        super().__init__(transport)
        self._cache = TTLCache(default_ttl=300.0)

    def create_asset_in_library(self, payload: Dict[str, Any]) -> Any:
        return self._post("/api/ss/library/asset", json=payload)

    def update_asset_in_library(self, asset_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/library/asset/{asset_id}", json=payload)

    def get_assets(self, params: Optional[Dict[str, Any]] = None, *, force_refresh: bool = False) -> Any:
        cache_key = "assets:list"
        if params is None and not force_refresh:
            cached = self._cache.get(cache_key)
            if cached is not None:
                return cached
        data = self._get("/api/ss/assets", params=params)
        if params is None:
            self._cache.set(cache_key, data)
        return data

    def get_asset_in_library(self, asset_id: str) -> Any:
        return self._get("/api/ss/library/asset", params={"id": asset_id})

    def get_asset_library_assets(self, payload: Dict[str, Any]) -> Any:
        return self._post("/api/ss/library/assets", json=payload)
