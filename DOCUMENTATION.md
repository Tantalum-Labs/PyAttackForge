**Overview**
PyAttackForge is a Python SDK for the AttackForge Self‑Service API (SSAPI). It provides a synchronous client, resource wrappers, helper methods, and convenience workflows such as finding deduplication, evidence FIFO retention, and testcase “touch” updates.

**Requirements**
- Python 3.10+
- Network access to your AttackForge instance

**Install**
```bash
pip install pyattackforge
```

**Configuration**
The SDK uses environment variables by default (via `pyattackforge.config.config_from_env`).

Required:
- `ATTACKFORGE_BASE_URL`
- `ATTACKFORGE_API_KEY`

Optional:
- `ATTACKFORGE_TEST_PROJECT_ID` (for integration tests)
- `ATTACKFORGE_FINDINGS_VISIBLE_DEFAULT` (default `false` = pending/hidden)
- `ATTACKFORGE_FINDINGS_SUBSTATUS_KEY` (default `substatus`)
- `ATTACKFORGE_FINDINGS_SUBSTATUS_VALUE` (default `Observed`)
- `ATTACKFORGE_UI_BASE_URL` (UI base URL for project testcase uploads and notes)
- `ATTACKFORGE_UI_TOKEN` (UI auth token for testcase uploads and notes)

Example `.env`:
```env
ATTACKFORGE_BASE_URL=https://demo.attackforge.com
ATTACKFORGE_API_KEY=replace-me
ATTACKFORGE_TEST_PROJECT_ID=replace-me
ATTACKFORGE_FINDINGS_VISIBLE_DEFAULT=false
ATTACKFORGE_FINDINGS_SUBSTATUS_KEY=substatus
ATTACKFORGE_FINDINGS_SUBSTATUS_VALUE=Observed
ATTACKFORGE_UI_BASE_URL=https://demo.attackforge.com
ATTACKFORGE_UI_TOKEN=replace-me
```

You can also construct a `ClientConfig` manually and pass it to `AttackForgeClient`.

**Quick Start**
```python
from pyattackforge import AttackForgeClient

with AttackForgeClient() as client:
    projects = client.projects.get_projects()
    print(projects)
```

**Client**
`AttackForgeClient` exposes resource groups:
- `client.assets`
- `client.projects`
- `client.groups`
- `client.findings`
- `client.writeups`
- `client.testcases`
- `client.testsuites`
- `client.notes`
- `client.users`
- `client.reports`

The client is a context manager and should be closed when done.

**Resources**
Each method returns the raw JSON payload from the SSAPI (or UI endpoints where noted).

Assets (`AssetsResource`)
- `create_asset_in_library(payload)`
- `update_asset_in_library(asset_id, payload)`
- `get_assets(params=None, force_refresh=False)`
- `get_asset_in_library(asset_id)`
- `get_asset_library_assets(payload)`

Projects (`ProjectsResource`)
- `create_project(payload)`
- `get_project(project_id, params=None, force_refresh=False)`
- `get_projects(params=None)`
- `get_projects_and_vulnerabilities(params=None)`
- `update_project(project_id, payload)`
- `archive_project(project_id)`
- `restore_project(project_id)`
- `destroy_projects(project_ids, keep_logs=None)`
- `clone_project(project_id, payload=None)`
- `create_scope(project_id, payload)`
- `update_scope(project_id, asset_id, payload)`
- `get_project_workspace(project_id)`
- `upload_workspace_file(project_id, file_path)`
- `download_workspace_file(project_id, file_name)`
- `get_project_notes(project_id)`
- `create_project_note(project_id, payload)`
- `update_project_note(project_id, note_id, payload)`
- `create_project_workspace_note(project_id, payload)`
- `update_project_workspace_note(project_id, note_id, payload)`
- `get_project_membership_administrators(project_id)`
- `add_project_membership_administrators(project_id, payload)`
- `update_project_membership_administrators(project_id, payload)`
- `remove_project_membership_administrators(project_id, payload)`
- `invite_user_to_project(project_id, payload)`
- `invite_users_to_project_team(project_id, payload)`
- `remove_project_team_members(project_id, payload)`
- `update_user_access_on_project(project_id, user_id, payload)`
- `add_project_to_group(project_id, group_id, project_data=None)`
- `extract_projects_list(projects_data)`
- `find_project_by_name(name, params=None)`

Groups (`GroupsResource`)
- `get_groups(params=None)`
- `get_group(group_id, params=None)`
- `create_group(payload)`

