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

## Idempotency and linkage requirements (must implement + test)

All behaviors below must be validated via live SSAPI integration tests (pytest marker: live) against the sandbox project.

### Definitions

#### Finding de-duplication key (required)
Two findings are considered the “same finding” (duplicates) if they share ALL of:
- project_id
- writeup identifier (preferred: vulnerability library issue id OR writeup title + belongs_to_library)
- finding title (canonical writeup title)

Assets are NOT part of the de-duplication key.

#### Asset append rule (required)
If a second “duplicate” finding submission differs only by assets, the client must:
- re-use the existing finding
- append any missing assets to the existing finding’s affected assets/scope representation
- return the existing finding id

#### Evidence de-duplication key (required)
Evidence is a duplicate if BOTH match:
- filename (exact match)
- size in bytes (exact match)

If filename+size already exists on the finding, skip uploading and log:
- "SKIP evidence (already exists): <filename> (<size> bytes)"

### Required client features

#### A) Upsert finding (required)
Add a high-level method:
- upsert_finding_from_writeup(..., assets=[...], dedupe=True, append_assets=True)

Behavior:
1) Find an existing matching finding in the sandbox project (by de-dup key).
2) If found:
   - if append_assets: ensure all requested assets are present on the finding/project scope
   - return existing finding id and a result indicating "deduped"
3) If not found:
   - create the finding and return the new id

The method must not create duplicate findings for the same de-dup key.

#### B) Evidence upload de-dupe (required)
Update upload_finding_evidence(..., dedupe=True):
- Before upload, fetch existing evidence list for the finding
- If filename+size exists already, skip upload and log as specified
- Return a structured result indicating uploaded/skipped

#### C) Finding ↔ testcase linkage (required)
Add/validate a method:
- link_finding_to_testcase(project_id, testcase_id, finding_id)

Must be verifiable via follow-up GET:
- fetch testcase and confirm the finding is linked (preferred)
or
- fetch finding and confirm testcase linkage (acceptable)

#### D) When attaching a finding to a testcase, add testcase notes + evidence (idempotent)
Add a high-level helper:
- attach_finding_to_testcase_with_notes_and_evidence(...)

Behavior:
- Link finding to testcase
- Add a testcase note that references the finding
- Upload testcase evidence (optional parameter)
- Do not duplicate:
  - note (same text)
  - evidence (same filename+size)
- Log skips similarly to evidence skip messaging

### Live test constraints
- Every live run must use a unique RUN_ID prefix: "PYAF-CI-<timestamp>-<suffix>"
- All created objects (finding title, testcase title, note content, evidence filenames) must include RUN_ID.
- Cleanup is preferred:
  - delete testcases created by tests (if SSAPI supports)
  - delete evidence created by tests (if permitted)
  - findings may be left if deletion isn’t supported; they must remain uniquely identifiable by RUN_ID.

