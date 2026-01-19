# GetProjectRequests

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojectrequest

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectRequests

This method can be used for the following functionality: Get details for all project requests user has access to. This method can be used with optional filter.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/requests HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**name (string) (optional)**

Name of the project requested.

Example:

Copy

```
GET /api/ss/requests?name=Test Project HTTP/1.1
```

**code (string) (optional)**

Project code.

Example:

**status (string) (optional)**

Status of the request. Must be one of the following: Approved, Rejected, Pending

Example:

**startDate (string) (optional)**

Start date to query requests from. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**endDate (string) (optional)**

End date to query requests to. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**skip (integer) (optional)**

Number of records to skip. Default is 0 (do not skip any records).

Example:

**limit (integer) (optional)**

Number of records to limit to. Default limit is 500. Max limit is 500.

Example:

**cf\_key\_allowlist (string) (optional)**

List of custom field keys to include in response. Add multiple for more than one key e.g. `?cf_key_allowlist=key1&cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?cf_key_allowlist=`

Example:

**cf\_key\_blocklist (string) (optional)**

List of custom field keys to exclude from response. Add multiple for more than one key e.g. `?cf_key_blocklist=key1&cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get all project requests with status 'Pending' which have a desired test window between 1st January 2020 to 31st December 2020.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of project request objects.

[PreviousGetProjectReportDatachevron-left](/attackforge-enterprise/modules/self-service-restful-api/getprojectreportdata)[NextGetProjectRequestByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojectrequestbyid)

Last updated 27 days ago
