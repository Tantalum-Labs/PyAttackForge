# GetUsers

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getusers

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetUsers

This method can be used for the following functionality: Get details for all users.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/users HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**firstName (string) (optional)**

First name of the user.

Example:

Copy

```
GET /api/ss/users?firstName=John HTTP/1.1
```

**lastName (string) (optional)**

Last name of the user.

Example:

**email (string) (optional)**

Email address of the user.

Example:

**username (string) (optional)**

Username of the user. This is typically the email address unless your tenant is configured otherwise.

Example:

## [hashtag](#example) Example

The following example is a cURL request to get all users with the first name Bob.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of user objects.

[PreviousGetUserProjectschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getuserprojects)[NextGetVulnerabilityByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getvulnerability)

Last updated 5 years ago
