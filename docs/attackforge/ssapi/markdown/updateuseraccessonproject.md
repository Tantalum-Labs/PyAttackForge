# UpdateUserAccessOnProject

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateuseraccessonproject

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateUserAccessOnProject

This method can be used for the following functionality: Update a users' access on a project.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/project/:project_id/access/:user_id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**project\_id (string)**

Id of the project.

Example:

Copy

```
PUT /api/ss/project/5e64179c899bb708b55ea48c/access/:user_id HTTP/1.1
```

**user\_id (string)**

Id of the user.

Example:

**update (string)**

Permissions on the project. Must be one of the following: View, Upload, Edit, Delete, Restore. If you select Delete the user will be removed from the project. If you select Restore the user will be restored on the project with prior permissions.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a users' access to Edit on a project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUpdateUserAccessOnGroupchevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateuseraccessongroup)[NextUpdateUserchevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateuser)

Last updated 5 years ago
