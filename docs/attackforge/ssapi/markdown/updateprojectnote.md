# UpdateProjectNote

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateprojectnote

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateProjectNote

This method can be used for the following: Update existing note on a project that you have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/project/:id/note/:noteId HTTP/1.1
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
PUT /api/ss/project/5f63de24fa1c9208d3e140b0/note/:noteId HTTP/1.1
```

**noteId (string)**

Id of the note.

Example:

**note (string) (optional)**

Details of the note.

Example:

**is\_private (boolean) (optional)**

Whether note is private or not.

Example:

**is\_exported\_to\_report (boolean) (optional)**

Whether note is exported into reports or not.

Example:

**is\_deleted (boolean) (optional)**

Whether note is deleted or not.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update an existing note for a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a result.

[PreviousUpdateProjectMembershipAdministratorschevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateprojectmembershipadministrators-1)[NextUpdateProjectRequestByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateprojectrequest)

Last updated 4 years ago
