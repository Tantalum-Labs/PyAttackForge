# UpdateFormConfig

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateformconfig

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateFormConfig

This method can be used for the following: Update form configuration for a type;

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/config/form/:type HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

#### [hashtag](#type-string) **type (*****string*****)**

Update configuration options for a particular type. Must be one of the following: *project, project-request, vulnerability, writeup, test-case, project-test-case, project-summary, project-reporting, group, asset-entity, portfolio*

Example:

Copy

```
PUT /api/ss/config/form/vulnerability HTTP/1.1
```

#### [hashtag](#config-array-of-objects) **config (*****array of objects*****)**

## [hashtag](#example) Example

The following example is a cURL request to update custom fields configuration for projects.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status and a list of custom field configuration objects.

[PreviousUpdateExecSummaryNoteschevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateexecsummarynotes)[NextUpdateGroupchevron-right](/attackforge-enterprise/modules/self-service-restful-api/updategroup)

Last updated 3 months ago
