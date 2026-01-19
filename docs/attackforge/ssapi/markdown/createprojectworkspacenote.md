# CreateProjectWorkspaceNote

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/createprojectworkspacenote

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CreateProjectWorkspaceNote

This method can be used for the following: Create new workspace note on a project that you have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/workspace/note HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Id of the project.

Example:

Copy

```
POST /api/ss/project/5f63de24fa1c9208d3e140b0/workspace/note HTTP/1.1
```

**title (string)**

Title of the note.

Example:

**details (string)**

Details of the note.

Example:

**details\_type (string) (optional)**

Must be either PLAINTEXT or RICHTEXT. Defaults to PLAINTEXT if not specified.

Example:

**assets (array of strings) (optional)**

Asset IDs for each asset on the project which is linked to the note.

Example:

## [hashtag](#example) Example

The following example is a cURL request to create a new workspace note for a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a result.

[PreviousCreateProjectTestCasechevron-left](/attackforge-enterprise/modules/self-service-restful-api/createprojecttestcase)[NextCreateRemediationNotechevron-right](/attackforge-enterprise/modules/self-service-restful-api/createremediationnote)

Last updated 2 years ago
