# CreateUsers

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/createusers

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CreateUsers

This method can be used for the following functionality: Create multiple new users in AttackForge.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/users HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**first\_name (string)**

First name of the user.

Example:

Copy

```
{
   "first_name": "..."
}
```

**last\_name (string)**

Last name of the user.

Example:

**username (string)**

Username of the user. If SSO is enabled, should be username in external identity provider. If SSO is disabled, should be email address.

Example:

**email (string)**

Email address of the user.

Example:

**password (string)**

Password. Should be minimum 15 characters in length.

Example:

**role (string)**

Role of the user. Must be one of the following: admin, librarymod, client, consultant, projectoperator.

Example:

**mfa (string)**

Whether MFA is enabled or disabled for the user. Must be one of the following: Yes, No.

Example:

## [hashtag](#example) Example

The following example is a cURL request to create multiple new users.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of user objects.

[PreviousCreateUserchevron-left](/attackforge-enterprise/modules/self-service-restful-api/createuser)[NextCreateVulnerabilitychevron-right](/attackforge-enterprise/modules/self-service-restful-api/createvulnerability)

Last updated 3 years ago
