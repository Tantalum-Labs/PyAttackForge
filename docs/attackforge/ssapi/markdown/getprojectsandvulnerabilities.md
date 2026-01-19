# GetProjectsAndVulnerabilities

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojectsandvulnerabilities

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectsAndVulnerabilities

This method can be used for the following:

* Get details for all projects (and their vulnerabilities) you have access to, with optional filter;
* This API returns maximum of twenty (20) projects per request. Use skip filter for pagination.
* Returned projects are sorted by created timestamp in descending order, i.e. latest created projects show first.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/projects-and-vulnerabilities
HTTP/1.1Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/jsonConnection: close
```

### [hashtag](#query) Query

**skip (*****number*****) (*****optional*****)**

This API returns maximum of twenty (20) projects per request. Use this filter to adjust starting index for pagination.

Example:

Copy

```
GET /api/ss/projects-and-vulnerabilities?skip=20 HTTP/1.1
```

**created (*****string*****) (*****optional*****)**

Project created date to query projects from. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**altCustomFields (*****boolean*****) (*****optional*****)**

Returns custom fields and custom tags in alternative format.

Example:

Example:

**q\_project (*****string*****) (*****optional*****)**

Provides options to query a custom selection of projects.

Please visit the following link for more details on how to use this filter: [https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filterarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filter)

**q\_vulnerability (*****string*****) (*****optional*****)**

Provides options to query a custom selection of vulnerabilities on the returned projects.

Please visit the following link for more details on how to use this filter: [https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filterarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filter)

**pendingVulnerabilities (*****boolean*****) (*****optional*****)**

Return pending vulnerabilities only.

Example:

**asset\_cf\_key\_allowlist (string) (optional)**

List of Asset custom field keys to include in response. Add multiple for more than one key e.g. `?asset_cf_key_allowlist=key1&asset_cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?asset_cf_key_allowlist=`

Example:

**asset\_cf\_key\_blocklist (string) (optional)**

List of Asset custom field keys to exclude from response. Add multiple for more than one key e.g. `?asset_cf_key_blocklist=key1&asset_cf_key_blocklist=key2`

Example:

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

**vulnerability\_cf\_key\_allowlist (string) (optional)**

List of Vulnerability custom field keys to include in response. Add multiple for more than one key e.g. `?vulnerability_cf_key_allowlist=key1&vulnerability_cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?vulnerability_cf_key_allowlist=`

Example:

**vulnerability\_cf\_key\_blocklist (string) (optional)**

List of Vulnerability custom field keys to exclude from response. Add multiple for more than one key e.g. `?vulnerability_cf_key_blocklist=key1&vulnerability_cf_key_blocklist=key2`

Example:

**writeup\_cf\_key\_allowlist (string) (optional)**

List of Writeup custom field keys to include in response. Add multiple for more than one key e.g. `?writeup_cf_key_allowlist=key1&writeup_cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?writeup_cf_key_allowlist=`

Example:

**writeup\_cf\_key\_blocklist (string) (optional)**

List of Writeup custom field keys to exclude from response. Add multiple for more than one key e.g. `?writeup_cf_key_blocklist=key1&writeup_cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get all projects and their vulnerabilities created since 1st January 2022.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of projects including an array of vulnerabilities for each project.

[PreviousGetProjectschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getprojects)[NextGetProjectsByGroupchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojectsbygroup)

Last updated 27 days ago
