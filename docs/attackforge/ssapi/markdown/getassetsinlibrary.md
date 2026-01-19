# GetAssetLibraryAssets

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getassetsinlibrary

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetAssetLibraryAssets

This method can be used for the following: Get assets in the library (must have Assets Module enabled in your tenant configuration!);

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
POST /api/ss/library/assets HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#body) Body

**name (string) (optional)**

Name of the asset.

Example:

Copy

```
{
   "name": "..."
}
```

**type (string) (optional)**

Type of asset. Must be one of the following: *Web App, API, Mobile, Cloud, Infrastructure, Network, Wifi, Hardware, Other*

Example:

**external\_id (string) (optional)**

External id for the asset. For example id associated with the assest in Configuration Management Database.

Example:

**skip (integer) (optional)**

Number of records to skip. Default is 0 (do not skip any records).

Example:

**limit (integer) (optional)**

Number of records to limit to. Default limit is 500. Max limit is 500.

Example:

**archived** ***(boolean) (optional)***

Return archived assets. Must have access to view archived assets.

Example:

**query (*****string*****) (*****optional*****)**

Provides options to query a custom selection of assets.

Example:

Please visit the following link for more details on how to use this filter: [https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filterarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filter)

**cf\_key\_allowlist (string) (optional)**

List of custom field keys to include in response.

Example:

**cf\_key\_blocklist (string array) (optional)**

List of custom field keys to exclude from response.

Example:

## [hashtag](#example) Example

The following example is a cURL request to get all assets from the library of type 'Web App'.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an asset library count and array of asset library objects.

[PreviousGetAssetInLibrarychevron-left](/attackforge-enterprise/modules/self-service-restful-api/getassetinlibrary)[NextGetFormConfigchevron-right](/attackforge-enterprise/modules/self-service-restful-api/getformconfig)

Last updated 4 months ago
