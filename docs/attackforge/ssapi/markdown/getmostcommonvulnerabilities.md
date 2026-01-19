# GetMostCommonVulnerabilities

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getmostcommonvulnerabilities

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetMostCommonVulnerabilities

This method can be used for the following functionality: Get details for the most common vulnerabilities this user has access to. This method allows to use optional filter.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/analytics/common/vulnerabilities HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**limit (integer) (optional)**

Limit how many vulnerabilities to return. Must be an integer e.g. 10.

Example:

Copy

```
GET /api/ss/analytics/common/vulnerabilities?limit=10 HTTP/1.1
```

**startDate (string) (optional)**

Start date to query vulnerabilities from. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**endDate (string) (optional)**

End date to query vulnerabilities to. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

## [hashtag](#example) Example

The following example is a cURL request to get Top 10 most common vulnerabilities between 1st January 2020 to 1st February 2020.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of vulnerability objects.

[PreviousGetGroupschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getgroups)[NextGetMostFailedTestcaseschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getmostfailedtestcases)

Last updated 2 years ago
