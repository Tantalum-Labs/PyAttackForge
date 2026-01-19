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
- `PYATTACKFORGE_ARTIFACT_DIR` (default: `.codex/artifacts`; where live tests write report.json and sample evidence)

## Endpoint-specific request validation (required)
For SSAPI calls that return VALIDATION_FAILED, implement endpoint-local validation:
- Add a helper per endpoint (or a shared helper with endpoint name), e.g.:
  - normalize_testcase_status(status: str) -> str
- The helper must:
  - accept a small set of friendly aliases
  - convert to the canonical strings required by the endpoint
  - raise ValueError for unsupported values, with the allowed set in the message

Rule of scope:
- These constraints apply only to that endpoint unless documented otherwise.

## Required Code Changes

### A) Fix response handling (unwrap helpers)
Implement consistent unwrapping so callers can safely treat returned objects as:
- project dict (not `{ "project": ... }`)
- vulnerability dict (not `{ "vulnerability": ... }`)
- testcase dict (must include top-level `id` when created)
- user dict, etc., where applicable

Add a small internal helper:
- `_unwrap(resp_json, key)` that returns `resp_json[key]` if present, else returns resp_json unchanged

Update methods that currently return wrapped objects:
- `get_project_by_id`
- `get_vulnerability`
- `create_testcase` (must return a dict with `id`)
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

Ensure finding creation/upsert can:
- Ensure affected assets are in project scope before creating the vulnerability
- Work whether assets are represented by name or asset_id (assets module)

### D) Writeup/library lookup correctness
Replace any `/api/ss/libraries/...` usage with documented library endpoints:
- `GET /api/ss/library` with `belongs_to_library=...` and/or `q=...`
Cache should be:
- optional (speed-up only)
- correct (no wrong default library name)

Default library should be `Main Vulnerabilities` unless configured.

### E) Evidence upload de-dupe (finding and testcase)
Finding evidence de-dupe:
- Before uploading, fetch existing evidence list for the finding (vulnerability_evidence)
- If an evidence item already exists with same filename AND same size (bytes), skip upload
- Print/log exactly:
  - `SKIP evidence (already exists): <filename> (<size> bytes)`
- Return a structured result indicating uploaded/skipped and reason.

Testcase evidence de-dupe (when attaching to testcase):
- Before uploading, list existing testcase files
- If filename AND size match, skip upload
- Record the skip in report.json and log a skip line.

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

2) Writeup lookup
- Find an existing writeup (preferred: "Open port detected" in the configured library), or create a minimal writeup if missing.

3) Finding upsert idempotency + asset append
- Upsert finding once (asset A) => created
- Upsert same finding again (asset A) => deduped (same id)
- Upsert same finding again (asset B) => deduped (same id) and asset B appended
- Verify via get/list that only ONE finding exists for the run_id/title
- Verify assets include A and B

4) Evidence upload idempotency using PNG evidence
- Generate a small PNG file as evidence and upload once => uploaded
- Upload the same PNG again => skipped as duplicate (filename+size)
- Generate a different-sized PNG and upload => uploaded

5) Testcase linkage
- Create a testcase
- Link the finding to the testcase
- Verify linkage via GET testcase

6) Testcase notes + evidence on attach (idempotent)
- Attach the finding to testcase with a note and a PNG evidence file => created
- Repeat the attach with identical note and identical PNG => skip duplicates (note and evidence)
- Verify exactly one matching note exists and exactly one matching file exists

### Test artifacts & reporting (required)
Live tests must produce a clear report per run:
- Directory: `.codex/artifacts/<RUN_ID>/`
- Required: `report.json`

report.json must record:
- created IDs (finding_id, testcase_id)
- dedupe decisions (deduped vs created)
- evidence decisions (uploaded vs skipped) with filename + size
- linkage verification result

Evidence used in tests must be generated PNGs (Pillow) stored under the run artifact directory.

## Acceptance Criteria
With live tests enabled (`PYATTACKFORGE_LIVE=1`) and valid sandbox credentials:
- `./ci.sh` exits 0
- Live tests pass and generate `.codex/artifacts/<RUN_ID>/report.json`
- Duplicate finding behavior is proven via API assertions (count==1 for the run title) and recorded in report.json
- Duplicate evidence behavior is proven using PNG files (filename+size) and recorded in report.json
- No secrets exist in the repo (keys/configs removed or sanitized)
- Client methods return correct unwrapped objects consistent with SSAPI response shapes
