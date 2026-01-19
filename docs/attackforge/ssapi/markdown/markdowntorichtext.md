# MarkdownToRichText

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/markdowntorichtext

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# MarkdownToRichText

This method can be used for the following functionality: Convert data from markdown to rich text.

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/utils/markdown-to-richtext HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#body) Body

**custom\_key (string)**

A user-supplied custom key with a markdown string supplied as the value. Multiple custom key/value pairs can be included within the object.

Example:

Copy

```
{
   "vuln_recommendation": "Proper validation, file type restrictions, size limits, and permission controls are essential to mitigate this vulnerability.\n\nAt this time the only check of file validity seems to be if it ends in '.jpg' (or other image type) and this is easy for an attacker to bypass.\n\nHere are some examples of other validation checks that could be used:\n\n### Validate file MIME type and content (magic bytes):\nCheck the actual file content and signature, not just the extension or the Content-Type header, which can be spoofed.\n\n### Sanitize and validate filenames:\nEnsure filenames do not contain special or dangerous characters (e.g., ../, %00, /, ) to prevent path traversal and overwrite attacks. Set a filename length limit and restrict allowed characters to alphanumeric if possible.\n\n### Rename uploaded files:\nAssign unique, random, or hashed names to uploaded files to prevent overwriting existing files and to obscure file paths from attackers.\n\n### Do not trust client-side validation:\nAlways perform all validation checks server-side, as client-side controls can be bypassed.\n\n\nSee:\nhttps://docs.guidewire.com/security/secure-coding-guidance/file-upload-vulnerabilities/"
}
```

## [hashtag](#example) Example

The following example is a cURL request to convert a custom value from markdown to rich text.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a rich text object.

[PreviousInviteUsersToProjectTeamchevron-left](/attackforge-enterprise/modules/self-service-restful-api/inviteuserstoprojectteam)[NextRejectProjectRequestByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/rejectprojectrequest)

Last updated 3 months ago
