# SendEmail

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/sendemail

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# SendEmail

This method can be used for the following functionality: Send a custom email.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/email HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**to (string | object)**

Send email To. Must be either an email as a string or an object with one field "user\_id"

Example:

Copy

```
{
   "to": [
      "[email protected]",
      {
        "user_id": "6698cbabba716055c969a658"
      }
    ]
}
```

**cc (string | object)**

CC email to. Must be either an email as a string or an object with one field "user\_id"

Example:

**bcc (string | object)**

BCC email to. Must be either an email as a string or an object with one field "user\_id"

Example:

**subject**

Email subject

Example:

**text**

Email body in plaintext

Example:

**html**

Email body in html

Example:

## [hashtag](#example) Example

The following example is a cURL request to send daily project commencement email to project team.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousRestoreProjectchevron-left](/attackforge-enterprise/modules/self-service-restful-api/restoreproject)[NextSendDailyCommencementEmailchevron-right](/attackforge-enterprise/modules/self-service-restful-api/senddailycommencementemail)

Last updated 11 months ago
