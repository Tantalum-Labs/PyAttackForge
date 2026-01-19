# DeactivateUser

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/deactivateuser

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# DeactivateUser

This method can be used for the following functionality: Deactivate a user on AttackForge.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/user/:id/deactivate HTTP/1.1
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
PUT /api/ss/user/5eacb8450c8d520a8281e539/deactivate HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to deactivate a user.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousCreateVulnerabilityWithLibrarychevron-left](/attackforge-enterprise/modules/self-service-restful-api/createvulnerabilitywithlibrary)[NextDestroyProjectchevron-right](/attackforge-enterprise/modules/self-service-restful-api/destroyproject)

Last updated 5 years ago
