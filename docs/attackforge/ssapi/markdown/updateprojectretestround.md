# UpdateProjectRetestRound

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateprojectretestround

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateProjectRetestRound

This method can be used for the following functionality: Update a project retesting round.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/project/:projectId/retest/:retestRoundNumber HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**projectId (string)**

Identifier for the project.

Example:

Copy

```
PUT /api/ss/project/5e8017d2e1385f0c58e8f4f8/retest/:retestRoundNumber HTTP/1.1
```

**retestRoundNumber (string)**

Number for the project retest round.

Example:

**requested\_date (string) (optional)**

Requested datetime for the project retest round. Must be an ISO8601 datetime string.

Example:

**completed\_date (string) (optional)**

Completed datetime for the project retest round. Must be an ISO8601 datetime string.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a project retest round.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status object.

[PreviousUpdateProjectRequestByIdchevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateprojectrequest)[NextUpdateProjectWorkspaceNotechevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateprojectworkspacenote)

Last updated 9 months ago
