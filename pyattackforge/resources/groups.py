"""Resource: groups."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .base import BaseResource


class GroupsResource(BaseResource):
    """Groups API resource wrapper."""

    def create_group(self, payload: Dict[str, Any]) -> Any:
        return self._post("/api/ss/group", json=payload)

    def get_groups(self, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get("/api/ss/groups", params=params)

    def get_group(self, group_id: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get(f"/api/ss/group/{group_id}", params=params)
