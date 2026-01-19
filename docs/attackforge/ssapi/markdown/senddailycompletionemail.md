# SendDailyCompletionEmail

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/senddailycompletionemail

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# SendDailyCompletionEmail

This method can be used for the following functionality: Send daily completion email to project team for a project that this user must have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/project/:id/sendDailyCompletionEmail HTTP/1.1
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
GET /api/ss/project/5e7c29afa3362408cf502a11/sendDailyCompletionEmail HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to send daily project commencement email to project team.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousSendDailyCommencementEmailchevron-left](/attackforge-enterprise/modules/self-service-restful-api/senddailycommencementemail)[NextUpdateAssetInLibrarychevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateassetinlibrary)

Last updated 5 years ago
