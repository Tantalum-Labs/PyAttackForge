# UpdateProjectWorkspaceNote

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateprojectworkspacenote

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateProjectWorkspaceNote

This method can be used for the following: Update existing workspace note on a project that you have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/project/:id/workspace/note/:noteId HTTP/1.1
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
PUT /api/ss/project/5f63de24fa1c9208d3e140b0/workspace/note/:noteId HTTP/1.1
```

**noteId (string)**

Id of the note.

Example:

**title (string) (optional)**

Title of the note.

Example:

**details (string) (optional)**

Details of the note.

Example:

**details\_type (string) (optional)**

Must be either PLAINTEXT or RICHTEXT. Defaults to PLAINTEXT if not specified.

Example:

**assets (array of strings) (optional)**

Asset IDs for each asset on the project which is linked to the note.

Example:

**is\_deleted (boolean) (optional)**

Whether note is deleted or not.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update an existing workspace note for a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a result.

[PreviousUpdateProjectRetestRoundchevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateprojectretestround)[NextUpdateRemediationNotechevron-right](/attackforge-enterprise/modules/self-service-restful-api/createremediationnote-1)

Last updated 2 years ago
