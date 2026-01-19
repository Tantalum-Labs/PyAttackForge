# GetProjectAuditLogs

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojectauditlogs

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectAuditLogs

This method can be used for the following functionality: Get audit logs for a project.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/project/:id/auditlogs HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Id of the project.

Example:

Copy

```
GET /api/ss/project/5e7c29afa3362408cf502a11/auditlogs HTTP/1.1
```

**skip (integer) (optional)**

Number of records to skip. Default is 0 (do not skip any records).

Example:

**limit (integer) (optional)**

Number of records to limit to. Default limit is 100. Max limit is 500.

Example:

**include\_request\_body (boolean) (optional)**

Whether to include HTTP request body or not. Defaults to false.

Example:

**endpoint (string) (optional)**

Filter logs by an endpoint. For list of endpoint names, please contact AttackForge Support.

Example:

**method (string) (optional)**

Filter logs by a HTTP request method. Must be either of DELETE, GET, PATCH, POST, PUT

Example:

## [hashtag](#example) Example

The following example is a cURL request to get last 500 audit logs for a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of logs.

[PreviousGetPortfolioStreamchevron-left](/attackforge-enterprise/modules/self-service-restful-api/getportfoliostream)[NextGetProjectByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getproject)

Last updated 1 year ago
