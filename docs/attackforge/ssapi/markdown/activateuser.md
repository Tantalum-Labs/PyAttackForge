# ActivateUser

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/activateuser

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# ActivateUser

This method can be used for the following function: Activate a user.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/user/:id/activate HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Contains Id of the user.

Example:

Copy

```
PUT /api/ss/user/5eacb8450c8d520a8281e539/activate HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to activate a user.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousADVANCED QUERY FILTERchevron-left](/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filter)[NextAddProjectMembershipAdministratorschevron-right](/attackforge-enterprise/modules/self-service-restful-api/addprojectmembershipadministrators)

Last updated 5 years ago
