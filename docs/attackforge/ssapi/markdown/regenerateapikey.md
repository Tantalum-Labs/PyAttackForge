# RegenerateAPIKey

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/regenerateapikey

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# RegenerateAPIKey

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/apikey/regenerate HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

## [hashtag](#example) Example

The following example is a cURL request to reject a project request.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

Copy

```
curl -X POST 'https://demo.attackforge.com/api/ss/apikey/regenerate' -H 'Host: demo.attackforge.com' -H 'X-SSAPI-KEY: ***************************************' -H 'Content-Type: application/json' -H 'Connection: close'
```

### [hashtag](#response) Response

Response contains a result object.

[PreviousRejectProjectRequestByIdchevron-left](/attackforge-enterprise/modules/self-service-restful-api/rejectprojectrequest)[NextRemoveProjectMembershipAdministratorschevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateprojectmembershipadministrators)

Last updated 2 years ago
