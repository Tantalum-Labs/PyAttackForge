# UpdateUserAccessOnGroup

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateuseraccessongroup

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateUserAccessOnGroup

This method can be used for the following functionality: Update a user's access on a group.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/group/user/:user_id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**group\_id (string)**

Id of the group.

Example:

Copy

```
{
   "group_id": "..."
}
```

**user\_id (string)**

Id of the user.

Example:

**access\_level (string)**

Default access level to all group projects. Must be one of the following: View, Upload, Edit, Delete. If you select Delete the user will be removed from the group and all group projects.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a users' access to Edit for all group projects.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUpdateTestsuitechevron-left](/attackforge-enterprise/modules/self-service-restful-api/updatetestsuite)[NextUpdateUserAccessOnProjectchevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateuseraccessonproject)

Last updated 5 years ago
