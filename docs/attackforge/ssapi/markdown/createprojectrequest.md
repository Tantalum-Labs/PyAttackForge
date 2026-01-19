# CreateProjectRequest

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/createprojectrequest

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CreateProjectRequest

This method can be used for the following functionality: Create a new Request for Project in AttackForge

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/request HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**name (string)**

Name of the project.

Example:

Copy

```
{
   "name": "..."
}
```

**code (string)**

Project code.

Example:

**groups (array of strings) (optional)**

Groups to link to the project. Must match exact group names.

Example:

**scope (array of strings)**

Project scope / assets to be tested.

Example:

**testsuites (array of strings)**

Testsuites to assign to the project. Must match exact testsuite names.

Example:

**startDate (string)**

Desired project start date. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**endDate (string)**

Desired project end date. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**test\_window (array of strings)**

Test window for the project. Must be one or more of the following: Weekdays-BusinessHours, Weekdays-NonBusinessHours, Weekends

Example:

**onsite\_testing (string)**

Whether onsite testing is required or not. Must be one or more of the following: Yes, No

Example:

**reason\_for\_testing (*****string*****) (*****optional*****)**

Reason or justification for testing.

Example:

**organization\_code (*****string*****) (*****optional*****)**

Organization code.

Example:

**custom\_fields (*****array of objects*****) (*****optional*****)**

Custom fields. Must include a key and value. Key must be unique and letters, number and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

## [hashtag](#example) Example

The following example is a cURL request to create a new project request.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a project request object.

[PreviousCreateProjectNotechevron-left](/attackforge-enterprise/modules/self-service-restful-api/createprojectnote)[NextCreateProjectTestCasechevron-right](/attackforge-enterprise/modules/self-service-restful-api/createprojecttestcase)

Last updated 1 year ago
