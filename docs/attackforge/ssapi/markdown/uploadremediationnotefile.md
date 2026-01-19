# UploadRemediationNoteFile

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/uploadremediationnotefile

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UploadRemediationNoteFile

This method can be used for the following: Upload a file on a remediation note user has Edit access to;

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/vulnerability/:vulnerabilityId/remediationNote/:remediationNoteId/file HTTP/1.1
Host: localhost:3000
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
POST /api/ss/vulnerability/5f63de24fa1c9208d3e140b0/remediationNote/:remediationNoteId/file HTTP/1.1
```

**remediationNoteId (*****string*****)**

Identifier for the remediation note.

Example:

**file (*****multipart/form-data*****)**

Multipart/form-data for the file to be uploaded.

## [hashtag](#example) Example

The following example is a cURL request to upload a file 'screenshot.png' to a remediation note on a vulnerability.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUpdateVulnerabilityWithLibrarychevron-left](/attackforge-enterprise/modules/self-service-restful-api/updatevulnerabilitywithlibrary)[NextUploadTestcaseFilechevron-right](/attackforge-enterprise/modules/self-service-restful-api/uploadtestcasefile)

Last updated 1 month ago
