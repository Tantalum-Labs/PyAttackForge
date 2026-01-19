# ADVANCED QUERY FILTER

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filter

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# ADVANCED QUERY FILTER

## [hashtag](#vulnerabilities) Vulnerabilities

### [hashtag](#q-filter) q= Filter

Query Filter (q=) is used to select the exact data set you would like the API to return. The filter works similar to a database query, where you can specify fields & operators - these help to narrow down the results to the data you would need. This filter is only supported for selected API endpoints. Please check the documentation for each endpoint for more details.

### [hashtag](#examples-for-querying-vulnerabilities) Examples for querying vulnerabilities:

#### [hashtag](#example-1-critical-or-high-vulnerabilities-only) Example 1 - Critical or High vulnerabilities only:

Copy

```
curl -G -X GET 'https://localhost:3000/api/ss/vulnerabilities' --data-urlencode 'q_vulnerability={ priority: { $in: ["Critical", "High" ] } }' -H 'Host: localhost:3000' -H 'X-SSAPI-KEY: ********' -H 'Content-Type: application/json' -H 'Connection: close'
```

#### [hashtag](#example-2-open-critical-or-open-high-vulnerabilities-only) Example 2 - Open Critical or Open High vulnerabilities only:

Copy

```
curl -G -X GET 'https://localhost:3000/api/ss/vulnerabilities' --data-urlencode 'q_vulnerability={ $and: [ { priority: { $in: [ "Critical", "High" ] } }, { status: { $eq: "Open" } } ] }' -H 'Host: localhost:3000' -H 'X-SSAPI-KEY: ********' -H 'Content-Type: application/json' -H 'Connection: close'
```

#### [hashtag](#example-3-critical-or-high-ready-for-retest-vulnerabilities-only) Example 3 - Critical or High Ready for Retest vulnerabilities only:

Copy

```
curl -G -X GET 'https://localhost:3000/api/ss/vulnerabilities' --data-urlencode 'q_vulnerability={ $and: [ { priority: { $in: [ "Critical", "High" ] } }, { is_retest: { $eq: "Yes" } } ] }' -H 'Host: localhost:3000' -H 'X-SSAPI-KEY: ********' -H 'Content-Type: application/json' -H 'Connection: close'
```

#### [hashtag](#example-4-critical-or-high-vulnerabilities-discovered-in-last-24-hours) Example 4 - Critical or High vulnerabilities discovered in last 24 hours:

Copy

```
curl -G -X GET 'https://localhost:3000/api/ss/vulnerabilities' --data-urlencode 'q_vulnerability={ $and: [ { priority: { $in: [ "Critical" ] } }, { status: { $eq: "Open" } }, { created: { $gte: datetime("now", "-1 days") } } ] }' -H 'Host: localhost:3000' -H 'X-SSAPI-KEY: ********' -H 'Content-Type: application/json' -H 'Connection: close'
```

### [hashtag](#examples-for-querying-writeups) Examples for querying writeups:

#### [hashtag](#example-5-writeups-with-title-sql-injection) Example 5 - Writeups with title *SQL Injection*:

#### [hashtag](#example-6-writeups-with-the-tag-pluginid-53360) Example 6 - Writeups with the tag *pluginID:53360*:

#### [hashtag](#example-7-writeups-with-the-custom-field-nessusid-and-value-53360) Example 7 - Writeups with the custom field *NessusID* and value *53360*:

### [hashtag](#operators) Operators

Query Filter supports the following operators:

**$and**

Can be used to AND two or more conditions.

*Example:* Filter vulnerabilities which are Open and Critical

**$or**

Can be used to OR two or more conditions.

*Example:* Filter vulnerabilities which are Critical or High

**$eq**

Used to check that a field is equal to a value. A value can be a string, boolean, number, null or a function.

*Example:* Filter vulnerabilities which are Critical

**$ne**

Used to check that a field is not equal to a value. A value can be a string, boolean, number, null or a function.

*Example:* Filter vulnerabilities which are not Informational

**$in**

Used to check that a value exists in a list. Supports an array of values.

*Example:* Filter vulnerabilities which have a tag 'OWASP Top 10' (Top 10 Vulnerability)

**$nin**

Used to check that a value does not exist in a list. Supports an array of values.

*Example:* Filter vulnerabilities which do not have a tag 'OWASP Top 10' (Not a Top 10 Vulnerability)

**$gt**

Used to check that a field is greater than a value. Supports strings, numbers and functions.

*Example:* Filter vulnerabilities which have a likelihood of exploitation greater than 7

**$gte**

Used to check that a field is greater than or equal to a value. Supports strings, numbers and functions.

*Example:* Filter vulnerabilities which have a likelihood of exploitation greater than or equal to 7

**$lt**

Used to check that a field is less than a value. Supports strings, numbers and functions.

*Example:* Filter vulnerabilities which have a likelihood of exploitation less than 7

**$lte**

