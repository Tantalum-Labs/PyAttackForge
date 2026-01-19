# GetProjects

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojects

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjects

This method can be used for the following functionality: Get details for all projects this user has access to. with optional filter. This method can be used with optional filter.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/projects HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**skip (integer) (optional)**

Number of records to skip. Default is 0 (do not skip any records).

Example:

Copy

```
GET /api/ss/projects?skip=10 HTTP/1.1
```

**limit (integer) (optional)**

Number of records to limit to. Default limit is 500. Max limit is 500.

Example:

**name (string) (optional)**

Name of the project.

Example:

**code (string) (optional)**

Project code.

Example:

**status (string) (optional)**

Status of the project. Must be one of the following: Waiting-to-Start, Testing, Completed, On-Hold

Example:

**startDate (string) (optional)**

Start date to query projects from. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**endDate (string) (optional)**

End date to query projects to. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**asset\_name (*****string*****) (*****optional*****)**

Limit results to projects with scope that has these asset(s). Partial match search. Case insensitive by default.

Example 1 - One asset:

Example 2 - Multiple assets:

Example 3 - Case sensitive:

Example 4 - Exact match:

**q (*****string*****) (*****optional*****)**

Provides options to query a custom selection of projects.

Please visit the following link for more details on how to use this filter: [https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filterarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filter)

**cf\_key\_allowlist (string) (optional)**

List of custom field keys to include in response. Add multiple for more than one key e.g. `?cf_key_allowlist=key1&cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?cf_key_allowlist=`

Example:

**cf\_key\_blocklist (string) (optional)**

List of custom field keys to exclude from response. Add multiple for more than one key e.g. `?cf_key_blocklist=key1&cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get all projects with status 'Testing' which have a test window between 1st January 2020 to 1st February 2020.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of project objects.

[PreviousGetProjectByIdchevron-left](/attackforge-enterprise/modules/self-service-restful-api/getproject)[NextGetProjectsAndVulnerabilitieschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojectsandvulnerabilities)

Last updated 27 days ago
