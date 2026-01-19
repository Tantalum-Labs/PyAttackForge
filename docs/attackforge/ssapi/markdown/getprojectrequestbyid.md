# GetProjectRequestById

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojectrequestbyid

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectRequestById

This method can be used for the following: Get details for a project request you have access to, by project request identifier (Id).

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/request/:id HTTP/1.1
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
GET /api/ss/request/5e8017d2e1385f0c58e8f4f8 HTTP/1.1
```

**cf\_key\_allowlist (string) (optional)**

List of custom field keys to include in response. Add multiple for more than one key e.g. `?cf_key_allowlist=key1&cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?cf_key_allowlist=`

Example:

**cf\_key\_blocklist (string) (optional)**

List of custom field keys to exclude from response. Add multiple for more than one key e.g. `?cf_key_blocklist=key1&cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get a project request by its identifier (Id).

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a project request object.

## [hashtag](#undefined)

[PreviousGetProjectRequestschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getprojectrequest)[NextGetProjectTestcasesByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojecttestcases)

Last updated 27 days ago
