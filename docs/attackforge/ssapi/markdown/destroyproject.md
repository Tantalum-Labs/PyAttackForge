# DestroyProject

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/destroyproject

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# DestroyProject

This method can be used for the following: Destroy project(s) data. WARNING: This is irreversible

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
DELETE /api/ss/project/destroy HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#body) Body

**project\_ids (*****array of strings*****)**

Project Ids for projects to be destroyed.

Example:

Copy

```
{
    "project_ids": [ "689ad06ba798a64475353712" ]
}
```

**keep\_logs (*****boolean*****) (*****optional*****)**

Keep project log files. Logs are removed (false) by default.

Example:

## [hashtag](#example) Example

The following example is a cURL request to destroy a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousDeactivateUserchevron-left](/attackforge-enterprise/modules/self-service-restful-api/deactivateuser)[NextDownloadProjectTestCaseFilechevron-right](/attackforge-enterprise/modules/self-service-restful-api/downloadprojecttestcasefile)

Last updated 5 months ago
