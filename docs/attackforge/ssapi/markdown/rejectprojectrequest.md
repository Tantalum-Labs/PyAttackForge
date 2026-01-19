# RejectProjectRequestById

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/rejectprojectrequest

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# RejectProjectRequestById

This method can be used for the following functionality: Reject a project request, by project request identifier (Id).

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/request/:id/reject HTTP/1.1
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
PUT /api/ss/request/5e8017d2e1385f0c58e8f4f8/reject HTTP/1.1
```

**reason (string)**

Include a reason why project has been rejected.

Example:

## [hashtag](#example) Example

The following example is a cURL request to reject a project request.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a result object.

[PreviousMarkdownToRichTextchevron-left](/attackforge-enterprise/modules/self-service-restful-api/markdowntorichtext)[NextRegenerateAPIKeychevron-right](/attackforge-enterprise/modules/self-service-restful-api/regenerateapikey)

Last updated 2 years ago
