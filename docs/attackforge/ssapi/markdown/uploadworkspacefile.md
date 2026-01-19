# UploadWorkspaceFile

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/uploadworkspacefile

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UploadWorkspaceFile

This method can be used for the following: Upload a file to the workspace for a project user has Upload or Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/workspace/file HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

#### [hashtag](#id-string) **id (*****string*****)**

Project Id.

Example:

Copy

```
POST /api/ss/project/620f1707c66ef8821d35ee17/workspace/file HTTP/1.1
```

#### [hashtag](#file-multipart-form-data) **file (*****multipart/form-data*****)**

Multipart/form-data for the file to be uploaded.

## [hashtag](#example) Example

The following example is a cURL request to upload a file 'solution-design.docx' to a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUploadVulnerabilityLibraryFilechevron-left](/attackforge-enterprise/modules/self-service-restful-api/uploadvulnerabilitylibraryfile)[NextSelf-Service Events APIchevron-right](/attackforge-enterprise/modules/self-service-events-api)

Last updated 3 years ago
