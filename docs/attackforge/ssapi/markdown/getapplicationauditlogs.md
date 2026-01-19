# GetApplicationAuditLogs

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getapplicationauditlogs

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetApplicationAuditLogs

This method can be used for the following: Get exportable audit logs for the application.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/auditlogs HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**skip (integer) (optional)**

Number of records to skip. Default is index of the last log entry previously returned.

Example:

Copy

```
GET /api/ss/auditlogs?skip=10 HTTP/1.1
```

**limit (integer) (optional)**

Number of records to limit to. Default limit is 5000. Max limit is 5000.

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

The following example is a cURL request to get exportable application audit logs since last request/fetch.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of logs.

[PreviousDownloadWorkspaceFilechevron-left](/attackforge-enterprise/modules/self-service-restful-api/downloadworkspacefile)[NextGetAssetschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getassets)

Last updated 1 year ago
