# AGENTS

Success command: ./ci.sh

Rules:
- Make minimal changes; no unrelated refactors.
- Always rerun ./ci.sh after modifications.
- Tests must clean up docker containers on failure.

Docs / API references:
- Do NOT browse the web for AttackForge docs during implementation or tests.
- Use ONLY the committed local docs cache under:
  - docs/attackforge/ssapi/index.md
  - docs/attackforge/ssapi/manifest.json
  - docs/attackforge/ssapi/markdown/*
- If required information is missing from the local docs cache:
  - Write a short note to .codex/missing_docs.txt describing the missing endpoint/method and what is needed.
  - Then proceed using live integration tests as the source of truth (sandbox API behavior), without attempting to fetch online docs.

Doc lookup process (required):
1) Search the local cache first:
   - For example: rg -n "CreateProjectNote|/api/ss/|UploadVulnerabilityEvidence|<endpoint name>" docs/attackforge/ssapi/markdown
2) If the endpoint is found, use the local markdown page as the reference.
3) If not found, rely on the live sandbox API behavior and record the missing-doc note as above.

Navigation/slugs:
- Never guess URL slugs; use docs/attackforge/ssapi/manifest.json for the authoritative href list.
- Never curl/wget AttackForge doc pages during a Codex run.

API validation errors (endpoint-specific):
- When an endpoint returns code "VALIDATION_FAILED" and includes error.details[]:
  1) Treat error.details[].path and error.details[].info (e.g., pattern/enum) as authoritative for THAT endpoint only.
  2) Implement client-side validation/normalization inside the specific client method that submits the request (e.g., create_testcase / update_testcase).
  3) Add a small unit test for the validation/normalization helper.
  4) Update live integration tests to use canonical values.
- Do NOT apply endpoint-specific constraints globally unless the docs explicitly state they are global.
- Do NOT brute-force retry random values. Use the details/pattern/enum from the API response or the local docs cache.

Testing/reporting rules:
- Live tests must write a per-run report to .codex/artifacts/<RUN_ID>/report.json with:
  - created IDs (finding_id, testcase_id, evidence storage/name where available)
  - dedupe decisions (deduped vs created, skipped evidence vs uploaded)
  - linkage verification results
- Prefer verifiable assertions via SSAPI (list/get) over manual UI inspection.
- When adding coverage, include both:
  1) an API assertion (count/ids/fields)
  2) a report event recording the IDs and decisions.
- Evidence used in tests must include generated PNG files (via Pillow) to exercise binary upload paths.
