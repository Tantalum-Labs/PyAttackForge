# UpdateTestsuite

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updatetestsuite

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateTestsuite

This method can be used for the following functionality: Update a test suite.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/testsuite/:id HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (*****string*****)**

Id of the test suite.

Example:

Copy

```
PUT /api/ss/testsuite/5eac95f1e594ea09107e9bb5 HTTP/1.1
```

**name (*****string*****) (*****optional*****)**

Name of the test suite.

Example:

**description (*****string*****) (*****optional*****)**

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

**tags (*****array of strings*****) (*****optional*****)**

Tags for the test suite.

Example:

**is\_deleted (*****boolean*****) (*****optional*****)**

Whether test suite is deleted or not.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a test suite.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUpdateTestcaseOnTestsuitechevron-left](/attackforge-enterprise/modules/self-service-restful-api/updatetestcaseontestsuite)[NextUpdateUserAccessOnGroupchevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateuseraccessongroup)

Last updated 9 months ago
