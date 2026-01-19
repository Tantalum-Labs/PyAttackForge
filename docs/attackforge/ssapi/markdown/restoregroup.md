# RestoreGroup

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/restoregroup

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# RestoreGroup

This method can be used for the following: Restore a Group.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/group/:id/restore HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#path) Path

**id (*****string*****)**

Identifier for the Group.

Example:

Copy

```
PUT /api/ss/group/5e8017d2e1385f0c58e8f4f8/restore HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to restore a group.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousRequestNewProjectRetestchevron-left](/attackforge-enterprise/modules/self-service-restful-api/requestnewprojectretest)[NextRestoreProjectchevron-right](/attackforge-enterprise/modules/self-service-restful-api/restoreproject)

Last updated 3 months ago
