# PyAttackForge

Next-generation Python SDK for the AttackForge SSAPI (Python 3.10+).

## Install (local)

```bash
pip install -e .
```

## Configuration

Environment variables:
- `ATTACKFORGE_BASE_URL`
- `ATTACKFORGE_API_KEY`
- `ATTACKFORGE_TEST_PROJECT_ID` (only needed for live integration tests)
- `ATTACKFORGE_FINDINGS_VISIBLE_DEFAULT` (optional, set to `true` to make new findings visible; default is pending/hidden)
- `ATTACKFORGE_FINDINGS_SUBSTATUS_KEY` (optional, default `substatus`)
- `ATTACKFORGE_FINDINGS_SUBSTATUS_VALUE` (optional, default `Observed`)
- `ATTACKFORGE_UI_BASE_URL` (optional, UI base URL for project testcase uploads/verification)
- `ATTACKFORGE_UI_TOKEN` (optional, UI authorization token for project testcase uploads/verification)

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

## Usage (sync)

```python
from pyattackforge import AttackForgeClient

with AttackForgeClient() as client:
    projects = client.projects.get_projects()
    print(projects)
```

Touch a testcase (updates `last_tested` and `testcase_type` in `project_testcase_custom_fields`):

```python
from pyattackforge import AttackForgeClient

with AttackForgeClient() as client:
    client.testcases.touch_testcase("project_id", "testcase_id")
```

By default, the SDK merges `last_tested` and `testcase_type` into existing project testcase custom fields. Use `overwrite=True` to replace the list.
Default format for `last_tested` is `YYYY-MM-DD` (date picker friendly). Override by supplying `timestamp=`.
Default `testcase_type` is `Security Test Case`. Override by supplying `testcase_type=`.

Create a testcase note with optional deduplication (case-insensitive, trimmed):

```python
from pyattackforge import AttackForgeClient

with AttackForgeClient() as client:
    payload = {"note": "Observed weak password policy", "note_type": "PLAINTEXT"}
    client.testcases.create_testcase_note("project_id", "testcase_id", payload, dedupe=True)
```

When `dedupe=True`, the SDK compares against notes returned by the project testcase listing. If notes are not included in that response, the check is best-effort and the note will be created.
If a UI token is configured (`ATTACKFORGE_UI_TOKEN`), the SDK will also check the UI notes endpoint to avoid duplicates.

Upload vulnerability evidence with FIFO retention and dedupe:

```python
from pyattackforge import AttackForgeClient

with AttackForgeClient() as client:
    client.findings.upload_vulnerability_evidence("vuln_id", "evidence.png")
    # keep_last defaults to 2 (FIFO, keep most recent). Set keep_last=None to disable.
    client.findings.upload_vulnerability_evidence("vuln_id", "evidence.png", dedupe=True)
```

For more reliable FIFO/dedupe, pass `project_id` so the SDK can use the project vulnerability listing (which contains evidence metadata):

```python
client.findings.upload_vulnerability_evidence("vuln_id", "evidence.png", project_id="project_id")
```

Upload project testcase evidence with FIFO retention and dedupe:

```python
from pyattackforge import AttackForgeClient

with AttackForgeClient() as client:
    client.testcases.upload_testcase_file("project_id", "testcase_id", "evidence.png")
    # keep_last defaults to 2 (FIFO, keep most recent). Set keep_last=None to disable.
    client.testcases.upload_testcase_file("project_id", "testcase_id", "evidence.png", dedupe=True)
```

When a UI token is configured, FIFO cleanup for testcase evidence uses the UI delete endpoint:
`/api/projects/:projectId/meta/:fileId/delete` (UI expects GET/POST semantics).

Helper methods (examples):

```python
with AttackForgeClient() as client:
    project = client.projects.find_project_by_name("Tantalum Labs Fake Pentest")
    suite = client.testsuites.find_testsuite_by_name("OWASP Web App Penetration Test")
    if suite:
        testcases = client.testsuites.get_testsuite_testcases(suite["id"])
    client.link_vulnerability_to_testcases("project_id", "vuln_id", ["testcase_id"])
```

## Testing

Unit tests:

```bash
python3 -m pytest
```

Integration tests (require env vars):

```bash
python3 -m pytest -m integration
```

Integration tests create and modify data in the target tenant and will attempt cleanup. They read `ATTACKFORGE_BASE_URL`, `ATTACKFORGE_API_KEY`, and `ATTACKFORGE_TEST_PROJECT_ID`.

## Status

This is a from-scratch rewrite. See `COVERAGE.md` for endpoint coverage and assumptions.

## Scripts

Import writeups from a JSON export:

```bash
python3 scripts/import_writeups.py --input writeups.json
```

By default the script will ensure custom libraries exist. If the SSAPI returns an error for a custom library key, it will create a small bootstrap writeup in that library. Use `--no-ensure-library` to skip.

Add missing writeup custom fields (Settings -> Writeups) based on the import file:

```bash
python3 scripts/import_writeups.py --input writeups.json --ensure-writeup-fields
```
