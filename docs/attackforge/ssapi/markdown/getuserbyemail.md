# GetUserByEmail

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getuserbyemail

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetUserByEmail

This method can be used for the following: Get details for a user, searching by email address;

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/users/email/:email HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**email (*****string*****)**

Email address of the user.

Example:

Copy

```
GET /api/ss/users/email/[email protected] HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to get a user by email.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a user object.

[PreviousGetTestsuiteschevron-left](/attackforge-enterprise/modules/self-service-restful-api/gettestsuites)[NextGetUserByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getuser)

Last updated 3 years ago
