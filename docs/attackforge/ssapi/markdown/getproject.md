# GetProjectById

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getproject

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectById

This method can be used for the following functionality: Get details for a project user has access to, by project identifier (Id).

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/project/:id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Identifier for the project.

Example:

Copy

```
GET /api/ss/project/5e48c12ec0376309d73aad71 HTTP/1.1
```

**project\_cf\_key\_allowlist (string) (optional)**

List of Project custom field keys to include in response. Add multiple for more than one key e.g. `?project_cf_key_allowlist=key1&project_cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?project_cf_key_allowlist=`

Example:

**project\_cf\_key\_blocklist (string) (optional)**

List of Project custom field keys to exclude from response. Add multiple for more than one key e.g. `?project_cf_key_blocklist=key1&project_cf_key_blocklist=key2`

Example:

**project\_reporting\_cf\_key\_allowlist (string) (optional)**

List of Project Reporting custom field keys to include in response. Add multiple for more than one key e.g. `?project_reporting_cf_key_allowlist=key1&project_reporting_cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?project_reporting_cf_key_allowlist=`

Example:

**project\_reporting\_cf\_key\_blocklist (string) (optional)**

List of Project Reporting custom field keys to exclude from response. Add multiple for more than one key e.g. `?project_reporting_cf_key_blocklist=key1&project_reporting_cf_key_blocklist=key2`

Example:

**project\_summary\_cf\_key\_allowlist (string) (optional)**

List of Project Summary custom field keys to include in response. Add multiple for more than one key e.g. `?project_summary_cf_key_allowlist=key1&project_summary_cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?project_summary_cf_key_allowlist=`

Example:

**project\_summary\_cf\_key\_blocklist (string) (optional)**

List of Project Summary custom field keys to exclude from response. Add multiple for more than one key e.g. `?project_summary_cf_key_blocklist=key1&project_summary_cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get a project by its identifier (Id).

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a project object.

[PreviousGetProjectAuditLogschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getprojectauditlogs)[NextGetProjectschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojects)

Last updated 27 days ago
