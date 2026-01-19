# CompleteProjectRetestRound

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/completeprojectretestround

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CompleteProjectRetestRound

This method can be used for the following functionality: Complete a retest round for a project that user have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/retest/:roundNumber/complete HTTP/1.1
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
POST /api/ss/project/5e7c29afa3362408cf502a11/retest/:roundNumber/complete HTTP/1.1
```

**roundNumber (integer)**

Round number for the retest round.

Example:

## [hashtag](#example) Example

The following example is a cURL request to complete a retest round on a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousCloneProjectchevron-left](/attackforge-enterprise/modules/self-service-restful-api/cloneproject)[NextCreateAssetInLibrarychevron-right](/attackforge-enterprise/modules/self-service-restful-api/createassetinlibrary)

Last updated 9 months ago
