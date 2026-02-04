# PyAttackForge SSAPI Coverage Matrix

This file captures the SSAPI endpoints in scope for PyAttackForge, the planned SDK methods, and any assumptions or exclusions.

## Assumptions
- Testcase evidence deletion is not supported in the live environment (HTTP 404). Tests assert this behavior and will be updated if SSAPI adds delete support.
- Project testcase evidence uploads default to `keep_last=2` (FIFO, keep most recent). FIFO deletion is best-effort and skips 404s.
- When UI credentials are present, testcase evidence FIFO deletes via `/api/projects/:projectId/meta/:fileId/delete` (UI uses GET/POST semantics rather than DELETE).
- Testcase "touch" uses `project_testcase_custom_fields` keys `last_tested` and `testcase_type` (custom fields).
- `last_tested` defaults to `YYYY-MM-DD` (date picker friendly). Touching merges with existing custom fields by default; `overwrite=True` replaces the list. Default `testcase_type` is `Security Test Case`.
- Evidence FIFO relies on best-effort extraction of file metadata from API responses; live testing will confirm the correct fields.
- Evidence FIFO/dedupe is most reliable when `project_id` is provided (project listings include evidence metadata).
- Evidence uploads default to `keep_last=2` (FIFO, keep most recent). Set `keep_last=None` to disable.
- Finding deduplication compares titles case-insensitively after trimming whitespace.
- `upsert_finding_by_title` enforces asset-agnostic payloads by default; set `validate_asset_agnostic=False` to disable.
- New findings default `custom_fields` substatus to `Observed` (configurable via `ATTACKFORGE_FINDINGS_SUBSTATUS_KEY/VALUE`).
- Newly created vulnerabilities appear under `pendingVulnerabilities=true` in list endpoints for this tenant; dedup + tests include pending results.
- Updating `affected_assets` on vulnerabilities requires `projectId` and entries with either `assetId` or `assetName` (not both).
- Workspace file downloads require the storage name (`full_name`) returned by `GetProjectWorkspace`.
- Project testcase file uploads via SSAPI return status only and do not surface in UI metadata for this tenant. The SDK supports UI uploads (`/api/projects/:projectId/upload/testcase/:testcaseId`) when `ATTACKFORGE_UI_TOKEN` is provided; tests verify visibility via `/api/projects/:projectId/meta/testcase?fk=:testcaseId`.
- Project testcase notes do not have a SSAPI list endpoint. When `dedupe=True`, the SDK queries the UI notes endpoint (`/api/projects/:projectId/testcases/:testcaseId/notes`) if a UI token is provided.
- Testsuite testcase file downloads use `files[].storage_name` returned by `GetTestsuite`.
- Writeup file downloads use `files[].storage_name` returned by `/api/ss/library` when filtered by `name` or `id`.
- Evidence file downloads resolve storage names from `GetProjectVulnerabilities` (`vulnerability_evidence[].storage_name`). If the evidence list is missing, downloads will fail until the SSAPI exposes storage names.
- Remediation note file downloads: SSAPI download endpoint returns HTTP 500 for known files when only original filename/hash is available. A report-data (base64) fallback is used when possible.

## Out Of Scope (explicitly skipped)
- Project requests, retest flows, project emails, and project audit logs.
- Groups, portfolios, analytics, and application audit logs.

## Coverage Matrix

### SDK Helpers
- `ProjectsResource.find_project_by_name` for idempotent project lookups.
- `TestsuitesResource.find_testsuite_by_name` and `get_testsuite_testcases`.
- `TestcasesResource.wait_for_project_testcases`, `build_project_testcase_map`, and linked-vulnerability helpers.
- `FindingsResource.find_project_vulnerability_by_title` and linked-testcase helpers.
- `AttackForgeClient.link_vulnerability_to_testcases` for bidirectional linking with verification.

