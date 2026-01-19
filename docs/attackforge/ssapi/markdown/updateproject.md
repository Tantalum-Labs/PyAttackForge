# UpdateProjectById

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateproject

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateProjectById

This method can be used for the following functionality: Update a project by it's Id.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/project/:id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Project Id.

Example:

Copy

```
PUT /api/ss/project/5eab99471e18050942c7607a HTTP/1.1
```

**created (string) (optional)**

Overwrite the created timestamp for the project. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**name (string) (optional)**

Name of the project.

Example:

**code (string) (optional)**

Project code.

Example:

**groups (array of strings) (optional)**

Groups to link to the project. Must match group IDs.

Example:

**startDate (string) (optional)**

Project start date. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**endDate (string) (optional)**

Project end date. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**scoringSystem (string) (optional)**

Scoring system to be used on the project. Must be either Manual or CVSSv3.1.

Example:

**isOnHold (string) (optional)**

Whether project is currently On-Hold. Must be either Yes or No.

Example:

**isOnHoldReason (string) (optional)**

If project is On-Hold, or is now Off-Hold - include a reason. This will be sent in email to project team informing status change.

Example:

**organization\_code (*****string*****) (*****optional*****)**

Project organization code.

Example:

**vulnerability\_code (*****string*****) (*****optional*****)**

Vulnerability code for user friendly vulnerability ids. Must be unique per project, 3-8 characters in length.

Example:

**team\_notifications (*****array of strings*****) (*****optional*****)**

Project team notifications. Must include one or more of the following: *critical*, *high*, *medium*, *low*, *info*, *retest*, *reopened*, *closed*

Example:

**admin\_notifications (*****array of strings*****) (*****optional*****)**

Admin notifications. Must include one or more of the following: *retest*, *reopened*, *closed*

Example:

**start\_stop\_testing\_email (*****string*****) (*****optional*****)**

Email body for daily start & stop testing notifications.

Example:

**start\_stop\_testing\_email\_additional\_recipients (*****array of strings*****) (*****optional*****)**

Additional email recipients for daily start & stop testing notifications. Must be a list of email addresses.

Example:

**new\_vulnerability\_email\_type (*****string*****) (*****optional*****)**

Individual or Grouped emails to be sent for new vulnerabilities. Must include one of the following: *individual*, *group*. If not specified, default option is *individual*

Example:

**new\_vulnerability\_email (*****string*****) (*****optional*****)**

Email body for new vulnerability discovered notifications.

Example:

**new\_vulnerability\_email\_additional\_recipients (*****array of strings*****) (*****optional*****)**

Additional email recipients for new vulnerability discovered notifications. Must be a list of email addresses.

Example:

**forced\_emails (*****array of strings*****) (*****optional*****)**

Force emails to project team. Must include one or more of the following: *all\_emails*, *daily\_start\_stop\_testing*, *new\_critical\_vulnerability*, *new\_high\_vulnerability*, *new\_medium\_vulnerability*, *new\_low\_vulnerability*, *new\_info\_vulnerability*, *vulnerability\_ready\_for\_retesting*, *vulnerability\_reopened*, *vulnerability\_closed*, *project\_role\_updated*, *project\_hold*, *retest\_completed*

Example:

**sla\_activation (*****string*****) (*****optional*****)**

Apply vulnerability SLAs automatically or manually. Must be either "automatic" or "manual". Automatic is default.

Example:

**executive\_summary (*****string*****) (*****optional*****)**

Executive summary for the reports.

Example:

**custom\_fields (*****array of objects*****) (*****optional*****)**

Custom fields. Must include a key and value. Key must be unique and letters, numbers and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

**reporting\_custom\_fields (*****array of objects*****) (*****optional*****)**

Reporting custom fields. Must include a key and value. Key must be unique and letters, numbers and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

**summary\_custom\_fields (*****array of objects*****) (*****optional*****)**

Summary page custom fields. Must include a key and value. Key must be unique and letters, numbers and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

**portfolio\_streams (*****array of objects*****) (*****optional*****)**

Enter a list of Portfolio & Stream Ids to link this project to. Stream must be part of the Portfolio.

Example:

**features (*****object*****) (*****optional*****)**

Configure features on the project. Roles must be either client, consultant or librarymod. Minimum Project Access Level must be either View, Upload or Edit.

Example:

**pages (*****object*****) (*****optional*****)**

Configure pages on the project. Roles must be either client, consultant or librarymod. Project Access Level must be either View, Upload or Edit.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a project by its identifier (Id).

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a project object.

[PreviousUpdatePortfoliochevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateportfolio)[NextUpdateProjectMembershipAdministratorschevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateprojectmembershipadministrators-1)

Last updated 6 months ago
