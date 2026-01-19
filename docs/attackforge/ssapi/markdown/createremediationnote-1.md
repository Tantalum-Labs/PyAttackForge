# UpdateRemediationNote

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/createremediationnote-1

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateRemediationNote

This method can be used for the following functionality: Update a remediation note for a vulnerability on a project that you have access to.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/vulnerability/:vulnerabilityId/remediationNote/:remediationNoteId HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**vulnerabilityId (string)**

Id of the vulnerability.

Example:

Copy

```
PUT /api/ss/vulnerability/5e8ee4657be05608d16c2e01/remediationNote/:remediationNoteId HTTP/1.1
```

**remediationNoteId (string)**

Id of the remediation note.

Example:

**note (string)**

Remediation note.

Example:

**note\_type (string) (optional)**

Must be either PLAINTEXT or RICHTEXT. Defaults to PLAINTEXT if not specified.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a remediation note on a vulnerability for a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' ' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUpdateProjectWorkspaceNotechevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateprojectworkspacenote)[NextUpdateScopechevron-right](/attackforge-enterprise/modules/self-service-restful-api/updatescope)

Last updated 1 month ago
