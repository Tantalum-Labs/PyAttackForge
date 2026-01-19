# AddProjectMembershipAdministrators

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/addprojectmembershipadministrators

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# AddProjectMembershipAdministrators

This method can be used for the following functionality: Add user(s) or group(s) as project membership administrators

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/{id}/member-admins HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#path) Path

**id (*****string*****)**

Id of the project.

Example:

Copy

```
POST /api/ss/project/5eac95f1e594ea09107e9bb5/member-admins HTTP/1.1
```

### [hashtag](#body) **Body**

**group\_id (string)**

Id of the group.

Example:

**user\_id (string)**

Id of the user.

Example:

**access\_level\_limit (string)**

Must be one of the following: None, View, Upload, Edit

Example:

**add\_user\_method (string)**

Defines how user can add other users to the project. Must be one of the following: list, email

Example:

**allow\_user\_invite (boolean)**

Determines if user can invite new users to the application.

Example:

## [hashtag](#example) Example

The following example is a cURL request to add project membership administrators to a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousActivateUserchevron-left](/attackforge-enterprise/modules/self-service-restful-api/activateuser)[NextAddTestcaseToTestsuitechevron-right](/attackforge-enterprise/modules/self-service-restful-api/addtestcasetotestsuite)

Last updated 10 months ago
