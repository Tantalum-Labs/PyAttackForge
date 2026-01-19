# GetProjectMembershipAdministrators

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojectmembershipadministrators

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectMembershipAdministrators

This method can be used for the following functionality: Get project membership administrators.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/project/:id/member-admins HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#path) Path

**id (string)**

Identifier for the project.

Example:

Copy

```
GET /api/ss/project/5e64179c899bb708b55ea48c/member-admins HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to get all project membership administrators for a given project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of project membership administrator objects.

[PreviousGetProjectsByGroupchevron-left](/attackforge-enterprise/modules/self-service-restful-api/getprojectsbygroup)[NextGetProjectNoteschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojectnotes)

Last updated 10 months ago
