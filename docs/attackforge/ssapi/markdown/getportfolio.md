# GetPortfolio

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getportfolio

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetPortfolio

This method can be used for the following: Get details for a Portfolio.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/portfolio/:id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (*****string*****)**

Identifier for the Portfolio.

Example:

Copy

```
GET /api/ss/portfolio/610647faf01ef1002fe97db9 HTTP/1.1
```

**cf\_key\_allowlist (string) (optional)**

List of custom field keys to include in response. Add multiple for more than one key e.g. `?cf_key_allowlist=key1&cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?cf_key_allowlist=`

Example:

**cf\_key\_blocklist (string) (optional)**

List of custom field keys to exclude from response. Add multiple for more than one key e.g. `?cf_key_blocklist=key1&cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get a Portfolio by its identifier (Id).

### [hashtag](#request) Request

### [hashtag](#response) Response

Response contains a portfolio object.

[PreviousGetMostVulnerableAssetschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getmostvulnerableassets)[NextGetPortfolioschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getportfolios)

Last updated 4 months ago
