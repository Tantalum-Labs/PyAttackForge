# AddUserToGroup

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/addusertogroup

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# AddUserToGroup

This method can be used for the following functionality: Add a user to a group.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/group/user HTTP/1.1
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

Default access level to all group projects. Must be one of the following: View, Upload, Edit

Example:

## [hashtag](#example) Example

The following example is a cURL request to add a user to a group with View access to all group projects.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousAddTestcasesToTestsuitechevron-left](/attackforge-enterprise/modules/self-service-restful-api/addtestcasestotestsuite)[NextApproveProjectRequestByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/approveprojectrequestbyid)

Last updated 10 months ago
