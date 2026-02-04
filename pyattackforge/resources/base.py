"""Base resource helpers."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..transport import AttackForgeTransport


class BaseResource:
    def __init__(self, transport: AttackForgeTransport) -> None:
        self._transport = transport

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._transport.request("GET", path, params=params).data

    def _post(self, path: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._transport.request("POST", path, json=json, params=params).data

    def _put(self, path: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._transport.request("PUT", path, json=json, params=params).data

    def _delete(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        return self._transport.request("DELETE", path, params=params, json=json).data

    def _post_files(self, path: str, files: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Any:
        return self._transport.request("POST", path, files=files, params=params).data
