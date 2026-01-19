# GetProjectsByGroup

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojectsbygroup

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectsByGroup

This method can be used for the following functionality: Get details for all projects for a group this user is a member of.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/groups/:id/projects HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Identifier for the group.

Example:

Copy

```
GET /api/ss/groups/5e6880f33e6d520a26fef4b0/projects HTTP/1.1
```

**cf\_key\_allowlist (string) (optional)**

List of custom field keys to include in response. Add multiple for more than one key e.g. `?cf_key_allowlist=key1&cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?cf_key_allowlist=`

Example:

**cf\_key\_blocklist (string) (optional)**

List of custom field keys to exclude from response. Add multiple for more than one key e.g. `?cf_key_blocklist=key1&cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get all projects for a group.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of project objects.

[PreviousGetProjectsAndVulnerabilitieschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getprojectsandvulnerabilities)[NextGetProjectMembershipAdministratorschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojectmembershipadministrators)

Last updated 4 months ago
