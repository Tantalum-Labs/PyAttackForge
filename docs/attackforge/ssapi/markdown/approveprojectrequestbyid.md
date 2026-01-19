# ApproveProjectRequestById

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/approveprojectrequestbyid

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# ApproveProjectRequestById

This method can be used for the following functionality: Approve a project request, by project request identifier (Id).

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/request/:id/approve HTTP/1.1
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
PUT /api/ss/request/5e8017d2e1385f0c58e8f4f8/approve HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to approve a project request.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a result object.

[PreviousAddUserToGroupchevron-left](/attackforge-enterprise/modules/self-service-restful-api/addusertogroup)[NextArchiveGroupchevron-right](/attackforge-enterprise/modules/self-service-restful-api/archivegroup)

Last updated 3 days ago
