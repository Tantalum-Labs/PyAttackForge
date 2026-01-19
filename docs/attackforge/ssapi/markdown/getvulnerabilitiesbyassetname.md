# GetVulnerabilitiesByAssetName

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getvulnerabilitiesbyassetname

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetVulnerabilitiesByAssetName

This method can be used for the following functionality: Get details for all vulnerabilities for an asset. This method can be used with optional filter.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/vulnerabilities/asset HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**name (string)**

Name of an asset. For example test.com.

Example:

Copy

```
GET /api/ss/vulnerabilities/asset?name=test.com HTTP/1.1
```

**startDate (string) (optional)**

Start date to query vulnerabilities from, based on creation date. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**endDate (string) (optional)**

End date to query vulnerabilities to, based on creation date. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**priority (string) (optional)**

Priority for vulnerabilities returned. Must be one of the following: Critical, High, Medium, Low, Info

Example:

**skip (integer) (optional)**

Number of records to skip. Default is 0 (do not skip any records).

Example:

**limit (integer) (optional)**

Number of records to limit to. Default limit is 500. Max limit is 500.

Example:

**altCustomFields (*****boolean*****) (*****optional*****)**

Returns custom fields and custom tags in alternative format.

Example:

Example:

**q (*****string*****) (*****optional*****)**

Provides options to query a custom selection of vulnerabilities.

Please visit the following link for more details on how to use this filter: [https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filterarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filter)

Example 1 - Critical or High vulnerabilities only:

Example 2 - Open Critical or Open High vulnerabilities only:

Example 3 - Critical or High Ready for Retest vulnerabilities only:

Example 4 - Critical or High vulnerabilities discovered in last 24 hours:

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

The following example is a cURL request to get all Critical vulnerabilities for asset test.com between 1st January 2020 to 31st December 2020.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of vulnerability objects.

[PreviousGetVulnerabilitieschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getvulnerabilities)[NextGetVulnerabilitiesByGroupchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getvulnerabilitiesbygroup)

Last updated 27 days ago
