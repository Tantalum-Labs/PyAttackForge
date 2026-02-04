"""Resource: writeups."""

from __future__ import annotations

from typing import Any, Dict, Optional
import os

from ..cache import TTLCache
from .base import BaseResource


class WriteupsResource(BaseResource):
    """Writeups (library vulnerabilities) API resource wrapper."""

    def __init__(self, transport) -> None:  # type: ignore[override]
        super().__init__(transport)
        self._cache = TTLCache(default_ttl=300.0)

    def get_writeups(self, params: Optional[Dict[str, Any]] = None, *, force_refresh: bool = False) -> Any:
        cache_key = "writeups:list"
        if params is None and not force_refresh:
            cached = self._cache.get(cache_key)
            if cached is not None:
                return cached
        data = self._get("/api/ss/library", params=params)
        if params is None:
            self._cache.set(cache_key, data)
        return data

    def get_writeup_files(self, *, writeup_id: Optional[str] = None, name: Optional[str] = None) -> list[Dict[str, Any]]:
        """
        Fetch file entries for a writeup (library vulnerability).

        The SSAPI returns file storage names under `files[].storage_name` when
        querying `/api/ss/library` with `id` or `name` filters.
        """
        params: Dict[str, Any] = {}
        if writeup_id:
            params["id"] = writeup_id
        if name:
            params["name"] = name
        data = self.get_writeups(params=params, force_refresh=True)
        if isinstance(data, dict):
            candidates = data.get("vulnerabilities") or data.get("library") or data.get("issues") or []
        elif isinstance(data, list):
            candidates = data
        else:
            candidates = []
        if not isinstance(candidates, list):
            return []
        for entry in candidates:
            if not isinstance(entry, dict):
                continue
            if writeup_id and entry.get("id") != writeup_id:
                continue
            if name and entry.get("title") != name:
                continue
            files = entry.get("files")
            if isinstance(files, list):
                return files
        return []

    def create_writeup(self, payload: Dict[str, Any]) -> Any:
        return self._post("/api/ss/library/vulnerability", json=payload)

    def update_writeup(self, writeup_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/library/{writeup_id}", json=payload)

    def upload_writeup_file(self, writeup_id: str, file_path: str) -> Any:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)
        with open(file_path, "rb") as handle:
            return self._post_files(
                f"/api/ss/library/{writeup_id}/file",
                files={"file": (os.path.basename(file_path), handle)},
            )

    def download_writeup_file(self, writeup_id: str, file_name: str) -> Any:
        return self._get(f"/api/ss/library/{writeup_id}/file/{file_name}")
