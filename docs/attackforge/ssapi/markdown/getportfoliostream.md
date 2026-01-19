# GetPortfolioStream

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getportfoliostream

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetPortfolioStream

This method can be used for the following: Get details for a Portfolio Stream.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/portfolio/stream/:id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (*****string*****)**

Identifier for the Portfolio Stream.

Example:

Copy

```
GET /api/ss/portfolio/stream/628f82669b462e581754980e HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to get a Portfolio Stream by its identifier (Id).

### [hashtag](#request) Request

### [hashtag](#response) Response

Response contains a portfolio stream object.

[PreviousGetPortfolioschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getportfolios)[NextGetProjectAuditLogschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojectauditlogs)

Last updated 3 years ago
