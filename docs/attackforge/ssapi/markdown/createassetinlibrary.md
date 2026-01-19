# CreateAssetInLibrary

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/createassetinlibrary

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# CreateAssetInLibrary

This method can be used for the following: Create an asset in the library (must have Assets Module enabled in your tenant configuration!);

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/library/asset HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**name (string)**

Name of the asset.

Example:

Copy

```
{
   "name": "..."
}
```

**type (string)**

Type of asset. Must be one of the following: *Web App, API, Mobile, Cloud, Infrastructure, Network, Wifi, Hardware, Other* or another custom type enabled in Global Configuration.

Example:

**external\_id (string) (optional)**

External id for the asset. For example id associated with the asset in Configuration Management Database.

Example:

**asset\_library\_ids (*****array of strings*****) (*****optional*****)**

Asset libraries to map asset against.

Example:

**details (string) (optional)**

Details or notes relating to the asset.

Example:

**groups (array of strings) (optional)**

List of AttackForge Groups to associate the asset with. Must include the Group Id.

Example:

**custom\_fields (*****array of objects*****) (*****optional*****)**

Custom fields. Must include a key and value. Key must be unique and letters, numbers and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

## [hashtag](#example) Example

The following example is a cURL request to create an asset in the library.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an asset library object.

[PreviousCompleteProjectRetestRoundchevron-left](/attackforge-enterprise/modules/self-service-restful-api/completeprojectretestround)[NextCreateGroupchevron-right](/attackforge-enterprise/modules/self-service-restful-api/creategroup)

Last updated 2 years ago