Used to check that a field is less than or equal to a value. Supports strings, numbers and functions.

*Example:* Filter vulnerabilities which have a likelihood of exploitation less than or equal to 7

#### [hashtag](#usdregex) $regex

Used to perform a regular expression for a field. Support Javascript regular expressions.

*Example:* Filter vulnerabilities which have SQL in the title, using a case insensitive search.

#### [hashtag](#usdelemmatch) $elemMatch

This operator matches documents that contain an array field with at least one element that matches all the specified query criteria.

*Example:* Filter vulnerabilities by a specific custom field name and value.

#### [hashtag](#usdall) $all

This operator selects the documents where the value of a field is an array that contains all the specified elements.

*Example:* Filter vulnerabilities which both CWE-520 and Web App in the tags.

### [hashtag](#functions) Functions

The following functions are currently supported:

* datetime()

#### [hashtag](#datetime-timevalue-modifiers) datetime(timeValue, modifiers)

datetime can be used to construct a date & time and then modify it (if needed).

* timeValue - must be either:

  + now
  + YYYY-MM-DD
  + YYYY-MM-DD HH:MM
* modifiers - must be either:

  + +999 years
  + -999 years
  + +999 months
  + -999 months
  + +999 days
  + -999 days
  + +999 hours
  + -999 hours
  + +999 minutes
  + -999 minutes
  + start of year
  + start of month
  + start of day

Example 1: Filter vulnerabilities created greater than June 1st, 2022.

Example 2: Filter vulnerabilities created greater than UTC 12:00 on June 1st, 2022.

Example 3: Filter vulnerabilities created greater than 7 days ago.

Example 4: Filter vulnerabilities with SLA greater than 7 days from now.

Example 5: Filter vulnerabilities with SLA greater than 7 days + 1 year from now. Multiple modifiers will execute in order i.e. add 7 days, then add 1 year.

### [hashtag](#vulnerability-fields) Vulnerability Fields

The following fields are supported in filters for the 'Vulnerability' type:

**id**

The id for the vulnerability.

*Example:* get vulnerability with id 62a190f7793b8ccd085e0d9d

**alternate\_id**

The alternateid for the vulnerability (set by the vulnerability code on the project).

*Example:* get vulnerability with alternate id GLOBEX-1

**created**

The created datefor the vulnerability.

*Example:* get vulnerabilities which have been created in the past 7 days.

**modified**

The modified datefor the vulnerability.

*Example:* get vulnerabilities which have been modified in the past 7 days.

**priority**

The priority for the vulnerability.Supports Critical, High, Medium, Low & Info.

*Example:* get vulnerabilities which are Critical.

**title**

The title for the vulnerability.

*Example:* get vulnerabilities which have SQL in the title.

**zero\_day**

Whether the vulnerability is a zero day or not. Supports Yes or No.

*Example:* get vulnerabilities which are a zero day.

**likelihood\_of\_exploitation**

The likelihood of exploitation for a vulnerability. Supports 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.

*Example:* get vulnerabilities which have a likelihood of exploitation greater than or equal to 7.

**status**

The status for the vulnerability. Supports Open or Closed.

*Example:* get all open vulnerabilities.

**status\_updated**

The date when the status was last updated for the vulnerability.

*Example:* get vulnerabilities which have had their status change in the past 7 days.

**is\_retest**

Whether the vulnerability is flagged for retesting or not. Supports Yes or No.

*Example:* get vulnerabilities which are currently flagged for retesting.

**sla**

The SLA datefor the vulnerability.

*Example:* get open vulnerabilities which have exceeded/breached their assigned SLA by 7 days.

**target\_remediation\_date**

The target remediation date for the vulnerability.

*Example:* get open vulnerabilities which have target remediation date exactly 7 days from now.

**release\_date**

The release datefor the vulnerability.

*Example:* get vulnerabilities which have been released in the past 7 days.

**tags**

The tags for the vulnerabilities.

*Example:* get vulnerabilities which have a tag "OWASP Top 10".

**custom\_tags**

The custom tags for the vulnerabilities.

*Example:* get vulnerabilities which have a custom tag "is\_pci" and value "Yes".

**custom\_fields**

The custom fields for the vulnerabilities.

*Example:* get vulnerabilities which have a custom field "qa\_passed" and value "Yes".

### [hashtag](#vulnerability-library-writeup-fields) Vulnerability Library (Writeup) Fields

The following fields are supported in filters for the 'Vulnerability Library' or 'Writeup' type:

**id**

The id for the vulnerability library writeup.

*Example:* get writeup with id 62a190f7793b8ccd085e0d9d

**created**

The created datefor the vulnerability library writeup.

*Example:* get writeups which have been created in the past 7 days.

**modified**

The modified datefor the vulnerability library writeup.

*Example:* get writeups which have been modified in the past 7 days.

**priority**

The priority for the writeup.Supports Critical, High, Medium, Low & Info.

*Example:* get writeups which are Critical.

**title**

The title for the writeup.

