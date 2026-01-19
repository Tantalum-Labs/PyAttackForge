# GetProjectReport

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojectreport

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectReport

This method can be used for the following: Get details in a reporting format for a project you have access to - including project vulnerabilities, test cases and other reporting data;

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/project/:id/report/:type HTTP/1.1
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

[PreviousGetProjectNoteschevron-left](/attackforge-enterprise/modules/self-service-restful-api/getprojectnotes)[NextGetProjectReportDatachevron-right](/attackforge-enterprise/modules/self-service-restful-api/getprojectreportdata)

Last updated 1 year ago
