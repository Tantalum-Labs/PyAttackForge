# DownloadRemediationNoteFile

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/downloadremediationnotefile

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# DownloadRemediationNoteFile

This method can be used for the following: Download a remediation note file.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/vulnerability/:vulnerabilityId/remediationNote/:remediationNoteId/file/:fileName HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**vulnerabilityId (*****string*****)**

Identifier for the vulnerability.

Example:

Copy

```
GET /api/ss/vulnerability/5f63de24fa1c9208d3e140b0/remediationNote/:remediationNoteId/file/:fileName HTTP/1.1
```

**remediationNoteId (*****string*****)**

Identifier for the remediation note.

Example:

**fileName (string)**

Storage name for the file.

Example:

## [hashtag](#example) Example

The following example is a cURL request to get a file on a remediation note.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains binary data. If using curl, use option --output to save the binary response as a file e.g.

[PreviousDownloadProjectTestCaseWorkspaceNoteFilechevron-left](/attackforge-enterprise/modules/self-service-restful-api/downloadprojecttestcaseworkspacenotefile)[NextDownloadTestSuiteTestCaseFilechevron-right](/attackforge-enterprise/modules/self-service-restful-api/downloadtestsuitetestcasefile)

Last updated 1 month ago
