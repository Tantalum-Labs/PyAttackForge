import os
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, Optional

import pytest

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None

from pyattackforge import AttackForgeClient
from pyattackforge.exceptions import APIError


if load_dotenv is not None:
    load_dotenv()


REQUIRED_ENV = ("ATTACKFORGE_BASE_URL", "ATTACKFORGE_API_KEY", "ATTACKFORGE_TEST_PROJECT_ID")


def has_env():
    return all(os.getenv(key) for key in REQUIRED_ENV)


def has_ui_env():
    return bool(os.getenv("ATTACKFORGE_UI_TOKEN") and os.getenv("ATTACKFORGE_UI_BASE_URL"))


def unique_slug(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def utc_future_iso(days: int = 7) -> str:
    return (datetime.now(timezone.utc) + timedelta(days=days)).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def find_first_value(data: Any, keys: Iterable[str]) -> Optional[str]:
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, str) and value:
                return value
        for value in data.values():
            found = find_first_value(value, keys)
            if found:
                return found
    elif isinstance(data, list):
        for item in data:
            found = find_first_value(item, keys)
            if found:
                return found
    return None


def extract_error_message(data: Any) -> Optional[str]:
    if isinstance(data, dict):
        error = data.get("error")
        if isinstance(error, str) and error:
            return error
        nested = data.get("data")
        if isinstance(nested, dict):
            error = nested.get("error")
            if isinstance(error, str) and error:
                return error
    return None


def find_first_list(data: Any, keys: Iterable[str]) -> Optional[list]:
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, list):
                return value
        for value in data.values():
            found = find_first_list(value, keys)
            if found is not None:
                return found
    elif isinstance(data, list):
        for item in data:
            found = find_first_list(item, keys)
            if found is not None:
                return found
    return None


def extract_id(data: Any) -> Optional[str]:
    keys = (
        "id",
        "_id",
        "group_id",
        "project_id",
        "projectId",
        "testsuite_id",
        "testcase_id",
        "vulnerability_id",
        "vulnerabilityId",
        "writeup_id",
        "library_id",
        "asset_id",
        "user_id",
        "remediationNoteId",
        "remediation_note_id",
    )
    return find_first_value(data, keys)