### Assets
| Endpoint | Method | Path | Notes | Status |
| --- | --- | --- | --- | --- |
| CreateAssetInLibrary | POST | `/api/ss/library/asset` | Create asset in library | Implemented |
| UpdateAssetInLibrary | PUT | `/api/ss/library/asset/:id` | Update asset in library | Implemented |
| GetAssets | GET | `/api/ss/assets` | List assets | Implemented |
| GetAssetInLibrary | GET | `/api/ss/library/asset?id=:id` | Get single library asset | Implemented |
| GetAssetLibraryAssets | POST | `/api/ss/library/assets` | Query assets in library | Implemented |
| GetAssetsByGroup | GET | `/api/ss/assets/group/:id` | Group-scoped assets (group out of scope) | Skipped |

### Projects
| Endpoint | Method | Path | Notes | Status |
| --- | --- | --- | --- | --- |
| CreateProject | POST | `/api/ss/project` | Create project | Implemented |
| GetProjectById | GET | `/api/ss/project/:id` | Get project by id | Implemented |
| GetProjects | GET | `/api/ss/projects` | List projects | Implemented |
| GetProjectsAndVulnerabilities | GET | `/api/ss/projects-and-vulnerabilities` | Combined listing | Implemented |
| UpdateProjectById | PUT | `/api/ss/project/:id` | Update project, includes report fields | Implemented |
| ArchiveProject | PUT | `/api/ss/project/:id/archive` | Archive project | Implemented |
| RestoreProject | PUT | `/api/ss/project/:id/restore` | Restore project | Implemented |
| DestroyProject | DELETE | `/api/ss/project/destroy` | Destroy project | Implemented |
| CloneProject | POST | `/api/ss/project/:id/clone` | Clone project | Implemented |
| CreateScope | POST | `/api/ss/project/:id/assets` | Add assets to scope | Implemented |
| UpdateScope | PUT | `/api/ss/project/:projectId/asset/:assetId` | Update asset in scope | Implemented |
| GetProjectWorkspace | GET | `/api/ss/project/:id/workspace` | Get workspace | Implemented |
| UploadWorkspaceFile | POST | `/api/ss/project/:id/workspace/file` | Upload workspace file | Implemented |
| DownloadWorkspaceFile | GET | `/api/ss/project/:id/workspace/:file` | Download workspace file | Implemented |
| GetProjectNotes | GET | `/api/ss/project/:id/notes` | List project notes | Implemented |
| CreateProjectNote | POST | `/api/ss/project/:id/note` | Create project note | Implemented |
| UpdateProjectNote | PUT | `/api/ss/project/:id/note/:noteId` | Update project note | Implemented |
| CreateProjectWorkspaceNote | POST | `/api/ss/project/:id/workspace/note` | Create workspace note | Implemented |
| UpdateProjectWorkspaceNote | PUT | `/api/ss/project/:id/workspace/note/:noteId` | Update workspace note | Implemented |
| GetProjectMembershipAdministrators | GET | `/api/ss/project/:id/member-admins` | Project membership admins | Implemented |
| AddProjectMembershipAdministrators | POST | `/api/ss/project/{id}/member-admins` | Add membership admins | Implemented |
| UpdateProjectMembershipAdministrators | PUT | `/api/ss/project/{id}/member-admins` | Update membership admins | Implemented |
| RemoveProjectMembershipAdministrators | DELETE | `/api/ss/project/{id}/member-admins` | Remove membership admins | Implemented |
| InviteUserToProject | POST | `/api/ss/project/:id/invite` | Invite user | Implemented |
| InviteUsersToProjectTeam | POST | `/api/ss/project/:id/team/invite` | Invite multiple users | Implemented |
| RemoveProjectTeamMembers | PUT | `/api/ss/project/:id/team/remove` | Remove team members | Implemented |
| UpdateUserAccessOnProject | PUT | `/api/ss/project/:project_id/access/:user_id` | Update project access | Implemented |
| GetProjectsByGroup | GET | `/api/ss/groups/:id/projects` | Group-scoped projects (group out of scope) | Skipped |

