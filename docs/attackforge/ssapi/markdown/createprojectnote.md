# CreateProjectNote

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/createprojectnote

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CreateProjectNote

This method can be used for the following: Create new project note on a project that you have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/note HTTP/1.1
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
POST /api/ss/project/5f63de24fa1c9208d3e140b0/note HTTP/1.1
```

**note (string)**

Details of the note.

Example:

**is\_private (boolean) (optional)**

Whether note is private or not.

Example:

**is\_exported\_to\_report (boolean) (optional)**

Whether note is exported into reports or not.

Example:

## [hashtag](#example) Example

The following example is a cURL request to create a new note for a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a result.

[PreviousCreateProjectchevron-left](/attackforge-enterprise/modules/self-service-restful-api/createproject)[NextCreateProjectRequestchevron-right](/attackforge-enterprise/modules/self-service-restful-api/createprojectrequest)

Last updated 1 year ago
