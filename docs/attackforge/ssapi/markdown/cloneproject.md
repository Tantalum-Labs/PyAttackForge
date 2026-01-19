# CloneProject

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/cloneproject

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CloneProject

This method can be used for the following: Create a new project from an existing project you have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/clone HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (*****string*****)**

Id of the project you are cloning from. You must have access to this project.

Example:

Copy

```
POST /api/ss/project/5e5cbecee365f1003f3b20b8/clone HTTP/1.1
```

**name (*****string*****) (*****optional*****)**

Name of the project. Will default to the cloned project name if not supplied.

Example:

**code (*****string*****) (*****optional*****)**

Project code. Will default to the cloned project code if not supplied.

Example:

**groups (*****array of strings*****) (*****optional*****)**

Groups to link to the project. Must match exact group names or ids. Will default to the cloned project groups if not supplied. Supply an empty list - [] - to link to no groups.

Example:

**startDate (*****string*****)**

Project start date. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**endDate (*****string*****)**

Project end date. Must be UTC string e.g. 2021-06-03T23:15:33.008Z.

Example:

**scoringSystem (*****string*****) (*****optional*****)**

Scoring system to be used on the project. Must be either *Manual* or *CVSSv3.1*. Will default to the cloned project scoring system if not supplied.

Example:

**scope (*****array of strings*****) (*****optional*****)**

Project scope / assets to be tested. Include name of asset or the asset Id if using the assets module. Will default to the cloned project scope if not supplied.

Example:

**asset\_library\_ids (*****array of strings*****) (*****optional*****)**

Asset libraries to map scope against. Only applicable if creating new assets.

Example:

**testsuites (*****array of strings*****) (*****optional*****)**

Test suites to assign to the project. Must match exact testsuite names or ids. Will default to the cloned project test suites if not supplied.

Example:

**organization\_code (*****string*****) (*****optional*****)**

Project organization code. Will default to the cloned project organization code if not supplied. Supply an empty string - "" - to assign no organization code.

Example:

**vulnerability\_code (*****string*****) (*****optional*****)**

Vulnerability code for user friendly vulnerability ids. Must be unique per project, 3-8 characters in length.

Example:

**team\_notifications (*****array of strings*****) (*****optional*****)**

Project team notifications. Must include one or more of the following: *critical*, *high*, *medium*, *low*, *info*, *retest*, *reopened*, *closed*. Will default to the cloned project team notifications if not supplied. Supply an empty list - [] - to set no project team notifications.

Example:

**admin\_notifications (*****array of strings*****) (*****optional*****)**

Admin notifications. Must include one or more of the following: *retest*, *reopened*, *closed*. Will default to the cloned project admin notifications if not supplied. Supply an empty list - [] - to set no admin notifications.

Example:

**start\_stop\_testing\_email (*****string*****) (*****optional*****)**

Email body for daily start & stop testing notifications. Will default to the cloned project email body for daily start & stop testing notifications if not supplied.

Example:

**start\_stop\_testing\_email\_additional\_recipients (*****array of strings*****) (*****optional*****)**

Additional email recipients for daily start & stop testing notifications. Must be a list of email addresses. Will default to the cloned project additional email recipients for daily start & stop testing notifications if not supplied. Supply an empty list - [] - to set no additional email recipients for daily start & stop testing notifications.

Example:

**new\_vulnerability\_email\_type (*****string*****) (*****optional*****)**

Individual or Grouped emails to be sent for new vulnerabilities. Must include one of the following: *individual*, *group*. Will default to the cloned project new vulnerability email type if not supplied.

Example:

**new\_vulnerability\_email (*****string*****) (*****optional*****)**

Email body for new vulnerability discovered notifications. Will default to the cloned project email body for new vulnerability discovered notifications if not supplied.

Example:

**new\_vulnerability\_email\_additional\_recipients (*****array of strings*****) (*****optional*****)**

Additional email recipients for new vulnerability discovered notifications. Must be a list of email addresses. Will default to the cloned project additional email recipients for new vulnerability discovered notifications if not supplied. Supply an empty list - [] - to set no additional email recipients for new vulnerability discovered notifications.

Example:

**forced\_emails (*****array of strings*****) (*****optional*****)**

Force emails to project team. Must include one or more of the following: *all\_emails*, *daily\_start\_stop\_testing*, *new\_critical\_vulnerability*, *new\_high\_vulnerability*, *new\_medium\_vulnerability*, *new\_low\_vulnerability*, *new\_info\_vulnerability*, *vulnerability\_ready\_for\_retesting*, *vulnerability\_reopened*, *vulnerability\_closed*, *project\_role\_updated*, *project\_hold*, *retest\_completed*. Will default to the cloned project forced emails if not supplied. Supply an empty list - [] - to set no forced emails.

Example:

**sla\_activation (*****string*****) (*****optional*****)**

Apply vulnerability SLAs automatically or manually. Must be either "automatic" or "manual". Will default to the cloned project SLA activation option if not supplied.

Example:

**custom\_fields (*****array of objects*****) (*****optional*****)**

Custom fields. Must include a key and value. Key must be unique and letters, numbers and underscores only. Will default to the cloned project custom fields if not supplied. Supply an empty list - [] - to set no custom fields.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

**portfolio\_streams (*****array of objects*****) (*****optional*****)**

Enter a list of Portfolio & Stream Ids to link this project to. Stream must be part of the Portfolio. Will default to the cloned project linked portfolio streams if not supplied. Supply an empty list - [] - to set no linked portfolio streams.

Example:

**features (*****object*****) (*****optional*****)**

Configure features on the project. Roles must be either client, consultant or librarymod. Minimum Project Access Level must be either View, Upload or Edit.

Example:

**pages (*****object*****) (*****optional*****)**

Configure pages on the project. Roles must be either client, consultant or librarymod. Project Access Level must be either View, Upload or Edit.

Example:

**link\_vulnerabilities (*****object*****) (*****optional*****)**

Link vulnerabilities from the cloned project to the new project. You can select vulnerabilities by their remediation status, priority or by providing their ids. Each option will stack i.e. open:true is all open vulnerabilities, open:true + critical:true is all open critical vulnerabilities.

Example:

**options (*****object*****) (*****optional*****)**

Cloning options.

Example:

## [hashtag](#example) Example

The following example is a cURL request to clone a new project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a project object.

[PreviousCancelProjectRetestRoundchevron-left](/attackforge-enterprise/modules/self-service-restful-api/cancelprojectretestround)[NextCompleteProjectRetestRoundchevron-right](/attackforge-enterprise/modules/self-service-restful-api/completeprojectretestround)

Last updated 1 year ago
