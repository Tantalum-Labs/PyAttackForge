# CreateScope

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/createscope

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CreateScope

This method can be used for the following functionality: Create new assets on a project that you have Edit access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/assets HTTP/1.1
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
POST /api/ss/project/5e7c29afa3362408cf502a11/assets HTTP/1.1
```

**assets (array of strings)**

Assets to create on the project.

Example:

**asset\_library\_ids (*****array of strings*****) (*****optional*****)**

Asset libraries to map scope against.

Example:

## [hashtag](#example) Example

The following example is a cURL request to create new assets on a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an array of created asset objects.

[PreviousCreateRemediationNotechevron-left](/attackforge-enterprise/modules/self-service-restful-api/createremediationnote)[NextCreateTestcaseNotechevron-right](/attackforge-enterprise/modules/self-service-restful-api/createtestcasenote)

Last updated 2 years ago
