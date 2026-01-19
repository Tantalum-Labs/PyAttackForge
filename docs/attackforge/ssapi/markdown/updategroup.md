# UpdateGroup

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updategroup

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateGroup

This method can be used for the following functionality: Update an existing group.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/group/:id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Id of the group.

Example:

Copy

```
PUT /api/ss/group/5eab99471e18050942c7607a HTTP/1.1
```

**name (string) (optional)**

Name of the group.

Example:

**group\_owner (string) (optional)**

Name of the owner for the group.

Example:

**primary\_contact\_name (string) (optional)**

Primary contact person name.

Example:

**primary\_contact\_number (string) (optional)**

Primary contact person number.

Example:

**primary\_contact\_email (string) (optional)**

Primary contact person email.

Example:

**is\_deleted (boolean) (optional)**

Whether group is deleted or not.

Example:

**custom\_fields (*****array of objects*****) (*****optional*****)**

Custom fields. Must include a key and value. Key must be unique and letters, number and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

**access** ***(object) (optional)***

Access details.

* sso\_1.action - must be either upsert or remove
* sso\_1.project\_access\_level - must be either none, view, upload or edit
* sso\_1.project\_request\_access\_level - must be either none, view, upload or edit
* member\_admins.action - must be either upsert or remove
* member\_admins.user\_id - specify either user\_id or group\_id but not both
* member\_admins.group\_id - specify either group\_id or user\_id but not both
* member\_admins.project\_limit - must be either none, view, upload or edit
* member\_admins.project\_request\_limit - must be either none, view, edit or action
* member\_admins.add\_user\_method - must be either list or email

Example:

**auto\_add\_project\_request** ***(boolean)***

Project requests created by group members will be automatically added to the group. Access to the project request can be configured for each group member in the members section.

Example:

**enable\_project\_team\_notification** ***(boolean)***

Group members will receive team notifications configured on a Project.

Example:

## [hashtag](#example) Example

The following example is a cURL request to update a group.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousUpdateFormConfigchevron-left](/attackforge-enterprise/modules/self-service-restful-api/updateformconfig)[NextUpdatePortfoliochevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateportfolio)

Last updated 3 months ago
