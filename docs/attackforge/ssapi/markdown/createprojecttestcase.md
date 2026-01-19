# CreateProjectTestCase

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/createprojecttestcase

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CreateProjectTestCase

This method can be used for the following functionality: Create a new Project Test Case

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/testcase HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**testcase (string)**

Name of the test case. For example, "Test for XYZ".

Example:

Copy

```
{
   "testcase": "..."
}
```

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

The following example is a cURL request to create a new project request.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a project request object.

[PreviousCreateProjectRequestchevron-left](/attackforge-enterprise/modules/self-service-restful-api/createprojectrequest)[NextCreateProjectWorkspaceNotechevron-right](/attackforge-enterprise/modules/self-service-restful-api/createprojectworkspacenote)

Last updated 1 year ago