Findings (`FindingsResource`)
- `create_vulnerability(payload)`
- `create_vulnerability_bulk(payload)`
- `create_vulnerability_with_library(payload)`
- `get_vulnerabilities(params=None)`
- `get_vulnerability(vulnerability_id, params=None)`
- `get_project_vulnerabilities(project_id, params=None)`
- `get_project_vulnerabilities_all(project_id, params=None)`
- `find_project_vulnerability_by_title(project_id, title, include_pending=True)`
- `find_project_vulnerability_by_library_id(project_id, library_id, include_pending=True)`
- `get_vulnerabilities_by_asset_name(asset_name, params=None)`
- `update_vulnerability(vulnerability_id, payload)`
- `update_vulnerability_with_library(vulnerability_id, payload)`
- `update_vulnerability_slas(payload)`
- `update_linked_projects_on_vulnerabilities(payload)`
- `get_vulnerability_revision_history(vulnerability_id)`
- `upload_vulnerability_evidence(vulnerability_id, file_path, keep_last=2, project_id=None, dedupe=False)`
- `download_vulnerability_evidence(vulnerability_id, file_name)`
- `delete_vulnerability_evidence(vulnerability_id, file_name)`
- `upsert_finding_by_title(project_id, title, affected_assets, create_payload, update_payload=None, use_library=False, validate_asset_agnostic=True)`
- `extract_linked_testcase_ids(vulnerability)`
- `assert_asset_agnostic(payload, asset_names, enabled=True)`

Writeups (`WriteupsResource`)
- `get_writeups(params=None, force_refresh=False)`
- `get_writeup_files(writeup_id=None, name=None)`
- `create_writeup(payload)`
- `update_writeup(writeup_id, payload)`
- `upload_writeup_file(writeup_id, file_path)`
- `download_writeup_file(writeup_id, file_name)`

Testcases (`TestcasesResource`)
- `create_testcase(project_id, payload)`
- `get_project_testcases(project_id, params=None)`
- `update_testcase(project_id, testcase_id, payload)`
- `create_testcase_note(project_id, testcase_id, payload, dedupe=False)`
- `upload_testcase_file(project_id, testcase_id, file_path, keep_last=2, dedupe=False, mode="auto", ui_token=None, ui_base_url=None)`
- `download_testcase_file(project_id, testcase_id, file_name)`
- `download_testcase_note_file(project_id, note_id, file_name)`
- `download_testcase_workspace_note_file(project_id, note_id, file_name)`
- `delete_testcase_file(project_id, testcase_id, file_name)`
- `get_project_testcase_meta_ui(project_id, testcase_id, ui_token=None, ui_base_url=None)`
- `get_project_testcase_notes_ui(project_id, testcase_id, ui_token=None, ui_base_url=None)`
- `touch_testcase(project_id, testcase_id, timestamp=None, testcase_type="Security Test Case", overwrite=False)`
- `extract_project_testcases_list(project_testcases)`
- `find_project_testcase_entry(project_testcases, testcase_id)`
- `build_project_testcase_map(project_testcases)`
- `wait_for_project_testcases(project_id, attempts=12, delay=2.0)`
- `extract_project_testcase_id(testcase)`
- `first_project_testcase_id(project_testcases)`
- `extract_linked_vulnerability_ids(testcase)`

Testsuites (`TestsuitesResource`)
- `create_testsuite(payload)`
- `get_testsuites(params=None)`
- `get_testsuite(testsuite_id)`
- `update_testsuite(testsuite_id, payload)`
- `add_testcase_to_testsuite(testsuite_id, payload)`
- `add_testcases_to_testsuite(testsuite_id, payload)`
- `update_testcase_on_testsuite(testsuite_id, testcase_id, payload)`
- `upload_testsuite_testcase_file(testsuite_id, testcase_id, file_path)`
- `download_testsuite_testcase_file(testsuite_id, testcase_id, file_name)`
- `extract_testsuites_list(testsuites_data)`
- `find_testsuite_by_name(name, params=None)`
- `extract_testsuite_testcases(suite_data)`
- `get_testsuite_testcases(testsuite_id)`

Notes (`NotesResource`)
- `create_remediation_note(vulnerability_id, payload)`
- `update_remediation_note(vulnerability_id, remediation_note_id, payload)`
- `upload_remediation_note_file(vulnerability_id, remediation_note_id, file_path)`
- `download_remediation_note_file(vulnerability_id, remediation_note_id, file_name=None, project_id=None)`

Users (`UsersResource`)
- `create_user(payload)`
- `create_users(users)`
- `get_user(user_id)`
- `get_users(params=None)`
- `get_user_by_email(email)`
- `get_user_by_username(username)`
- `update_user(user_id, payload)`
- `activate_user(user_id)`
- `deactivate_user(user_id)`
- `add_user_to_group(payload)`
- `update_user_access_on_group(user_id, payload)`
- `get_user_groups(user_id)`
- `get_user_projects(user_id)`
- `get_user_audit_logs(user_id, params=None)`
- `get_user_login_history(user_id, params=None)`

Reports (`ReportsResource`)
- `get_project_report(project_id, report_type, params=None)`
- `get_project_report_data(project_id, report_type, payload)`
- `update_exec_summary_notes(project_id, payload)`

Client‑level helpers (`AttackForgeClient`)
- `link_vulnerability_to_testcases(project_id, vulnerability_id, testcase_ids, verify=True, attempts=3, delay=1.0)`

**Finding Deduplication**
`FindingsResource.upsert_finding_by_title` prevents duplicate findings by title (case‑insensitive, trimmed) within a project. If a matching finding exists, it appends missing affected assets.

