# GetUserById

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getuser

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetUserById

This method can be used for the following functionality: Get details for a user.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/users/:id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Id of the user.

Example:

Copy

```
GET /api/ss/users/5d5b27734a83a708c46f4748 HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to get a user.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a user object.

[PreviousGetUserByEmailchevron-left](/attackforge-enterprise/modules/self-service-restful-api/getuserbyemail)[NextGetUserByUsernamechevron-right](/attackforge-enterprise/modules/self-service-restful-api/getuserbyusername)

Last updated 5 years ago
