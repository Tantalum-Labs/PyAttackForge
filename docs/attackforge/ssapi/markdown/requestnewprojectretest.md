# RequestNewProjectRetest

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/requestnewprojectretest

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# RequestNewProjectRetest

This method can be used for the following functionality: Request a new retest for a project that user has access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/retest/request HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#parameters-1) Parameters

**id (string)**

Id of the project.

Example:

Copy

```
POST /api/ss/project/5e7c29afa3362408cf502a11/retest/request HTTP/1.1
```

**retesting\_window\_start (*****string*****)**

Start date for retest window. Must be ISO8601 datetime e.g. 2025-03-23T00:00:00.000Z.

Example:

**retesting\_window\_end (*****string*****) (*****optional*****)**

End date for retest window. Must be ISO8601 datetime e.g. 2025-03-30T00:00:00.000Z.

Example:

**vulnerability\_ids (*****array of strings*****)**

Project Vulnerability Ids to include in-scope for the retest round. Vulnerabilities must be in 'Retest' status.

Example:

## [hashtag](#example) Example

The following example is a cURL request to request a retest round on a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousRemoveProjectTeamMemberschevron-left](/attackforge-enterprise/modules/self-service-restful-api/removeprojectteammembers)[NextRestoreGroupchevron-right](/attackforge-enterprise/modules/self-service-restful-api/restoregroup)

Last updated 9 months ago
