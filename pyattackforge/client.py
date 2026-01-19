"""
PyAttackForge is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyAttackForge is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional, Set, Tuple, List

import requests


logger = logging.getLogger("pyattackforge")


class PyAttackForgeClient:
    """
    Python client for interacting with the AttackForge API.

    Provides methods to manage assets, projects, and vulnerabilities.
    Supports dry-run mode for testing without making real API calls.
    """

    def _unwrap(self, resp_json: Any, key: str) -> Any:
        if isinstance(resp_json, dict) and key in resp_json:
            return resp_json.get(key)
        return resp_json

    def _ensure_response(
        self,
        resp: Any,
        expected: Tuple[int, ...],
        action: str,
    ) -> None:
        if resp.status_code in (401, 403):
            raise PermissionError(
                f"Permission denied when attempting to {action}: {resp.status_code} {resp.text}"
            )
        if resp.status_code not in expected:
            raise RuntimeError(f"Failed to {action}: {resp.text}")

    def _build_asset_payloads(
        self,
        affected_assets: Optional[list]
    ) -> Tuple[List[Dict[str, Any]], List[str], List[str]]:
        payloads: List[Dict[str, Any]] = []
        asset_names: List[str] = []
        asset_ids: List[str] = []
        for asset in affected_assets or []:
            if isinstance(asset, dict):
                nested_asset = asset.get("asset") if isinstance(asset.get("asset"), dict) else {}
                name = asset.get("assetName") or asset.get("asset_name") or asset.get("name")
                if not name:
                    if isinstance(asset.get("asset"), dict):
                        name = nested_asset.get("name") or nested_asset.get("asset") or nested_asset.get("asset_name")
                    else:
                        name = asset.get("asset")
                asset_id = (
                    asset.get("assetId")
                    or asset.get("asset_id")
                    or asset.get("asset_library_id")
                    or asset.get("id")
                )
                if not asset_id and nested_asset:
                    asset_id = (
                        nested_asset.get("assetId")
                        or nested_asset.get("asset_id")
                        or nested_asset.get("asset_library_id")
                        or nested_asset.get("id")
                    )
                if name:
                    asset_names.append(str(name))
                if asset_id:
                    asset_ids.append(str(asset_id))
                payload: Dict[str, Any] = {}
                if name:
                    payload["name"] = name
                    payload["assetName"] = name
                if asset_id:
                    payload["assetId"] = asset_id
                payloads.append(payload or asset)
            else:
                if asset is None:
                    continue
                asset_names.append(str(asset))
                payloads.append({"name": asset, "assetName": asset})
        return payloads, asset_names, asset_ids

    def _build_update_finding_payload(
        self,
        project_id: Optional[str],
        affected_assets: Optional[list],
        notes: Optional[list],
        extra_fields: Optional[Dict[str, Any]],
    ) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
        payload: Dict[str, Any] = {}
        params: Optional[Dict[str, Any]] = None
        if project_id:
            params = {"projectId": project_id}
        if affected_assets is not None:
            asset_payloads, _, _ = self._build_asset_payloads(affected_assets)
            payload["affected_assets"] = asset_payloads
        if notes is not None:
            payload["notes"] = notes
        for key, value in (extra_fields or {}).items():
            if value is not None:
                payload[key] = value
        return payload, params

    def _cache_vulnerability_evidence(self, vulnerability_id: str, basename: str, file_size: int) -> None:
        if not vulnerability_id or not basename or file_size is None:
            return
        cache = self._vulnerability_evidence_cache.setdefault(str(vulnerability_id), set())
        cache.add((str(basename), int(file_size)))

    def _cache_testcase_evidence(
        self, project_id: str, testcase_id: str, basename: str, file_size: int
    ) -> None:
        if not project_id or not testcase_id or not basename or file_size is None:
            return
        key = (str(project_id), str(testcase_id))
        cache = self._testcase_evidence_cache.setdefault(key, set())
        cache.add((str(basename), int(file_size)))

    def _cache_testcase_link(self, project_id: str, testcase_id: str, finding_id: str) -> None:
        if not project_id or not testcase_id or not finding_id:
            return
        key = (str(project_id), str(testcase_id))
        cache = self._testcase_link_cache.setdefault(key, set())
        cache.add(str(finding_id))

    def _normalize_testcase_status(self, status: Any) -> str:
        if status is None:
            raise ValueError("Testcase status cannot be empty")
        raw = str(status).strip()
        if not raw:
            raise ValueError("Testcase status cannot be empty")
        key = " ".join(raw.lower().replace("_", " ").replace("-", " ").split())
        canonical = {
            "tested": "Tested",
            "testing in progress": "Testing In Progress",
            "not tested": "Not Tested",
            "not applicable": "Not Applicable",
        }
        aliases = {
            "not started": "Not Tested",
            "in progress": "Testing In Progress",
            "n/a": "Not Applicable",
            "na": "Not Applicable",
        }
        if key in aliases:
            return aliases[key]
        if key in canonical:
            return canonical[key]
        allowed = ", ".join(canonical.values())
        raise ValueError(f"Unsupported testcase status '{status}'. Allowed: {allowed}")

    def _normalize_testcase_payload(self, testcase: Any) -> Any:
        if not isinstance(testcase, dict):
            return testcase
        outer = testcase
        for key in (
            "testcase",
            "project_testcase",
            "projectTestcase",
            "project_test_case",
        ):
            if isinstance(outer.get(key), dict):
                testcase = dict(outer.get(key) or {})
                for extra_key in (
                    "testcase_notes",
                    "notes",
                    "testcaseNotes",
                    "project_testcase_notes",
                    "testcase_note",
                    "files",
                    "testcase_files",
                    "testcaseFiles",
                    "project_testcase_files",
                    "projectTestcaseFiles",
                    "uploaded_files",
                    "attachments",
                    "evidence",
                    "testcase_evidence",
                    "linked_vulnerabilities",
                    "linked_findings",
                    "linked_vulnerability_ids",
                    "linked_vulnerability_id",
                ):
                    if extra_key not in testcase and extra_key in outer:
                        testcase[extra_key] = outer.get(extra_key)
                break
        if not testcase.get("id"):
            for key in (
                "_id",
                "project_testcase_id",
                "project_test_case_id",
                "projectTestcaseId",
                "testcase_id",
                "testcaseId",
            ):
                value = testcase.get(key)
                if value:
                    testcase["id"] = value
                    break
        else:
            project_id = (
                testcase.get("project_testcase_id")
                or testcase.get("project_test_case_id")
                or testcase.get("projectTestcaseId")
            )
            if project_id and testcase.get("id") in (
                testcase.get("testcase_id"),
                testcase.get("testcaseId"),
            ):
                testcase["id"] = project_id
        return testcase

    def _normalize_vulnerability_payload(self, vulnerability: Any) -> Any:
        if not isinstance(vulnerability, dict):
            return vulnerability
        outer = vulnerability
        if isinstance(outer.get("vulnerability"), dict):
            vulnerability = dict(outer.get("vulnerability") or {})
            for extra_key in (
                "vulnerability_evidence",
                "vulnerabilityEvidence",
                "evidence",
                "evidences",
                "files",
                "attachments",
                "vulnerability_affected_assets",
                "affected_assets",
                "affectedAssets",
                "assets",
                "affected_asset",
                "affectedAsset",
                "vulnerability_affected_asset_name",
                "affected_asset_name",
                "asset_name",
            ):
                if extra_key not in vulnerability and extra_key in outer:
                    vulnerability[extra_key] = outer.get(extra_key)
        for extra_key in (
            "vulnerability_affected_assets",
            "affected_assets",
            "affectedAssets",
            "assets",
            "affected_asset",
            "affectedAsset",
            "vulnerability_affected_asset_name",
            "affected_asset_name",
            "asset_name",
        ):
            if extra_key not in vulnerability and extra_key in outer:
                vulnerability[extra_key] = outer.get(extra_key)
        if not vulnerability.get("id"):
            for key in ("vulnerability_id", "vulnerabilityId", "_id"):
                value = vulnerability.get(key)
                if value:
                    vulnerability["id"] = value
                    break
        if isinstance(vulnerability.get("vulnerability_evidence"), dict):
            vulnerability["vulnerability_evidence"] = [vulnerability["vulnerability_evidence"]]
        if not vulnerability.get("vulnerability_evidence"):
            for key in (
                "vulnerabilityEvidence",
                "evidence",
                "evidences",
                "files",
                "attachments",
            ):
                value = vulnerability.get(key)
                if value is None:
                    continue
                if isinstance(value, list):
                    vulnerability["vulnerability_evidence"] = value
                elif isinstance(value, dict):
                    vulnerability["vulnerability_evidence"] = [value]
                else:
                    vulnerability["vulnerability_evidence"] = []
                break
        return vulnerability

    def _extract_vulnerability_id(self, payload: Any) -> Optional[str]:
        if not payload:
            return None
        if isinstance(payload, dict) and "vulnerability" in payload:
            payload = payload.get("vulnerability")
        if isinstance(payload, dict):
            for key in ("vulnerability_id", "vulnerabilityId", "id", "_id"):
                value = payload.get(key)
                if value:
                    return str(value)
        return None

    def _extract_writeup_identity(
        self,
        writeup: Any,
        title: Optional[str] = None,
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        writeup_id = None
        library = None
        resolved_title = title
        if isinstance(writeup, dict):
            for key in (
                "reference_id",
                "id",
                "_id",
                "vulnerability_library_id",
                "vulnerability_library_issue_id",
            ):
                value = writeup.get(key)
                if value:
                    writeup_id = str(value)
                    break
            resolved_title = (
                resolved_title
                or writeup.get("title")
                or writeup.get("vulnerability_title")
                or writeup.get("name")
            )
            library = (
                writeup.get("belongs_to_library")
                or writeup.get("library")
                or writeup.get("library_name")
            )
        elif isinstance(writeup, str):
            writeup_id = writeup
        return writeup_id, resolved_title, library

    def _extract_asset_payloads_from_finding(
        self,
        finding: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        payloads: List[Dict[str, Any]] = []
        if not isinstance(finding, dict):
            return payloads
        raw_assets = (
            finding.get("vulnerability_affected_assets")
            or finding.get("affected_assets")
            or finding.get("affectedAssets")
            or finding.get("assets")
            or finding.get("affected_asset")
            or finding.get("affectedAsset")
            or []
        )
        if isinstance(raw_assets, dict):
            raw_assets = [raw_assets]
        for asset in raw_assets:
            if isinstance(asset, dict):
                name = asset.get("assetName") or asset.get("asset_name") or asset.get("name") or asset.get("asset")
                asset_id = (
                    asset.get("assetId")
                    or asset.get("asset_id")
                    or asset.get("asset_library_id")
                    or asset.get("id")
                )
                if not asset_id and isinstance(asset.get("asset"), dict):
                    nested = asset.get("asset") or {}
                    name = name or nested.get("name") or nested.get("asset") or nested.get("asset_name")
                    asset_id = (
                        asset_id
                        or nested.get("assetId")
                        or nested.get("asset_id")
                        or nested.get("asset_library_id")
                        or nested.get("id")
                    )
                payload: Dict[str, Any] = {}
                if name:
                    payload["name"] = name
                    payload["assetName"] = name
                if asset_id:
                    payload["assetId"] = asset_id
                payloads.append(payload or asset)
            elif isinstance(asset, str):
                payloads.append({"name": asset, "assetName": asset})
        for key in (
            "vulnerability_affected_asset_name",
            "affected_asset_name",
            "affectedAssetName",
            "asset_name",
        ):
            value = finding.get(key)
            if value:
                payloads.append({"name": value, "assetName": value})
        return payloads

    def _merge_asset_payloads(
        self,
        existing: List[Dict[str, Any]],
        new: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        merged: List[Dict[str, Any]] = []
        seen: Set[str] = set()
        for payload in existing + new:
            if isinstance(payload, dict):
                key = payload.get("assetId") or payload.get("assetName") or payload.get("name") or payload.get("asset")
                if key:
                    key_value = str(key)
                    if key_value in seen:
                        continue
                    seen.add(key_value)
            merged.append(payload)
        return merged

    def _append_assets_to_finding(
        self,
        project_id: str,
        finding_id: Optional[str],
        asset_payloads: List[Dict[str, Any]],
        existing_finding: Optional[Dict[str, Any]] = None,
    ) -> bool:
        if not finding_id or not asset_payloads:
            return False
        vuln = existing_finding or {}
        if not isinstance(vuln, dict) or not vuln:
            try:
                vuln = self.get_vulnerability(finding_id)
            except Exception:
                vuln = {}
        existing_payloads = self._extract_asset_payloads_from_finding(vuln)
        existing_keys = {
            str(p.get("assetId") or p.get("assetName") or p.get("name") or p.get("asset"))
            for p in existing_payloads
            if isinstance(p, dict)
            and (p.get("assetId") or p.get("assetName") or p.get("name") or p.get("asset"))
        }
        new_keys = {
            str(p.get("assetId") or p.get("assetName") or p.get("name") or p.get("asset"))
            for p in asset_payloads
            if isinstance(p, dict)
            and (p.get("assetId") or p.get("assetName") or p.get("name") or p.get("asset"))
        }
        if not new_keys - existing_keys:
            return False
        merged_assets = self._merge_asset_payloads(existing_payloads, asset_payloads)
        self.update_finding(
            vulnerability_id=finding_id,
            project_id=project_id,
            affected_assets=merged_assets,
        )
        return True

    def _collect_writeup_ids_from_finding(self, finding: Dict[str, Any]) -> Set[str]:
        ids: Set[str] = set()
        if not isinstance(finding, dict):
            return ids
        for key in (
            "vulnerability_library_issue_id",
            "vulnerability_library_id",
            "vulnerability_library_reference_id",
            "vulnerability_library_issue_reference_id",
            "vulnerabilityLibraryIssueId",
            "vulnerabilityLibraryId",
            "vulnerabilityLibraryReferenceId",
            "vulnerabilityLibraryIssueReferenceId",
            "library_issue_reference_id",
            "libraryIssueReferenceId",
            "library_issue_id",
            "libraryIssueId",
            "reference_id",
            "referenceId",
            "library_reference_id",
            "libraryReferenceId",
        ):
            value = finding.get(key)
            if value:
                ids.add(str(value))
        nested = (
            finding.get("vulnerability_library_issue")
            or finding.get("vulnerabilityLibraryIssue")
            or finding.get("library_issue")
            or finding.get("writeup")
        )
        if isinstance(nested, dict):
            for key in ("reference_id", "id", "_id"):
                value = nested.get(key)
                if value:
                    ids.add(str(value))
        elif isinstance(nested, str):
            ids.add(nested)
        return ids

    def _collect_writeup_ids_from_writeup(self, writeup: Any) -> Set[str]:
        ids: Set[str] = set()
        if isinstance(writeup, dict):
            for key in (
                "reference_id",
                "referenceId",
                "id",
                "_id",
                "vulnerability_library_id",
                "vulnerability_library_issue_id",
                "vulnerabilityLibraryId",
                "vulnerabilityLibraryIssueId",
                "vulnerability_library_issue_reference_id",
                "vulnerability_library_issue_referenceId",
                "vulnerabilityLibraryIssueReferenceId",
                "library_issue_reference_id",
                "libraryIssueReferenceId",
            ):
                value = writeup.get(key)
                if value:
                    ids.add(str(value))
            nested = (
                writeup.get("vulnerability_library_issue")
                or writeup.get("library_issue")
                or writeup.get("writeup")
            )
            if isinstance(nested, dict):
                for key in ("reference_id", "referenceId", "id", "_id"):
                    value = nested.get(key)
                    if value:
                        ids.add(str(value))
            elif isinstance(nested, str):
                ids.add(nested)
        elif isinstance(writeup, str):
            ids.add(writeup)
        return ids

    def _finding_title_matches(self, finding: Any, expected_title: Optional[str]) -> bool:
        if not expected_title or not isinstance(finding, dict):
            return False
        for key in ("vulnerability_title", "title", "vulnerabilityTitle", "name"):
            value = finding.get(key)
            if value is not None and str(value) == str(expected_title):
                return True
        return False

    def _finding_matches_writeup(
        self,
        finding: Dict[str, Any],
        writeup_id: Optional[Any],
        writeup_title: Optional[str],
        library: Optional[str],
    ) -> bool:
        if writeup_id:
            ids_to_match: Set[str] = set()
            if isinstance(writeup_id, (list, set, tuple)):
                for value in writeup_id:
                    if value:
                        ids_to_match.add(str(value))
            else:
                ids_to_match.add(str(writeup_id))
            if ids_to_match and ids_to_match.intersection(self._collect_writeup_ids_from_finding(finding)):
                return True
        if not writeup_title:
            return False
        title_candidates: List[str] = []
        for key in (
            "vulnerability_library_issue_title",
            "writeup_title",
            "library_issue_title",
            "vulnerability_library_title",
        ):
            value = finding.get(key)
            if value:
                title_candidates.append(str(value))
        nested = finding.get("vulnerability_library_issue")
        if isinstance(nested, dict) and nested.get("title"):
            title_candidates.append(str(nested.get("title")))
        if not title_candidates:
            fallback_title = finding.get("vulnerability_title") or finding.get("title")
            if fallback_title:
                title_candidates.append(str(fallback_title))
        if writeup_title not in title_candidates:
            return False
        if library:
            library_value = (
                finding.get("belongs_to_library")
                or finding.get("library")
                or finding.get("library_name")
                or finding.get("vulnerability_library_name")
            )
            if library_value and str(library_value) != str(library):
                return False
        return True

    def _finding_dedupe_keys(
        self,
        project_id: str,
        finding_title: str,
        writeup_ids: Set[str],
        writeup_title: Optional[str],
        library: Optional[str],
    ) -> List[str]:
        keys: List[str] = []
        for wid in writeup_ids:
            keys.append(f"{project_id}|writeup_id:{wid}|title:{finding_title}")
        if writeup_title:
            keys.append(
                f"{project_id}|writeup_title:{writeup_title}|library:{library or ''}|title:{finding_title}"
            )
        return keys

    def _lookup_finding_dedupe_cache(self, keys: List[str]) -> Optional[str]:
        for key in keys:
            cached = self._finding_dedupe_cache.get(key)
            if cached:
                return cached
        return None

    def _cache_finding_dedupe(self, keys: List[str], finding_id: Optional[str]) -> None:
        if not finding_id:
            return
        for key in keys:
            self._finding_dedupe_cache[key] = str(finding_id)

    def _apply_cached_testcase_links(
        self,
        project_id: str,
        testcase_id: str,
        testcase: Optional[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        if not isinstance(testcase, dict):
            return testcase
        cache_key = (str(project_id), str(testcase_id))
        cached_links = self._testcase_link_cache.get(cache_key)
        if not cached_links:
            return testcase
        existing = testcase.get("linked_vulnerabilities") or []
        merged: List[str] = []
        seen: Set[str] = set()
        if isinstance(existing, dict):
            existing = [existing]
        for item in existing or []:
            if isinstance(item, dict):
                value = item.get("id") or item.get("vulnerability_id") or item.get("_id")
                if value:
                    value = str(value)
            else:
                value = str(item)
            if value and value not in seen:
                merged.append(value)
                seen.add(value)
        for fid in cached_links:
            if fid not in seen:
                merged.append(fid)
                seen.add(fid)
        testcase["linked_vulnerabilities"] = merged
        return testcase

    def _find_testcase_in_list(self, project_id: str, testcase_id: str) -> Optional[Dict[str, Any]]:
        try:
            testcases = self.get_testcases(project_id)
        except Exception:
            return None
        for item in testcases:
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            if item_id and str(item_id) == str(testcase_id):
                return item
        return None

    def upsert_finding_for_project(
        self,
        project_id: str,
        title: str,
        affected_assets: list,
        priority: str,
        likelihood_of_exploitation: int,
        description: str,
        attack_scenario: str,
        remediation_recommendation: str,
        steps_to_reproduce: str,
        tags: Optional[list] = None,
        notes: Optional[list] = None,
        is_zeroday: bool = False,
        is_visible: bool = True,
        import_to_library: Optional[str] = None,
        import_source: Optional[str] = None,
        import_source_id: Optional[str] = None,
        custom_fields: Optional[list] = None,
        linked_testcases: Optional[list] = None,
        custom_tags: Optional[list] = None,
        writeup_custom_fields: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Create or update a finding for a project. If a finding with the same title and writeup exists,
        append the assets and notes; otherwise, create a new finding.

        Args:
            project_id (str): The project ID.
            title (str): The title of the finding.
            affected_assets (list): List of affected asset objects or names.
            priority (str): The priority (e.g., "Critical").
            likelihood_of_exploitation (int): Likelihood of exploitation (e.g., 10).
            description (str): Description of the finding.
            attack_scenario (str): Attack scenario details.
            remediation_recommendation (str): Remediation recommendation.
            steps_to_reproduce (str): Steps to reproduce the finding.
            tags (list, optional): List of tags.
            notes (list, optional): List of notes.
            is_zeroday (bool, optional): Whether this is a zero-day finding.
            is_visible (bool, optional): Whether the finding is visible.
            import_to_library (str, optional): Library to import to.
            import_source (str, optional): Source of import.
            import_source_id (str, optional): Source ID for import.
            custom_fields (list, optional): List of custom fields.
            linked_testcases (list, optional): List of linked testcases.
            custom_tags (list, optional): List of custom tags.
            writeup_custom_fields (list, optional): List of custom fields for the writeup.

        Returns:
            dict: The created or updated finding.
        """
        asset_names = []
        for asset in affected_assets:
            name = asset["name"] if isinstance(asset, dict) and "name" in asset else asset
            self.get_asset_by_name(name)
            asset_names.append(name)

        findings = self.get_findings_for_project(project_id)
        logger.debug(
            "Found %s findings for project %s",
            len(findings),
            project_id
        )
        for f in findings:
            logger.debug(
                "Finding id=%s title=%s steps=%s",
                f.get("vulnerability_id"),
                f.get("vulnerability_title"),
                f.get("vulnerability_steps_to_reproduce"),
            )
            logger.debug("Finding payload: %s", f)
        match = None
        for f in findings:
            if f.get("vulnerability_title") == title:
                match = f
                break

        if match:
            updated_assets = set()
            if "vulnerability_affected_assets" in match:
                for asset in match["vulnerability_affected_assets"]:
                    if isinstance(asset, dict):
                        if "asset" in asset and isinstance(asset["asset"], dict) and "name" in asset["asset"]:
                            updated_assets.add(asset["asset"]["name"])
                        elif "name" in asset:
                            updated_assets.add(asset["name"])
                    elif isinstance(asset, str):
                        updated_assets.add(asset)
            elif "vulnerability_affected_asset_name" in match:
                updated_assets.add(match["vulnerability_affected_asset_name"])
            updated_assets.update(asset_names)
            existing_notes = match.get("vulnerability_notes", [])
            new_notes = notes or []
            note_texts = {n["note"] for n in existing_notes if "note" in n}
            for n in new_notes:
                if isinstance(n, dict) and "note" in n:
                    if n["note"] not in note_texts:
                        existing_notes.append(n)
                        note_texts.add(n["note"])
                elif isinstance(n, str):
                    if n not in note_texts:
                        existing_notes.append({"note": n, "type": "PLAINTEXT"})
                        note_texts.add(n)
            update_payload = {
                "affected_assets": [{"assetName": n} for n in updated_assets],
                "notes": existing_notes,
                "projectId": project_id,
            }
            resp = self._request("put", f"/api/ss/vulnerability/{match['vulnerability_id']}", json_data=update_payload)
            if resp.status_code not in (200, 201):
                raise RuntimeError(f"Failed to update finding: {resp.text}")
            return {
                "action": "update",
                "existing_finding_id": match["vulnerability_id"],
                "update_payload": update_payload,
                "api_response": resp.json(),
            }
        else:
            assets_payload = []
            for asset in affected_assets:
                if isinstance(asset, dict) and "name" in asset:
                    assets_payload.append({"assetName": asset["name"]})
                else:
                    assets_payload.append({"assetName": asset})
            result = self.create_vulnerability(
                project_id=project_id,
                title=title,
                affected_assets=assets_payload,
                priority=priority,
                likelihood_of_exploitation=likelihood_of_exploitation,
                description=description,
                attack_scenario=attack_scenario,
                remediation_recommendation=remediation_recommendation,
                steps_to_reproduce=steps_to_reproduce,
                tags=tags,
                notes=notes,
                is_zeroday=is_zeroday,
                is_visible=is_visible,
                import_to_library=import_to_library,
                import_source=import_source,
                import_source_id=import_source_id,
                custom_fields=custom_fields,
                linked_testcases=linked_testcases,
                custom_tags=custom_tags,
                writeup_custom_fields=writeup_custom_fields,
            )
            return {
                "action": "create",
                "result": result,
            }

    def _list_project_findings(
        self,
        project_id: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Internal helper to fetch findings for a project with optional query params.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        resp = self._request(
            "get",
            f"/api/ss/project/{project_id}/vulnerabilities",
            params=params or {},
        )
        self._ensure_response(resp, (200,), "fetch findings")
        data = resp.json()
        if isinstance(data, dict) and "vulnerabilities" in data:
            findings = data.get("vulnerabilities") or []
        elif isinstance(data, list):
            findings = data
        else:
            findings = []
        return findings if isinstance(findings, list) else []

    def get_findings(
        self,
        project_id: str,
        page: int = 1,
        limit: int = 100,
        priority: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Backwards-compatible listing of findings with optional pagination.

        Args:
            project_id (str): The project ID.
            page (int, optional): 1-based page number. Defaults to 1.
            limit (int, optional): Page size. Defaults to 100.
            priority (str, optional): Filter by priority.

        Returns:
            list: Page of finding/vulnerability dicts.
        """
        if page < 1:
            raise ValueError("page must be >= 1")
        if limit < 1:
            raise ValueError("limit must be >= 1")
        params: Dict[str, Any] = {
            "skip": (page - 1) * limit,
            "limit": limit,
            "page": page,
        }
        if priority:
            params["priority"] = priority
        findings = self._list_project_findings(project_id, params=params)
        if len(findings) > limit:
            start = (page - 1) * limit
            findings = findings[start:start + limit]
        return findings

    def get_findings_for_project(self, project_id: str, priority: Optional[str] = None) -> list:
        """
        Fetch all findings/vulnerabilities for a given project.

        Args:
            project_id (str): The project ID.
            priority (str, optional): Filter by priority (e.g., "Critical"). Defaults to None.

        Returns:
            list: List of finding/vulnerability dicts.
        """
        params = {"priority": priority} if priority else None
        return self._list_project_findings(project_id, params=params)

    def get_vulnerability(self, vulnerability_id: str) -> Dict[str, Any]:
        """
        Retrieve a single vulnerability by ID.

        Args:
            vulnerability_id (str): The vulnerability ID.

        Returns:
            dict: Vulnerability details.
        """
        if not vulnerability_id:
            raise ValueError("Missing required field: vulnerability_id")
        resp = self._request("get", f"/api/ss/vulnerability/{vulnerability_id}")
        self._ensure_response(resp, (200,), "fetch vulnerability")
        data = resp.json()
        vulnerability = self._normalize_vulnerability_payload(data)
        if isinstance(vulnerability, dict):
            evidence_items = vulnerability.get("vulnerability_evidence") or []
            if isinstance(evidence_items, dict):
                evidence_items = [evidence_items]
            for item in evidence_items or []:
                if not isinstance(item, dict):
                    continue
                name = (
                    item.get("file_name_custom")
                    or item.get("file_name")
                    or item.get("name")
                    or item.get("filename")
                    or item.get("original_name")
                    or item.get("original_filename")
                )
                if not name:
                    continue
                size = (
                    item.get("file_size")
                    or item.get("size")
                    or item.get("file_size_bytes")
                    or item.get("fileSize")
                    or item.get("fileSizeBytes")
                )
                try:
                    if size is not None:
                        self._cache_vulnerability_evidence(
                            vulnerability_id,
                            os.path.basename(str(name)),
                            int(size),
                        )
                except (TypeError, ValueError):
                    continue
        return vulnerability

    def extract_assets_from_finding(self, finding: Dict[str, Any]) -> Set[str]:
        """
        Extract affected asset names from a finding/vulnerability payload.

        Args:
            finding (dict): Finding/vulnerability payload.

        Returns:
            set: Asset names.
        """
        names: Set[str] = set()
        if not isinstance(finding, dict):
            return names
        raw_assets = (
            finding.get("vulnerability_affected_assets")
            or finding.get("affected_assets")
            or finding.get("affectedAssets")
            or finding.get("assets")
            or finding.get("affected_asset")
            or finding.get("affectedAsset")
            or []
        )
        if isinstance(raw_assets, dict):
            raw_assets = [raw_assets]
        for asset in raw_assets:
            if isinstance(asset, dict):
                name = asset.get("assetName") or asset.get("asset_name") or asset.get("name") or asset.get("asset")
                if not name and isinstance(asset.get("asset"), dict):
                    nested = asset.get("asset") or {}
                    name = nested.get("name") or nested.get("asset") or nested.get("asset_name")
                if name:
                    names.add(str(name))
            elif isinstance(asset, str):
                names.add(asset)
        for key in (
            "vulnerability_affected_asset_name",
            "affected_asset_name",
            "affectedAssetName",
            "asset_name",
        ):
            value = finding.get(key)
            if value:
                names.add(str(value))
        return names

    def update_finding(
        self,
        vulnerability_id: str,
        project_id: Optional[str] = None,
        affected_assets: Optional[list] = None,
        notes: Optional[list] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing finding/vulnerability with the provided fields.

        Args:
            vulnerability_id (str): The vulnerability ID to update.
            project_id (str, optional): Project ID when required by the API.
            affected_assets (list, optional): List of asset names or dicts with 'name'/'assetName'.
            notes (list, optional): Notes payload to set.
            **kwargs: Any additional fields accepted by the AttackForge API.

        Returns:
            dict: API response body.
        """
        if not vulnerability_id:
            raise ValueError("Missing required field: vulnerability_id")
        payload, params = self._build_update_finding_payload(
            project_id,
            affected_assets,
            notes,
            kwargs,
        )
        resp = self._request(
            "put",
            f"/api/ss/vulnerability/{vulnerability_id}",
            json_data=payload,
            params=params,
        )
        self._ensure_response(resp, (200, 201), "update finding")
        data = resp.json()
        return self._unwrap(data, "vulnerability")

    def add_note_to_finding(
        self,
        vulnerability_id: str,
        note: Any,
        note_type: str = "PLAINTEXT"
    ) -> Dict[str, Any]:
        """
        Append a note to an existing finding.

        Args:
            vulnerability_id (str): The vulnerability ID.
            note (str or dict): Note text or note object with a 'note' key.
            note_type (str): Note type when passing a plain string (default: "PLAINTEXT").

        Returns:
            dict: API response.
        """
        if not vulnerability_id:
            raise ValueError("Missing required field: vulnerability_id")
        if note is None or note == "":
            raise ValueError("Missing required field: note")
        if isinstance(note, dict):
            note_text = note.get("note")
            note_entry = note
        else:
            note_text = str(note)
            note_entry = {"note": note_text, "type": note_type}
        if not note_text:
            raise ValueError("Note text cannot be empty")
        try:
            vuln = self.get_vulnerability(vulnerability_id)
            existing_notes = (
                vuln.get("vulnerability_notes")
                or vuln.get("notes")
                or []
            ) if isinstance(vuln, dict) else []
        except Exception as exc:
            logger.warning(
                "Unable to fetch existing vulnerability notes; proceeding with provided note only: %s",
                exc
            )
            existing_notes = []
        collected_notes = []
        note_texts = set()
        for n in existing_notes:
            if isinstance(n, dict) and "note" in n:
                if n["note"] in note_texts:
                    continue
                collected_notes.append(n)
                note_texts.add(n["note"])
        if note_entry.get("note") not in note_texts:
            collected_notes.append(note_entry)
        payload = {"notes": collected_notes}
        resp = self._request("put", f"/api/ss/vulnerability/{vulnerability_id}", json_data=payload)
        self._ensure_response(resp, (200, 201), "add note to finding")
        data = resp.json()
        return self._unwrap(data, "vulnerability")

    def link_vulnerability_to_testcases(
        self,
        vulnerability_id: str,
        testcase_ids: List[str],
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Link a vulnerability to one or more testcases.

        Args:
            vulnerability_id (str): The vulnerability ID.
            testcase_ids (list): List of testcase IDs to link.
            project_id (str, optional): Project ID if required by the API.

        Returns:
            dict: API response.
        """
        if not vulnerability_id:
            raise ValueError("Missing required field: vulnerability_id")
        if not testcase_ids:
            raise ValueError("testcase_ids must contain at least one ID")
        payload: Dict[str, Any] = {
            "linked_testcases": testcase_ids,
        }
        params = {"projectId": project_id} if project_id else None
        resp = self._request(
            "put",
            f"/api/ss/vulnerability/{vulnerability_id}",
            json_data=payload,
            params=params,
        )
        self._ensure_response(resp, (200, 201), "link vulnerability to testcases")
        data = resp.json()
        if project_id:
            for tc_id in testcase_ids:
                self._cache_testcase_link(project_id, tc_id, vulnerability_id)
        return self._unwrap(data, "vulnerability")

    def get_testcases(
        self,
        project_id: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve testcases for a project.

        Args:
            project_id (str): Project ID.
            params (dict, optional): Optional query params (e.g., pagination or filters).

        Returns:
            list: List of testcase dicts.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        resp = self._request(
            "get",
            f"/api/ss/project/{project_id}/testcases",
            params=params or None
        )
        self._ensure_response(resp, (200, 201), "fetch testcases")
        data = resp.json()
        if isinstance(data, dict) and "testcases" in data:
            testcases = data.get("testcases", [])
        elif isinstance(data, list):
            testcases = data
        else:
            return []
        normalized: List[Dict[str, Any]] = []
        for item in testcases:
            normalized.append(self._normalize_testcase_payload(item))
        return normalized

    def get_testcase(self, project_id: str, testcase_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single testcase by ID.

        Args:
            project_id (str): Project ID.
            testcase_id (str): Testcase ID.

        Returns:
            dict or None: Testcase details if found, else None.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not testcase_id:
            raise ValueError("Missing required field: testcase_id")
        resp = self._request("get", f"/api/ss/project/{project_id}/testcase/{testcase_id}")
        if resp.status_code == 404:
            testcase = self._find_testcase_in_list(project_id, testcase_id)
            return self._apply_cached_testcase_links(project_id, testcase_id, testcase)
        self._ensure_response(resp, (200, 201), "fetch testcase")
        data = resp.json()
        testcase = self._normalize_testcase_payload(data if isinstance(data, dict) else None)
        if not isinstance(testcase, dict):
            testcase = self._find_testcase_in_list(project_id, testcase_id)
        return self._apply_cached_testcase_links(project_id, testcase_id, testcase)

    def get_project_testcase_by_id(
        self,
        project_id: str,
        testcase_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Alias for get_testcase to support project testcase lookup.
        """
        return self.get_testcase(project_id, testcase_id)

    def extract_findings_from_testcase(self, testcase: Dict[str, Any]) -> List[str]:
        """
        Extract linked finding IDs from a testcase payload.
        """
        if not isinstance(testcase, dict):
            return []
        linked = (
            testcase.get("linked_vulnerabilities")
            or testcase.get("linked_findings")
            or testcase.get("linked_vulnerability_ids")
            or testcase.get("linked_vulnerability_id")
            or []
        )
        if isinstance(linked, dict):
            linked = [linked]
        findings: List[str] = []
        seen: Set[str] = set()
        for item in linked:
            value = None
            if isinstance(item, dict):
                for key in ("id", "vulnerability_id", "_id"):
                    if item.get(key):
                        value = str(item.get(key))
                        break
            elif isinstance(item, str):
                value = item
            if value and value not in seen:
                findings.append(value)
                seen.add(value)
        return findings

    def list_testcase_notes(self, project_id: str, testcase_id: str) -> List[Dict[str, Any]]:
        """
        List notes associated with a testcase.
        """
        testcase = self.get_project_testcase_by_id(project_id, testcase_id)
        if not testcase:
            testcases = self.get_testcases(project_id)
            testcase = next((t for t in testcases if t.get("id") == testcase_id), None)
        raw_notes = []
        if isinstance(testcase, dict):
            for key in (
                "testcase_notes",
                "notes",
                "testcaseNotes",
                "project_testcase_notes",
                "testcase_note",
            ):
                if key in testcase and testcase.get(key) is not None:
                    raw_notes = testcase.get(key) or []
                    break
        if isinstance(raw_notes, dict):
            raw_notes = [raw_notes]
        notes: List[Dict[str, Any]] = []
        for note in raw_notes or []:
            if isinstance(note, dict):
                content = (
                    note.get("content")
                    or note.get("note")
                    or note.get("details")
                    or note.get("text")
                )
                entry = dict(note)
                if content is not None:
                    entry.setdefault("content", content)
                notes.append(entry)
            else:
                notes.append({"content": str(note)})
        return notes

    def list_testcase_files(self, project_id: str, testcase_id: str) -> List[Dict[str, Any]]:
        """
        List files/evidence associated with a testcase.
        """
        testcase = self.get_project_testcase_by_id(project_id, testcase_id)
        if not testcase:
            testcases = self.get_testcases(project_id)
            testcase = next((t for t in testcases if t.get("id") == testcase_id), None)
        raw_files = []
        if isinstance(testcase, dict):
            for key in (
                "files",
                "testcase_files",
                "testcaseFiles",
                "project_testcase_files",
                "projectTestcaseFiles",
                "uploaded_files",
                "attachments",
                "evidence",
                "testcase_evidence",
            ):
                if key in testcase and testcase.get(key) is not None:
                    raw_files = testcase.get(key) or []
                    break
        if isinstance(raw_files, dict):
            raw_files = [raw_files]
        files: List[Dict[str, Any]] = []
        for item in raw_files or []:
            if isinstance(item, dict):
                files.append(item)
            else:
                files.append({"name": str(item)})
        cache_key = (str(project_id), str(testcase_id))
        cache = self._testcase_evidence_cache.setdefault(cache_key, set())
        for item in files:
            if not isinstance(item, dict):
                continue
            name = (
                item.get("file_name_custom")
                or item.get("file_name")
                or item.get("name")
                or item.get("filename")
                or item.get("original_name")
                or item.get("original_filename")
            )
            size = (
                item.get("file_size")
                or item.get("size")
                or item.get("file_size_bytes")
                or item.get("fileSize")
                or item.get("fileSizeBytes")
            )
            if not name or size is None:
                continue
            try:
                cache.add((os.path.basename(str(name)), int(size)))
            except (TypeError, ValueError):
                continue
        if cache:
            existing_keys = set()
            for item in files:
                if not isinstance(item, dict):
                    continue
                name = (
                    item.get("file_name_custom")
                    or item.get("file_name")
                    or item.get("name")
                    or item.get("filename")
                    or item.get("original_name")
                    or item.get("original_filename")
                )
                size = (
                    item.get("file_size")
                    or item.get("size")
                    or item.get("file_size_bytes")
                    or item.get("fileSize")
                    or item.get("fileSizeBytes")
                )
                if not name or size is None:
                    continue
                try:
                    existing_keys.add((os.path.basename(str(name)), int(size)))
                except (TypeError, ValueError):
                    continue
            for basename, size in cache:
                if (basename, size) in existing_keys:
                    continue
                files.append({"file_name_custom": basename, "file_size": size, "source": "cache"})
        return files

    def link_finding_to_testcase(
        self,
        project_id: str,
        testcase_id: str,
        finding_id: str,
    ) -> Dict[str, Any]:
        """
        Link a finding to a testcase.
        """
        if not finding_id:
            raise ValueError("Missing required field: finding_id")
        response: Optional[Dict[str, Any]] = None
        try:
            response = self.link_vulnerability_to_testcases(
                vulnerability_id=finding_id,
                testcase_ids=[testcase_id],
                project_id=project_id,
            )
        except PermissionError:
            raise
        except Exception as exc:
            logger.warning("Unable to link finding via vulnerability update: %s", exc)
        try:
            tc_response = self.add_findings_to_testcase(
                project_id=project_id,
                testcase_id=testcase_id,
                vulnerability_ids=[finding_id],
            )
            if response is None:
                response = tc_response
        except PermissionError:
            raise
        except Exception as exc:
            if response is None:
                raise
            logger.warning("Unable to link finding via testcase update: %s", exc)
        self._cache_testcase_link(project_id, testcase_id, finding_id)
        return response or {"linked": True}

    def attach_finding_to_testcase_with_notes_and_evidence(
        self,
        project_id: str,
        testcase_id: str,
        finding_id: str,
        note_text: Optional[str] = None,
        evidence_path: Optional[str] = None,
        dedupe: bool = True,
    ) -> Dict[str, Any]:
        """
        Link a finding to a testcase, add a note, and upload evidence with idempotent checks.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not testcase_id:
            raise ValueError("Missing required field: testcase_id")
        if not finding_id:
            raise ValueError("Missing required field: finding_id")
        result: Dict[str, Any] = {}
        result["link_response"] = self.link_finding_to_testcase(
            project_id=project_id,
            testcase_id=testcase_id,
            finding_id=finding_id,
        )

        if note_text is not None:
            note_created = False
            note_reason = None
            if dedupe:
                try:
                    notes = self.list_testcase_notes(project_id, testcase_id)
                    if any(
                        note_text == (n.get("content") or n.get("note") or "")
                        for n in notes
                        if isinstance(n, dict)
                    ):
                        note_reason = "duplicate"
                    else:
                        note_created = True
                except Exception:
                    note_created = True
            else:
                note_created = True

            if note_created:
                result["note_response"] = self.add_note_to_testcase(
                    project_id=project_id,
                    testcase_id=testcase_id,
                    note=note_text,
                )
                result["note_created"] = True
            else:
                if note_reason == "duplicate":
                    print(f"SKIP note (already exists): {note_text}")
                result["note_created"] = False
                result["note_reason"] = note_reason or "duplicate"
        else:
            result["note_created"] = False

        if evidence_path:
            evidence_uploaded = False
            evidence_reason = None
            if dedupe:
                try:
                    basename = os.path.basename(evidence_path)
                    file_size = os.path.getsize(evidence_path)
                    cache_key = (str(project_id), str(testcase_id))
                    cache = self._testcase_evidence_cache.get(cache_key, set())
                    files: List[Dict[str, Any]] = []
                    if (basename, int(file_size)) in cache:
                        print(
                            f"SKIP evidence (already exists): {basename} ({file_size} bytes)"
                        )
                        evidence_reason = "duplicate"
                    else:
                        files = self.list_testcase_files(project_id, testcase_id)
                    for item in files if evidence_reason != "duplicate" else []:
                        if not isinstance(item, dict):
                            continue
                        name = (
                            item.get("file_name_custom")
                            or item.get("file_name")
                            or item.get("name")
                            or item.get("filename")
                            or item.get("original_name")
                            or item.get("original_filename")
                        )
                        if not name:
                            continue
                        if os.path.basename(str(name)) != basename:
                            continue
                        existing_size = (
                            item.get("file_size")
                            or item.get("size")
                            or item.get("file_size_bytes")
                            or item.get("fileSize")
                            or item.get("fileSizeBytes")
                        )
                        if existing_size is None:
                            continue
                        try:
                            if int(existing_size) == int(file_size):
                                print(
                                    f"SKIP evidence (already exists): {basename} ({file_size} bytes)"
                                )
                                evidence_reason = "duplicate"
                                self._cache_testcase_evidence(
                                    project_id, testcase_id, basename, int(file_size)
                                )
                                break
                        except (TypeError, ValueError):
                            continue
                    if evidence_reason != "duplicate":
                        evidence_uploaded = True
                except Exception:
                    evidence_uploaded = True
            else:
                evidence_uploaded = True

            if evidence_uploaded:
                result["evidence_response"] = self.upload_testcase_evidence(
                    project_id=project_id,
                    testcase_id=testcase_id,
                    file_path=evidence_path,
                )
                try:
                    self._cache_testcase_evidence(
                        project_id,
                        testcase_id,
                        os.path.basename(evidence_path),
                        int(os.path.getsize(evidence_path)),
                    )
                except (OSError, ValueError, TypeError):
                    pass
                result["evidence_uploaded"] = True
            else:
                result["evidence_uploaded"] = False
                result["evidence_reason"] = evidence_reason or "duplicate"
        else:
            result["evidence_uploaded"] = False

        return result

    def create_testcase(
        self,
        project_id: str,
        testcase: Optional[str] = None,
        details: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        title: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a testcase for a project.

        Args:
            project_id (str): Project ID.
            testcase (str): Testcase title/name.
            title (str, optional): Alias for testcase title/name.
            details (str, optional): Testcase details/description.
            status (str, optional): Initial status (e.g., "Not Tested").
            tags (list, optional): Tags to associate with the testcase.
            **kwargs: Additional fields accepted by the API.

        Returns:
            dict: Created testcase details.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        resolved_testcase = testcase or title
        if not resolved_testcase:
            raise ValueError("Missing required field: testcase")
        payload: Dict[str, Any] = {"testcase": resolved_testcase}
        if details is not None:
            payload["details"] = details
        if tags is not None:
            payload["tags"] = tags
        payload.update(kwargs)
        if status is not None:
            payload["status"] = status
        if "status" in payload:
            if payload["status"] is None:
                payload.pop("status")
            else:
                payload["status"] = self._normalize_testcase_status(payload["status"])
        resp = self._request(
            "post",
            f"/api/ss/project/{project_id}/testcase",
            json_data=payload
        )
        self._ensure_response(resp, (200, 201), "create testcase")
        data = resp.json()
        testcase_payload = self._unwrap(data, "testcase")
        return self._normalize_testcase_payload(testcase_payload)

    def delete_testcase(self, project_id: str, testcase_id: str) -> Dict[str, Any]:
        """
        Delete a testcase from a project.

        Args:
            project_id (str): Project ID.
            testcase_id (str): Testcase ID.

        Returns:
            dict: API response (or a simple deleted marker if empty).
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not testcase_id:
            raise ValueError("Missing required field: testcase_id")
        resp = self._request(
            "delete",
            f"/api/ss/project/{project_id}/testcase/{testcase_id}"
        )
        if resp.status_code == 404:
            return {"deleted": False, "reason": "not_found"}
        self._ensure_response(resp, (200, 204), "delete testcase")
        if resp.status_code == 204:
            return {"deleted": True}
        try:
            data = resp.json()
        except ValueError:
            return {"deleted": True}
        return data if data else {"deleted": True}

    def upload_finding_evidence(
        self,
        vulnerability_id: str,
        file_path: str,
        dedupe: bool = True
    ) -> Dict[str, Any]:
        """
        Upload evidence to a finding/vulnerability.

        Args:
            vulnerability_id (str): The vulnerability ID.
            file_path (str): Path to the evidence file.

            dedupe (bool): Skip upload if evidence already exists (default: True).

        Returns:
            dict: API response.
        """
        if not vulnerability_id:
            raise ValueError("Missing required field: vulnerability_id")
        if not file_path:
            raise ValueError("Missing required field: file_path")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Evidence file not found: {file_path}")
        endpoint = f"/api/ss/vulnerability/{vulnerability_id}/evidence"
        basename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        if dedupe:
            cached = self._vulnerability_evidence_cache.get(str(vulnerability_id), set())
            if (basename, int(file_size)) in cached:
                print(
                    f"SKIP evidence (already exists): {basename} ({file_size} bytes)"
                )
                return {
                    "uploaded": False,
                    "reason": "duplicate",
                    "existing_evidence": {
                        "file_name_custom": basename,
                        "file_size": file_size,
                        "source": "cache",
                    },
                }
            try:
                vuln = self.get_vulnerability(vulnerability_id)
                evidence_items = []
                if isinstance(vuln, dict):
                    evidence_items = vuln.get("vulnerability_evidence") or []
                if isinstance(evidence_items, dict):
                    evidence_items = [evidence_items]
                if not isinstance(evidence_items, list):
                    evidence_items = []
                file_hash = None
                for item in evidence_items:
                    existing_hash = self._evidence_hash_value(item)
                    if existing_hash and file_hash is None:
                        file_hash = self._sha256_file(file_path)
                    if self._evidence_matches(
                        item,
                        basename,
                        file_size,
                        file_hash=file_hash,
                        evidence_hash=existing_hash,
                    ):
                        print(
                            f"SKIP evidence (already exists): {basename} ({file_size} bytes)"
                        )
                        try:
                            self._cache_vulnerability_evidence(
                                vulnerability_id, basename, int(file_size)
                            )
                        except (TypeError, ValueError):
                            pass
                        return {
                            "uploaded": False,
                            "reason": "duplicate",
                            "existing_evidence": item,
                        }
            except PermissionError:
                raise
            except Exception as exc:
                logger.warning("Evidence dedupe check failed; proceeding with upload: %s", exc)
        if self.dry_run:
            resp = self._request("post", endpoint)
            return {"uploaded": True, "dry_run": True, "response": resp.json()}
        with open(file_path, "rb") as evidence:
            resp = self._request(
                "post",
                endpoint,
                files={"file": (os.path.basename(file_path), evidence)}
            )
        self._ensure_response(resp, (200, 201), "upload finding evidence")
        try:
            self._cache_vulnerability_evidence(
                vulnerability_id, basename, int(file_size)
            )
        except (TypeError, ValueError):
            pass
        return {"uploaded": True, "response": resp.json()}

    def delete_finding_evidence(self, vulnerability_id: str, storage_name: str) -> Dict[str, Any]:
        """
        Delete evidence from a vulnerability by storage name.

        Args:
            vulnerability_id (str): The vulnerability ID.
            storage_name (str): Evidence storage name returned by the API.

        Returns:
            dict: API response or deleted marker.
        """
        if not vulnerability_id:
            raise ValueError("Missing required field: vulnerability_id")
        if not storage_name:
            raise ValueError("Missing required field: storage_name")
        endpoint = f"/api/ss/vulnerability/{vulnerability_id}/evidence/{storage_name}"
        resp = self._request("delete", endpoint)
        self._ensure_response(resp, (200, 204), "delete finding evidence")
        if resp.status_code == 204:
            return {"deleted": True}
        try:
            data = resp.json()
        except ValueError:
            return {"deleted": True}
        return data if data else {"deleted": True}

    def upload_testcase_evidence(
        self,
        project_id: str,
        testcase_id: str,
        file_path: str
    ) -> Dict[str, Any]:
        """
        Upload evidence to a testcase.

        Args:
            project_id (str): The project ID.
            testcase_id (str): The testcase ID.
            file_path (str): Path to the evidence file.

        Returns:
            dict: API response.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not testcase_id:
            raise ValueError("Missing required field: testcase_id")
        if not file_path:
            raise ValueError("Missing required field: file_path")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Evidence file not found: {file_path}")
        endpoint = f"/api/ss/project/{project_id}/testcase/{testcase_id}/file"
        if self.dry_run:
            resp = self._request("post", endpoint)
            return resp.json()
        with open(file_path, "rb") as evidence:
            resp = self._request(
                "post",
                endpoint,
                files={"file": (os.path.basename(file_path), evidence)}
            )
        self._ensure_response(resp, (200, 201), "upload testcase evidence")
        try:
            self._cache_testcase_evidence(
                project_id,
                testcase_id,
                os.path.basename(file_path),
                int(os.path.getsize(file_path)),
            )
        except (OSError, ValueError, TypeError):
            pass
        return resp.json()

    def add_note_to_testcase(
        self,
        project_id: str,
        testcase_id: str,
        note: str,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a testcase note via the dedicated note endpoint, optionally updating status via update_testcase.

        Args:
            project_id (str): Project ID.
            testcase_id (str): Testcase ID.
            note (str): Note text to set in the details field.
            status (str, optional): Status to set (e.g., "Tested").

        Returns:
            dict: API response.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not testcase_id:
            raise ValueError("Missing required field: testcase_id")
        if not note:
            raise ValueError("Missing required field: note")
        endpoint = f"/api/ss/project/{project_id}/testcase/{testcase_id}/note"
        payload: Dict[str, Any] = {"note": note, "note_type": "PLAINTEXT"}
        resp = self._request("post", endpoint, json_data=payload)
        self._ensure_response(resp, (200, 201), "add testcase note")
        result = resp.json()

        if status:
            try:
                self.update_testcase(project_id, testcase_id, {"status": status})
            except Exception:
                pass
        return result

    def assign_findings_to_testcase(
        self,
        project_id: str,
        testcase_id: str,
        vulnerability_ids: List[str],
        existing_linked_vulnerabilities: Optional[List[str]] = None,
        additional_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Assign one or more findings to a testcase.

        Args:
            project_id (str): The project ID.
            testcase_id (str): The testcase ID.
            vulnerability_ids (list): List of vulnerability IDs to assign.
            existing_linked_vulnerabilities (list, optional): Existing linked vulnerability IDs to merge with.
            additional_fields (dict, optional): Additional testcase fields to include (e.g., status, tags).

        Returns:
            dict: API response.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not testcase_id:
            raise ValueError("Missing required field: testcase_id")
        if not vulnerability_ids:
            raise ValueError("vulnerability_ids must contain at least one ID")
        payload = additional_fields.copy() if additional_fields else {}
        merged_ids = []
        seen = set()
        for vid in (existing_linked_vulnerabilities or []) + vulnerability_ids:
            if vid and vid not in seen:
                merged_ids.append(vid)
                seen.add(vid)
        payload["linked_vulnerabilities"] = merged_ids
        resp = self.update_testcase(project_id, testcase_id, payload)
        for vid in merged_ids:
            self._cache_testcase_link(project_id, testcase_id, vid)
        return resp

    def update_testcase(
        self,
        project_id: str,
        testcase_id: str,
        update_fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a testcase with the provided fields.

        Args:
            project_id (str): The project ID.
            testcase_id (str): The testcase ID.
            update_fields (dict): Fields to update (e.g., linked_vulnerabilities, details).

        Returns:
            dict: API response.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not testcase_id:
            raise ValueError("Missing required field: testcase_id")
        if not update_fields:
            raise ValueError("update_fields cannot be empty")
        update_fields = dict(update_fields)
        if "status" in update_fields:
            if update_fields["status"] is None:
                update_fields.pop("status")
            else:
                update_fields["status"] = self._normalize_testcase_status(update_fields["status"])
        if not update_fields:
            raise ValueError("update_fields cannot be empty")
        endpoint = f"/api/ss/project/{project_id}/testcase/{testcase_id}"
        resp = self._request("put", endpoint, json_data=update_fields)
        self._ensure_response(resp, (200, 201), "update testcase")
        data = resp.json()
        testcase = self._unwrap(data, "testcase")
        return self._normalize_testcase_payload(testcase)

    def add_findings_to_testcase(
        self,
        project_id: str,
        testcase_id: str,
        vulnerability_ids: List[str],
        additional_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Fetch a testcase, merge existing linked vulnerabilities with the provided list, and update it.

        Args:
            project_id (str): The project ID.
            testcase_id (str): The testcase ID.
            vulnerability_ids (list): List of vulnerability IDs to add.
            additional_fields (dict, optional): Extra fields to include (e.g., status).

        Returns:
            dict: API response from the update.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not testcase_id:
            raise ValueError("Missing required field: testcase_id")
        if not vulnerability_ids:
            raise ValueError("vulnerability_ids must contain at least one ID")

        testcase = None
        try:
            testcase = self.get_testcase(project_id, testcase_id)
        except Exception:
            testcase = None
        if not testcase:
            testcases = self.get_testcases(project_id)
            testcase = next((t for t in testcases if t.get("id") == testcase_id), None)
        if not testcase:
            raise RuntimeError(f"Testcase '{testcase_id}' not found in project '{project_id}'")

        existing_raw = testcase.get("linked_vulnerabilities", []) or []
        existing_ids: List[str] = []
        for item in existing_raw:
            if isinstance(item, dict) and item.get("id"):
                existing_ids.append(item["id"])
            elif isinstance(item, str):
                existing_ids.append(item)

        return self.assign_findings_to_testcase(
            project_id=project_id,
            testcase_id=testcase_id,
            vulnerability_ids=vulnerability_ids,
            existing_linked_vulnerabilities=existing_ids,
            additional_fields=additional_fields,
        )

    def create_user(
        self,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
        role: str,
        mfa: str,
    ) -> Dict[str, Any]:
        """
        Create a new user in AttackForge.

        Args:
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
            username (str): Username for the user (email if SSO is disabled).
            email (str): Email address of the user.
            password (str): User password (min 15 characters per API docs).
            role (str): Role for the user (admin, librarymod, client, consultant, projectoperator).
            mfa (str): MFA setting ("Yes" or "No").

        Returns:
            dict: Created user details.
        """
        required_fields = [
            ("first_name", first_name),
            ("last_name", last_name),
            ("username", username),
            ("email", email),
            ("password", password),
            ("role", role),
            ("mfa", mfa),
        ]
        for field_name, value in required_fields:
            if value is None or value == "":
                raise ValueError(f"Missing required field: {field_name}")
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password": password,
            "role": role,
            "mfa": mfa,
        }
        resp = self._request("post", "/api/ss/user", json_data=payload)
        if resp.status_code in (200, 201):
            data = resp.json()
            return self._unwrap(data, "user")
        self._ensure_response(resp, (200, 201), "create user")
        return resp.json()

    def create_users(self, users: List[Dict[str, Any]]) -> Any:
        """
        Create multiple users in AttackForge.

        Args:
            users (list): List of user payloads.

        Returns:
            object: API response body.
        """
        if not users:
            raise ValueError("users must contain at least one user payload")
        resp = self._request("post", "/api/ss/users", json_data=users)
        self._ensure_response(resp, (200, 201), "bulk create users")
        return resp.json()

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve a user by ID.

        Args:
            user_id (str): User ID.

        Returns:
            dict: User details.
        """
        if not user_id:
            raise ValueError("Missing required field: user_id")
        resp = self._request("get", f"/api/ss/users/{user_id}")
        self._ensure_response(resp, (200,), "fetch user")
        data = resp.json()
        return self._unwrap(data, "user")

    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        """
        Retrieve a user by email address.

        Args:
            email (str): Email address to look up.

        Returns:
            dict: User details.
        """
        if not email:
            raise ValueError("Missing required field: email")
        email_value = requests.utils.quote(email, safe="")
        resp = self._request("get", f"/api/ss/users/email/{email_value}")
        self._ensure_response(resp, (200,), "fetch user by email")
        data = resp.json()
        return self._unwrap(data, "user")

    def get_user_by_username(self, username: str) -> Dict[str, Any]:
        """
        Retrieve a user by username.

        Args:
            username (str): Username to look up.

        Returns:
            dict: User details.
        """
        if not username:
            raise ValueError("Missing required field: username")
        username_value = requests.utils.quote(username, safe="")
        resp = self._request("get", f"/api/ss/users/username/{username_value}")
        self._ensure_response(resp, (200,), "fetch user by username")
        data = resp.json()
        return self._unwrap(data, "user")

    def get_users(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        username: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve users, optionally filtered by name or identifier.

        Args:
            first_name (str, optional): Filter by first name.
            last_name (str, optional): Filter by last name.
            email (str, optional): Filter by email address.
            username (str, optional): Filter by username.

        Returns:
            list: List of user dicts.
        """
        params: Dict[str, Any] = {}
        if first_name:
            params["firstName"] = first_name
        if last_name:
            params["lastName"] = last_name
        if email:
            params["email"] = email
        if username:
            params["username"] = username
        resp = self._request("get", "/api/ss/users", params=params or None)
        self._ensure_response(resp, (200,), "fetch users")
        data = resp.json()
        if isinstance(data, dict) and "users" in data:
            return data.get("users", [])
        if isinstance(data, list):
            return data
        return []

    def update_user(
        self,
        user_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email_address: Optional[str] = None,
        username: Optional[str] = None,
        is_deleted: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Update a user's profile fields.

        Args:
            user_id (str): User ID.
            first_name (str, optional): First name.
            last_name (str, optional): Last name.
            email_address (str, optional): Email address.
            username (str, optional): Username.
            is_deleted (bool, optional): Mark user deleted.

        Returns:
            dict: Updated user details.
        """
        if not user_id:
            raise ValueError("Missing required field: user_id")
        payload: Dict[str, Any] = {}
        if first_name is not None:
            payload["first_name"] = first_name
        if last_name is not None:
            payload["last_name"] = last_name
        if email_address is not None:
            payload["email_address"] = email_address
        if username is not None:
            payload["username"] = username
        if is_deleted is not None:
            payload["is_deleted"] = is_deleted
        if not payload:
            raise ValueError("No update fields provided for user")
        resp = self._request("put", f"/api/ss/user/{user_id}", json_data=payload)
        self._ensure_response(resp, (200, 201), "update user")
        data = resp.json()
        return self._unwrap(data, "user")

    def activate_user(self, user_id: str) -> Dict[str, Any]:
        """
        Activate a user.

        Args:
            user_id (str): User ID.

        Returns:
            dict: API response.
        """
        if not user_id:
            raise ValueError("Missing required field: user_id")
        resp = self._request("put", f"/api/ss/user/{user_id}/activate")
        self._ensure_response(resp, (200, 201), "activate user")
        return resp.json()

    def deactivate_user(self, user_id: str) -> Dict[str, Any]:
        """
        Deactivate a user.

        Args:
            user_id (str): User ID.

        Returns:
            dict: API response.
        """
        if not user_id:
            raise ValueError("Missing required field: user_id")
        resp = self._request("put", f"/api/ss/user/{user_id}/deactivate")
        self._ensure_response(resp, (200, 201), "deactivate user")
        return resp.json()

    def add_user_to_group(
        self,
        group_id: str,
        user_id: str,
        access_level: str,
    ) -> Dict[str, Any]:
        """
        Add a user to a group with a default access level.

        Args:
            group_id (str): Group ID.
            user_id (str): User ID.
            access_level (str): View, Upload, or Edit.

        Returns:
            dict: API response.
        """
        if not group_id:
            raise ValueError("Missing required field: group_id")
        if not user_id:
            raise ValueError("Missing required field: user_id")
        if not access_level:
            raise ValueError("Missing required field: access_level")
        payload = {
            "group_id": group_id,
            "user_id": user_id,
            "access_level": access_level,
        }
        resp = self._request("post", "/api/ss/group/user", json_data=payload)
        self._ensure_response(resp, (200, 201), "add user to group")
        return resp.json()

    def update_user_access_on_group(
        self,
        group_id: str,
        user_id: str,
        access_level: str,
    ) -> Dict[str, Any]:
        """
        Update a user's access on a group.

        Args:
            group_id (str): Group ID.
            user_id (str): User ID.
            access_level (str): View, Upload, Edit, or Delete.

        Returns:
            dict: API response.
        """
        if not group_id:
            raise ValueError("Missing required field: group_id")
        if not user_id:
            raise ValueError("Missing required field: user_id")
        if not access_level:
            raise ValueError("Missing required field: access_level")
        payload = {
            "group_id": group_id,
            "user_id": user_id,
            "access_level": access_level,
        }
        resp = self._request(
            "put",
            f"/api/ss/group/user/{user_id}",
            json_data=payload,
        )
        self._ensure_response(resp, (200, 201), "update user access on group")
        return resp.json()

    def update_user_access_on_project(
        self,
        project_id: str,
        user_id: str,
        update_action: str,
    ) -> Dict[str, Any]:
        """
        Update a user's access on a project.

        Args:
            project_id (str): Project ID.
            user_id (str): User ID.
            update_action (str): View, Upload, Edit, Delete, or Restore.

        Returns:
            dict: API response.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not user_id:
            raise ValueError("Missing required field: user_id")
        if not update_action:
            raise ValueError("Missing required field: update_action")
        payload = {"update": update_action}
        resp = self._request(
            "put",
            f"/api/ss/project/{project_id}/access/{user_id}",
            json_data=payload,
        )
        self._ensure_response(resp, (200, 201), "update user access on project")
        return resp.json()

    def invite_user_to_project(
        self,
        project_id: str,
        username: str,
        access_level: str,
        role: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Invite a single user to a project.

        Args:
            project_id (str): Project ID.
            username (str): Username or email address.
            access_level (str): View, Upload, or Edit.
            role (str, optional): Collaboration role.

        Returns:
            dict: API response.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not username:
            raise ValueError("Missing required field: username")
        if not access_level:
            raise ValueError("Missing required field: access_level")
        payload: Dict[str, Any] = {
            "id": project_id,
            "username": username,
            "accessLevel": access_level,
        }
        if role is not None:
            payload["role"] = role
        resp = self._request(
            "post",
            f"/api/ss/project/{project_id}/invite",
            json_data=payload,
        )
        self._ensure_response(resp, (200, 201), "invite user to project")
        return resp.json()

    def invite_users_to_project_team(
        self,
        project_id: str,
        users: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Invite multiple users to a project team.

        Args:
            project_id (str): Project ID.
            users (list): List of user invite payloads.

        Returns:
            dict: API response.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not users:
            raise ValueError("users must contain at least one user payload")
        payload = {"users": users}
        resp = self._request(
            "post",
            f"/api/ss/project/{project_id}/team/invite",
            json_data=payload,
        )
        self._ensure_response(resp, (200, 201), "invite users to project team")
        return resp.json()

    def get_user_groups(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve groups for a user.

        Args:
            user_id (str): User ID.

        Returns:
            list: List of group dicts.
        """
        if not user_id:
            raise ValueError("Missing required field: user_id")
        resp = self._request("get", f"/api/ss/user/{user_id}/groups")
        self._ensure_response(resp, (200,), "fetch user groups")
        data = resp.json()
        if isinstance(data, dict) and "groups" in data:
            return data.get("groups", [])
        if isinstance(data, list):
            return data
        return []

    def get_user_projects(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve projects for a user.

        Args:
            user_id (str): User ID.

        Returns:
            list: List of project dicts.
        """
        if not user_id:
            raise ValueError("Missing required field: user_id")
        resp = self._request("get", f"/api/ss/user/{user_id}/projects")
        self._ensure_response(resp, (200,), "fetch user projects")
        data = resp.json()
        if isinstance(data, dict) and "projects" in data:
            return data.get("projects", [])
        if isinstance(data, list):
            return data
        return []

    def get_user_audit_logs(
        self,
        user_id: str,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        include_request_body: Optional[bool] = None,
        endpoint: Optional[str] = None,
        method: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve audit logs for a user.

        Args:
            user_id (str): User ID.
            skip (int, optional): Number of records to skip.
            limit (int, optional): Max number of records to return.
            include_request_body (bool, optional): Include request body in logs.
            endpoint (str, optional): Filter logs by endpoint.
            method (str, optional): Filter logs by HTTP method.

        Returns:
            list: List of audit log entries.
        """
        if not user_id:
            raise ValueError("Missing required field: user_id")
        params: Dict[str, Any] = {}
        if skip is not None:
            params["skip"] = skip
        if limit is not None:
            params["limit"] = limit
        if include_request_body is not None:
            params["include_request_body"] = include_request_body
        if endpoint is not None:
            params["endpoint"] = endpoint
        if method is not None:
            params["method"] = method
        resp = self._request(
            "get",
            f"/api/ss/user/{user_id}/auditlogs",
            params=params or None,
        )
        self._ensure_response(resp, (200,), "fetch user audit logs")
        data = resp.json()
        if isinstance(data, dict) and "logs" in data:
            return data.get("logs", [])
        if isinstance(data, list):
            return data
        return []

    def get_user_login_history(
        self,
        user_id: str,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve login history for a user.

        Args:
            user_id (str): User ID.
            skip (int, optional): Number of records to skip.
            limit (int, optional): Max number of records to return.

        Returns:
            list: List of login entries.
        """
        if not user_id:
            raise ValueError("Missing required field: user_id")
        params: Dict[str, Any] = {}
        if skip is not None:
            params["skip"] = skip
        if limit is not None:
            params["limit"] = limit
        resp = self._request(
            "get",
            f"/api/ss/user/{user_id}/logins",
            params=params or None,
        )
        self._ensure_response(resp, (200,), "fetch user login history")
        data = resp.json()
        if isinstance(data, dict) and "logs" in data:
            return data.get("logs", [])
        if isinstance(data, list):
            return data
        return []

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://demo.attackforge.com",
        dry_run: bool = False,
        verify_ssl: Optional[bool] = None,
        default_library: Optional[str] = None,
        ssapi_key: Optional[str] = None,
    ):
        """
        Initialize the PyAttackForgeClient.

        Args:
            api_key (str): Your AttackForge API key.
            ssapi_key (str, optional): Alias for api_key (used by some integrations/tests).
            base_url (str, optional): The base URL for the AttackForge instance. Defaults to "https://demo.attackforge.com".
            dry_run (bool, optional): If True, no real API calls are made. Defaults to False.
        """
        if api_key is None:
            api_key = ssapi_key
        if api_key is None:
            raise ValueError("Missing required field: api_key")
        base = (base_url or "").strip()
        if base and not base.startswith(("http://", "https://")):
            base = f"https://{base}"
        self.base_url = base.rstrip("/")
        self.headers = {
            "X-SSAPI-KEY": api_key,
            "Content-Type": "application/json",
            "Connection": "close"
        }
        self.dry_run = dry_run
        if verify_ssl is None:
            verify_ssl = os.getenv("ATTACKFORGE_VERIFY_SSL", "1") not in ("0", "false", "False")
        self.verify_ssl = bool(verify_ssl)
        self.default_library = default_library or os.getenv(
            "PYATTACKFORGE_BELONGS_TO_LIBRARY", "Main Vulnerabilities"
        )
        self._asset_cache = None
        self._project_scope_cache = {}
        self._writeup_cache: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
        self._vulnerability_evidence_cache: Dict[str, Set[Tuple[str, int]]] = {}
        self._testcase_evidence_cache: Dict[Tuple[str, str], Set[Tuple[str, int]]] = {}
        self._testcase_link_cache: Dict[Tuple[str, str], Set[str]] = {}
        self._finding_dedupe_cache: Dict[str, str] = {}

    def get_all_writeups(
        self,
        force_refresh: bool = False,
        belongs_to_library: Optional[str] = None,
        query: Optional[str] = None,
    ) -> list:
        """
        Fetches and caches all writeups from the /api/ss/library endpoint.

        Args:
            force_refresh (bool): If True, refresh the cache even if it exists.

            belongs_to_library (str, optional): Filter by library name.
            query (str, optional): Search term for writeups.

        Returns:
            list: List of writeup dicts.
        """
        library_name = belongs_to_library or self.default_library
        cache_key = (library_name or "", query or "")
        if cache_key in self._writeup_cache and not force_refresh:
            return self._writeup_cache[cache_key]
        params: Dict[str, Any] = {}
        if library_name:
            params["belongs_to_library"] = library_name
        if query:
            params["q"] = query
        resp = self._request("get", "/api/ss/library", params=params or None)
        self._ensure_response(resp, (200,), "fetch writeups")
        data = resp.json()
        if isinstance(data, dict) and "vulnerabilities" in data:
            writeups = data["vulnerabilities"]
        elif isinstance(data, list):
            writeups = data
        else:
            writeups = data if isinstance(data, list) else []
        self._writeup_cache[cache_key] = writeups if isinstance(writeups, list) else []
        return self._writeup_cache[cache_key]

    def find_writeup_in_cache(self, title: str, library: Optional[str] = None) -> Optional[str]:
        """
        Searches the cached writeups for a writeup with the given title and library.

        Args:
            title (str): The title of the writeup to find.
            library (str): The library name (default: "Main Vulnerabilities").

        Returns:
            str: The writeup's reference_id if found, else None.
        """
        library_name = library or self.default_library
        writeups = self.get_all_writeups(belongs_to_library=library_name)
        for w in writeups:
            if w.get("title") != title:
                continue
            library_value = (
                w.get("belongs_to_library")
                or w.get("library")
                or w.get("library_name")
            )
            if library_name and library_value != library_name:
                continue
            return w.get("reference_id") or w.get("id") or w.get("_id")
        return None

    def get_or_create_library_issue(
        self,
        title: str,
        belongs_to_library: Optional[str] = None,
        description: Optional[str] = None,
        remediation_recommendation: Optional[str] = None,
        attack_scenario: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Fetch a vulnerability writeup from the library or create it if missing.
        """
        if not title:
            raise ValueError("Missing required field: title")
        library_name = belongs_to_library or self.default_library
        writeups = self.get_all_writeups(belongs_to_library=library_name)
        match = next(
            (
                w
                for w in writeups
                if w.get("title") == title
                and (
                    not library_name
                    or (w.get("belongs_to_library") or w.get("library")) == library_name
                )
            ),
            None,
        )
        if match:
            return match

        description_value = description or f"Auto-generated writeup for {title}."
        remediation_value = remediation_recommendation or "Review and remediate per guidance."
        attack_value = attack_scenario or "Auto-generated by PyAttackForge."
        self.create_writeup(
            title=title,
            description=description_value,
            remediation_recommendation=remediation_value,
            attack_scenario=attack_value,
            belongs_to_library=library_name,
            **kwargs,
        )
        self.get_all_writeups(force_refresh=True, belongs_to_library=library_name)
        writeups = self.get_all_writeups(belongs_to_library=library_name)
        match = next(
            (
                w
                for w in writeups
                if w.get("title") == title
                and (
                    not library_name
                    or (w.get("belongs_to_library") or w.get("library")) == library_name
                )
            ),
            None,
        )
        if not match:
            raise RuntimeError("Writeup creation failed: missing library issue")
        return match

    def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers_override: Optional[Dict[str, str]] = None
    ) -> Any:
        url = f"{self.base_url}{endpoint}"
        if self.dry_run:
            logger.info("[DRY RUN] %s %s", method.upper(), url)
            if json_data:
                logger.info("Payload: %s", json_data)
            if params:
                logger.info("Params: %s", params)
            if files:
                logger.info("Files: %s", list(files.keys()))
            if data:
                logger.info("Data: %s", data)
            return DummyResponse()
        headers = self.headers.copy()
        if files:
            headers.pop("Content-Type", None)
        if headers_override:
            headers.update(headers_override)
        return requests.request(
            method,
            url,
            headers=headers,
            json=json_data,
            params=params,
            files=files,
            data=data,
            verify=self.verify_ssl,
        )

    def get_assets(self) -> Dict[str, Dict[str, Any]]:
        if self._asset_cache is None:
            self._asset_cache = {}
            skip, limit = 0, 500
            while True:
                resp = self._request("get", "/api/ss/assets", params={"skip": skip, "limit": limit})
                self._ensure_response(resp, (200,), "fetch assets")
                data = resp.json()
                for asset in data.get("assets", []):
                    name = asset.get("asset")
                    if name:
                        self._asset_cache[name] = asset
                if skip + limit >= data.get("count", 0):
                    break
                skip += limit
        return self._asset_cache

    def get_asset_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        return self.get_assets().get(name)

    def create_asset(
        self,
        asset_data: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        asset_type: Optional[str] = None,
        asset_library_ids: Optional[List[str]] = None,
        custom_fields: Optional[list] = None,
        external_ids: Optional[list] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a new asset in the asset library.

        Args:
            asset_data (dict, optional): Asset details. Supports keys like "name", "asset",
                "type", "asset_type", "custom_fields", and "external_ids".
            name (str, optional): Asset name.
            asset_type (str, optional): Asset type (defaults to "Other").
            asset_library_ids (list, optional): Asset library IDs to map.
            custom_fields (list, optional): Custom fields payload for the asset.
            external_ids (list, optional): External IDs payload for the asset.
            **kwargs: Additional fields accepted by the API.

        Returns:
            dict: Created asset details or existing asset if already present.
        """
        if asset_data is not None and not isinstance(asset_data, dict):
            raise ValueError("asset_data must be a dict when provided")
        payload: Dict[str, Any] = {}
        if asset_data:
            payload.update(asset_data)
        if kwargs:
            payload.update(kwargs)
        resolved_name = (
            name
            or payload.get("name")
            or payload.get("asset")
            or payload.get("asset_name")
            or payload.get("assetName")
        )
        if not resolved_name:
            raise ValueError("Missing required field: asset name")
        payload["name"] = resolved_name
        payload.setdefault("asset", resolved_name)
        resolved_type = (
            asset_type
            or payload.get("type")
            or payload.get("asset_type")
            or payload.get("assetType")
        )
        if not resolved_type:
            resolved_type = "Other"
        payload["type"] = resolved_type
        payload.setdefault("asset_type", resolved_type)
        if custom_fields is not None:
            payload["custom_fields"] = custom_fields
        if asset_library_ids is not None:
            payload["asset_library_ids"] = [str(a) for a in asset_library_ids if a]
        if external_ids is not None:
            external_id_value: Optional[Any] = external_ids
            if isinstance(external_ids, (list, tuple)):
                external_id_value = next((item for item in external_ids if item), None)
            if external_id_value is not None:
                payload["external_id"] = external_id_value
            payload.pop("external_ids", None)
        elif "external_ids" in payload and "external_id" not in payload:
            external_id_value = payload.pop("external_ids", None)
            if isinstance(external_id_value, (list, tuple)):
                external_id_value = next((item for item in external_id_value if item), None)
            if external_id_value is not None:
                payload["external_id"] = external_id_value

        try:
            existing = self.get_asset_by_name(resolved_name)
        except PermissionError as exc:
            logger.warning(
                "Unable to check existing assets due to permissions; proceeding to create: %s",
                exc,
            )
            existing = None
        if existing:
            return existing

        resp = self._request("post", "/api/ss/library/asset", json_data=payload)
        if resp.status_code in (200, 201):
            data = resp.json()
            asset = self._unwrap(data, "asset")
            self._asset_cache = None
            return asset
        already_exists = "already exists" in resp.text.lower() if resp.text else False
        if not already_exists:
            try:
                data = resp.json()
            except ValueError:
                data = {}
            message = ""
            if isinstance(data, dict):
                message = str(
                    data.get("message")
                    or data.get("error")
                    or data.get("detail")
                    or ""
                ).lower()
            already_exists = "already exists" in message
        if already_exists:
            self._asset_cache = None
            try:
                return self.get_asset_by_name(resolved_name) or {
                    "already_exists": True,
                    "name": resolved_name,
                }
            except PermissionError:
                return {"already_exists": True, "name": resolved_name}
        self._ensure_response(resp, (200, 201), "create asset")
        data = resp.json()
        return self._unwrap(data, "asset")

    def get_project_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        params = {
            "startDate": "2000-01-01T00:00:00.000Z",
            "endDate": "2100-01-01T00:00:00.000Z",
            "status": "All"
        }
        resp = self._request("get", "/api/ss/projects", params=params)
        self._ensure_response(resp, (200,), "fetch projects")
        for proj in resp.json().get("projects", []):
            if proj.get("project_name") == name:
                return proj
        return None

    def get_project_by_id(self, project_id: str) -> Dict[str, Any]:
        """
        Retrieve a project by ID.

        Args:
            project_id (str): Project ID.

        Returns:
            dict: Project details.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        resp = self._request("get", f"/api/ss/project/{project_id}")
        self._ensure_response(resp, (200,), "fetch project")
        data = resp.json()
        return self._unwrap(data, "project")

    def get_project_scope(self, project_id: str) -> Set[str]:
        if project_id in self._project_scope_cache:
            return self._project_scope_cache[project_id]
        project = self.get_project_by_id(project_id)
        scope_raw = []
        if isinstance(project, dict):
            scope_raw = project.get("scope") or project.get("assets") or []
        names: Set[str] = set()
        for asset in scope_raw or []:
            name = None
            if isinstance(asset, dict):
                name = (
                    asset.get("assetName")
                    or asset.get("name")
                    or asset.get("asset")
                )
                if not name and isinstance(asset.get("asset"), dict):
                    name = asset["asset"].get("name")
            elif isinstance(asset, str):
                name = asset
            if name:
                names.add(str(name))
        self._project_scope_cache[project_id] = names
        return names

    def add_assets_to_project(
        self,
        project_id: str,
        assets: List[Any],
        asset_library_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Add assets to a project's scope using the documented CreateScope endpoint.

        Args:
            project_id (str): Project ID.
            assets (list): Asset names or dicts containing name/id.
            asset_library_ids (list, optional): Asset library IDs to map (if assets module enabled).

        Returns:
            dict: API response.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not assets and not asset_library_ids:
            raise ValueError("Missing required field: assets")
        asset_names: List[str] = []
        collected_ids: List[str] = []
        for asset in assets or []:
            if isinstance(asset, dict):
                name = asset.get("assetName") or asset.get("name") or asset.get("asset")
                if name:
                    asset_names.append(str(name))
                aid = (
                    asset.get("asset_id")
                    or asset.get("assetId")
                    or asset.get("asset_library_id")
                    or asset.get("id")
                )
                if aid:
                    collected_ids.append(str(aid))
            else:
                asset_names.append(str(asset))
        if asset_library_ids:
            collected_ids.extend([str(a) for a in asset_library_ids if a])
        payload: Dict[str, Any] = {}
        if asset_names:
            payload["assets"] = asset_names
        if collected_ids:
            payload["asset_library_ids"] = list(dict.fromkeys(collected_ids))
        resp = self._request(
            "post",
            f"/api/ss/project/{project_id}/assets",
            json_data=payload,
        )
        self._ensure_response(resp, (200, 201), "add assets to project scope")
        if asset_names:
            self._project_scope_cache.pop(project_id, None)
        return resp.json()

    def update_project_scope(self, project_id: str, new_assets: List[str]) -> Dict[str, Any]:
        """
        Backwards-compatible helper to add assets to a project scope.
        """
        return self.add_assets_to_project(project_id, new_assets)

    def create_project(self, name: str, **kwargs) -> Dict[str, Any]:
        start, end = get_default_dates()
        payload = {
            "name": name,
            "code": kwargs.get("code", "DEFAULT"),
            "groups": kwargs.get("groups", []),
            "startDate": kwargs.get("startDate", start),
            "endDate": kwargs.get("endDate", end),
            "scope": kwargs.get("scope", []),
            "testsuites": kwargs.get("testsuites", []),
            "organization_code": kwargs.get("organization_code", "ORG_DEFAULT"),
            "vulnerability_code": kwargs.get("vulnerability_code", "VULN_"),
            "scoringSystem": kwargs.get("scoringSystem", "CVSSv3.1"),
            "team_notifications": kwargs.get("team_notifications", []),
            "admin_notifications": kwargs.get("admin_notifications", []),
            "custom_fields": kwargs.get("custom_fields", []),
            "asset_library_ids": kwargs.get("asset_library_ids", []),
            "sla_activation": kwargs.get("sla_activation", "automatic")
        }
        resp = self._request("post", "/api/ss/project", json_data=payload)
        self._ensure_response(resp, (200, 201), "create project")
        data = resp.json()
        return self._unwrap(data, "project")

    def update_project(self, project_id: str, update_fields: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._request("put", f"/api/ss/project/{project_id}", json_data=update_fields)
        self._ensure_response(resp, (200, 201), "update project")
        data = resp.json()
        return self._unwrap(data, "project")

    def create_writeup(
        self,
        title: str,
        description: str,
        remediation_recommendation: str,
        custom_fields: Optional[list] = None,
        **kwargs
    ) -> Dict[str, Any]:
        if not title or not description or not remediation_recommendation:
            raise ValueError("Missing required field: title, description, or remediation_recommendation")

        payload = {
            "title": title,
            "description": description,
            "remediation_recommendation": remediation_recommendation,
            "custom_fields": custom_fields or []
        }
        payload.update(kwargs)
        resp = self._request("post", "/api/ss/library/vulnerability", json_data=payload)
        self._ensure_response(resp, (200, 201), "create writeup")
        data = resp.json()
        data = self._unwrap(data, "vulnerability")
        return self._unwrap(data, "writeup")

    def create_finding_from_writeup(
        self,
        project_id: str,
        writeup_id: str,
        priority: str,
        affected_assets: Optional[list] = None,
        linked_testcases: Optional[list] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a finding from a writeup, supporting multiple affected assets.

        Args:
            project_id (str): The project ID.
            writeup_id (str): The writeup/library ID.
            priority (str): The priority.
            affected_assets (list, optional): List of affected asset objects or names.
            linked_testcases (list, optional): List of testcase IDs to link.
            **kwargs: Additional fields.

        Returns:
            dict: Created finding details.
        """
        if not project_id or not writeup_id or not priority:
            raise ValueError("Missing required field: project_id, writeup_id, or priority")

        payload = {
            "projectId": project_id,
            "vulnerabilityLibraryId": writeup_id,
            "priority": priority
        }
        if affected_assets is not None:
            asset_payloads, _, _ = self._build_asset_payloads(affected_assets)
            payload["affected_assets"] = asset_payloads
        if linked_testcases:
            payload["linked_testcases"] = linked_testcases
        payload.update(kwargs)
        resp = self._request("post", "/api/ss/vulnerability-with-library", json_data=payload)
        self._ensure_response(resp, (200, 201), "create finding from writeup")
        data = resp.json()
        return self._unwrap(data, "vulnerability")

    def upsert_finding_from_writeup(
        self,
        project_id: str,
        writeup: Any,
        title: Optional[str] = None,
        assets: Optional[List[Any]] = None,
        dedupe: bool = True,
        append_assets: bool = True,
        priority: Optional[str] = None,
        likelihood_of_exploitation: int = 1,
        steps_to_reproduce: Optional[str] = None,
        linked_testcases: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Upsert a finding from a library writeup with idempotent dedupe and asset append.
        """
        if not project_id:
            raise ValueError("Missing required field: project_id")
        if not writeup:
            raise ValueError("Missing required field: writeup")

        writeup_id, writeup_title, library_name = self._extract_writeup_identity(writeup)
        finding_title = title or writeup_title
        if not finding_title:
            raise ValueError("Missing required field: title")

        assets = assets or []
        asset_payloads, asset_names, asset_ids = self._build_asset_payloads(assets)
        writeup_ids = self._collect_writeup_ids_from_writeup(writeup)
        if writeup_id:
            writeup_ids.add(str(writeup_id))
        dedupe_keys = self._finding_dedupe_keys(
            project_id,
            finding_title,
            writeup_ids,
            writeup_title,
            library_name,
        )

        if asset_names or asset_ids:
            scope = self.get_project_scope(project_id)
            missing_in_scope = [n for n in asset_names if n not in scope]
            if missing_in_scope or asset_ids:
                self.add_assets_to_project(
                    project_id,
                    missing_in_scope or asset_names,
                    asset_library_ids=asset_ids,
                )

        if dedupe:
            cached_id = self._lookup_finding_dedupe_cache(dedupe_keys)
            if cached_id:
                updated_assets = False
                if append_assets and asset_payloads:
                    try:
                        updated_assets = self._append_assets_to_finding(
                            project_id,
                            cached_id,
                            asset_payloads,
                        )
                    except Exception:
                        updated_assets = False
                return {
                    "finding_id": cached_id,
                    "deduped": True,
                    "created": False,
                    "updated_assets": updated_assets,
                }
            findings = self.get_findings_for_project(project_id)
            match = None
            detail_checked: Set[str] = set()
            for finding in findings:
                finding_id = self._extract_vulnerability_id(finding)
                title_match = self._finding_title_matches(finding, finding_title)
                writeup_match = self._finding_matches_writeup(
                    finding, writeup_ids or writeup_id, writeup_title, library_name
                )
                if title_match and writeup_match:
                    match = finding
                    break
                needs_detail = False
                if finding_id and (title_match or writeup_match):
                    needs_detail = True
                elif finding_id and writeup_title and self._finding_title_matches(finding, writeup_title):
                    needs_detail = True
                if needs_detail and finding_id:
                    try:
                        detail = self.get_vulnerability(finding_id)
                    except Exception:
                        continue
                    detail_checked.add(finding_id)
                    if self._finding_title_matches(detail, finding_title) and self._finding_matches_writeup(
                        detail, writeup_ids or writeup_id, writeup_title, library_name
                    ):
                        match = detail
                        break
            if not match:
                for finding in findings:
                    finding_id = self._extract_vulnerability_id(finding)
                    if not finding_id or finding_id in detail_checked:
                        continue
                    try:
                        detail = self.get_vulnerability(finding_id)
                    except Exception:
                        continue
                    detail_checked.add(finding_id)
                    if self._finding_title_matches(detail, finding_title) and self._finding_matches_writeup(
                        detail, writeup_ids or writeup_id, writeup_title, library_name
                    ):
                        match = detail
                        break
            if match:
                finding_id = self._extract_vulnerability_id(match)
                updated_assets = False
                if append_assets and asset_payloads:
                    try:
                        updated_assets = self._append_assets_to_finding(
                            project_id,
                            finding_id,
                            asset_payloads,
                            existing_finding=match if isinstance(match, dict) else None,
                        )
                    except Exception:
                        updated_assets = False
                self._cache_finding_dedupe(dedupe_keys, finding_id)
                return {
                    "finding_id": finding_id,
                    "deduped": True,
                    "created": False,
                    "updated_assets": updated_assets,
                }

        if not writeup_id and writeup_title:
            library_lookup = library_name or self.default_library
            self.get_all_writeups(belongs_to_library=library_lookup)
            writeup_id = self.find_writeup_in_cache(writeup_title, library_lookup)
        if not writeup_id:
            raise RuntimeError("Missing writeup identifier for finding creation")

        priority_value = priority or "Low"
        steps_value = steps_to_reproduce or "See writeup"
        payload_kwargs = dict(kwargs)
        payload_kwargs.setdefault("likelihood_of_exploitation", likelihood_of_exploitation)
        payload_kwargs.setdefault("steps_to_reproduce", steps_value)

        result = self.create_finding_from_writeup(
            project_id=project_id,
            writeup_id=writeup_id,
            priority=priority_value,
            affected_assets=asset_payloads or None,
            linked_testcases=linked_testcases,
            **payload_kwargs,
        )
        finding_id = self._extract_vulnerability_id(result)
        if finding_id and title:
            try:
                self.update_finding(
                    vulnerability_id=finding_id,
                    project_id=project_id,
                    title=title,
                )
            except Exception:
                pass
        self._cache_finding_dedupe(dedupe_keys, finding_id)
        return {
            "finding_id": finding_id,
            "deduped": False,
            "created": True,
            "response": result,
        }

    def create_vulnerability(
        self,
        project_id: str,
        title: str,
        affected_assets: list,
        priority: str,
        likelihood_of_exploitation: int,
        description: str,
        attack_scenario: str,
        remediation_recommendation: str,
        steps_to_reproduce: str,
        writeup_id: Optional[str] = None,
        tags: Optional[list] = None,
        notes: Optional[list] = None,
        is_zeroday: bool = False,
        is_visible: bool = True,
        import_to_library: Optional[str] = None,
        import_source: Optional[str] = None,
        import_source_id: Optional[str] = None,
        custom_fields: Optional[list] = None,
        linked_testcases: Optional[list] = None,
        custom_tags: Optional[list] = None,
        writeup_custom_fields: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Create a new security finding (vulnerability) in AttackForge with support for multiple assets.

        Args:
            project_id (str): The project ID.
            title (str): The title of the finding.
            affected_assets (list): List of affected asset objects or names.
            priority (str): The priority (e.g., "Critical").
            likelihood_of_exploitation (int): Likelihood of exploitation (e.g., 10).
            description (str): Description of the finding.
            attack_scenario (str): Attack scenario details.
            remediation_recommendation (str): Remediation recommendation.
            steps_to_reproduce (str): Steps to reproduce the finding.
            writeup_id (str, optional): Existing writeup/library reference ID to use directly.
            tags (list, optional): List of tags.
            notes (list, optional): List of notes.
            is_zeroday (bool, optional): Whether this is a zero-day finding.
            is_visible (bool, optional): Whether the finding is visible.
            import_to_library (str, optional): Library to import to.
            import_source (str, optional): Source of import.
            import_source_id (str, optional): Source ID for import.
            custom_fields (list, optional): List of custom fields.
            linked_testcases (list, optional): List of linked testcases.
            custom_tags (list, optional): List of custom tags.
            writeup_custom_fields (list, optional): List of custom fields for the writeup.

        Returns:
            dict: Created vulnerability details.
        """
        asset_payloads, asset_names, asset_ids = self._build_asset_payloads(affected_assets)
        scope = self.get_project_scope(project_id)
        missing_in_scope = [n for n in asset_names if n not in scope]
        if missing_in_scope or asset_ids:
            self.add_assets_to_project(project_id, missing_in_scope or asset_names, asset_library_ids=asset_ids)

        finding_payload = {
            "affected_assets": asset_payloads,
            "likelihood_of_exploitation": likelihood_of_exploitation,
            "steps_to_reproduce": steps_to_reproduce,
            "tags": tags or [],
            "is_zeroday": is_zeroday,
            "is_visible": is_visible,
            "import_to_library": import_to_library,
            "import_source": import_source,
            "import_source_id": import_source_id,
            "custom_fields": custom_fields or [],
            "linked_testcases": linked_testcases or [],
            "custom_tags": custom_tags or [],
        }
        if notes:
            finding_payload["notes"] = notes
        finding_payload = {k: v for k, v in finding_payload.items() if v is not None}
        resolved_writeup_id = writeup_id
        if not resolved_writeup_id:
            self.get_all_writeups(belongs_to_library=self.default_library)
            resolved_writeup_id = self.find_writeup_in_cache(title, self.default_library)
            if not resolved_writeup_id:
                writeup_fields = writeup_custom_fields[:] if writeup_custom_fields else []
                if import_source:
                    writeup_fields.append({"key": "import_source", "value": import_source})
                self.create_writeup(
                    title=title,
                    description=description,
                    remediation_recommendation=remediation_recommendation,
                    attack_scenario=attack_scenario,
                    belongs_to_library=self.default_library,
                    custom_fields=writeup_fields
                )
                self.get_all_writeups(force_refresh=True, belongs_to_library=self.default_library)
                resolved_writeup_id = self.find_writeup_in_cache(
                    title, self.default_library
                )
                if not resolved_writeup_id:
                    raise RuntimeError(
                        "Writeup creation failed: missing reference_id"
                    )
        result = self.create_finding_from_writeup(
            project_id=project_id,
            writeup_id=resolved_writeup_id,
            priority=priority,
            **finding_payload
        )
        return result

    def _sha256_file(self, file_path: str) -> str:
        digest = hashlib.sha256()
        with open(file_path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _evidence_hash_value(self, evidence: Dict[str, Any]) -> Optional[str]:
        if not isinstance(evidence, dict):
            return None
        for key in (
            "sha256",
            "sha_256",
            "file_sha256",
            "file_hash",
            "hash",
            "checksum",
        ):
            value = evidence.get(key)
            if value:
                return str(value)
        for nested_key in ("file", "evidence"):
            nested = evidence.get(nested_key)
            if not isinstance(nested, dict):
                continue
            for key in (
                "sha256",
                "sha_256",
                "file_sha256",
                "file_hash",
                "hash",
                "checksum",
            ):
                value = nested.get(key)
                if value:
                    return str(value)
        return None

    def _evidence_matches(
        self,
        evidence: Dict[str, Any],
        basename: str,
        file_size: int,
        file_hash: Optional[str] = None,
        evidence_hash: Optional[str] = None,
    ) -> bool:
        if not isinstance(evidence, dict):
            return False
        candidate_dicts = [evidence]
        for nested_key in ("file", "evidence"):
            nested = evidence.get(nested_key)
            if isinstance(nested, dict):
                candidate_dicts.append(nested)
        name_candidates = []
        for candidate in candidate_dicts:
            for key in (
                "file_name_custom",
                "file_name",
                "fileNameCustom",
                "name",
                "filename",
                "original_name",
                "original_filename",
                "file_name_original",
                "fileName",
                "originalName",
                "originalFileName",
            ):
                value = candidate.get(key)
                if value:
                    name_candidates.append(str(value))
        if not name_candidates:
            return False
        name_match = False
        for candidate in name_candidates:
            if os.path.basename(candidate) == basename:
                name_match = True
                break
        if not name_match:
            return False
        existing_size = None
        for candidate in candidate_dicts:
            existing_size = (
                candidate.get("file_size")
                or candidate.get("size")
                or candidate.get("file_size_bytes")
                or candidate.get("fileSize")
                or candidate.get("fileSizeBytes")
                or candidate.get("size_bytes")
                or candidate.get("bytes")
                or candidate.get("length")
                or candidate.get("content_length")
            )
            if existing_size is not None:
                break
        size_match = False
        if existing_size is not None:
            try:
                size_match = int(existing_size) == int(file_size)
            except (TypeError, ValueError):
                size_match = False
        if size_match:
            return True
        if existing_size is not None:
            return False
        if file_hash:
            if evidence_hash is None:
                evidence_hash = self._evidence_hash_value(evidence)
            if evidence_hash and evidence_hash.lower() == file_hash.lower():
                return True
        return False

    def create_vulnerability_old(
        self,
        project_id: str,
        title: str,
        affected_asset_name: str,
        priority: str,
        likelihood_of_exploitation: int,
        description: str,
        attack_scenario: str,
        remediation_recommendation: str,
        steps_to_reproduce: str,
        tags: Optional[list] = None,
        notes: Optional[list] = None,
        is_zeroday: bool = False,
        is_visible: bool = True,
        import_to_library: Optional[str] = None,
        import_source: Optional[str] = None,
        import_source_id: Optional[str] = None,
        custom_fields: Optional[list] = None,
        linked_testcases: Optional[list] = None,
        custom_tags: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        [DEPRECATED] Create a new security finding (vulnerability) in AttackForge.

        Args:
            project_id (str): The project ID.
            title (str): The title of the finding.
            affected_asset_name (str): The name of the affected asset.
            priority (str): The priority (e.g., "Critical").
            likelihood_of_exploitation (int): Likelihood of exploitation (e.g., 10).
            description (str): Description of the finding.
            attack_scenario (str): Attack scenario details.
            remediation_recommendation (str): Remediation recommendation.
            steps_to_reproduce (str): Steps to reproduce the finding.
            tags (list, optional): List of tags.
            notes (list, optional): List of notes.
            is_zeroday (bool, optional): Whether this is a zero-day finding.
            is_visible (bool, optional): Whether the finding is visible.
            import_to_library (str, optional): Library to import to.
            import_source (str, optional): Source of import.
            import_source_id (str, optional): Source ID for import.
            custom_fields (list, optional): List of custom fields.
            linked_testcases (list, optional): List of linked testcases.
            custom_tags (list, optional): List of custom tags.

        Returns:
            dict: Created vulnerability details.

        Raises:
            ValueError: If any required field is missing.
            RuntimeError: If vulnerability creation fails.
        """
        required_fields = [
            ("project_id", project_id),
            ("title", title),
            ("affected_asset_name", affected_asset_name),
            ("priority", priority),
            ("likelihood_of_exploitation", likelihood_of_exploitation),
            ("description", description),
            ("attack_scenario", attack_scenario),
            ("remediation_recommendation", remediation_recommendation),
            ("steps_to_reproduce", steps_to_reproduce),
        ]
        for field_name, value in required_fields:
            if value is None:
                raise ValueError(f"Missing required field: {field_name}")

        payload = {
            "projectId": project_id,
            "title": title,
            "affected_asset_name": affected_asset_name,
            "priority": priority,
            "likelihood_of_exploitation": likelihood_of_exploitation,
            "description": description,
            "attack_scenario": attack_scenario,
            "remediation_recommendation": remediation_recommendation,
            "steps_to_reproduce": steps_to_reproduce,
            "tags": tags or [],
            "is_zeroday": is_zeroday,
            "is_visible": is_visible,
            "import_to_library": import_to_library,
            "import_source": import_source,
            "import_source_id": import_source_id,
            "custom_fields": custom_fields or [],
            "linked_testcases": linked_testcases or [],
            "custom_tags": custom_tags or [],
        }
        if notes:
            payload["notes"] = notes
        payload = {k: v for k, v in payload.items() if v is not None}
        resp = self._request("post", "/api/ss/vulnerability", json_data=payload)
        self._ensure_response(resp, (200, 201), "create vulnerability")
        data = resp.json()
        return self._unwrap(data, "vulnerability")


class DummyResponse:
    def __init__(self) -> None:
        self.status_code = 200
        self.text = "[DRY RUN] No real API call performed."

    def json(self) -> Dict[str, Any]:
        return {}


def get_default_dates() -> Tuple[str, str]:
    now = datetime.now(timezone.utc)
    start = now.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    end = (
        now + timedelta(days=30)
    ).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return start, end
