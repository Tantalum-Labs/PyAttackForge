# GetPortfolios

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getportfolios

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetPortfolios

This method can be used for the following: Get details for all Portfolios.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/portfolios HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**cf\_key\_allowlist (string) (optional)**

List of custom field keys to include in response. Add multiple for more than one key e.g. `?cf_key_allowlist=key1&cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?cf_key_allowlist=`

Example:

Copy

```
GET /api/ss/portfolios?cf_key_allowlist=key1&cf_key_allowlist=key2 HTTP/1.1
```

**cf\_key\_blocklist (string) (optional)**

List of custom field keys to exclude from response. Add multiple for more than one key e.g. `?cf_key_blocklist=key1&cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get details for all Portfolios.

### [hashtag](#request) Request

### [hashtag](#response) Response

Response contains a list of Portfolio objects.

[PreviousGetPortfoliochevron-left](/attackforge-enterprise/modules/self-service-restful-api/getportfolio)[NextGetPortfolioStreamchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getportfoliostream)

Last updated 4 months ago
