# GetUserByUsername

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getuserbyusername

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetUserByUsername

This method can be used for the following: Get details for a user, searching by username;

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/users/username/:username HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**username (*****string*****)**

Username of the user.

Example:

Copy

```
GET /api/ss/users/username/bruce.wayne HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to get a user by username.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a user object.

[PreviousGetUserByIdchevron-left](/attackforge-enterprise/modules/self-service-restful-api/getuser)[NextGetUserAuditLogschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getuserauditlogs)

Last updated 3 years ago
