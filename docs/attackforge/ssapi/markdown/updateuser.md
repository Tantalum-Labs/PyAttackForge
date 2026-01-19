# UpdateUser

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateuser

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateUser

This method can be used for the following functionality: Update a users' details.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/user/:id HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (*****string*****)**

Id of the user.

Example:

Copy

```
PUT /api/ss/user/5e5cbecee365f1003f3b20b8 HTTP/1.1
```

**first\_name (*****string*****) (*****optional*****)**

First name of the user.

Example:

**last\_name (*****string*****) (*****optional*****)**

Last name of the user.

Example:

**email\_address (*****string*****) (*****optional*****)**

Email address of the user.

Example:

**username (*****string*****) (*****optional*****)**

Username of the user.

Example:

**is\_deleted (*****boolean*****) (*****optional*****)**

Whether user is deleted or not.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a users' name and email address.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains the updated users' details.

[PreviousUpdateUserAccessOnProjectchevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateuseraccessonproject)[NextUpdateVulnerabilityByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/updatevulnerability)

Last updated 3 years ago
