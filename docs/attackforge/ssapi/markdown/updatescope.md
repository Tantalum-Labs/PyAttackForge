# UpdateScope

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updatescope

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateScope

This method can be used for the following functionality: Update an asset on a project that this user must have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/project/:projectId/asset/:assetId HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**projectId (string)**

Id of the project.

Example:

Copy

```
PUT /api/ss/project/5e7c29afa3362408cf502a11/asset/:assetId HTTP/1.1
```

**assetId (string)**

Id of the asset.

Example:

**name (string) (optional)**

Name of the asset.

Example:

**is\_deleted (boolean) (optional)**

Delete asset.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update name of an asset.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUpdateRemediationNotechevron-left](/attackforge-enterprise/modules/self-service-restful-api/createremediationnote-1)[NextUpdateTestcasechevron-right](/attackforge-enterprise/modules/self-service-restful-api/updatetestcase)

Last updated 2 years ago