Key behaviors:
- Duplicate = same title on same project.
- If a matching finding already has the asset, no update occurs.
- When assets are missing, the finding is updated with the combined asset list.
- `validate_asset_agnostic=True` rejects payloads that embed asset names outside `affected_assets`.

**Finding Defaults**
Findings created via `create_vulnerability`, `create_vulnerability_bulk`, and `create_vulnerability_with_library` are normalized by `_apply_finding_defaults`.

Defaults:
- `is_visible` is set from `ATTACKFORGE_FINDINGS_VISIBLE_DEFAULT` (default is pending/hidden).
- `custom_fields` include `substatus=Observed` (configurable via env).

You can override by providing `is_visible` or a `custom_fields` entry yourself.

**Evidence Handling**
Findings evidence:
- `upload_vulnerability_evidence(..., keep_last=2, dedupe=False)`
- FIFO deletes oldest files above `keep_last`.
- `dedupe=True` skips upload if filename already exists.
- Pass `project_id` to improve evidence metadata resolution.

Project testcase evidence:
- `upload_testcase_file(..., keep_last=2, dedupe=False, mode="auto")`
- `mode="auto"` uses UI upload when UI token is present, otherwise SSAPI.
- UI FIFO deletion uses `/api/projects/:projectId/meta/:fileId/delete` with GET/POST semantics.

**Testcase Notes Deduplication**
`create_testcase_note(..., dedupe=True)` compares the note text against:
- Notes included in the project testcase listing
- The UI notes endpoint if `ATTACKFORGE_UI_TOKEN` is available

If a matching note exists, the method returns a `noop` response.

**Touching Testcases**
`touch_testcase` writes project testcase custom fields:
- `last_tested` default format `YYYY-MM-DD`
- `testcase_type` default `Security Test Case`

Custom fields are merged by default. Use `overwrite=True` to replace the list.

**Caching**
The SDK uses a small TTL cache to reduce API calls.

Cached endpoints:
- `assets.get_assets()`
- `projects.get_project()`
- `writeups.get_writeups()`

You can bypass cache with `force_refresh=True` where available.

**Transport and Retries**
- HTTP client is `httpx.Client`.
- Automatic retries for 429, 500, 502, 503, 504 with exponential backoff (`max_retries`, `backoff_factor`).
- File uploads retry with an HTTP/2 client on 5xx responses.

**Errors**
Requests that return HTTP >= 400 raise `APIError` with `status_code` and payload data.

**UI Endpoints**
Some project testcase operations require the UI API (not SSAPI) to reflect in the UI:
- Uploading project testcase evidence
- Listing project testcase notes

Provide:
- `ATTACKFORGE_UI_TOKEN`
- `ATTACKFORGE_UI_BASE_URL`

**Testing**
Integration tests live at `PyAttackForge/tests/integration/test_live_full.py`.

Examples:
```bash
python3 -m pytest -m integration -vv
python3 -m pytest -m integration -k evidence_fifo_dedupe -vv
```

**Seed Script**
`PyAttackForge/scripts/seed_mock_project.py` creates:
- A mock project `Tantalum Labs Fake Pentest`
- Mock assets, findings, evidence, notes
- Findings linked to project testcases
- Uses writeups from the `approved_writeups` library via SSAPI (`/api/ss/library?belongs_to_library=...`)
- Falls back to `writeups.json` only if the API returns no entries

Run:
```bash
python3 scripts/seed_mock_project.py
```

**Writeup Import Script**
`PyAttackForge/scripts/import_writeups.py` imports writeups from a JSON export.
- By default it will ensure custom libraries exist. If the SSAPI returns an error for a custom library key, the script will create a small bootstrap writeup in that library.
- Use `--no-ensure-library` to skip this behavior.
- Use `--ensure-writeup-fields` to add missing custom fields in Settings -> Writeups. Fields are created under a section named `Imported`.

**DoppleSpy Import Script**
`PyAttackForge/scripts/import_dopplespy_findings.py` imports findings from a DoppleSpy JSON file into a target project.
It matches findings to writeups in the `approved_writeups` library and attaches evidence if a PNG is present alongside the JSON.
It uses mappings in `PyAttackForge/scripts/library.py` to translate source titles into approved writeup titles.

**Known Limitations**
- Project testcase evidence deletion via SSAPI is not supported for this tenant; UI delete is used.
- Evidence metadata availability varies by endpoint. FIFO/dedupe relies on best‑effort extraction.
- Remediation note file downloads sometimes require report‑data fallbacks when storage names are not returned.

**Code Map**
- Client: `PyAttackForge/pyattackforge/client.py`
- Resources: `PyAttackForge/pyattackforge/resources/`
- Transport: `PyAttackForge/pyattackforge/transport.py`
- Caching: `PyAttackForge/pyattackforge/cache.py`
- Seed script: `PyAttackForge/scripts/seed_mock_project.py`
- Coverage matrix: `PyAttackForge/COVERAGE.md`