### Findings
| Endpoint | Method | Path | Notes | Status |
| --- | --- | --- | --- | --- |
| CreateVulnerability | POST | `/api/ss/vulnerability` | Create finding | Implemented |
| CreateVulnerabilityBulk | POST | `/api/ss/vulnerability/bulk` | Bulk create | Implemented |
| CreateVulnerabilityWithLibrary | POST | `/api/ss/vulnerability-with-library` | Create from writeup | Implemented |
| GetVulnerabilities | GET | `/api/ss/vulnerabilities` | List vulnerabilities | Implemented |
| GetVulnerabilityById | GET | `/api/ss/vulnerability/:id` | Get vulnerability | Implemented |
| GetProjectVulnerabilitiesById | GET | `/api/ss/project/:id/vulnerabilities` | List project vulnerabilities | Implemented |
| GetVulnerabilitiesByAssetName | GET | `/api/ss/vulnerabilities/asset` | List by asset | Implemented |
| GetVulnerabilitiesByGroup | GET | `/api/ss/groups/:id/vulnerabilities` | Group-scoped vulnerabilities (group out of scope) | Skipped |
| UpdateVulnerabilityById | PUT | `/api/ss/vulnerability/:id` | Update finding | Implemented |
| UpdateVulnerabilityWithLibrary | PUT | `/api/ss/vulnerability-with-library/:vulnerabilityId` | Update from writeup | Implemented |
| UpdateVulnerabilitySLAs | PUT | `/api/ss/vulnerabilities/sla` | SLA updates | Implemented |
| UpdateLinkedProjectsOnVulnerabilities | PUT | `/api/ss/vulnerabilities/projects` | Cross-project linking | Implemented |
| GetVulnerabilityRevisionHistory | GET | `/api/ss/vulnerability/:id/revision-history` | Revision history | Implemented |
| UploadVulnerabilityEvidence | POST | `/api/ss/vulnerability/:id/evidence` | Evidence upload | Implemented |
| DeleteVulnerabilityEvidence | DELETE | `/api/ss/vulnerability/:id/evidence/:file` | Evidence delete | Implemented |

### Writeups
| Endpoint | Method | Path | Notes | Status |
| --- | --- | --- | --- | --- |
| GetVulnerabilityLibraryIssues | GET | `/api/ss/library` | List writeups | Implemented |
| CreateVulnerabilityLibraryIssue | POST | `/api/ss/library/vulnerability` | Create writeup | Implemented |
| UpdateVulnerabilityLibraryIssue | PUT | `/api/ss/library/:id` | Update writeup | Implemented |
| UploadVulnerabilityLibraryFile | POST | `/api/ss/library/:id/file` | Upload writeup file | Implemented |
| DownloadVulnerabilityLibraryFile | GET | `/api/ss/library/:id/file/:file` | Download writeup file | Implemented |

### Testcases
| Endpoint | Method | Path | Notes | Status |
| --- | --- | --- | --- | --- |
| CreateProjectTestCase | POST | `/api/ss/project/:id/testcase` | Create testcase | Implemented |
| GetProjectTestcasesById | GET | `/api/ss/project/:id/testcases` | List testcases | Implemented |
| UpdateTestcase | PUT | `/api/ss/project/:projectId/testcase/:testcaseId` | Update testcase | Implemented |
| CreateTestcaseNote | POST | `/api/ss/project/:projectId/testcase/:testcaseId/note` | Create testcase note | Implemented |
| UploadTestcaseFile | POST | `/api/ss/project/:projectId/testcase/:testcaseId/file` | Upload testcase file | Implemented |
| DownloadProjectTestCaseFile | GET | `/api/ss/project/:projectId/testcase/:testcaseId/file/:fileName` | Download testcase file | Implemented |
| DownloadProjectTestCaseNoteFile | GET | `/api/ss/project/:projectId/testcase-note/:testcaseNoteId/file/:fileName` | Download testcase note file | Implemented |
| DownloadProjectTestCaseWorkspaceNoteFile | GET | `/api/ss/project/:projectId/testcase-workspace-note/:testcaseWorkspaceNoteId/file/:fileName` | Download testcase workspace note file | Implemented |

