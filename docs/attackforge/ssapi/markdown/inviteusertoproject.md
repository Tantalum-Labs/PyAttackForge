# InviteUserToProject

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/inviteusertoproject

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# InviteUserToProject

This method can be used for the following functionality: Invite a user to a project, by the project Id and username.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/project/:id/invite HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Project Id.

Example:

Copy

```
{
   "id": "..."
}
```

**username (string)**

Username or email address for the user you are inviting to the project.

Example:

**accessLevel (string)**

Access level to assign to the user for the specified project. Must be either View, Upload or Edit.

Example:

**role (string) (optional)**

Collaboration role to assign to the user. Must be one of the following options: *Not Assigned, Client, Consultant, Pentester, Pentest Lead, Security Manager, Project Manager, Executive, Business Owner, Developer, Engineer, Architect, Red Team, Blue Team, SOC*

Example:

## [hashtag](#example) Example

The following example is a cURL request to add a user to a specified project.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a result object.

[PreviousGetVulnerabilityRevisionHistorychevron-left](/attackforge-enterprise/modules/self-service-restful-api/getvulnerabilityrevisionhistory)[NextInviteUsersToProjectTeamchevron-right](/attackforge-enterprise/modules/self-service-restful-api/inviteuserstoprojectteam)

Last updated 11 months ago
