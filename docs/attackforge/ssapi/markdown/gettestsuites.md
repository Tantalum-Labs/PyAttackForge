# GetTestsuites

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/gettestsuites

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetTestsuites

This method can be used for the following functionality: Get details for all testsuites.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/testsuites HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

## [hashtag](#example) Example

The following example is a cURL request to get all testsuites.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

Copy

```
curl -X GET 'https://demo.attackforge.com/api/ss/testsuites' -H 'Host: demo.attackforge.com' -H 'X-SSAPI-KEY: ***************************************' -H 'Content-Type: application/json' -H 'Connection: close'
```

### [hashtag](#response) Response

Response contains an array of testsuite objects.

[PreviousGetTestsuiteByIdchevron-left](/attackforge-enterprise/modules/self-service-restful-api/gettestsuite)[NextGetUserByEmailchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getuserbyemail)

Last updated 28 days ago