### Testsuites
| Endpoint | Method | Path | Notes | Status |
| --- | --- | --- | --- | --- |
| CreateTestsuite | POST | `/api/ss/testsuite` | Create testsuite | Implemented |
| GetTestsuites | GET | `/api/ss/testsuites` | List testsuites | Implemented |
| GetTestsuiteById | GET | `/api/ss/testsuites/:id` | Get testsuite | Implemented |
| UpdateTestsuite | PUT | `/api/ss/testsuite/:id` | Update testsuite | Implemented |
| AddTestcaseToTestsuite | POST | `/api/ss/testsuite/:id/testcase` | Add testcase to testsuite | Implemented |
| AddTestcasesToTestsuite | POST | `/api/ss/testsuite/:id/testcases` | Add multiple testcases | Implemented |
| UpdateTestcaseOnTestsuite | PUT | `/api/ss/testsuite/:testsuite_id/testcase/:testcase_id` | Update testcase in testsuite | Implemented |
| UploadTestSuiteTestCaseFile | POST | `/api/ss/testsuites/:testsuiteId/testcase/:testcaseId/file` | Upload testsuite testcase file | Implemented |
| DownloadTestSuiteTestCaseFile | GET | `/api/ss/testsuites/:testsuiteId/testcase/:testcaseId/file/:file` | Download testsuite testcase file | Implemented |

### Notes
| Endpoint | Method | Path | Notes | Status |
| --- | --- | --- | --- | --- |
| CreateRemediationNote | POST | `/api/ss/vulnerability/:vulnerabilityId/remediationNote` | Create remediation note | Implemented |
| UpdateRemediationNote | PUT | `/api/ss/vulnerability/:vulnerabilityId/remediationNote/:remediationNoteId` | Update remediation note | Implemented |
| UploadRemediationNoteFile | POST | `/api/ss/vulnerability/:vulnerabilityId/remediationNote/:remediationNoteId/file` | Upload remediation note file | Implemented |
| DownloadRemediationNoteFile | GET | `/api/ss/vulnerability/:vulnerabilityId/remediationNote/:remediationNoteId/file/:fileName` | Download remediation note file | Implemented |

### Users
| Endpoint | Method | Path | Notes | Status |
| --- | --- | --- | --- | --- |
| CreateUser | POST | `/api/ss/user` | Create user | Implemented |
| CreateUsers | POST | `/api/ss/users` | Bulk create users | Implemented |
| GetUserById | GET | `/api/ss/users/:id` | Get user | Implemented |
| GetUsers | GET | `/api/ss/users` | List users | Implemented |
| GetUserByEmail | GET | `/api/ss/users/email/:email` | Get by email | Implemented |
| GetUserByUsername | GET | `/api/ss/users/username/:username` | Get by username | Implemented |
| UpdateUser | PUT | `/api/ss/user/:id` | Update user | Implemented |
| ActivateUser | PUT | `/api/ss/user/:id/activate` | Activate user | Implemented |
| DeactivateUser | PUT | `/api/ss/user/:id/deactivate` | Deactivate user | Implemented |
| AddUserToGroup | POST | `/api/ss/group/user` | Add user to group | Implemented |
| UpdateUserAccessOnGroup | PUT | `/api/ss/group/user/:user_id` | Update access on group | Implemented |
| GetUserGroups | GET | `/api/ss/user/:id/groups` | User groups | Implemented |
| GetUserProjects | GET | `/api/ss/user/:id/projects` | User projects | Implemented |
| GetUserAuditLogs | GET | `/api/ss/user/:id/auditlogs` | User audit logs | Implemented |
| GetUserLoginHistory | GET | `/api/ss/user/:id/logins` | User login history | Implemented |
| InviteUserToProject | POST | `/api/ss/project/:id/invite` | Invite user to project | Implemented |
| InviteUsersToProjectTeam | POST | `/api/ss/project/:id/team/invite` | Invite users to team | Implemented |
| UpdateUserAccessOnProject | PUT | `/api/ss/project/:project_id/access/:user_id` | Update access on project | Implemented |

### Reports
| Endpoint | Method | Path | Notes | Status |
| --- | --- | --- | --- | --- |
| GetProjectReport | GET | `/api/ss/project/:id/report/:type` | Report output | Implemented |
| GetProjectReportData | POST | `/api/ss/project/:id/report/:type` | Report output with filter body | Implemented |
| UpdateExecSummaryNotes | PUT | `/api/ss/project/:projectId/execSummaryNotes` | Executive summary notes | Implemented |
| UpdateProjectById (report fields) | PUT | `/api/ss/project/:id` | Executive summary + reporting/summary custom fields | Implemented |