*Example:* get writeups which have SQL in the title.

**description**

Description of writeup.

*Example:* get writeups which have SQL in the description.

#### [hashtag](#attack_scenario) attack\_scenario

Attack Scenario for writeup.

*Example:* get writeups which have SQL in the attack scenario.

#### [hashtag](#remediation_recommendation) remediation\_recommendation

Remediation recommendation for writeup.

*Example:* get writeups which have SQL in the recommendation.

**severity**

The severity for the writeup.Supports 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

*Example:* get writeups which have a severity greater than or equal to 7.

**likelihood\_of\_exploitation**

The likelihood of exploitation for a vulnerability. Supports 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.

*Example:* get vulnerabilities which have a likelihood of exploitation greater than or equal to 7.

**category**

The category for the vulnerability.

*Example:* get all writeups with category *Web App*

#### [hashtag](#impact_on_confidentiality) impact\_on\_confidentiality

The confidentiality rating for the writeup.

*Example:* get all writeups with confidentiality rating of *High*

#### [hashtag](#impact_on_integrity) impact\_on\_integrity

The integrity rating for the writeup.

*Example:* get all writeups with integrity rating of *High*

#### [hashtag](#impact_on_availability) impact\_on\_availability

The availability rating for the writeup.

*Example:* get all writeups with availability rating of *High*

#### [hashtag](#import_source) import\_source

The import source for the writeups.

*Example:* get writeups which have an import source of *Nessus*

#### [hashtag](#import_source_id) import\_source\_id

The import source id for the writeups.

*Example:* get writeups which have an import source id of *53360*

#### [hashtag](#tags) **tags**

The tags for the writeups.

*Example:* get writeups which have a tag *pluginID:53360*

**custom\_tags**

The custom tags for the writeups.

*Example:* get writeups which have a custom tag "is\_pci" and value "Yes".

**custom\_fields**

The custom fields for the writeups.

*Example:* get writeups which have a custom field "NessusID" and value "53360".

### [hashtag](#project-fields) Project Fields

The following fields are supported in filters for the 'Project' type:

**id**

The id for the project.

*Example:* get project with id 62a190f7793b8ccd085e0d9d

**created**

The created datefor the project.

*Example:* get projects which have been created in the past 7 days.

**modified**

The modified datefor the project.

*Example:* get projects which have been modified in the past 7 days.

**name**

The name of the project.

*Example:* get projects with the name "ACME Corp".

**code**

The code for the project.

*Example:* get projects which have "9999" in the code.

**start\_date**

The start datefor the project.

*Example:* get projects which have a start date in the past 7 days. NOTE: You must specify "isostring" at the end for this field.

**end\_date**

The end datefor the project.

*Example:* get projects which have a end date in the past 7 days. NOTE: You must specify "isostring" at the end for this field.

**group\_names**

Group names associated to the project.

*Example:* get projects with the group "ACME Developers" associated.

#### [hashtag](#status) status

Status of the project. Must be either "Waiting to Start", "Testing", "On-Hold", "Overrun", "Retest", "Completed".

*Example:* get Completed projects.

#### [hashtag](#org_code) org\_code

Organization code for the project.

*Example:* get projects with "ACME1" in the org code.

**vuln\_code**

The vulnerability code for the project.

*Example:* get projects which have a vulnerability code of "ACME18".

**custom\_tags**

The custom tags for the project.

*Example:* get projects which have a custom tag "is\_pci" and value "Yes".

**custom\_fields**

The custom fields for the project.

*Example:* get projects which have a custom field "exported\_to\_jira" and value "No".

### [hashtag](#asset-fields) Asset Fields

The following fields are supported in filters for the 'Asset' type:

**id**

The id for the asset.

*Example:* get asset with id 62a190f7793b8ccd085e0d9d

**created**

The created datefor the asset.

*Example:* get assets which have been created in the past 7 days.

**modified**

The modified datefor the asset.

*Example:* get assets which have been modified in the past 7 days.

**name**

The name of the asset.

*Example:* get assets with the name "ACME Corp".

**type**

The type of the asset.

*Example:* get assets with the type "Web App".

**details**

The details of the asset.

*Example:* get assets with "Used for XYZ" in the details.

**external\_id**

The external Id of the asset.

*Example:* get assets with the external Id "SNOW-123".

**asset\_library\_keys**

A list of asset library keys. Use this to query assets in libraries.

You can retrieve the key for a asset library from the URL when viewing the asset library.

*Example:* get assets in a library with the library key "662f1bafcdd044fcc3e4e28d".

**custom\_fields**

The custom fields for the asset.

*Example:* get assets which have a custom field "from\_cmdb" and value "SNOW".

[PreviousEXPORTING TO CSVchevron-left](/attackforge-enterprise/modules/self-service-restful-api/exporting-to-csv)[NextActivateUserchevron-right](/attackforge-enterprise/modules/self-service-restful-api/activateuser)

Last updated 1 year ago
