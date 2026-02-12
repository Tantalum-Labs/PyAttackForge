"""Resource: testcases."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set
import os
import hashlib
import json
import uuid
import httpx
from datetime import datetime, timezone
import time

from .base import BaseResource


class TestcasesResource(BaseResource):
    """Testcases API resource wrapper."""
    __test__ = False

    def create_testcase(self, project_id: str, payload: Dict[str, Any]) -> Any:
        return self._post(f"/api/ss/project/{project_id}/testcase", json=payload)

    def get_project_testcases(self, project_id: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._get(f"/api/ss/project/{project_id}/testcases", params=params)

    def update_testcase(self, project_id: str, testcase_id: str, payload: Dict[str, Any]) -> Any:
        return self._put(f"/api/ss/project/{project_id}/testcase/{testcase_id}", json=payload)

    def create_testcase_note(
        self,
        project_id: str,
        testcase_id: str,
        payload: Dict[str, Any],
        *,
        dedupe: bool = False,
    ) -> Any:
        """
        Create a note on a project testcase. When dedupe=True, skip creation if
        an existing note matches the incoming note text (case-insensitive, trimmed).
        """
        if dedupe:
            note_text = payload.get("note") if isinstance(payload, dict) else None
            if isinstance(note_text, str) and note_text.strip():
                existing = self._find_testcase(project_id, testcase_id)
                notes = self._extract_notes(existing)
                if not notes:
                    ui_notes = self.get_project_testcase_notes_ui(project_id, testcase_id)
                    if ui_notes:
                        notes = self._extract_notes(ui_notes)
                match = self._find_matching_note(notes, note_text)
                if match is not None:
                    return {"action": "noop", "existing": match}
        return self._post(f"/api/ss/project/{project_id}/testcase/{testcase_id}/note", json=payload)

    def upload_testcase_file(
        self,
        project_id: str,
        testcase_id: str,
        file_path: str,
        *,
        keep_last: Optional[int] = 2,
        dedupe: bool = False,
        mode: str = "auto",
        ui_token: Optional[str] = None,
        ui_base_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload evidence to a project testcase.

        keep_last defaults to 2 (FIFO, keep most recent). Set keep_last=None to disable FIFO.
        If dedupe=True, skip upload when an existing file entry matches the filename.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)
        if mode not in {"auto", "ssapi", "ui"}:
            raise ValueError(f"Unsupported upload mode: {mode}")
        config = getattr(self._transport, "_config", None)
        token = ui_token or (getattr(config, "ui_token", None) if config else None)
        base_url = ui_base_url or (getattr(config, "ui_base_url", None) if config else None) or (
            getattr(config, "base_url", None) if config else None
        )
        use_ui = mode == "ui" or (mode == "auto" and token)
        file_name = os.path.basename(file_path)
        if dedupe:
            entries = self._get_testcase_file_entries(
                project_id, testcase_id, use_ui=use_ui, ui_token=token, ui_base_url=base_url
            )
            match = self._find_matching_file_entry(entries, file_name)
            if match is not None:
                result: Dict[str, Any] = {"action": "noop", "existing": match}
                if keep_last is not None and not use_ui:
                    deletions = self._safe_enforce_testcase_file_fifo(project_id, testcase_id, keep_last)
                    result["deleted"] = deletions
                return result
        before_entries = None
        if use_ui and keep_last is not None:
            before_entries = self._get_testcase_file_entries(
                project_id, testcase_id, use_ui=True, ui_token=token, ui_base_url=base_url
            )
        if use_ui and token and base_url:
            upload_result = self._upload_testcase_file_ui(project_id, testcase_id, file_path, base_url, token)
        else:
            with open(file_path, "rb") as handle:
                upload_result = self._post_files(
                    f"/api/ss/project/{project_id}/testcase/{testcase_id}/file",
                    files={"file": (file_name, handle)},
                )
        if keep_last is None:
            return {"upload": upload_result}
        if use_ui:
            deletions = self._enforce_testcase_file_fifo_ui(
                project_id,
                testcase_id,
                keep_last,
                ui_token=token,
                ui_base_url=base_url,
                fallback_entries=before_entries,
            )
            return {"upload": upload_result, "deleted": deletions}
        deletions = self._safe_enforce_testcase_file_fifo(project_id, testcase_id, keep_last)
        return {"upload": upload_result, "deleted": deletions}

    def download_testcase_file(self, project_id: str, testcase_id: str, file_name: str) -> Any:
        return self._get(f"/api/ss/project/{project_id}/testcase/{testcase_id}/file/{file_name}")

    def download_testcase_note_file(self, project_id: str, note_id: str, file_name: str) -> Any:
        return self._get(f"/api/ss/project/{project_id}/testcase-note/{note_id}/file/{file_name}")

    def download_testcase_workspace_note_file(self, project_id: str, note_id: str, file_name: str) -> Any:
        return self._get(f"/api/ss/project/{project_id}/testcase-workspace-note/{note_id}/file/{file_name}")

    def delete_testcase_file(self, project_id: str, testcase_id: str, file_name: str) -> Any:
        """
        Assumption: DELETE is supported for testcase files using the download path.
        """
        return self._delete(f"/api/ss/project/{project_id}/testcase/{testcase_id}/file/{file_name}")

    def get_project_testcase_meta_ui(
        self,
        project_id: str,
        testcase_id: str,
        *,
        ui_token: Optional[str] = None,
        ui_base_url: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        config = getattr(self._transport, "_config", None)
        token = ui_token or (getattr(config, "ui_token", None) if config else None)
        base_url = ui_base_url or (getattr(config, "ui_base_url", None) if config else None) or (
            getattr(config, "base_url", None) if config else None
        )
        if not token or not base_url:
            return None
        url = f"{base_url.rstrip('/')}/api/projects/{project_id}/meta/testcase"
        try:
            with httpx.Client(timeout=20.0, headers={"authorization": token}) as client:
                resp = client.get(url, params={"fk": testcase_id})
        except httpx.HTTPError:
            return None
        if resp.status_code >= 400:
            return None
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
        return None

    def get_project_testcase_notes_ui(
        self,
        project_id: str,
        testcase_id: str,
        *,
        ui_token: Optional[str] = None,
        ui_base_url: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        config = getattr(self._transport, "_config", None)
        token = ui_token or (getattr(config, "ui_token", None) if config else None)
        base_url = ui_base_url or (getattr(config, "ui_base_url", None) if config else None) or (
            getattr(config, "base_url", None) if config else None
        )
        if not token or not base_url:
            return None
        url = f"{base_url.rstrip('/')}/api/projects/{project_id}/testcases/{testcase_id}/notes"
        try:
            with httpx.Client(timeout=20.0, headers={"authorization": token}) as client:
                resp = client.get(url)
        except httpx.HTTPError:
            return None
        if resp.status_code >= 400:
            return None
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
        return None

    def _upload_testcase_file_ui(
        self, project_id: str, testcase_id: str, file_path: str, base_url: str, token: str
    ) -> Any:
        path = os.fspath(file_path)
        with open(path, "rb") as handle:
            content = handle.read()
        metadata = {
            "upload_id": str(uuid.uuid4()),
            "total_size": len(content),
            "start_index": 0,
            "end_index": len(content),
            "chunk_sha1": hashlib.sha1(content).hexdigest(),
        }
        url = f"{base_url.rstrip('/')}/api/projects/{project_id}/upload/testcase/{testcase_id}"
        with httpx.Client(timeout=30.0, headers={"authorization": token}) as client:
            resp = client.post(
                url,
                files={
                    "file": (os.path.basename(path), content, "application/octet-stream"),
                    "metadata": (None, json.dumps(metadata), "application/json"),
                },
            )
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
        return resp.text

    def touch_testcase(
        self,
        project_id: str,
        testcase_id: str,
        *,
        timestamp: Optional[str] = None,
        testcase_type: Optional[str] = "Security Test Case",
        overwrite: bool = False,
    ) -> Any:
        """
        Update the project testcase custom field `last_tested` (and optional `testcase_type`).

        Uses `project_testcase_custom_fields` per SSAPI docs. By default, merge into existing
        project testcase custom fields; set overwrite=True to replace the list.
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).date().isoformat()
        new_entries = [{"key": "last_tested", "value": timestamp}]
        if testcase_type:
            new_entries.append({"key": "testcase_type", "value": testcase_type})
        if overwrite:
            merged_fields = new_entries
        else:
            existing = self._extract_project_testcase_custom_fields(
                self._find_testcase(project_id, testcase_id)
            )
            merged_fields = self._merge_custom_fields_list(existing, new_entries)
        payload = {"project_testcase_custom_fields": merged_fields}
        return self.update_testcase(project_id, testcase_id, payload)

    def _enforce_testcase_file_fifo(self, project_id: str, testcase_id: str, keep_last: int) -> List[str]:
        if keep_last <= 0:
            return []
        testcase = self._find_testcase(project_id, testcase_id)
        entries = self._extract_file_entries(testcase)
        ordered = self._sort_entries(entries)
        if len(ordered) <= keep_last:
            return []
        to_delete = ordered[: len(ordered) - keep_last]
        deleted = []
        for entry in to_delete:
            file_name = self._extract_file_name(entry)
            if not file_name:
                continue
            self.delete_testcase_file(project_id, testcase_id, file_name)
            deleted.append(file_name)
        return deleted

    def _find_testcase(self, project_id: str, testcase_id: str) -> Dict[str, Any]:
        data = self.get_project_testcases(project_id)
        testcases = self._extract_list(data, ["testcases", "project_testcases"])  # best-effort
        for testcase in testcases:
            if testcase.get("id") == testcase_id or testcase.get("testcase_id") == testcase_id:
                return testcase
        return {}

    def _extract_list(self, data: Any, keys: Iterable[str]) -> List[Dict[str, Any]]:
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if isinstance(data, dict):
            for key in keys:
                value = data.get(key)
                if isinstance(value, list):
                    return [item for item in value if isinstance(item, dict)]
        return []

    def extract_project_testcases_list(self, project_testcases: Any) -> List[Dict[str, Any]]:
        if not isinstance(project_testcases, dict):
            return []
        testcases = (
            project_testcases.get("testcases")
            or project_testcases.get("project_testcases")
            or (project_testcases.get("data") or {}).get("project_testcases")
            or (project_testcases.get("data") or {}).get("testcases")
            or []
        )
        return [tc for tc in testcases if isinstance(tc, dict)] if isinstance(testcases, list) else []

    def find_project_testcase_entry(self, project_testcases: Any, testcase_id: str) -> Optional[Dict[str, Any]]:
        for testcase in self.extract_project_testcases_list(project_testcases):
            if self.extract_project_testcase_id(testcase) == testcase_id:
                return testcase
        return None

    def build_project_testcase_map(self, project_testcases: Any) -> Dict[str, Dict[str, Any]]:
        mapping: Dict[str, Dict[str, Any]] = {}
        for testcase in self.extract_project_testcases_list(project_testcases):
            title = testcase.get("testcase") or testcase.get("name") or testcase.get("title")
            if isinstance(title, str) and title.strip():
                mapping[self._normalize_string(title)] = testcase
        return mapping

    def wait_for_project_testcases(
        self, project_id: str, *, attempts: int = 12, delay: float = 2.0
    ) -> Dict[str, Any]:
        last: Dict[str, Any] = {}
        for _ in range(attempts):
            data = self.get_project_testcases(project_id)
            last = data if isinstance(data, dict) else {}
            if self.extract_project_testcases_list(last):
                return last
            time.sleep(delay)
        return last

    def extract_project_testcase_id(self, testcase: Dict[str, Any]) -> Optional[str]:
        for key in ("id", "project_testcase_id", "projectTestcaseId"):
            value = testcase.get(key)
            if isinstance(value, str) and value.strip():
                return value
        return None

    def first_project_testcase_id(self, project_testcases: Any) -> Optional[str]:
        for testcase in self.extract_project_testcases_list(project_testcases):
            tc_id = self.extract_project_testcase_id(testcase) or testcase.get("testcase_id")
            if isinstance(tc_id, str):
                return tc_id
        return None

    def extract_linked_vulnerability_ids(self, testcase: Dict[str, Any]) -> Set[str]:
        linked = (
            testcase.get("linked_vulnerabilities")
            or testcase.get("linkedVulnerabilities")
            or testcase.get("linked_vulnerability_ids")
            or testcase.get("linkedVulnerabilityIds")
            or testcase.get("vulnerabilities")
            or []
        )
        ids: Set[str] = set()
        if not isinstance(linked, list):
            return ids
        for item in linked:
            if isinstance(item, str):
                ids.add(item)
            elif isinstance(item, dict):
                value = item.get("id") or item.get("vulnerability_id")
                if isinstance(value, str):
                    ids.add(value)
        return ids

    def _get_testcase_file_entries(
        self,
        project_id: str,
        testcase_id: str,
        *,
        use_ui: bool = False,
        ui_token: Optional[str] = None,
        ui_base_url: Optional[str] = None,
    ) -> List[Any]:
        if use_ui:
            meta = self.get_project_testcase_meta_ui(
                project_id, testcase_id, ui_token=ui_token, ui_base_url=ui_base_url
            )
            if meta:
                return self._extract_file_entries(meta)
        testcase = self._find_testcase(project_id, testcase_id)
        return self._extract_file_entries(testcase)

    def _extract_file_entries(self, testcase: Any) -> List[Any]:
        if not isinstance(testcase, dict):
            return []
        for key in (
            "uploaded_files",
            "files",
            "testcase_files",
            "attachments",
        ):
            value = testcase.get(key)
            if isinstance(value, list):
                return value
        return []

    def _extract_notes(self, testcase: Any) -> List[Any]:
        if not isinstance(testcase, dict):
            return []
        for key in ("notes", "testcase_notes", "project_testcase_notes", "testcaseNotes"):
            value = testcase.get(key)
            if isinstance(value, list):
                return value
        return []

    def _extract_project_testcase_custom_fields(self, testcase: Any) -> List[Dict[str, Any]]:
        if not isinstance(testcase, dict):
            return []
        for key in ("project_testcase_custom_fields", "projectTestcaseCustomFields"):
            value = testcase.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return []

    def _find_matching_note(self, notes: List[Any], note_text: str) -> Optional[Dict[str, Any]]:
        normalized = note_text.strip().lower()
        for note in notes:
            if isinstance(note, str):
                candidate = note.strip().lower()
                if candidate == normalized:
                    return {"note": note}
                continue
            if not isinstance(note, dict):
                continue
            for key in ("note", "note_text", "text", "body", "content"):
                value = note.get(key)
                if isinstance(value, str) and value.strip().lower() == normalized:
                    return note
        return None

    def _normalize_string(self, value: str) -> str:
        return value.strip().lower()

    def _find_matching_file_entry(self, entries: List[Any], original_name: str) -> Optional[Any]:
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

    def _extract_file_id(self, entry: Any) -> Optional[str]:
        if not isinstance(entry, dict):
            return None
        for key in ("id", "file_id", "fileId"):
            value = entry.get(key)
            if isinstance(value, str) and value.strip():
                return value
        return None

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

    def _merge_custom_fields(self, existing: Any, new_entry: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not isinstance(existing, list):
            existing_list: List[Dict[str, Any]] = []
        else:
            existing_list = [item for item in existing if isinstance(item, dict)]
        key_name = new_entry.get("key")
        merged: List[Dict[str, Any]] = []
        for item in existing_list:
            if item.get("key") == key_name:
                continue
            merged.append(item)
        merged.append(new_entry)
        return merged

    def _merge_custom_fields_list(
        self, existing: Any, new_entries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        if not isinstance(existing, list):
            existing_list: List[Dict[str, Any]] = []
        else:
            existing_list = [item for item in existing if isinstance(item, dict)]
        keys_to_replace = {entry.get("key") for entry in new_entries if isinstance(entry, dict)}
        merged: List[Dict[str, Any]] = [item for item in existing_list if item.get("key") not in keys_to_replace]
        merged.extend([entry for entry in new_entries if isinstance(entry, dict)])
        return merged

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

    def _safe_enforce_testcase_file_fifo(self, project_id: str, testcase_id: str, keep_last: int) -> List[str]:
        try:
            return self._enforce_testcase_file_fifo(project_id, testcase_id, keep_last)
        except Exception as exc:
            try:
                from ..exceptions import APIError  # local import to avoid cycles
            except Exception:
                raise
            if isinstance(exc, APIError) and exc.status_code == 404:
                return []
            raise

    def _enforce_testcase_file_fifo_ui(
        self,
        project_id: str,
        testcase_id: str,
        keep_last: int,
        *,
        ui_token: Optional[str] = None,
        ui_base_url: Optional[str] = None,
        fallback_entries: Optional[List[Any]] = None,
    ) -> List[str]:
        if keep_last <= 0:
            return []
        entries = self._get_testcase_file_entries(
            project_id, testcase_id, use_ui=True, ui_token=ui_token, ui_base_url=ui_base_url
        )
        if len(entries) <= keep_last and fallback_entries:
            fallback_len = len(fallback_entries)
            extra = fallback_len + 1 - keep_last
            if extra > 0:
                ordered = self._sort_entries(fallback_entries)
                to_delete = ordered[:extra]
            else:
                return []
        else:
            ordered = self._sort_entries(entries)
            if len(ordered) <= keep_last:
                return []
            to_delete = ordered[: len(ordered) - keep_last]
        deleted: List[str] = []
        for entry in to_delete:
            file_id = self._extract_file_id(entry)
            if not file_id:
                continue
            if self._delete_testcase_file_ui(project_id, file_id, ui_token=ui_token, ui_base_url=ui_base_url):
                file_name = self._extract_file_name(entry) or file_id
                deleted.append(file_name)
        return deleted

    def _delete_testcase_file_ui(
        self,
        project_id: str,
        file_id: str,
        *,
        ui_token: Optional[str] = None,
        ui_base_url: Optional[str] = None,
    ) -> bool:
        config = getattr(self._transport, "_config", None)
        token = ui_token or (getattr(config, "ui_token", None) if config else None)
        base_url = ui_base_url or (getattr(config, "ui_base_url", None) if config else None) or (
            getattr(config, "base_url", None) if config else None
        )
        if not token or not base_url:
            return False
        url = f"{base_url.rstrip('/')}/api/projects/{project_id}/meta/{file_id}/delete"
        try:
            with httpx.Client(timeout=20.0, headers={"authorization": token}) as client:
                for method in ("DELETE", "GET", "POST"):
                    resp = client.request(method, url)
                    if resp.status_code < 400:
                        return True
        except httpx.HTTPError:
            return False
        return False
