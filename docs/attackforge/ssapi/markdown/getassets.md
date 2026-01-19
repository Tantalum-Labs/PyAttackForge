# GetAssets

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getassets

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetAssets

This method can be used for the following functionality: Get details for all assets user has access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/assets HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**skip (integer) (optional)**

Number of records to skip. Default is 0 (do not skip any records).

Example:

Copy

```
GET /api/ss/assets?skip=10 HTTP/1.1
```

**limit (integer) (optional)**

Number of records to limit to. Default limit is 500. Max limit is 500.

Example:

## [hashtag](#example) Example

The following example is a cURL request to get all assets user has access to.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of asset objects.

[PreviousGetApplicationAuditLogschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getapplicationauditlogs)[NextGetAssetsByGroupchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getassetsbygroup)

Last updated 1 year ago
