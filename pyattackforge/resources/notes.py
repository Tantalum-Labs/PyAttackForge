"""Resource: notes."""

from __future__ import annotations

from typing import Any, Dict, Optional
import os
import base64

from .base import BaseResource
from ..exceptions import APIError


class NotesResource(BaseResource):
    """Notes API resource wrapper."""

    def create_remediation_note(self, vulnerability_id: str, payload: Dict[str, Any]) -> Any:
        return self._post(f"/api/ss/vulnerability/{vulnerability_id}/remediationNote", json=payload)

    def update_remediation_note(self, vulnerability_id: str, remediation_note_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(
            f"/api/ss/vulnerability/{vulnerability_id}/remediationNote/{remediation_note_id}",
            json=payload,
        )

    def upload_remediation_note_file(self, vulnerability_id: str, remediation_note_id: str, file_path: str) -> Any:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)
        with open(file_path, "rb") as handle:
            return self._post_files(
                f"/api/ss/vulnerability/{vulnerability_id}/remediationNote/{remediation_note_id}/file",
                files={"file": (os.path.basename(file_path), handle)},
            )

    def download_remediation_note_file(
        self,
        vulnerability_id: str,
        remediation_note_id: str,
        file_name: str,
        *,
        project_id: Optional[str] = None,
        allow_report_fallback: bool = True,
    ) -> Any:
        """
        Download a remediation note file.

        If the SSAPI download endpoint fails, optionally fall back to report data
        (base64) when available.
        """
        try:
            return self._get(
                f"/api/ss/vulnerability/{vulnerability_id}/remediationNote/{remediation_note_id}/file/{file_name}"
            )
        except APIError as exc:
            if not allow_report_fallback:
                raise
            resolved_project_id = project_id or self._find_project_id_for_vulnerability(vulnerability_id)
            if not resolved_project_id:
                raise
            report = self._post(
                f"/api/ss/project/{resolved_project_id}/report/raw",
                json={"excludeBinaries": False, "vulnerabilityIds": [vulnerability_id]},
            )
            file_entry = self._find_remediation_note_file_from_report(
                report, vulnerability_id, remediation_note_id, file_name
            )
            if file_entry is None:
                report = self._post(
                    f"/api/ss/project/{resolved_project_id}/report/raw",
                    json={"excludeBinaries": False},
                )
                file_entry = self._find_remediation_note_file_from_report(
                    report, vulnerability_id, remediation_note_id, file_name
                )
            if isinstance(file_entry, dict):
                payload = file_entry.get("fileBase64")
                if isinstance(payload, str) and payload:
                    try:
                        padded = payload + ("=" * (-len(payload) % 4))
                        return base64.b64decode(padded)
                    except (ValueError, TypeError):
                        pass
            raise exc

    def _find_project_id_for_vulnerability(self, vulnerability_id: str) -> Optional[str]:
        data = self._get("/api/ss/projects-and-vulnerabilities")
        projects = data.get("projects") if isinstance(data, dict) else None
        if not isinstance(projects, list):
            return None
        for project in projects:
            if not isinstance(project, dict):
                continue
            vulns = project.get("project_vulnerabilities")
            if not isinstance(vulns, list):
                continue
            for vuln in vulns:
                if not isinstance(vuln, dict):
                    continue
                vid = vuln.get("vulnerability_id") or vuln.get("id")
                if vid == vulnerability_id:
                    return project.get("project_id") or project.get("id")
        return None

    def _find_remediation_note_file_from_report(
        self,
        report: Any,
        vulnerability_id: str,
        remediation_note_id: str,
        file_name: Optional[str],
    ) -> Optional[Dict[str, Any]]:
        if not isinstance(report, dict):
            return None
        vulnerabilities = report.get("vulnerabilities")
        if not isinstance(vulnerabilities, list):
            return None
        for vuln in vulnerabilities:
            if not isinstance(vuln, dict):
                continue
            vid = vuln.get("id") or vuln.get("vulnerability_id")
            if vid != vulnerability_id:
                continue
            for asset in vuln.get("affected_assets") or []:
                if not isinstance(asset, dict):
                    continue
                for note in asset.get("remediation_notes") or []:
                    if not isinstance(note, dict):
                        continue
                    nid = note.get("id") or note.get("remediation_note_id") or note.get("note_id")
                    if nid != remediation_note_id:
                        continue
                    files = note.get("remediation_note_files") or []
                    if not isinstance(files, list):
                        continue
                    for entry in files:
                        if not isinstance(entry, dict):
                            continue
                        entry_name = entry.get("fileName") or entry.get("file_name") or entry.get("name")
                        if file_name is None or entry_name == file_name:
                            return entry
        return None
