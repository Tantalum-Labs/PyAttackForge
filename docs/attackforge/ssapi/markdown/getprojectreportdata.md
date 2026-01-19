# GetProjectReportData

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojectreportdata

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectReportData

This method can be used for the following: Get details in a reporting format for a project you have access to - including project vulnerabilities, test cases and other reporting data;

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/report/:type HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

#### [hashtag](#id-string) **id (*****string*****)**

Identifier for the project.

Example:

Copy

```
GET /api/ss/project/5e48c12ec0376309d73aad71/report/:type HTTP/1.1
```

#### [hashtag](#type-string) **type (*****string*****)**

Type of report. This must be one of the following: *raw, csv*

Example:

#### [hashtag](#excludebinaries-boolean) **excludeBinaries (*****boolean*****)**

Exclude binaries from the response object. Only applies to type *raw*.

Example:

**vulnerabilityIds (string array) (optional)**

Ids for the vulnerabilities to scope the report to.

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

**group\_cf\_key\_allowlist (string) (optional)**

List of Group custom field keys to include in response. Add multiple for more than one key e.g. `?group_cf_key_allowlist=key1&group_cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?group_cf_key_allowlist=`

Example:

**group\_cf\_key\_blocklist (string) (optional)**

List of Group custom field keys to exclude from response. Add multiple for more than one key e.g. `?group_cf_key_blocklist=key1&group_cf_key_blocklist=key2`

Example:

**project\_testcase\_cf\_key\_allowlist (string) (optional)**

List of Project Test Case custom field keys to include in response. Add multiple for more than one key e.g. `?project_testcase_cf_key_allowlist=key1&project_testcase_cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?project_testcase_cf_key_allowlist=`

Example:

**project\_testcase\_cf\_key\_blocklist (string) (optional)**

List of Project Test Case custom field keys to exclude from response. Add multiple for more than one key e.g. `?project_testcase_cf_key_blocklist=key1&project_testcase_cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get a raw report by the project id.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a body. For RAW reports, the body is in JSON format.

## [hashtag](#example-1) Example

The following example is a cURL request to get a csv report by the project id.

### [hashtag](#request-1) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response-1) Response

Response contains a body. For CSV reports, the body is in CSV format. Using cURL, save the output with > filename.csv

The following vulnerability fields are returned in the CSV:

* **Status** - Open / Ready for Retest / Closed
* **Priority**- Critical / High / Medium / Low / Info
* **Vulnerability** - vulnerability title
* **Affected Targets** - asset name
* **Likelihood Of Exploitation** - 1-10
* **Zeroday** - Yes / No
* **Description** - description for the vulnerability
* **Attack Scenario** - attack scenario for the vulnerability
* **Recommendation** - remediation recommendation for the vulnerability
* **Notes** - array of notes e.g. [{"note":"..."}]
* **Proof of Concept** - steps to reproduce the vulnerability
* **Tags** - array of strings e.g. ["tag 1", "tag 2", ...]
* **ReportGen Tags** - array of ReportGen tags e.g. [{"name":"...", "value":"..."}]
* **Custom Fields** - array of custom fields e.g. [{"name":"...", "value":"..."}]

[PreviousGetProjectReportchevron-left](/attackforge-enterprise/modules/self-service-restful-api/getprojectreport)[NextGetProjectRequestschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojectrequest)

Last updated 1 month ago
