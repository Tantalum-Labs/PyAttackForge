# DownloadTestSuiteTestCaseFile

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/downloadtestsuitetestcasefile

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# DownloadTestSuiteTestCaseFile

This method can be used for the following: Download a Test Suite Test Case file.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/testsuites/:testsuiteId/testcase/:testcaseId/file/:file HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**testsuiteId (string)**

Identifier for the test suite.

Example:

Copy

```
GET /api/ss/testsuites/5f63de24fa1c9208d3e140b0/testcase/:testcaseId/file/:file HTTP/1.1
```

**testcaseId (string)**

Identifier for the test case.

Example:

**file (string)**

Storage name for the file.

Example:

## [hashtag](#example) Example

The following example is a cURL request to get a file on a test suite test case.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains binary data. If using curl, use option --output to save the binary response as a file e.g.

[PreviousDownloadRemediationNoteFilechevron-left](/attackforge-enterprise/modules/self-service-restful-api/downloadremediationnotefile)[NextDeleteVulnerabilityEvidencechevron-right](/attackforge-enterprise/modules/self-service-restful-api/downloadvulnerabilityevidence)

Last updated 2 months ago
