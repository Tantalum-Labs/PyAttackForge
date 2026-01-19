# GetUserLoginHistory

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getuserloginhistory

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetUserLoginHistory

This method can be used for the following functionality: Get login history for a user.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/user/:id/logins HTTP/1.1
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
GET /api/ss/user/5d5b27734a83a708c46f4748/logins HTTP/1.1
```

**skip (integer) (optional)**

Number of records to skip. Skip starts from last record created. Default is 0.

Example:

**limit (integer) (optional)**

Number of records to return. Default is 100.

Example:

## [hashtag](#example) Example

The following example is a cURL request to get last 500 logins for a user.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of logs.

[PreviousGetUserGroupschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getusergroups)[NextGetUserProjectschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getuserprojects)

Last updated 5 years ago
