# InviteUsersToProjectTeam

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/inviteuserstoprojectteam

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# InviteUsersToProjectTeam

This method can be used for the following functionality: Invite user(s) to a project.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as *mandatory*.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/team/invite 
HTTP/1.1
Host: localhost:3000
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

#### [hashtag](#id-string) **id (*****string*****)**

Project Id.

Example:

Copy

```
POST /api/ss/project/620f1707c66ef8821d35ee17/team/invite HTTP/1.1
```

#### [hashtag](#users-array-of-objects) **users (*****array of objects*****)**

Usernames, email addresses or userIds + access level for the users you are inviting to the project. Access level to assign to the user for the specified project must be either *View*, *Upload* or *Edit*. Collaboration role to assign to the user. Must be one of the following options: *Not Assigned, Client, Consultant, Pentester, Pentest Lead, Security Manager, Project Manager, Executive, Business Owner, Developer, Engineer, Architect, Red Team, Blue Team, SOC*

Example:

## [hashtag](#example) Example

The following example is a cURL request to add multiple users to a specified project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a results array.

### [hashtag](#errors) Errors

Error response will appear as follows.

"user" will contain the data submitted for the user:

When user cannot be found:

When access level is not either *View*, *Upload* or *Edit*:

[PreviousInviteUserToProjectchevron-left](/attackforge-enterprise/modules/self-service-restful-api/inviteusertoproject)[NextMarkdownToRichTextchevron-right](/attackforge-enterprise/modules/self-service-restful-api/markdowntorichtext)

Last updated 2 years ago
