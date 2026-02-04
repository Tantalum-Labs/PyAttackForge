"""Resource: projects."""

from __future__ import annotations

from typing import Any, Dict, Optional, Iterable, List
import os

from ..cache import TTLCache
from .base import BaseResource


class ProjectsResource(BaseResource):
    """Projects API resource wrapper."""

    def __init__(self, transport) -> None:  # type: ignore[override]
        super().__init__(transport)
        self._cache = TTLCache(default_ttl=300.0)

    def create_project(self, payload: Dict[str, Any]) -> Any:
        return self._post("/api/ss/project", json=payload)

    def get_project(self, project_id: str, params: Optional[Dict[str, Any]] = None, *, force_refresh: bool = False) -> Any:
        cache_key = f"project:{project_id}"
        if params is None and not force_refresh:
            cached = self._cache.get(cache_key)
            if cached is not None:
                return cached
        data = self._get(f"/api/ss/project/{project_id}", params=params)
        if params is None:
            self._cache.set(cache_key, data)
        return data

    def get_projects(self, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get("/api/ss/projects", params=params)

    def get_projects_and_vulnerabilities(self, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get("/api/ss/projects-and-vulnerabilities", params=params)

    def update_project(self, project_id: str, payload: Dict[str, Any]) -> Any:
        data = self._put(f"/api/ss/project/{project_id}", json=payload)
        self._cache.set(f"project:{project_id}", data)
        return data

    def archive_project(self, project_id: str) -> Any:
        return self._put(f"/api/ss/project/{project_id}/archive")

    def restore_project(self, project_id: str) -> Any:
        return self._put(f"/api/ss/project/{project_id}/restore")

    def destroy_projects(self, project_ids: Iterable[str], keep_logs: Optional[bool] = None) -> Any:
        payload: Dict[str, Any] = {"project_ids": list(project_ids)}
        if keep_logs is not None:
            payload["keep_logs"] = keep_logs
        return self._delete("/api/ss/project/destroy", json=payload)

    def clone_project(self, project_id: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        return self._post(f"/api/ss/project/{project_id}/clone", json=payload or {})

    def create_scope(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._post(f"/api/ss/project/{project_id}/assets", json=payload)

    def update_scope(self, project_id: str, asset_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/project/{project_id}/asset/{asset_id}", json=payload)

    def get_project_workspace(self, project_id: str) -> Any:
        return self._get(f"/api/ss/project/{project_id}/workspace")

    def upload_workspace_file(self, project_id: str, file_path: str) -> Any:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)
        with open(file_path, "rb") as handle:
            return self._post_files(
                f"/api/ss/project/{project_id}/workspace/file",
                files={"file": (os.path.basename(file_path), handle)},
            )

    def download_workspace_file(self, project_id: str, file_name: str) -> Any:
        return self._get(f"/api/ss/project/{project_id}/workspace/{file_name}")

    def get_project_notes(self, project_id: str) -> Any:
        return self._get(f"/api/ss/project/{project_id}/notes")

    def create_project_note(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._post(f"/api/ss/project/{project_id}/note", json=payload)

    def update_project_note(self, project_id: str, note_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/project/{project_id}/note/{note_id}", json=payload)

    def create_project_workspace_note(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._post(f"/api/ss/project/{project_id}/workspace/note", json=payload)

    def update_project_workspace_note(self, project_id: str, note_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/project/{project_id}/workspace/note/{note_id}", json=payload)

    def get_project_membership_administrators(self, project_id: str) -> Any:
        return self._get(f"/api/ss/project/{project_id}/member-admins")

    def _normalize_member_admin_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if "member_admins" in payload:
            return payload
        return {"member_admins": [payload]}

    def add_project_membership_administrators(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._post(
            f"/api/ss/project/{project_id}/member-admins",
            json=self._normalize_member_admin_payload(payload),
        )

    def update_project_membership_administrators(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(
            f"/api/ss/project/{project_id}/member-admins",
            json=self._normalize_member_admin_payload(payload),
        )

    def remove_project_membership_administrators(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._delete(
            f"/api/ss/project/{project_id}/member-admins",
            json=self._normalize_member_admin_payload(payload),
        )

    def invite_user_to_project(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._post(f"/api/ss/project/{project_id}/invite", json=payload)

    def invite_users_to_project_team(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._post(f"/api/ss/project/{project_id}/team/invite", json=payload)

    def remove_project_team_members(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/project/{project_id}/team/remove", json=payload)

    def update_user_access_on_project(self, project_id: str, user_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/project/{project_id}/access/{user_id}", json=payload)

    def extract_projects_list(self, projects_data: Any) -> List[Dict[str, Any]]:
        if not isinstance(projects_data, dict):
            return []
        projects = projects_data.get("projects") or (projects_data.get("data") or {}).get("projects") or []
        return [proj for proj in projects if isinstance(proj, dict)] if isinstance(projects, list) else []

    def find_project_by_name(
        self, name: str, *, projects_data: Optional[Any] = None, case_insensitive: bool = True
    ) -> Optional[Dict[str, Any]]:
        data = projects_data if projects_data is not None else self.get_projects()
        desired = self._normalize_string(name) if case_insensitive else name
        for project in self.extract_projects_list(data):
            project_name = project.get("project_name") or project.get("name")
            if not isinstance(project_name, str):
                continue
            candidate = self._normalize_string(project_name) if case_insensitive else project_name
            if candidate == desired:
                return project
        return None

    def _normalize_string(self, value: str) -> str:
        return value.strip().lower()
