# SPEC: PyAttackForge - Live SSAPI Contract + Idempotency

## Goal
Make PyAttackForge a reliable, tested Python client for AttackForge SSAPI that:
- Works against a real AttackForge sandbox tenant
- Correctly handles SSAPI response shapes
- Supports idempotent workflows (no accidental duplicates)
- Produces repeatable integration tests that can run in CI

Primary success condition:
- `./ci.sh` exits 0 with live SSAPI tests enabled and correctly configured.

## Background
PyAttackForge wraps the AttackForge Self-Service RESTful API (SSAPI). SSAPI responses often return wrapped objects such as:
- `GET /api/ss/project/:id -> { "project": {...} }`
- `GET /api/ss/vulnerability/:id -> { "vulnerability": {...} }`
Evidence metadata is available via `vulnerability_evidence` on the vulnerability object.

SSAPI access is explicitly permissioned per method; missing permissions must be surfaced clearly and tests should skip with a clear reason when appropriate.

## Non-goals
- Building a full CLI application
- Implementing unrelated AttackForge modules not already represented in the client
- Perfect backwards compatibility with older un-documented endpoints if the official endpoints work

## Security / Secrets Requirements
- Remove any hardcoded API keys or secrets from the repository (including example scripts and json config files).
- Add `.env.example` with placeholder variable names only.
- Ensure `.gitignore` excludes `.env`, build artifacts, and virtual environments.
- Never print API keys or auth headers in logs.

## Environment Variables
Required for live tests:
- `ATTACKFORGE_BASE_URL` (e.g. https://demo.attackforge.com)
- `ATTACKFORGE_SSAPI_KEY`  (SSAPI key; passed via X-SSAPI-KEY)
- `ATTACKFORGE_PROJECT_ID` (sandbox project id)

Optional:
- `ATTACKFORGE_VERIFY_SSL` (default: 1)
- `PYATTACKFORGE_LIVE` (default: 0; set 1 to run live integration tests)
- `PYATTACKFORGE_RUN_USER_MUTATION_TESTS` (default: 0; opt-in)
- `PYATTACKFORGE_BELONGS_TO_LIBRARY` (default: "Main Vulnerabilities")
- `PYATTACKFORGE_CLEANUP` (default: 1; remove testcases and test evidence when possible)

## Required Code Changes

### A) Fix response handling (unwrap helpers)
Implement consistent unwrapping so callers can safely treat returned objects as:
- project dict (not `{ "project": ... }`)
- vulnerability dict (not `{ "vulnerability": ... }`)
- user dict, etc., where applicable

Add a small internal helper:
- `_unwrap(resp_json, key)` that returns `resp_json[key]` if present, else returns resp_json unchanged

Update methods that currently return wrapped objects:
- `get_project_by_id`
- `get_vulnerability`
- Any other methods returning `{ "X": {...} }`

### B) Implement create_asset (library asset creation)
Implement `create_asset()` using the documented SSAPI endpoint:
- `POST /api/ss/library/asset`
Inputs should allow:
- asset name
- asset type (default reasonable type)
- optional custom fields / external ids if supported

If the asset already exists, the method should:
- return the existing asset (lookup by name) OR
- return a structured response that indicates "already exists"

### C) Project scope handling
Replace or supplement any undocumented scope update logic with documented behavior:
- Add assets to a project using CreateScope:
  `POST /api/ss/project/:id/assets`
This may take asset names and optionally `asset_library_ids` for mapping (if Assets module is enabled).

Ensure `create_vulnerability()` can:
- Ensure affected assets are in project scope before creating the vulnerability
- Work whether assets are represented by name or asset_id (assets module)

### D) Writeup/library lookup correctness
Replace any `/api/ss/libraries/...` usage with documented library endpoints:
- `GET /api/ss/library` with `belongs_to_library=...` and/or `q=...`
Cache should be:
- optional (speed-up only)
- correct (no wrong default library name)

Default library should be `Main Vulnerabilities` unless configured.

### E) Evidence upload de-dupe
Update `upload_finding_evidence()` to prevent duplicates by default:
- Fetch vulnerability (`get_vulnerability(vuln_id)`)
- Inspect `vulnerability_evidence` list
- If an evidence item already exists with same `file_name_custom` (or same basename) AND same size (or same sha256), skip upload

Add an override flag:
- `dedupe=True` default
- If `dedupe=False`, always upload

When cleanup is enabled, delete test evidence using:
- `DELETE /api/ss/vulnerability/:id/evidence/:file` (storage_name)

### F) Remove insecure/outdated sample scripts
The root-level test scripts that embed credentials or use outdated method signatures must be removed or rewritten to:
- load env vars
- be safe
- be compatible with the current API client

## Tests

### Test framework
Use `pytest`.

Markers:
- Unit tests: default (no marker)
- Live SSAPI tests: `@pytest.mark.live`

### Live SSAPI test plan (minimum)
Given env vars are set and access is granted:

1) Connectivity + permissions smoke test
- Call a lightweight endpoint (e.g. get_project_by_id) and assert response contains expected fields.

2) Writeup lookup + create if missing
- Ensure writeup can be found or created in the configured library.

3) Create finding from writeup on a real project
- Create vulnerability using `create_finding_from_writeup` / `create_vulnerability`
- Assert created vulnerability id is returned and can be fetched

4) Update finding
- Call `update_finding` and verify fields changed (title/tag/notes/etc)

5) Evidence upload idempotency
- Upload a small test file once
- Confirm evidence count increased by 1
- Upload the same file again with dedupe enabled
- Confirm evidence count did NOT increase
- Optionally clean up evidence (delete by storage_name)

6) Testcase flow (if enabled for that project)
- Create a testcase
- Update testcase
- Link finding(s) to testcase
- Delete testcase (cleanup)

User mutation tests:
- Only run when `PYATTACKFORGE_RUN_USER_MUTATION_TESTS=1`

### Cleanup
Default behavior:
- Clean up testcases created by tests
- Clean up evidence created by tests (when delete evidence is permitted)
Vulnerabilities/findings may not always be safely deletable; if no delete is supported, keep them but label them clearly:
- Title prefix: `PYAF-CI <run_id> - ...`
- Add note: `Created by PyAttackForge CI`

## Acceptance Criteria
With live tests enabled (`PYATTACKFORGE_LIVE=1`) and valid sandbox credentials:
- `./ci.sh` exits 0
- All live tests pass (no skips due to missing env)
- Evidence de-dupe test proves no duplicate evidence is uploaded
- No secrets exist in the repo (keys/configs removed or sanitized)
- Client methods return correct unwrapped objects consistent with official SSAPI response shapes
