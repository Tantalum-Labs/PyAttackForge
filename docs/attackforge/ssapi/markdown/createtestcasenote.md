# CreateTestcaseNote

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/createtestcasenote

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CreateTestcaseNote

This method can be used for the following functionality: Update a testcase on a project that you have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:projectId/testcase/:testcaseId/note HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**projectId (string)**

Id of the project.

Example:

Copy

```
POST /api/ss/project/5e7c29afa3362408cf502a11/testcase/:testcaseId/note HTTP/1.1
```

**assetId (string)**

Id of the testcase.

Example:

**note (string)**

Testcase note.

Example:

**note\_type (string)**

Must be either PLAINTEXT or RICHTEXT. Defaults to PLAINTEXT if not specified.

Example:

## [hashtag](#example) Example

The following example is a cURL request to create a note on a testcase for a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousCreateScopechevron-left](/attackforge-enterprise/modules/self-service-restful-api/createscope)[NextCreateTestsuitechevron-right](/attackforge-enterprise/modules/self-service-restful-api/createtestsuite)

Last updated 2 years ago
