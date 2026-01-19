# UpdateTestcaseOnTestsuite

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updatetestcaseontestsuite

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateTestcaseOnTestsuite

This method can be used for the following functionality: Update a test case on a test suite.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/testsuite/:testsuite_id/testcase/:testcase_id HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**testsuite\_id (*****string*****)**

Id of the test suite.

Example:

Copy

```
PUT /api/ss/testsuite/5eac95f1e594ea09107e9bb5/testcase/:testcase_id HTTP/1.1
```

**testcase\_id (*****string*****)**

Id of the test case.

Example:

**testcase (*****string*****) (*****optional*****)**

Details for the test case.

Example:

**details (*****string*****)**

Details for the test case. Supports rich-text.

Example:

**code (*****string*****) (*****optional*****)**

Code for the test case.

Example:

**sort\_order (*****number*****) (*****optional*****)**

Sort Order to apply to the test case.

Example:

**tags (*****array of strings*****) (*****optional*****)**

Tags for the test case.

Example:

**is\_deleted (*****boolean*****) (*****optional*****)**

Whether test case is deleted or not.

Example:

**execution\_flow (*****array of objects*****) (*****optional*****)**

Execution flows for the test case.

Example:

**custom\_fields (*****array of objects*****) (*****optional*****)**

Custom fields. Must include a key and value. Key must be unique and letters, number and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a test case on a test suite.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUpdateTestcasechevron-left](/attackforge-enterprise/modules/self-service-restful-api/updatetestcase)[NextUpdateTestsuitechevron-right](/attackforge-enterprise/modules/self-service-restful-api/updatetestsuite)

Last updated 2 years ago
