"""Resource: users."""

from __future__ import annotations

from typing import Any, Dict, Optional
import urllib.parse

from .base import BaseResource


class UsersResource(BaseResource):
    """Users API resource wrapper."""

    def create_user(self, payload: Dict[str, Any]) -> Any:
        return self._post("/api/ss/user", json=payload)

    def create_users(self, users: Any) -> Any:
        return self._post("/api/ss/users", json=users)

    def get_user(self, user_id: str) -> Any:
        return self._get(f"/api/ss/users/{user_id}")

    def get_users(self, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get("/api/ss/users", params=params)

    def get_user_by_email(self, email: str) -> Any:
        email_value = urllib.parse.quote(email, safe="")
        return self._get(f"/api/ss/users/email/{email_value}")

    def get_user_by_username(self, username: str) -> Any:
        username_value = urllib.parse.quote(username, safe="")
        return self._get(f"/api/ss/users/username/{username_value}")

    def update_user(self, user_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/user/{user_id}", json=payload)

    def activate_user(self, user_id: str) -> Any:
        return self._put(f"/api/ss/user/{user_id}/activate")

    def deactivate_user(self, user_id: str) -> Any:
        return self._put(f"/api/ss/user/{user_id}/deactivate")

    def add_user_to_group(self, payload: Dict[str, Any]) -> Any:
        return self._post("/api/ss/group/user", json=payload)

    def update_user_access_on_group(self, user_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/group/user/{user_id}", json=payload)

    def get_user_groups(self, user_id: str) -> Any:
        return self._get(f"/api/ss/user/{user_id}/groups")

    def get_user_projects(self, user_id: str) -> Any:
        return self._get(f"/api/ss/user/{user_id}/projects")

    def get_user_audit_logs(self, user_id: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get(f"/api/ss/user/{user_id}/auditlogs", params=params)

    def get_user_login_history(self, user_id: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get(f"/api/ss/user/{user_id}/logins", params=params)
