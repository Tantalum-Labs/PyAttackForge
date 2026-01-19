# GetProjectTestcasesById

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojecttestcases

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectTestcasesById

This method can be used for the following functionality: Get all testcases for a project you have access to, by project identifier (Id).

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/project/:id/testcases HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Identifier for the project.

Example:

Copy

```
GET /api/ss/project/5e64179c899bb708b55ea48c/testcases HTTP/1.1
```

**status (string) (optional)**

Test case status. Must be one of the following: Tested, Not-Tested, In-Progress, Not-Applicable

Example:

**project\_testcase\_cf\_key\_allowlist (string) (optional)**

List of Project Test Case custom field keys to include in response. Add multiple for more than one key e.g. `?project_testcase_cf_key_allowlist=key1&project_testcase_cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?project_testcase_cf_key_allowlist=`

Example:

**project\_testcase\_cf\_key\_blocklist (string) (optional)**

List of Project Test Case custom field keys to exclude from response. Add multiple for more than one key e.g. `?project_testcase_cf_key_blocklist=key1&project_testcase_cf_key_blocklist=key2`

Example:

**testcase\_cf\_key\_allowlist (string) (optional)**

List of Test Case custom field keys to include in response. Add multiple for more than one key e.g. `?testcase_cf_key_allowlist=key1&testcase_cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?testcase_cf_key_allowlist=`

Example:

**testcase\_cf\_key\_blocklist (string) (optional)**

List of Test Case custom field keys to exclude from response. Add multiple for more than one key e.g. `?testcase_cf_key_blocklist=key1&testcase_cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get all Tested test cases on a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of test case objects.

[PreviousGetProjectRequestByIdchevron-left](/attackforge-enterprise/modules/self-service-restful-api/getprojectrequestbyid)[NextGetProjectVulnerabilitiesByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojectvulnerabilities)

Last updated 27 days ago
