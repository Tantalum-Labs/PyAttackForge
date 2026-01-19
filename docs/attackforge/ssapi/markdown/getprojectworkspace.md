# GetProjectWorkspace

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getprojectworkspace

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetProjectWorkspace

This method can be used for the following: Get project workspaces notes and uploaded files and logs meta data for a project you have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/project/:id/workspace HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Identifier for the project.

Example:

Copy

```
GET /api/ss/project/5f63de24fa1c9208d3e140b0/workspace HTTP/1.1
```

## [hashtag](#example) Example

The following example is a cURL request to get a project workspace by the project id.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a workspace object.

[PreviousGetProjectVulnerabilitiesByIdchevron-left](/attackforge-enterprise/modules/self-service-restful-api/getprojectvulnerabilities)[NextGetTestsuiteByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/gettestsuite)

Last updated 28 days ago
