"""Resource: findings."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence
import os
from datetime import datetime
import time

from ..cache import TTLCache
from .base import BaseResource


class FindingsResource(BaseResource):
    """Findings (vulnerabilities) API resource wrapper."""

    def __init__(self, transport) -> None:  # type: ignore[override]
        super().__init__(transport)
        self._cache = TTLCache(default_ttl=120.0)

    def create_vulnerability(self, payload: Dict[str, Any]) -> Any:
        payload = self._apply_finding_defaults(payload)
        return self._post("/api/ss/vulnerability", json=payload)

    def create_vulnerability_bulk(self, payload: Dict[str, Any]) -> Any:
        payload = self._apply_finding_defaults(payload)
        return self._post("/api/ss/vulnerability/bulk", json=payload)

    def create_vulnerability_with_library(self, payload: Dict[str, Any]) -> Any:
        payload = self._apply_finding_defaults(payload)
        return self._post("/api/ss/vulnerability-with-library", json=payload)

    def get_vulnerabilities(self, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get("/api/ss/vulnerabilities", params=params)

    def get_vulnerability(self, vulnerability_id: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get(f"/api/ss/vulnerability/{vulnerability_id}", params=params)

    def get_project_vulnerabilities(self, project_id: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get(f"/api/ss/project/{project_id}/vulnerabilities", params=params)

    def get_project_vulnerabilities_all(self, project_id: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []
        params = dict(params or {})
        skip = int(params.get("skip", 0))
        limit = int(params.get("limit", 500))
        while True:
            params.update({"skip": skip, "limit": limit})
            data = self.get_project_vulnerabilities(project_id, params=params)
            page = self._extract_list(data, ["vulnerabilities"])  # best-effort
            if not page:
                break
            items.extend(page)
            if len(page) < limit:
                break
            skip += limit
        return items

    def find_project_vulnerability_by_title(
        self, project_id: str, title: str, *, include_pending: bool = True
    ) -> Optional[Dict[str, Any]]:
        desired = self._normalize_title(title)
        findings = self.get_project_vulnerabilities_all(project_id)
        if include_pending:
            pending = self.get_project_vulnerabilities_all(project_id, params={"pendingVulnerabilities": True})
            if pending:
                seen: set = set()
                merged: List[Dict[str, Any]] = []
                for finding in findings + pending:
                    key = finding.get("vulnerability_id") or finding.get("id")
                    if key in seen:
                        continue
                    seen.add(key)
                    merged.append(finding)
                findings = merged
        for finding in findings:
            candidate = self._extract_title(finding)
            if candidate and self._normalize_title(candidate) == desired:
                return finding
        return None

    def find_project_vulnerability_by_library_id(
        self, project_id: str, library_id: str, *, include_pending: bool = True
    ) -> Optional[Dict[str, Any]]:
        if not library_id:
            return None
        findings = self.get_project_vulnerabilities_all(project_id)
        if include_pending:
            pending = self.get_project_vulnerabilities_all(project_id, params={"pendingVulnerabilities": True})
            if pending:
                seen: set = set()
                merged: List[Dict[str, Any]] = []
                for finding in findings + pending:
                    key = finding.get("vulnerability_id") or finding.get("id")
                    if key in seen:
                        continue
                    seen.add(key)
                    merged.append(finding)
                findings = merged
        for finding in findings:
            candidate = self._find_first_value(
                finding,
                (
                    "library_id",
                    "libraryId",
                    "vulnerability_library_id",
                    "vulnerabilityLibraryId",
                    "vulnerability_library_issue_id",
                    "vulnerabilityLibraryIssueId",
                    "writeup_id",
                    "writeupId",
                ),
            )
            if candidate == library_id:
                return finding
        return None

    def get_vulnerabilities_by_asset_name(self, asset_name: str, params: Optional[Dict[str, Any]] = None) -> Any:
        params = dict(params or {})
        params["name"] = asset_name
        return self._get("/api/ss/vulnerabilities/asset", params=params)

    def update_vulnerability(self, vulnerability_id: str, payload: Dict[str, Any]) -> Any:
        if "project_id" in payload and "projectId" not in payload:
            payload = dict(payload)
            payload["projectId"] = payload.pop("project_id")
        return self._put(f"/api/ss/vulnerability/{vulnerability_id}", json=payload)

    def update_vulnerability_with_library(self, vulnerability_id: str, payload: Dict[str, Any]) -> Any:
        if "project_id" in payload and "projectId" not in payload:
            payload = dict(payload)
            payload["projectId"] = payload.pop("project_id")
        return self._put(f"/api/ss/vulnerability-with-library/{vulnerability_id}", json=payload)

    def update_vulnerability_slas(self, payload: Dict[str, Any]) -> Any:
        return self._put("/api/ss/vulnerabilities/sla", json=payload)

    def update_linked_projects_on_vulnerabilities(self, payload: Dict[str, Any]) -> Any:
        return self._put("/api/ss/vulnerabilities/projects", json=payload)

    def get_vulnerability_revision_history(self, vulnerability_id: str) -> Any:
        return self._get(f"/api/ss/vulnerability/{vulnerability_id}/revision-history")

    def upload_vulnerability_evidence(
        self,
        vulnerability_id: str,
        file_path: str,
        *,
        keep_last: Optional[int] = 2,
        project_id: Optional[str] = None,
        dedupe: bool = False,
    ) -> Dict[str, Any]:
        """
        Upload evidence to a vulnerability.

        keep_last defaults to 2 (FIFO, keep most recent). Set keep_last=None to disable FIFO.
        If dedupe=True, skip upload when an existing evidence entry matches the filename.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)
        file_name = os.path.basename(file_path)
        resolved_project_id = project_id
        if keep_last is not None and project_id is None:
            resolved_project_id = self._resolve_project_id_for_vulnerability(vulnerability_id)
        if dedupe:
            entries = self._get_vulnerability_evidence_entries(
                vulnerability_id, project_id=resolved_project_id
            )
            match = self._find_matching_evidence_entry(entries, file_name)
            if match is not None:
                result: Dict[str, Any] = {"action": "noop", "existing": match}
                if keep_last is not None:
                    deletions = self._enforce_vulnerability_evidence_fifo(
                        vulnerability_id, keep_last, project_id=resolved_project_id
                    )
                    result["deleted"] = deletions
                return result
        with open(file_path, "rb") as handle:
            upload_result = self._post_files(
                f"/api/ss/vulnerability/{vulnerability_id}/evidence",
                files={"file": (file_name, handle)},
            )
        if keep_last is None:
            return {"upload": upload_result}
        deletions = self._enforce_vulnerability_evidence_fifo(
            vulnerability_id, keep_last, project_id=resolved_project_id
        )
        return {"upload": upload_result, "deleted": deletions}

    def download_vulnerability_evidence(self, vulnerability_id: str, file_name: str) -> Any:
        return self._get(f"/api/ss/vulnerability/{vulnerability_id}/evidence/{file_name}")

    def delete_vulnerability_evidence(self, vulnerability_id: str, file_name: str) -> Any:
        return self._delete(f"/api/ss/vulnerability/{vulnerability_id}/evidence/{file_name}")

    def upsert_finding_by_title(
        self,
        *,
        project_id: str,
        title: str,
        affected_assets: Sequence[Any],
        create_payload: Dict[str, Any],
        update_payload: Optional[Dict[str, Any]] = None,
        use_library: bool = False,
        validate_asset_agnostic: bool = True,
    ) -> Dict[str, Any]:
        """
        Deduplicate findings by title (case-insensitive, trimmed) within a project.
        If a matching finding exists, append missing affected assets and update.
        Otherwise, create a new finding using the provided payload.
        When validate_asset_agnostic is True, reject payloads that embed asset names
        outside of affected_assets.
        """
        if validate_asset_agnostic:
            asset_names = [str(value) for value in affected_assets if isinstance(value, str)]
            if asset_names:
                self.assert_asset_agnostic(create_payload, asset_names, enabled=True)
                if update_payload:
                    self.assert_asset_agnostic(update_payload, asset_names, enabled=True)
        normalized_title = self._normalize_title(title)
        findings = self.get_project_vulnerabilities_all(project_id)
        pending = self.get_project_vulnerabilities_all(project_id, params={"pendingVulnerabilities": True})
        if pending:
            seen: set = set()
            merged: List[Dict[str, Any]] = []
            for finding in findings + pending:
                key = finding.get("vulnerability_id") or finding.get("id")
                if key in seen:
                    continue
                seen.add(key)
                merged.append(finding)
            findings = merged
        match = None
        for finding in findings:
            candidate = self._extract_title(finding)
            if candidate and self._normalize_title(candidate) == normalized_title:
                match = finding
                break
        if not match:
            if use_library:
                return {"action": "create", "result": self.create_vulnerability_with_library(create_payload)}
            return {"action": "create", "result": self.create_vulnerability(create_payload)}

        existing_assets = self._extract_asset_names_from_finding(match)
        new_assets = self._extract_asset_names(affected_assets)
        missing = sorted(new_assets - existing_assets)
        if not missing:
            return {"action": "noop", "existing": match}

        merged = sorted(existing_assets.union(new_assets))
        asset_ids = {}
        asset_ids.update(self._extract_asset_id_map_from_finding(match))
        asset_ids.update(self._map_names_to_ids_from_payload(affected_assets, create_payload))
        if update_payload:
            asset_ids.update(self._map_names_to_ids_from_payload(affected_assets, update_payload))
        resolved = self._resolve_project_asset_ids_with_retry(project_id, merged)
        asset_ids.update(resolved)
        payload_assets = self._build_affected_assets_payload(merged, asset_ids)
        payload = dict(update_payload or {})
        payload.pop("affected_assets", None)
        payload.pop("vulnerability_affected_assets", None)
        payload.pop("projectId", None)
        payload.pop("project_id", None)
        payload["affected_assets"] = payload_assets
        vuln_id = match.get("vulnerability_id") or match.get("id")
        result = self.update_vulnerability(vuln_id, payload)
        if missing:
            result = self._ensure_assets_on_vulnerability(
                vulnerability_id=vuln_id,
                project_id=project_id,
                desired_assets=merged,
                asset_ids=asset_ids,
            )
        return {"action": "update", "result": result, "added_assets": missing}

    def _normalize_title(self, title: str) -> str:
        return (title or "").strip().lower()

    def _apply_finding_defaults(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            return payload
        config = getattr(self._transport, "_config", None)
        new_payload = dict(payload)

        if "is_visible" not in new_payload and "isVisible" not in new_payload:
            default_visible = getattr(config, "default_findings_visible", None)
            if default_visible is not None:
                new_payload["is_visible"] = bool(default_visible)

        substatus_key = getattr(config, "default_findings_substatus_key", None)
        substatus_value = getattr(config, "default_findings_substatus_value", None)
        if substatus_key and substatus_value:
            new_payload = self._apply_substatus_default(new_payload, substatus_key, substatus_value)

        return new_payload

    def _apply_substatus_default(self, payload: Dict[str, Any], key: str, value: str) -> Dict[str, Any]:
        fields_key = None
        if "custom_fields" in payload:
            fields_key = "custom_fields"
        elif "vulnerability_custom_fields" in payload:
            fields_key = "vulnerability_custom_fields"
        else:
            fields_key = "custom_fields"

        fields = payload.get(fields_key)
        if not isinstance(fields, list):
            fields = []
        # If already present, do not override.
        for entry in fields:
            if isinstance(entry, dict) and entry.get("key") == key:
                return payload

        new_payload = dict(payload)
        new_fields = [entry for entry in fields if isinstance(entry, dict)]
        new_fields.append({"key": key, "value": value})
        new_payload[fields_key] = new_fields
        return new_payload

    def _extract_title(self, finding: Dict[str, Any]) -> Optional[str]:
        for key in ("vulnerability_title", "title", "vulnerability", "name"):
            value = finding.get(key)
            if isinstance(value, str) and value.strip():
                return value
            if isinstance(value, dict):
                for nested_key in ("vulnerability_title", "title", "name"):
                    nested_value = value.get(nested_key)
                    if isinstance(nested_value, str) and nested_value.strip():
                        return nested_value
        return None

    def _extract_asset_names(self, assets: Sequence[Any]) -> set:
        names = set()
        for item in assets:
            if isinstance(item, str):
                if item.strip():
                    names.add(item.strip())
                continue
            if not isinstance(item, dict):
                continue
            for key in ("assetName", "name"):
                value = item.get(key)
                if isinstance(value, str) and value.strip():
                    names.add(value.strip())
            asset_obj = item.get("asset")
            if isinstance(asset_obj, dict):
                value = asset_obj.get("name")
                if isinstance(value, str) and value.strip():
                    names.add(value.strip())
        return names

    def _extract_asset_names_from_finding(self, finding: Dict[str, Any]) -> set:
        raw = finding.get("vulnerability_affected_assets") or finding.get("affected_assets") or []
        names = self._extract_asset_names(raw if isinstance(raw, list) else [])
        single = finding.get("vulnerability_affected_asset_name") or finding.get("affected_asset_name")
        if isinstance(single, str) and single.strip():
            names.add(single.strip())
        return names

    def _extract_list(self, data: Any, keys: Iterable[str]) -> List[Dict[str, Any]]:
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if isinstance(data, dict):
            for key in keys:
                value = data.get(key)
                if isinstance(value, list):
                    return [item for item in value if isinstance(item, dict)]
        return []

    def _resolve_project_asset_ids(self, project_id: str, asset_names: Sequence[str]) -> Dict[str, str]:
        if not asset_names:
            return {}
        try:
            project = self._get(f"/api/ss/project/{project_id}")
        except Exception:
            return {}
        if isinstance(project, dict) and isinstance(project.get("data"), dict):
            project = project["data"]
        if isinstance(project, dict) and isinstance(project.get("project"), dict):
            project = project["project"]
        if not isinstance(project, dict):
            return {}
        details = project.get("project_scope_details")
        if not isinstance(details, list):
            return {}
        mapping: Dict[str, str] = {}
        for entry in details:
            if not isinstance(entry, dict):
                continue
            name = entry.get("name")
            asset_id = entry.get("id") or entry.get("asset_id") or entry.get("assetId")
            if isinstance(name, str) and isinstance(asset_id, str):
                stripped = name.strip()
                if stripped:
                    mapping[stripped] = asset_id
        return mapping

    def _resolve_project_asset_ids_with_retry(
        self,
        project_id: str,
        asset_names: Sequence[str],
        *,
        attempts: int = 3,
        delay: float = 0.5,
    ) -> Dict[str, str]:
        seen: set = set()
        unique_names: List[str] = []
        for value in asset_names:
            if not isinstance(value, str):
                continue
            name = value.strip()
            if not name or name in seen:
                continue
            seen.add(name)
            unique_names.append(name)
        if not unique_names:
            return {}
        mapping = self._resolve_project_asset_ids(project_id, unique_names)
        missing = [name for name in unique_names if name not in mapping]
        if not missing or attempts <= 1:
            return mapping
        for _ in range(attempts - 1):
            time.sleep(delay)
            refreshed = self._resolve_project_asset_ids(project_id, missing)
            mapping.update(refreshed)
            missing = [name for name in missing if name not in mapping]
            if not missing:
                break
        return mapping

    def _build_affected_assets_payload(self, asset_names: Sequence[str], asset_ids: Dict[str, str]) -> List[Dict[str, Any]]:
        payload_assets: List[Dict[str, Any]] = []
        for name in asset_names:
            if not isinstance(name, str):
                continue
            stripped = name.strip()
            if not stripped:
                continue
            asset_id = asset_ids.get(stripped)
            if asset_id:
                payload_assets.append({"assetId": asset_id})
            else:
                payload_assets.append({"assetName": stripped})
        return payload_assets

    def _ensure_assets_on_vulnerability(
        self,
        *,
        vulnerability_id: str,
        project_id: str,
        desired_assets: Sequence[str],
        asset_ids: Dict[str, str],
        attempts: int = 3,
        delay: float = 1.0,
    ) -> Any:
        last_result: Any = None
        for _ in range(max(attempts, 1)):
            try:
                vuln = self.get_vulnerability(vulnerability_id)
            except Exception:
                break
            current_assets = self._extract_asset_names_from_finding(vuln)
            missing = [name for name in desired_assets if name not in current_assets]
            if not missing:
                return last_result if last_result is not None else vuln
            refreshed = self._resolve_project_asset_ids_with_retry(
                project_id, missing, attempts=2, delay=delay
            )
            asset_ids.update(refreshed)
            payload_assets = self._build_affected_assets_payload(desired_assets, asset_ids)
            payload = {"affected_assets": payload_assets}
            last_result = self.update_vulnerability(vulnerability_id, payload)
            time.sleep(delay)
        return last_result

    def _extract_asset_id_map_from_finding(self, finding: Dict[str, Any]) -> Dict[str, str]:
        raw = finding.get("vulnerability_affected_assets") or finding.get("affected_assets") or []
        return self._extract_asset_id_map(raw if isinstance(raw, list) else [])

    def _extract_asset_id_map(self, assets: Sequence[Any]) -> Dict[str, str]:
        mapping: Dict[str, str] = {}
        for item in assets:
            if not isinstance(item, dict):
                continue
            name = None
            asset_id = None
            for key in ("assetName", "name"):
                value = item.get(key)
                if isinstance(value, str) and value.strip():
                    name = value.strip()
                    break
            asset_obj = item.get("asset")
            if isinstance(asset_obj, dict):
                obj_name = asset_obj.get("name")
                if isinstance(obj_name, str) and obj_name.strip():
                    name = obj_name.strip()
                obj_id = asset_obj.get("id") or asset_obj.get("asset_id") or asset_obj.get("assetId")
                if isinstance(obj_id, str) and obj_id.strip():
                    asset_id = obj_id.strip()
            for key in ("assetId", "asset_id", "id"):
                value = item.get(key)
                if isinstance(value, str) and value.strip():
                    asset_id = value.strip()
                    break
            if name and asset_id:
                mapping[name] = asset_id
        return mapping

    def _map_names_to_ids_from_payload(
        self, asset_names: Sequence[Any], payload: Optional[Dict[str, Any]]
    ) -> Dict[str, str]:
        if not isinstance(payload, dict):
            return {}
        payload_assets = payload.get("affected_assets") or payload.get("vulnerability_affected_assets") or []
        if not isinstance(payload_assets, list):
            return {}
        mapping = self._extract_asset_id_map(payload_assets)
        names_list = [name for name in asset_names if isinstance(name, str) and name.strip()]
        if names_list and len(names_list) == len(payload_assets):
            for name, entry in zip(names_list, payload_assets):
                if name in mapping or not isinstance(entry, dict):
                    continue
                asset_id = entry.get("assetId") or entry.get("asset_id") or entry.get("id")
                if isinstance(asset_id, str) and asset_id.strip():
                    mapping[name] = asset_id.strip()
        return mapping

    def _enforce_vulnerability_evidence_fifo(
        self, vulnerability_id: str, keep_last: int, *, project_id: Optional[str] = None
    ) -> List[str]:
        if keep_last <= 0:
            return []
        entries: List[Any] = []
        resolved_project_id = project_id
        if project_id:
            vulns = self.get_project_vulnerabilities_all(project_id, params={"pendingVulnerabilities": True})
            for entry in vulns:
                if (entry.get("vulnerability_id") or entry.get("id")) == vulnerability_id:
                    entries = self._extract_evidence_entries(entry)
                    break
        if not entries and project_id is None:
            resolved_project_id = self._resolve_project_id_for_vulnerability(vulnerability_id)
            if resolved_project_id:
                vulns = self.get_project_vulnerabilities_all(
                    resolved_project_id, params={"pendingVulnerabilities": True}
                )
                for entry in vulns:
                    if (entry.get("vulnerability_id") or entry.get("id")) == vulnerability_id:
                        entries = self._extract_evidence_entries(entry)
                        break
        if not entries:
            vuln = self.get_vulnerability(vulnerability_id)
            entries = self._extract_evidence_entries(vuln)
        ordered = self._sort_entries(entries)
        if len(ordered) <= keep_last:
            return []
        to_delete = ordered[: len(ordered) - keep_last]
        deleted = []
        for entry in to_delete:
            file_name = self._extract_file_name(entry)
            if not file_name:
                continue
            self.delete_vulnerability_evidence(vulnerability_id, file_name)
            deleted.append(file_name)
        return deleted

    def _extract_evidence_entries(self, vuln: Any) -> List[Any]:
        if not isinstance(vuln, dict):
            return []
        if isinstance(vuln.get("data"), dict):
            vuln = vuln.get("data")
        if isinstance(vuln.get("vulnerability"), dict):
            vuln = vuln.get("vulnerability")
        for key in (
            "evidence",
            "evidence_files",
            "vulnerability_evidence",
            "vulnerability_evidence_files",
            "files",
            "attachments",
        ):
            value = vuln.get(key)
            if isinstance(value, list):
                return value
        return []

    def _get_vulnerability_evidence_entries(
        self, vulnerability_id: str, *, project_id: Optional[str] = None
    ) -> List[Any]:
        entries: List[Any] = []
        resolved_project_id = project_id
        if project_id:
            vulns = self.get_project_vulnerabilities_all(project_id, params={"pendingVulnerabilities": True})
            for entry in vulns:
                if (entry.get("vulnerability_id") or entry.get("id")) == vulnerability_id:
                    entries = self._extract_evidence_entries(entry)
                    break
        if not entries and project_id is None:
            resolved_project_id = self._resolve_project_id_for_vulnerability(vulnerability_id)
            if resolved_project_id:
                vulns = self.get_project_vulnerabilities_all(
                    resolved_project_id, params={"pendingVulnerabilities": True}
                )
                for entry in vulns:
                    if (entry.get("vulnerability_id") or entry.get("id")) == vulnerability_id:
                        entries = self._extract_evidence_entries(entry)
                        break
        if entries:
            return entries
        vuln = self.get_vulnerability(vulnerability_id)
        return self._extract_evidence_entries(vuln)

    def _find_matching_evidence_entry(self, entries: List[Any], original_name: str) -> Optional[Any]:
        normalized = original_name.strip()
        if not normalized:
            return None
        for entry in entries:
            if self._matches_file_name(entry, normalized):
                return entry
        return None

    def _matches_file_name(self, entry: Any, original_name: str) -> bool:
        if isinstance(entry, str):
            return entry.strip() == original_name
        if not isinstance(entry, dict):
            return False
        candidates = (
            entry.get("storage_name"),
            entry.get("storageName"),
            entry.get("full_name"),
            entry.get("fullName"),
            entry.get("file"),
            entry.get("fileName"),
            entry.get("file_name"),
            entry.get("file_name_custom"),
            entry.get("alternative_name"),
            entry.get("original_name"),
            entry.get("filename"),
            entry.get("name"),
        )
        for candidate in candidates:
            if isinstance(candidate, str) and candidate.strip() == original_name:
                return True
        path = entry.get("path")
        if isinstance(path, str) and path.endswith(original_name):
            return True
        return False

    def _extract_file_name(self, entry: Any) -> Optional[str]:
        if isinstance(entry, str) and entry.strip():
            return entry
        if isinstance(entry, dict):
            for key in (
                "storage_name",
                "storageName",
                "full_name",
                "fullName",
                "file",
                "fileName",
                "file_name",
                "file_name_custom",
                "alternative_name",
                "filename",
                "name",
                "path",
            ):
                value = entry.get(key)
                if isinstance(value, str) and value.strip():
                    return value
        return None

    def _sort_entries(self, entries: List[Any]) -> List[Any]:
        if not entries:
            return []

        def parse_time(value: Any) -> Optional[float]:
            if not isinstance(value, str):
                return None
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
            except ValueError:
                return None

        with_timestamp = []
        for entry in entries:
            if isinstance(entry, dict):
                for key in ("created", "created_at", "uploaded", "uploaded_at", "timestamp"):
                    ts = parse_time(entry.get(key))
                    if ts is not None:
                        with_timestamp.append((ts, entry))
                        break
            else:
                with_timestamp.append((None, entry))
        if all(ts is None for ts, _ in with_timestamp):
            return entries
        return [entry for ts, entry in sorted(with_timestamp, key=lambda pair: pair[0] or 0.0)]

    def extract_linked_testcase_ids(self, vulnerability: Any) -> set:
        vuln = self._unwrap_vulnerability(vulnerability)
        linked = (
            vuln.get("linked_testcases")
            or vuln.get("linkedTestcases")
            or vuln.get("linked_testcase_ids")
            or vuln.get("linkedTestcaseIds")
            or vuln.get("vulnerability_testcases")
            or vuln.get("vulnerabilityTestcases")
            or []
        )
        ids = set()
        if not isinstance(linked, list):
            return ids
        for item in linked:
            if isinstance(item, str):
                ids.add(item)
            elif isinstance(item, dict):
                value = item.get("id") or item.get("testcase_id")
                if isinstance(value, str):
                    ids.add(value)
        return ids

    def assert_asset_agnostic(
        self, payload: Dict[str, Any], asset_names: Sequence[str], *, enabled: bool = True
    ) -> None:
        """
        Ensure asset names are not present in any string fields except affected_assets.
        """
        if not enabled:
            return
        needles = [name.lower() for name in asset_names if isinstance(name, str)]

        def walk(value: Any, path: str) -> None:
            if isinstance(value, dict):
                for key, item in value.items():
                    if key == "affected_assets":
                        continue
                    next_path = f"{path}.{key}" if path else key
                    walk(item, next_path)
            elif isinstance(value, list):
                for idx, item in enumerate(value):
                    walk(item, f"{path}[{idx}]")
            elif isinstance(value, str):
                lower = value.lower()
                for needle in needles:
                    if needle and needle in lower:
                        raise ValueError(f"Payload field '{path}' contains asset name '{needle}'")

        walk(payload, "")

    def _unwrap_vulnerability(self, data: Any) -> Dict[str, Any]:
        if isinstance(data, dict) and isinstance(data.get("data"), dict):
            data = data["data"]
        if isinstance(data, dict) and isinstance(data.get("vulnerability"), dict):
            data = data["vulnerability"]
        return data if isinstance(data, dict) else {}

    def _resolve_project_id_for_vulnerability(self, vulnerability_id: str) -> Optional[str]:
        vuln = self.get_vulnerability(vulnerability_id)
        project_id = self._find_first_value(vuln, ("project_id", "projectId"))
        if project_id:
            return project_id
        project = self._find_first_dict(vuln, "project")
        if isinstance(project, dict):
            candidate = project.get("id") or project.get("project_id") or project.get("projectId")
            if isinstance(candidate, str) and candidate:
                return candidate
        return None

    def _find_first_value(self, data: Any, keys: Iterable[str]) -> Optional[str]:
        if isinstance(data, dict):
            for key in keys:
                value = data.get(key)
                if isinstance(value, str) and value:
                    return value
            for value in data.values():
                found = self._find_first_value(value, keys)
                if found:
                    return found
        elif isinstance(data, list):
            for item in data:
                found = self._find_first_value(item, keys)
                if found:
                    return found
        return None

    def _find_first_dict(self, data: Any, key: str) -> Optional[Dict[str, Any]]:
        if isinstance(data, dict):
            value = data.get(key)
            if isinstance(value, dict):
                return value
            for child in data.values():
                found = self._find_first_dict(child, key)
                if found:
                    return found
        elif isinstance(data, list):
            for item in data:
                found = self._find_first_dict(item, key)
                if found:
                    return found
        return None
