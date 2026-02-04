"""Resource: reports."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .base import BaseResource


class ReportsResource(BaseResource):
    """Reports API resource wrapper."""

    def get_project_report(self, project_id: str, report_type: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get(f"/api/ss/project/{project_id}/report/{report_type}", params=params)

    def get_project_report_data(self, project_id: str, report_type: str, payload: Dict[str, Any]) -> Any:
        return self._post(f"/api/ss/project/{project_id}/report/{report_type}", json=payload)

    def update_exec_summary_notes(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/project/{project_id}/execSummaryNotes", json=payload)
