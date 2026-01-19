# UpdateTestcase

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updatetestcase

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateTestcase

This method can be used for the following functionality: Update a testcase on a project that this user must have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/project/:projectId/testcase/:testcaseId HTTP/1.1
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
PUT /api/ss/project/5e7c29afa3362408cf502a11/testcase/:testcaseId HTTP/1.1
```

**testcaseId (string)**

Id of the testcase.

Example:

**testcase (string) (optional)**

Name of the test case. For example, "Test for XYZ".

Example:

**assigned\_to\_user (string) (optional)**

User Id to assign test case to.

Example:

**assigned\_to\_assets** **(array of strings) (optional)**

Project scope assets to assign test case to.

Example:

**status (string) (optional)**

Status of the test case. Must match exactly one of the following: *Tested, Testing In Progress, Not Tested, Not Applicable*

Example:

**linked\_vulnerabilities (array of strings) (optional)**

Vulnerability Ids to link to test case.

Example:

**code (string) (optional)**

Test case code.

Example:

**details (string) (optional)**

Test case details. Supports limited HTML for styling.

Example:

**execution\_flow (array of objects) (optional)**

Test case execution flow. Details supports limited HTML for styling.

Example:

**tags (array of strings) (optional)**

Test case tags.

Example:

**sort\_order (integer) (optional)**

Sort order when viewing testing case in the user interface.

Example:

**project\_testcase\_custom\_fields (array of objects) (optional)**

Custom fields. Must include a key and value. Key must be unique and letters, number and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

**testcase\_custom\_fields (array of objects) (optional)**

Custom fields. Must include a key and value. Key must be unique and letters, number and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a testcase on a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUpdateScopechevron-left](/attackforge-enterprise/modules/self-service-restful-api/updatescope)[NextUpdateTestcaseOnTestsuitechevron-right](/attackforge-enterprise/modules/self-service-restful-api/updatetestcaseontestsuite)

Last updated 1 year ago
