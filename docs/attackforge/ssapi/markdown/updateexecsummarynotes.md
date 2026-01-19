# UpdateExecSummaryNotes

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateexecsummarynotes

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateExecSummaryNotes

This method can be used for the following functionality: Update executive summary notes on a project that this user must have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/project/:projectId/execSummaryNotes HTTP/1.1
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
PUT /api/ss/project/5e7c29afa3362408cf502a11/execSummaryNotes HTTP/1.1
```

**exec\_summary\_notes (string)**

Executive summary notes.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update the executive summary notes on a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUpdateAssetInLibrarychevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateassetinlibrary)[NextUpdateFormConfigchevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateformconfig)

Last updated 5 years ago
