# UploadTestcaseFile

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/uploadtestcasefile

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UploadTestcaseFile

This method can be used for the following: Upload a file on a test case for a project user has Edit access to;

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:projectId/testcase/:testcaseId/file HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**projectId (*****string*****)**

Identifier for the project.

Example:

Copy

```
POST /api/ss/project/62d647d9fac9fe3ad1cf5b23/testcase/:testcaseId/file HTTP/1.1
```

**testcaseId (*****string*****)**

Identifier for the test case.

Example:

**file (*****multipart/form-data*****)**

Multipart/form-data for the file to be uploaded.

## [hashtag](#example) Example

The following example is a cURL request to upload a file 'evidence.png' to a test case on a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUploadRemediationNoteFilechevron-left](/attackforge-enterprise/modules/self-service-restful-api/uploadremediationnotefile)[NextUploadTestSuiteTestCaseFilechevron-right](/attackforge-enterprise/modules/self-service-restful-api/uploadtestsuitetestcasefile)

Last updated 1 month ago
