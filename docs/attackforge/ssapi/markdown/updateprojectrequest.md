# UpdateProjectRequestById

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateprojectrequest

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateProjectRequestById

This method can be used for the following functionality: Update a project request that you have access to, by project request identifier (Id).

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/request/:id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Identifier for the project request.

Example:

Copy

```
PUT /api/ss/request/5e8017d2e1385f0c58e8f4f8 HTTP/1.1
```

**name (string) (optional)**

Name of the project.

Example:

**code (string) (optional)**

Project code.

Example:

**groups (array of strings) (optional)**

Groups to link to the project. Must match exact group names.

Example:

**scope (array of strings) (optional)**

Project scope / assets to be tested.

Example:

**testsuites (array of strings) (optional)**

Testsuites to assign to the project. Must match exact testsuite names.

Example:

**startDate (string) (optional)**

Desired project start date. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**endDate (string) (optional)**

Desired project end date. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**test\_window (array of strings) (optional)**

Test window for the project. Must be one or more of the following: Weekdays-BusinessHours, Weekdays-NonBusinessHours, Weekends

Example:

**onsite\_testing (string) (optional)**

Whether onsite testing is required or not. Must be one or more of the following: Yes, No

Example:

**reason\_for\_testing (*****string*****) (*****optional*****)**

Reason or justification for testing.

Example:

**organization\_code (*****string*****) (*****optional*****)**

Organization code.

Example:

**custom\_fields (*****array of objects*****) (*****optional*****)**

Custom fields. Must include a key and value. Key must be unique and letters, numbers and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a project request.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a result object.

[PreviousUpdateProjectNotechevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateprojectnote)[NextUpdateProjectRetestRoundchevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateprojectretestround)

Last updated 10 months ago
