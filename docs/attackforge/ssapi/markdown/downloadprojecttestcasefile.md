# DownloadProjectTestCaseFile

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/downloadprojecttestcasefile

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# DownloadProjectTestCaseFile

This method can be used for the following: Download a project test case file.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/project/:projectId/testcase/:testcaseId/file/:fileName HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**projectId (string)**

Identifier for the project.

Example:

Copy

```
GET /api/ss/project/5f5ebf3b31ff1d08c1e5fa91/testcase/:testcaseId/file/:fileName HTTP/1.1
```

**testcaseId (string)**

Identifier for the test case.

Example:

**fileName (string)**

Storage name for the file.

Example:

## [hashtag](#example) Example

The following example is a cURL request to get a file on a project test case.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains binary data. If using curl, use option --output to save the binary response as a file e.g.

[PreviousDestroyProjectchevron-left](/attackforge-enterprise/modules/self-service-restful-api/destroyproject)[NextDownloadProjectTestCaseNoteFilechevron-right](/attackforge-enterprise/modules/self-service-restful-api/downloadprojecttestcasenotefile)

Last updated 10 months ago
