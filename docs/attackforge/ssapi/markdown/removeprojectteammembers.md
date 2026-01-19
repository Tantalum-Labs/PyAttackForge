# RemoveProjectTeamMembers

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/removeprojectteammembers

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# RemoveProjectTeamMembers

This method can be used for the following functionality: Remove user(s) from a project team.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/project/:id/team/remove HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

#### [hashtag](#id-string) **id (*****string*****)**

Project Id.

Example:

Copy

```
PUT /api/ss/project/620f1707c66ef8821d35ee17/team/remove HTTP/1.1
```

#### [hashtag](#users-string-array) **users (*****string array*****)**

Usernames, email addresses or userIds for each user you are removing from the project team.

Example:

## [hashtag](#example) Example

The following example is a cURL request to remove multiple users from a specified project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a results array.

[PreviousRemoveProjectMembershipAdministratorschevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateprojectmembershipadministrators)[NextRequestNewProjectRetestchevron-right](/attackforge-enterprise/modules/self-service-restful-api/requestnewprojectretest)

Last updated 3 years ago
