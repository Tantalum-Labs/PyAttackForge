# UpdateAssetInLibrary

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateassetinlibrary

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdateAssetInLibrary

This method can be used for the following: Update an asset in the library (must have Assets Module enabled in your tenant configuration!);

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/library/asset/:id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Identifier for the asset.

Example:

Copy

```
PUT /api/ss/library/asset/6035baa5fa29850a2a100ea9 HTTP/1.1
```

**name (string) (optional)**

Name of the asset.

Example:

**type (string) (optional)**

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

**is\_archived** ***(boolean) (optional)***

Whether asset is archived or not.

Example:

**is\_deleted** ***(boolean) (optional)***

Whether asset is deleted or not.

Example:

**custom\_fields (*****array of objects*****) (*****optional*****)**

Custom fields. Must include a key and value. Key must be unique and letters, numbers and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

## [hashtag](#example) Example

The following example is a cURL request to update an asset in the library.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a status.

[PreviousSendDailyCompletionEmailchevron-left](/attackforge-enterprise/modules/self-service-restful-api/senddailycompletionemail)[NextUpdateExecSummaryNoteschevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateexecsummarynotes)

Last updated 8 months ago
