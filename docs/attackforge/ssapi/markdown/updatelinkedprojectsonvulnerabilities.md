# UpdateLinkedProjectsOnVulnerabilities

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updatelinkedprojectsonvulnerabilities

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateLinkedProjectsOnVulnerabilities

This method can be used for the following functionality: Update linked projects on vulnerabilities.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#access) Access

This API can only be used by **Administrators**.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/vulnerabilities/projects HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#body) Body

The body supplied must be a list of link objects:

Copy

```
{
  "links": [
    {
      "projectId": "64b500641f57624e0d52063e",
      "vulnerabilityId": "68096c7e53dba8b392978423",
      "action": "link"
    }
  ]
}
```

**projectId**

Project Id for the project to link/unlink the vulnerability.

Example:

**vulnerabilityId**

Vulnerability Id for the vulnerability to link/unlink.

Example:

**action**

Must be either *link* or *unlink.*

Example:

## [hashtag](#example) Example

The following example is a cURL request to link a vulnerability to a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a result or error.

[PreviousUpdateVulnerabilitySLAschevron-left](/attackforge-enterprise/modules/self-service-restful-api/updatevulnerabilityslas)[NextUpdateVulnerabilityWithLibrarychevron-right](/attackforge-enterprise/modules/self-service-restful-api/updatevulnerabilitywithlibrary)

Last updated 6 months ago
