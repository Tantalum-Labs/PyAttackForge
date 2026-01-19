# UploadTestSuiteTestCaseFile

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/uploadtestsuitetestcasefile

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UploadTestSuiteTestCaseFile

This method can be used for the following: Upload a Test Suite Test Case file;

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/testsuites/:testsuiteId/testcase/:testcaseId/file HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**testsuiteId (*****string*****)**

Identifier for the test suite.

Example:

Copy

```
POST /api/ss/testsuites/5f63de24fa1c9208d3e140b0/testcase/:testcaseId/file HTTP/1.1
```

**testcaseId (*****string*****)**

Identifier for the test case.

Example:

**file (*****multipart/form-data*****)**

Multipart/form-data for the file to be uploaded.

## [hashtag](#example) Example

The following example is a cURL request to upload a file 'evidence.png' to a test case on a test suite.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUploadTestcaseFilechevron-left](/attackforge-enterprise/modules/self-service-restful-api/uploadtestcasefile)[NextUploadVulnerabilityEvidencechevron-right](/attackforge-enterprise/modules/self-service-restful-api/uploadvulnerabilityevidence)

Last updated 2 months ago
