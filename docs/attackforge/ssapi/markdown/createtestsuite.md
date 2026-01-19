# CreateTestsuite

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/createtestsuite

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CreateTestsuite

This method can be used for the following functionality: Create a new test suite.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/testsuite HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: API
KeyContent-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**name (*****string*****)**

Name of the test suite.

Example:

Copy

```
{   
    "name": "..."
}
```

**description (*****string*****)**

Brief description of the test suite.

Example:

**code (*****string*****) (*****optional*****)**

Code for the test suite.

Example:

**sort\_order (*****number*****) (*****optional*****)**

Sort Order to apply to the test suite.

Example:

**is\_visible\_on\_project\_requests (*****boolean*****) (*****optional*****)**

Whether this test suite should be displayed and made available to be selected when a user is requesting a project.

Example:

**tags (*****array of strings*****)**

Tags for the test suite.

Example:

## [hashtag](#example) Example

The following example is a cURL request to create a new test suite.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousCreateTestcaseNotechevron-left](/attackforge-enterprise/modules/self-service-restful-api/createtestcasenote)[NextCreateUserchevron-right](/attackforge-enterprise/modules/self-service-restful-api/createuser)

Last updated 3 months ago