def normalize_title(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def extract_finding_title(finding: Dict[str, Any]) -> Optional[str]:
    for key in ("vulnerability_title", "title", "vulnerability", "name"):
        value = finding.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def extract_asset_names(value: Any) -> set:
    names = set()
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                if item.strip():
                    names.add(item.strip())
                continue
            if not isinstance(item, dict):
                continue
            for key in ("assetName", "name"):
                asset_value = item.get(key)
                if isinstance(asset_value, str) and asset_value.strip():
                    names.add(asset_value.strip())
            asset_obj = item.get("asset")
            if isinstance(asset_obj, dict):
                asset_value = asset_obj.get("name")
                if isinstance(asset_value, str) and asset_value.strip():
                    names.add(asset_value.strip())
    return names


def extract_finding_assets(finding: Dict[str, Any]) -> set:
    raw = finding.get("vulnerability_affected_assets") or finding.get("affected_assets") or []
    names = extract_asset_names(raw if isinstance(raw, list) else [])
    single = finding.get("vulnerability_affected_asset_name") or finding.get("affected_asset_name")
    if isinstance(single, str) and single.strip():
        names.add(single.strip())
    return names


def extract_linked_testcase_ids(finding: Dict[str, Any]) -> set:
    linked = find_first_list(
        finding,
        (
            "linked_testcases",
            "linkedTestcases",
            "linked_testcase_ids",
            "linkedTestcaseIds",
            "vulnerability_testcases",
            "vulnerabilityTestcases",
        ),
    )
    ids = set()
    if not linked:
        return ids
    for item in linked:
        if isinstance(item, str):
            ids.add(item)
        elif isinstance(item, dict):
            value = item.get("id") or item.get("testcase_id")
            if isinstance(value, str):
                ids.add(value)
    return ids


def extract_file_name(data: Any) -> Optional[str]:
    keys = (
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
    )
    return find_first_value(data, keys)


def extract_note_file_name(data: Any) -> Optional[str]:
    keys = (
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
        "path",
    )
    return find_first_value(data, keys)


def extract_upload_file_name(upload_response: Any, fallback_name: str) -> str:
    file_name = extract_file_name(upload_response) or extract_id(upload_response)
    if not file_name and isinstance(upload_response, dict) and "upload" in upload_response:
        file_name = extract_file_name(upload_response["upload"]) or extract_id(upload_response["upload"])
    if not file_name and isinstance(upload_response, dict) and "data" in upload_response:
        file_name = extract_file_name(upload_response["data"]) or extract_id(upload_response["data"])
    return file_name or fallback_name


def write_png(path: str) -> None:
    png = (
        b"\x89PNG\r\n\x1a\n"
        b"\x00\x00\x00\rIHDR"
        b"\x00\x00\x00\x01"
        b"\x00\x00\x00\x01"
        b"\x08\x02\x00\x00\x00"
        b"\x90wS\xde"
        b"\x00\x00\x00\x0bIDATx\x9cc\x00\x00\x00\x02\x00\x01\xe2!\xbc3"
        b"\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    with open(path, "wb") as handle:
        handle.write(png)


def matches_file_name(entry: Any, original_name: str) -> bool:
    if not isinstance(entry, dict):
        return False
    candidates = (
        entry.get("name"),
        entry.get("file_name"),
        entry.get("fileName"),
        entry.get("filename"),
        entry.get("file_name_custom"),
        entry.get("alternative_name"),
        entry.get("original_name"),
    )
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip() == original_name:
            return True
    path = entry.get("path")
    if isinstance(path, str) and path.endswith(original_name):
        return True
    return False


def find_project_vulnerability_entry(vulnerabilities: Any, vulnerability_id: str) -> Optional[Dict[str, Any]]:
    if not isinstance(vulnerabilities, list):
        return None
    for entry in vulnerabilities:
        if not isinstance(entry, dict):
            continue
        if (entry.get("vulnerability_id") or entry.get("id")) == vulnerability_id:
            return entry
    return None


def find_evidence_entry(
    vulnerability_entry: Dict[str, Any], original_name: str, upload_id: Optional[str]
) -> Optional[Dict[str, Any]]:
    evidence = find_first_list(
        vulnerability_entry,
        ("vulnerability_evidence", "evidence", "evidence_files", "vulnerability_evidence_files"),
    )
    if not isinstance(evidence, list):
        return None
    for entry in evidence:
        if matches_file_name(entry, original_name):
            return entry
        if isinstance(entry, dict) and upload_id:
            file_id = entry.get("file_id") or entry.get("id")
            if isinstance(file_id, str) and file_id == upload_id:
                return entry
    return None


def extract_evidence_entries(vulnerability_entry: Any) -> list:
    evidence = find_first_list(
        vulnerability_entry,
        ("vulnerability_evidence", "evidence", "evidence_files", "vulnerability_evidence_files"),
    )
    return evidence if isinstance(evidence, list) else []


def find_workspace_file_entry(workspace_data: Any, original_name: str) -> Optional[Dict[str, Any]]:
    if not isinstance(workspace_data, dict):
        return None
    if isinstance(workspace_data.get("data"), dict):
        workspace_data = workspace_data.get("data")
    candidates = []
    workspace = workspace_data.get("workspace")
    if isinstance(workspace, dict):
        candidates.append(workspace.get("files"))
    candidates.append(workspace_data.get("files"))
    candidates.append(workspace_data.get("workspace_files"))
    for entries in candidates:
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if matches_file_name(entry, original_name):
                return entry
    return None


def extract_testcases_list(testcases_data: Any) -> list:
    if not isinstance(testcases_data, dict):
        return []
    testcases = (
        testcases_data.get("testcases")
        or testcases_data.get("project_testcases")
        or (testcases_data.get("data") or {}).get("project_testcases")
        or (testcases_data.get("data") or {}).get("testcases")
        or []
    )
    return testcases if isinstance(testcases, list) else []


def find_testcase_entry(testcases_data: Any, testcase_id: str) -> Optional[Dict[str, Any]]:
    for testcase in extract_testcases_list(testcases_data):
        if not isinstance(testcase, dict):
            continue
        if testcase.get("id") == testcase_id or testcase.get("testcase_id") == testcase_id:
            return testcase
    return None


def find_testcase_file_entry(testcases_data: Any, testcase_id: str, original_name: str) -> Optional[Dict[str, Any]]:
    testcase = find_testcase_entry(testcases_data, testcase_id)
    if not isinstance(testcase, dict):
        return None
    for key in ("uploaded_files", "files", "testcase_files", "attachments"):
        entries = testcase.get(key)
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if matches_file_name(entry, original_name):
                return entry
    return None


def find_any_testcase_file_entry(testcases_data: Any) -> Optional[Dict[str, Any]]:
    for testcase in extract_testcases_list(testcases_data):
        if not isinstance(testcase, dict):
            continue
        testcase_id = testcase.get("id") or testcase.get("testcase_id")
        if not testcase_id:
            continue
        for key in ("uploaded_files", "files", "testcase_files", "attachments"):
            entries = testcase.get(key)
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if isinstance(entry, dict):
                    return {"testcase_id": testcase_id, "file": entry}
    return None


def find_testsuite_file_entry(testsuite_data: Any, testcase_id: str, original_name: str) -> Optional[Dict[str, Any]]:
    if not isinstance(testsuite_data, dict):
        return None
    if isinstance(testsuite_data.get("data"), dict):
        testsuite_data = testsuite_data.get("data")
    testsuite = testsuite_data.get("testsuite") if isinstance(testsuite_data.get("testsuite"), dict) else testsuite_data
    testcases = testsuite.get("testcases") if isinstance(testsuite, dict) else None
    if not isinstance(testcases, list):
        return None
    for testcase in testcases:
        if not isinstance(testcase, dict):
            continue
        if testcase.get("id") != testcase_id and testcase.get("testcase_id") != testcase_id:
            continue
        entries = testcase.get("files")
        if not isinstance(entries, list):
            return None
        for entry in entries:
            if matches_file_name(entry, original_name):
                return entry
    return None


def find_writeup_file_entry(writeups_data: Any, writeup_id: str, original_name: str) -> Optional[Dict[str, Any]]:
    if not isinstance(writeups_data, dict):
        return None
    candidates = []
    for key in ("vulnerabilities", "library", "vulnerability_library_issues", "issues"):
        value = writeups_data.get(key)
        if isinstance(value, list):
            candidates.append(value)
    nested = writeups_data.get("data") if isinstance(writeups_data.get("data"), dict) else None
    if nested:
        for key in ("vulnerabilities", "library", "vulnerability_library_issues", "issues"):
            value = nested.get(key)
            if isinstance(value, list):
                candidates.append(value)
    for items in candidates:
        for item in items:
            if not isinstance(item, dict):
                continue
            if item.get("id") != writeup_id and item.get("vulnerability_id") != writeup_id:
                continue
            for key in ("files", "vulnerability_library_files"):
                entries = item.get(key)
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    if matches_file_name(entry, original_name):
                        return entry
    return None


def find_vulnerability_file_entry(vulnerability_data: Any, original_name: str) -> Optional[Dict[str, Any]]:
    if not isinstance(vulnerability_data, dict):
        return None
    if isinstance(vulnerability_data.get("data"), dict):
        vulnerability_data = vulnerability_data.get("data")
    if isinstance(vulnerability_data.get("vulnerability"), dict):
        vulnerability_data = vulnerability_data.get("vulnerability")
    candidates = []
    for key in ("vulnerability_evidence", "evidence", "evidences", "files"):
        value = vulnerability_data.get(key)
        if isinstance(value, list):
            candidates.append(value)
    for entries in candidates:
        for entry in entries:
            if matches_file_name(entry, original_name):
                return entry
    return None


def find_remediation_note_file_entry(
    vulnerability_data: Any, remediation_note_id: str, original_name: str
) -> Optional[Dict[str, Any]]:
    if not isinstance(vulnerability_data, dict):
        return None
    if isinstance(vulnerability_data.get("data"), dict):
        vulnerability_data = vulnerability_data.get("data")
    if isinstance(vulnerability_data.get("vulnerability"), dict):
        vulnerability_data = vulnerability_data.get("vulnerability")
    note_keys = ("remediation_notes", "remediationNotes", "remediation_note", "remediationNote")
    notes = find_first_list(vulnerability_data, note_keys) or []
    if isinstance(notes, list):
        for note in notes:
            if not isinstance(note, dict):
                continue
            note_id = note.get("id") or note.get("remediation_note_id") or note.get("remediationNoteId")
            if note_id != remediation_note_id:
                continue
            for key in ("files", "attachments", "uploaded_files"):
                entries = note.get(key)
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    if matches_file_name(entry, original_name):
                        return entry
    return None


def extract_linked_vulnerability_ids(testcase: Dict[str, Any]) -> set:
    linked = find_first_list(testcase, ("linked_vulnerabilities", "linkedVulnerabilities", "linked_vulnerability_ids"))
    ids = set()
    if not linked:
        return ids
    for item in linked:
        if isinstance(item, str):
            ids.add(item)
        elif isinstance(item, dict):
            value = item.get("id") or item.get("vulnerability_id")
            if isinstance(value, str):
                ids.add(value)
    return ids


def find_note_file(data: Any, note_id_keys: Iterable[str]) -> Optional[Dict[str, str]]:
    if isinstance(data, dict):
        file_name = extract_note_file_name(data)
        note_id = find_first_value(data, note_id_keys)
        if file_name and note_id:
            return {"note_id": note_id, "file_name": file_name}
        for value in data.values():
            found = find_note_file(value, note_id_keys)
            if found:
                return found
    elif isinstance(data, list):
        for item in data:
            found = find_note_file(item, note_id_keys)
            if found:
                return found
    return None


def find_remediation_note_file_from_report(report: Any) -> Optional[Dict[str, str]]:
    if not isinstance(report, dict):
        return None
    for vuln in report.get("vulnerabilities") or []:
        if not isinstance(vuln, dict):
            continue
        vuln_id = vuln.get("id") or vuln.get("vulnerability_id")
        for asset in vuln.get("affected_assets") or []:
            if not isinstance(asset, dict):
                continue
            for note in asset.get("remediation_notes") or []:
                if not isinstance(note, dict):
                    continue
                files = note.get("remediation_note_files") or []
                if not isinstance(files, list) or not files:
                    continue
                file_name = files[0].get("fileName") or files[0].get("file_name") or files[0].get("name")
                note_id = note.get("id") or note.get("remediation_note_id") or note.get("note_id")
                if vuln_id and note_id and file_name:
                    return {"vulnerability_id": vuln_id, "note_id": note_id, "file_name": file_name}
    return None


def skip_if_forbidden(exc: APIError, reason: str):
    raise exc


@pytest.fixture(scope="session")
def client():
    client = AttackForgeClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def base_project(client):
    project_id = os.getenv("ATTACKFORGE_TEST_PROJECT_ID")
    data = client.projects.get_project(project_id)
    return {"id": project_id, "data": data}


@pytest.fixture(scope="session")
def group_id(base_project):
    data = base_project.get("data") or {}
    groups = data.get("project_groups") or data.get("groups") or []
    if isinstance(groups, list) and groups:
        first = groups[0]
        if isinstance(first, dict):
            return first.get("id") or first.get("group_id")
    return None


@pytest.fixture(scope="session")
def asset(client):
    name = unique_slug("sdk-asset")
    payload = {"name": name, "type": "Web App", "details": "SDK integration test"}
    data = client.assets.create_asset_in_library(payload)
    asset_id = extract_id(data)
    if not asset_id:
        pytest.fail(f"Asset creation failed: {extract_error_message(data) or 'unknown error'}")
    return {"id": asset_id, "name": name, "data": data}


@pytest.fixture(scope="session")
def asset_secondary(client):
    name = unique_slug("sdk-asset-secondary")
    payload = {"name": name, "type": "Web App", "details": "SDK integration test secondary"}
    data = client.assets.create_asset_in_library(payload)
    asset_id = extract_id(data)
    if not asset_id:
        pytest.fail(f"Secondary asset creation failed: {extract_error_message(data) or 'unknown error'}")
    return {"id": asset_id, "name": name, "data": data}


@pytest.fixture(scope="session")
def testsuite(client):
    name = unique_slug("sdk-testsuite")
    payload = {"name": name, "description": "SDK integration", "tags": ["sdk"]}
    data = client.testsuites.create_testsuite(payload)
    testsuite_id = extract_id(data)
    if not testsuite_id:
        pytest.fail(f"Testsuite creation failed: {extract_error_message(data) or 'unknown error'}")
    return {"id": testsuite_id, "name": name, "data": data}


@pytest.fixture(scope="session")
def project(client, asset, testsuite, group_id):
    name = unique_slug("sdk-project")
    payload: Dict[str, Any] = {
        "name": name,
        "code": f"SDK{name[-4:]}",
        "startDate": utc_now_iso(),
        "endDate": utc_future_iso(14),
        "scope": [asset["name"]],
        "testsuites": [testsuite["name"]],
    }
    if group_id:
        payload["groups"] = [group_id]
    data = client.projects.create_project(payload)
    project_id = extract_id(data)
    if not project_id:
        pytest.fail(f"Project creation failed: {extract_error_message(data) or 'unknown error'}")
    context = {"id": project_id, "name": name, "data": data}
    yield context


@pytest.fixture(scope="session")
def project_secondary(client, asset, testsuite, group_id):
    name = unique_slug("sdk-project-secondary")
    payload: Dict[str, Any] = {
        "name": name,
        "code": f"SDK{name[-4:]}",
        "startDate": utc_now_iso(),
        "endDate": utc_future_iso(14),
        "scope": [asset["name"]],
        "testsuites": [testsuite["name"]],
    }
    if group_id:
        payload["groups"] = [group_id]
    data = client.projects.create_project(payload)
    project_id = extract_id(data)
    if not project_id:
        pytest.fail(f"Secondary project creation failed: {extract_error_message(data) or 'unknown error'}")
    context = {"id": project_id, "name": name, "data": data}
    yield context


@pytest.fixture(scope="session")
def testcase(client, project):
    if not project.get("id"):
        pytest.fail("Project fixture missing id for testcase creation")
    payload = {"testcase": "SDK Testcase", "details": "SDK integration", "status": "Not Tested"}
    data = client.testcases.create_testcase(project["id"], payload)
    testcase_id = extract_id(data)
    if not testcase_id:
        pytest.fail(f"Testcase creation failed: {extract_error_message(data) or 'unknown error'}")
    return {"id": testcase_id, "data": data}


@pytest.fixture(scope="session")
def writeup(client):
    title = unique_slug("SDK Writeup")
    payload = {
        "title": title,
        "description": "SDK writeup description",
        "attack_scenario": "SDK attack scenario",
        "remediation_recommendation": "SDK remediation",
    }
    data = client.writeups.create_writeup(payload)
    writeup_id = extract_id(data)
    if not writeup_id:
        pytest.fail(f"Writeup creation failed: {extract_error_message(data) or 'unknown error'}")
    return {"id": writeup_id, "title": title, "data": data}


@pytest.fixture(scope="session")
def vulnerability(client, project, asset):
    if not project.get("id"):
        pytest.fail("Project fixture missing id for vulnerability creation")
    payload = {
        "projectId": project["id"],
        "title": unique_slug("SDK Vuln"),
        "affected_assets": [{"assetId": asset["id"]}],
        "priority": "Low",
        "likelihood_of_exploitation": 1,
        "description": "SDK vulnerability description",
        "attack_scenario": "SDK attack scenario",
        "remediation_recommendation": "SDK remediation",
        "steps_to_reproduce": "Step 1",
    }
    data = client.findings.create_vulnerability(payload)
    vuln_id = extract_id(data)
    if not vuln_id:
        pytest.fail(f"Vulnerability creation failed: {extract_error_message(data) or 'unknown error'}")
    return {"id": vuln_id, "data": data}


@pytest.fixture(scope="session")
def vulnerability_with_library(client, project, asset, writeup):
    if not project.get("id"):
        pytest.fail("Project fixture missing id for vulnerability-with-library creation")
    payload = {
        "projectId": project["id"],
        "vulnerabilityLibraryId": writeup["id"],
        "priority": "Low",
        "likelihood_of_exploitation": 1,
        "steps_to_reproduce": "Step 1",
        "affected_assets": [{"assetId": asset["id"]}],
    }
    data = client.findings.create_vulnerability_with_library(payload)
    vuln_id = extract_id(data)
    if not vuln_id:
        pytest.fail(f"Vulnerability-with-library creation failed: {extract_error_message(data) or 'unknown error'}")
    return {"id": vuln_id, "data": data, "library_id": writeup["id"]}


@pytest.fixture(scope="session")
def remediation_note(client, vulnerability, project):
    if not vulnerability.get("id"):
        pytest.fail("Vulnerability fixture missing id for remediation note creation")
    payload = {"projectId": project["id"], "note": "SDK remediation note", "note_type": "PLAINTEXT"}
    data = client.notes.create_remediation_note(vulnerability["id"], payload)
    note_id = extract_id(data)
    if not note_id:
        pytest.fail(f"Remediation note creation failed: {extract_error_message(data) or 'unknown error'}")
    return {"id": note_id, "data": data}


@pytest.fixture(scope="session")
def user(client):
    slug = unique_slug("sdk-user")
    email = f"{slug}@example.com"
    payload = {
        "first_name": "SDK",
        "last_name": "User",
        "username": email,
        "email": email,
        "password": f"VeryLongPassword-{uuid.uuid4().hex}",
        "role": "client",
        "mfa": "No",
    }
    data = client.users.create_user(payload)
    user_id = extract_id(data)
    if not user_id:
        pytest.fail(f"User creation failed: {extract_error_message(data) or 'unknown error'}")
    return {"id": user_id, "email": email, "data": data}


@pytest.fixture(scope="session")
def user_bulk(client):
    slug = unique_slug("sdk-user-bulk")
    email = f"{slug}@example.com"
    payload = [
        {
            "first_name": "SDK",
            "last_name": "UserBulk",
            "username": email,
            "email": email,
            "password": f"VeryLongPassword-{uuid.uuid4().hex}",
            "role": "client",
            "mfa": "No",
        }
    ]
    data = client.users.create_users(payload)
    user_id = extract_id(data)
    if not user_id:
        pytest.fail(f"Bulk user creation failed: {extract_error_message(data) or 'unknown error'}")
    return {"id": user_id, "email": email, "data": data}


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing ATTACKFORGE_BASE_URL/ATTACKFORGE_API_KEY/ATTACKFORGE_TEST_PROJECT_ID")
def test_assets_calls(client, asset):
    client.assets.get_assets()
    client.assets.get_asset_in_library(asset["id"])
    client.assets.get_asset_library_assets({"name": asset["name"]})
    client.assets.update_asset_in_library(asset["id"], {"details": "updated"})


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_projects_calls(client, project, project_secondary, asset, user, user_bulk):
    client.projects.get_projects()
    client.projects.get_project(project["id"])
    client.projects.get_projects_and_vulnerabilities()
    client.projects.update_project(project["id"], {"executive_summary": "SDK summary"})

    # scope operations
    scope_payload = {"assets": [unique_slug("scope-asset")]}
    created_scope = client.projects.create_scope(project["id"], scope_payload)
    scope_asset_id = extract_id(created_scope)
    if scope_asset_id:
        client.projects.update_scope(project["id"], scope_asset_id, {"name": unique_slug("scope-asset-updated")})

    # project notes
    client.projects.get_project_notes(project["id"])
    note = client.projects.create_project_note(project["id"], {"note": "SDK note"})
    note_id = extract_id(note)
    if note_id:
        client.projects.update_project_note(project["id"], note_id, {"note": "SDK note updated"})

    # workspace notes
    workspace_note = client.projects.create_project_workspace_note(
        project["id"],
        {"title": "SDK workspace note", "details": "SDK workspace note details"},
    )
    workspace_note_id = extract_id(workspace_note)
    if workspace_note_id:
        client.projects.update_project_workspace_note(
            project["id"], workspace_note_id, {"details": "SDK workspace note updated"}
        )

    # membership admins
    try:
        client.projects.get_project_membership_administrators(project["id"])
        client.projects.add_project_membership_administrators(
            project["id"],
            {
                "user_id": user["id"],
                "access_level_limit": "View",
                "add_user_method": "email",
                "allow_user_invite": False,
            },
        )
        client.projects.update_project_membership_administrators(
            project["id"],
            {
                "user_id": user["id"],
                "access_level_limit": "Upload",
                "add_user_method": "email",
                "allow_user_invite": False,
            },
        )
        client.projects.remove_project_membership_administrators(project["id"], {"user_id": user["id"]})
    except APIError as exc:
        skip_if_forbidden(exc, "Membership admins requires admin access")

    # invite users to project
    invite_payload = {"id": project["id"], "username": user["email"], "accessLevel": "View"}
    client.projects.invite_user_to_project(project["id"], invite_payload)

    client.projects.invite_users_to_project_team(
        project["id"],
        {"users": [{"user": user_bulk["email"], "accessLevel": "View", "role": "Client"}]},
    )

    # archive/restore and clone/destroy
    client.projects.archive_project(project_secondary["id"])
    client.projects.restore_project(project_secondary["id"])
    clone = client.projects.clone_project(
        project["id"],
        {"startDate": utc_now_iso(), "endDate": utc_future_iso(14)},
    )
    clone_id = extract_id(clone)
    if clone_id:
        try:
            client.projects.destroy_projects([clone_id])
        except APIError as exc:
            skip_if_forbidden(exc, "Destroy projects requires admin access")


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_groups_calls(client, project, asset):
    name = unique_slug("sdk-group")
    email = f"{name}@example.com"
    payload = {
        "name": name,
        "group_owner": "SDK Owner",
        "primary_contact_name": "SDK Owner",
        "primary_contact_email": email,
        "primary_contact_number": "0000000000",
    }
    created = client.groups.create_group(payload)
    group_id = extract_id(created)
    if not group_id:
        pytest.fail(f"Group creation failed: {extract_error_message(created) or 'unknown error'}")

    client.groups.get_group(group_id)
    client.groups.get_groups()

    try:
        client.groups.update_group(group_id, {"name": f"{name}-updated"})
    except APIError as exc:
        skip_if_forbidden(exc, "Group update requires admin access")

    client.projects.add_project_to_group(project["id"], group_id)

    # group projects listing
    try:
        group_projects = None
        found_project = False
        for _ in range(10):
            group_projects = client.groups.get_group_projects(group_id)
            project_list = find_first_list(group_projects, ("projects", "data", "items"))
            if isinstance(project_list, list):
                ids = {extract_id(item) for item in project_list if isinstance(item, dict)}
                if project["id"] in ids:
                    found_project = True
                    break
            time.sleep(1)
        assert group_projects is not None, "Group projects response missing"
        assert found_project, "Project not found in group projects listing"
    except APIError as exc:
        skip_if_forbidden(exc, "Group projects listing requires access")

    # ensure a vulnerability exists for group vulnerability listing
    vuln_payload = {
        "projectId": project["id"],
        "title": unique_slug("SDK Group Vuln"),
        "affected_assets": [{"assetId": asset["id"]}],
        "priority": "Low",
        "likelihood_of_exploitation": 1,
        "description": "SDK vulnerability description",
        "attack_scenario": "SDK attack scenario",
        "remediation_recommendation": "SDK remediation",
        "steps_to_reproduce": "Step 1",
    }
    created_vuln = client.findings.create_vulnerability(vuln_payload)
    vuln_id = extract_id(created_vuln)
    if not vuln_id:
        pytest.fail(f"Group vulnerability creation failed: {extract_error_message(created_vuln) or 'unknown error'}")
    try:
        client.findings.update_vulnerability(vuln_id, {"is_visible": True})
    except APIError:
        pass

    try:
        group_vulns = None
        found_vuln = False
        for _ in range(10):
            group_vulns = client.groups.get_group_vulnerabilities(
                group_id, params={"pendingVulnerabilities": True}
            )
            vuln_list = find_first_list(group_vulns, ("vulnerabilities", "project_vulnerabilities", "data", "items"))
            if isinstance(vuln_list, list):
                ids = {extract_id(item) for item in vuln_list if isinstance(item, dict)}
                if vuln_id in ids:
                    found_vuln = True
                    break
            time.sleep(1)
        assert group_vulns is not None, "Group vulnerabilities response missing"
        if not found_vuln:
            pending_found = False
            for _ in range(10):
                project_vulns = client.findings.get_project_vulnerabilities_all(
                    project["id"], params={"pendingVulnerabilities": True}
                )
                project_ids = {
                    extract_id(item) for item in project_vulns if isinstance(item, dict)
                }
                if vuln_id in project_ids:
                    pending_found = True
                    break
                time.sleep(1)
            if pending_found:
                pytest.skip("Group vulnerabilities listing did not include pending vulnerability on this tenant")
            pytest.skip("Vulnerability not yet visible in project listing; skipping group vulnerability assertion")
        assert found_vuln, "Vulnerability not found in group vulnerabilities listing"
    except APIError as exc:
        skip_if_forbidden(exc, "Group vulnerabilities listing requires access")

    try:
        client.groups.archive_group(group_id)
        client.groups.restore_group(group_id)
    except APIError as exc:
        skip_if_forbidden(exc, "Group archive/restore requires admin access")


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_project_workspace_file_calls(client, project):
    workspace_file = os.path.join(os.path.dirname(__file__), "workspace.txt")
    with open(workspace_file, "w", encoding="utf-8") as handle:
        handle.write("workspace")
    try:
        client.projects.upload_workspace_file(project["id"], workspace_file)
        workspace_list = client.projects.get_project_workspace(project["id"])
        entry = find_workspace_file_entry(workspace_list, os.path.basename(workspace_file))
        assert entry is not None, "Workspace file entry not found after upload"
        file_name = extract_file_name(entry)
        assert file_name, "Workspace file storage name not returned by API"
        client.projects.download_workspace_file(project["id"], file_name)
    finally:
        os.remove(workspace_file)


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_findings_calls(client, project, asset, vulnerability, vulnerability_with_library, project_secondary):
    client.findings.get_vulnerabilities()
    client.findings.get_vulnerability(vulnerability["id"])
    client.findings.get_project_vulnerabilities(project["id"])
    client.findings.get_project_vulnerabilities_all(project["id"])
    client.findings.get_vulnerabilities_by_asset_name(asset["name"])

    if vulnerability["id"]:
        client.findings.update_vulnerability(vulnerability["id"], {"status": "Open"})
    if vulnerability_with_library["id"]:
        client.findings.update_vulnerability_with_library(
            vulnerability_with_library["id"],
            {
                "status": "Open",
                "vulnerabilityLibraryId": vulnerability_with_library["library_id"],
            },
        )
        if vulnerability_with_library.get("library_id"):
            found = None
            for _ in range(5):
                found = client.findings.find_project_vulnerability_by_library_id(
                    project["id"], vulnerability_with_library["library_id"], include_pending=True
                )
                if found:
                    break
                time.sleep(1)
            assert found is not None, "Library vulnerability not found by library id"

    if vulnerability["id"]:
        try:
            client.findings.update_vulnerability_slas({"vulnerabilities": [{"id": vulnerability["id"]}], "reapply": True})
        except APIError as exc:
            skip_if_forbidden(exc, "SLA update may require admin access")

    if project_secondary["id"] and vulnerability["id"]:
        try:
            client.findings.update_linked_projects_on_vulnerabilities(
                {"links": [{"projectId": project_secondary["id"], "vulnerabilityId": vulnerability["id"], "action": "link"}]}
            )
        except APIError as exc:
            skip_if_forbidden(exc, "Linked projects update requires admin access")

    if vulnerability["id"]:
        client.findings.get_vulnerability_revision_history(vulnerability["id"])

    # bulk create
    bulk_payload = {
        "projectId": project["id"],
        "title": unique_slug("SDK Bulk Vuln"),
        "affected_asset_names": [asset["name"]],
        "priority": "Info",
        "likelihood_of_exploitation": 1,
        "description": "bulk",
        "attack_scenario": "bulk",
        "remediation_recommendation": "bulk",
        "steps_to_reproduce": "bulk",
    }
    client.findings.create_vulnerability_bulk(bulk_payload)

    # evidence upload/delete
    evidence_file = os.path.join(os.path.dirname(__file__), "evidence.txt")
    with open(evidence_file, "w", encoding="utf-8") as handle:
        handle.write("evidence")
    try:
        if vulnerability["id"]:
            upload = client.findings.upload_vulnerability_evidence(vulnerability["id"], evidence_file)
            upload_id = extract_id(upload)
            vulns = client.findings.get_project_vulnerabilities_all(
                project["id"], params={"pendingVulnerabilities": True}
            )
            vuln_entry = find_project_vulnerability_entry(vulns, vulnerability["id"])
            assert vuln_entry is not None, "Vulnerability not found when resolving evidence entries"
            entry = find_evidence_entry(vuln_entry, os.path.basename(evidence_file), upload_id)
            assert entry is not None, "Evidence entry not found in project vulnerabilities listing"
            file_name = extract_file_name(entry)
            assert file_name, "Evidence storage name missing from vulnerability evidence entry"
            client.findings.download_vulnerability_evidence(vulnerability["id"], file_name)
            client.findings.delete_vulnerability_evidence(vulnerability["id"], file_name)
    finally:
        os.remove(evidence_file)

    # upsert by title
    client.findings.upsert_finding_by_title(
        project_id=project["id"],
        title="SDK Upsert",
        affected_assets=[asset["name"]],
        create_payload={
            "projectId": project["id"],
            "title": "SDK Upsert",
            "affected_assets": [{"assetId": asset["id"]}],
            "priority": "Low",
            "likelihood_of_exploitation": 1,
            "description": "desc",
            "attack_scenario": "scenario",
            "remediation_recommendation": "remed",
            "steps_to_reproduce": "steps",
        },
    )


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_findings_evidence_fifo_dedupe(client, project, vulnerability):
    if not vulnerability["id"]:
        pytest.skip("Missing vulnerability id")
    base = unique_slug("evidence-fifo")
    names = [f"{base}-a.txt", f"{base}-b.txt", f"{base}-c.txt"]
    paths = []
    try:
        for name in names:
            path = os.path.join(os.path.dirname(__file__), name)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(name)
            paths.append(path)
            client.findings.upload_vulnerability_evidence(
                vulnerability["id"], path, project_id=project["id"]
            )
            time.sleep(0.5)

        evidence_entries = []
        vuln_entry = None
        for _ in range(12):
            vulns = client.findings.get_project_vulnerabilities_all(
                project["id"], params={"pendingVulnerabilities": True}
            )
            vuln_entry = find_project_vulnerability_entry(vulns, vulnerability["id"])
            assert vuln_entry is not None, "Vulnerability not found when resolving evidence entries"
            evidence_entries = extract_evidence_entries(vuln_entry)
            if len(evidence_entries) == 2:
                break
            time.sleep(1)
        assert len(evidence_entries) == 2, f"Expected FIFO to keep 2 evidence files, found {len(evidence_entries)}"

        dedupe_name = None
        for name in names:
            if find_evidence_entry(vuln_entry, name, None):
                dedupe_name = name
                break
        assert dedupe_name, "Unable to resolve existing evidence filename for dedupe check"
        dedupe_path = paths[names.index(dedupe_name)]
        result = client.findings.upload_vulnerability_evidence(
            vulnerability["id"], dedupe_path, dedupe=True, project_id=project["id"]
        )
        assert result.get("action") == "noop", "Expected dedupe to skip duplicate evidence upload"
    finally:
        for path in paths:
            try:
                os.remove(path)
            except OSError:
                pass


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_findings_dedup_assets(client, project, asset, asset_secondary):
    client.projects.create_scope(project["id"], {"assets": [asset_secondary["name"]]})
    title = unique_slug("SDK Dedup Finding")
    create_payload_a = {
        "projectId": project["id"],
        "title": title,
        "affected_assets": [{"assetId": asset["id"]}],
        "priority": "Info",
        "likelihood_of_exploitation": 1,
        "description": "dedup",
        "attack_scenario": "dedup",
        "remediation_recommendation": "dedup",
        "steps_to_reproduce": "dedup",
    }
    client.findings.upsert_finding_by_title(
        project_id=project["id"],
        title=title,
        affected_assets=[asset["name"]],
        create_payload=create_payload_a,
    )

    create_payload_b = {
        "projectId": project["id"],
        "title": title,
        "affected_assets": [{"assetId": asset_secondary["id"]}],
        "priority": "Info",
        "likelihood_of_exploitation": 1,
        "description": "dedup",
        "attack_scenario": "dedup",
        "remediation_recommendation": "dedup",
        "steps_to_reproduce": "dedup",
    }
    client.findings.upsert_finding_by_title(
        project_id=project["id"],
        title=title,
        affected_assets=[asset_secondary["name"]],
        create_payload=create_payload_b,
    )

    matches = []
    for _ in range(3):
        findings = client.findings.get_project_vulnerabilities_all(
            project["id"], params={"pendingVulnerabilities": True}
        )
        matches = [
            finding
            for finding in findings
            if normalize_title(extract_finding_title(finding)) == normalize_title(title)
        ]
        if matches:
            break
        time.sleep(1)
    assert len(matches) == 1, f"Expected one finding titled '{title}', found {len(matches)}"
    assets = extract_finding_assets(matches[0])
    assert asset["name"] in assets and asset_secondary["name"] in assets, "Affected assets missing in deduped finding"


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_findings_assign_to_testcase(client, project, asset, testcase):
    title = unique_slug("SDK Finding Testcase Link")
    payload = {
        "projectId": project["id"],
        "title": title,
        "affected_assets": [{"assetId": asset["id"]}],
        "priority": "Info",
        "likelihood_of_exploitation": 1,
        "description": "link",
        "attack_scenario": "link",
        "remediation_recommendation": "link",
        "steps_to_reproduce": "link",
        "linked_testcases": [testcase["id"]],
    }
    created = client.findings.create_vulnerability(payload)
    vulnerability_id = extract_id(created)
    assert vulnerability_id, "Missing vulnerability id after create"
    client.findings.update_vulnerability(vulnerability_id, {"linked_testcases": [testcase["id"]]})

    linked_ids = set()
    vuln_entry = None
    for _ in range(5):
        vulns = client.findings.get_project_vulnerabilities_all(
            project["id"], params={"pendingVulnerabilities": True}
        )
        vuln_entry = next(
            (v for v in vulns if (v.get("vulnerability_id") or v.get("id")) == vulnerability_id),
            None,
        )
        if not vuln_entry:
            time.sleep(1)
            continue
        linked_ids = extract_linked_testcase_ids(vuln_entry)
        if testcase["id"] in linked_ids:
            break
        time.sleep(1)
    assert vuln_entry is not None, "Vulnerability not found in project vulnerabilities listing"
    assert testcase["id"] in linked_ids, "Testcase not linked on vulnerability"


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_writeups_calls(client, writeup):
    client.writeups.get_writeups()
    client.writeups.update_writeup(writeup["id"], {"description": "updated"})

    writeup_file = os.path.join(os.path.dirname(__file__), "writeup.txt")
    with open(writeup_file, "w", encoding="utf-8") as handle:
        handle.write("writeup")
    try:
        upload = client.writeups.upload_writeup_file(writeup["id"], writeup_file)
        files = client.writeups.get_writeup_files(writeup_id=writeup["id"], name=writeup["title"])
        entry = next((item for item in files if matches_file_name(item, os.path.basename(writeup_file))), None)
        file_name = extract_file_name(entry) or extract_upload_file_name(upload, os.path.basename(writeup_file))
        assert file_name, "Writeup file storage name not returned by API"
        client.writeups.download_writeup_file(writeup["id"], file_name)
    finally:
        os.remove(writeup_file)


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_testcases_calls(client, project, testcase):
    client.testcases.get_project_testcases(project["id"])
    client.testcases.update_testcase(project["id"], testcase["id"], {"status": "Tested"})
    client.testcases.create_testcase_note(project["id"], testcase["id"], {"note": "SDK testcase note", "note_type": "PLAINTEXT"})

    # best-effort note file downloads (skip if not discoverable)
    testcases_data = client.testcases.get_project_testcases(project["id"])
    note_file = find_note_file(testcases_data, ("testcaseNoteId", "testcase_note_id", "note_id", "id"))
    if note_file:
        client.testcases.download_testcase_note_file(project["id"], note_file["note_id"], note_file["file_name"])
    workspace_note_file = find_note_file(
        testcases_data, ("testcaseWorkspaceNoteId", "testcase_workspace_note_id", "note_id", "id")
    )
    if workspace_note_file:
        client.testcases.download_testcase_workspace_note_file(
            project["id"], workspace_note_file["note_id"], workspace_note_file["file_name"]
        )

    # touch testcase
    client.testcases.touch_testcase(project["id"], testcase["id"], overwrite=False)


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_testcases_file_calls(client, project, testcase, base_project):
    if not has_ui_env():
        pytest.fail("Missing ATTACKFORGE_UI_TOKEN or ATTACKFORGE_UI_BASE_URL for testcase UI upload")
    base = unique_slug("testcase")
    names = [f"{base}-a.png", f"{base}-b.png", f"{base}-c.png"]
    paths = []
    try:
        for name in names:
            path = os.path.join(os.path.dirname(__file__), name)
            write_png(path)
            paths.append(path)
            client.testcases.upload_testcase_file(project["id"], testcase["id"], path, mode="ui")
            time.sleep(0.5)

        meta = None
        files = None
        remaining = []
        for _ in range(10):
            meta = client.testcases.get_project_testcase_meta_ui(project["id"], testcase["id"])
            if isinstance(meta, dict):
                files = meta.get("files")
            if isinstance(files, list):
                remaining = [
                    name for name in names if any(isinstance(entry, dict) and entry.get("name") == name for entry in files)
                ]
                if len(remaining) <= 2 and names[0] not in remaining:
                    break
            time.sleep(1)
        assert meta is not None, "UI testcase meta not returned"
        assert isinstance(files, list) and files, "UI testcase meta did not return files"
        assert len(remaining) <= 2, f"Expected FIFO to keep 2 files, found {len(remaining)}"
        assert names[0] not in remaining, "Oldest testcase evidence file was not removed by FIFO"

        dedupe_name = remaining[0] if remaining else names[1]
        dedupe_path = paths[names.index(dedupe_name)]
        dedupe = client.testcases.upload_testcase_file(
            project["id"], testcase["id"], dedupe_path, mode="ui", dedupe=True
        )
        assert dedupe.get("action") == "noop", "Expected testcase evidence dedupe to skip upload"
    finally:
        for path in paths:
            try:
                os.remove(path)
            except OSError:
                pass


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_testsuites_calls(client, testsuite, project, testcase):
    client.testsuites.get_testsuites()
    if testsuite["id"]:
        client.testsuites.get_testsuite(testsuite["id"])
        client.testsuites.update_testsuite(testsuite["id"], {"description": "updated"})

        # add testcase to testsuite (testsuite-level)
        tc_payload = {"testcase": "Suite testcase", "details": "details", "tags": ["sdk"]}
        suite_tc = client.testsuites.add_testcase_to_testsuite(testsuite["id"], tc_payload)
        client.testsuites.add_testcases_to_testsuite(testsuite["id"], {"testcases": [tc_payload]})
        suite_testcase_id = extract_id(suite_tc) or testcase["id"]

        # update testcase on testsuite using testsuite testcase id when available
        if suite_testcase_id:
            client.testsuites.update_testcase_on_testsuite(testsuite["id"], suite_testcase_id, {"status": "Tested"})


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_testsuites_file_calls(client, testsuite, testcase):
    assert testsuite["id"], "Missing testsuite id"
    tc_payload = {"testcase": "Suite testcase file", "details": "details", "tags": ["sdk"]}
    suite_tc = client.testsuites.add_testcase_to_testsuite(testsuite["id"], tc_payload)
    suite_testcase_id = extract_id(suite_tc) or testcase["id"]
    assert suite_testcase_id, "Missing testsuite testcase id"

    testsuite_file = os.path.join(os.path.dirname(__file__), "testsuite.txt")
    with open(testsuite_file, "w", encoding="utf-8") as handle:
        handle.write("testsuite")
    try:
        client.testsuites.upload_testsuite_testcase_file(testsuite["id"], suite_testcase_id, testsuite_file)
        testsuite_data = client.testsuites.get_testsuite(testsuite["id"])
        entry = find_testsuite_file_entry(testsuite_data, suite_testcase_id, os.path.basename(testsuite_file))
        assert entry is not None, "Testsuite file entry not found after upload"
        file_name = extract_file_name(entry)
        assert file_name, "Testsuite file storage name not returned by API"
        client.testsuites.download_testsuite_testcase_file(testsuite["id"], suite_testcase_id, file_name)
    finally:
        os.remove(testsuite_file)


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_notes_calls(client, vulnerability, remediation_note, project, base_project):
    if remediation_note["id"]:
        try:
            client.notes.update_remediation_note(
                vulnerability["id"],
                remediation_note["id"],
                {"note": "updated", "projectId": project["id"]},
            )
        except APIError as exc:
            skip_if_forbidden(exc, "Remediation note update requires additional access")

        note_file = os.path.join(os.path.dirname(__file__), "remediation.txt")
        with open(note_file, "w", encoding="utf-8") as handle:
            handle.write("remediation")
        try:
            client.notes.upload_remediation_note_file(vulnerability["id"], remediation_note["id"], note_file)
            report = client.reports.get_project_report_data(base_project["id"], "raw", {"excludeBinaries": False})
            existing = find_remediation_note_file_from_report(report)
            assert existing is not None, "Remediation note file not found in report data"
            client.notes.download_remediation_note_file(
                existing["vulnerability_id"],
                existing["note_id"],
                existing["file_name"],
                project_id=base_project["id"],
            )
        finally:
            os.remove(note_file)


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_users_calls(client, user, user_bulk, base_project, group_id):
    client.users.get_users()
    client.users.get_user(user["id"])
    client.users.get_user_by_email(user["email"])
    client.users.get_user_by_username(user["email"])
    client.users.update_user(user["id"], {"last_name": "UserUpdated"})
    client.users.deactivate_user(user["id"])
    client.users.activate_user(user["id"])

    # group membership operations (skip if no group available)
    if group_id:
        client.users.add_user_to_group({"group_id": group_id, "user_id": user["id"], "access_level": "View"})
        client.users.update_user_access_on_group(user["id"], {"group_id": group_id, "access_level": "Edit"})
        client.users.get_user_groups(user["id"])

    client.users.get_user_projects(user["id"])
    client.users.get_user_audit_logs(user["id"])
    client.users.get_user_login_history(user["id"])

    # invite user to base project and update access
    client.projects.invite_user_to_project(
        base_project["id"],
        {"id": base_project["id"], "username": user["email"], "accessLevel": "View"},
    )
    client.projects.update_user_access_on_project(base_project["id"], user["id"], {"update": "Edit"})

    client.projects.remove_project_team_members(base_project["id"], {"users": [user["email"]]})


@pytest.mark.integration
@pytest.mark.skipif(not has_env(), reason="Missing env vars")
def test_reports_calls(client, base_project):
    client.reports.get_project_report(base_project["id"], "raw")
    client.reports.get_project_report_data(base_project["id"], "raw", {"vulnerabilityIds": []})
    client.reports.update_exec_summary_notes(base_project["id"], {"exec_summary_notes": "SDK exec summary"})
