# GetAssetInLibrary

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getassetinlibrary

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GetAssetInLibrary

This method can be used for the following: Get an asset in the library (must have Assets Module enabled in your tenant configuration!);

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
GET /api/ss/library/asset?id=:id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#query) Query

**id (string)**

Id of the asset.

Example:

Copy

```
GET /api/ss/library/asset?id=60c92f6113100562a6a58a6f HTTP/1.1
```

**cf\_key\_allowlist (string) (optional)**

List of custom field keys to include in response. Add multiple for more than one key e.g. `?cf_key_allowlist=key1&cf_key_allowlist=key2` or specify no keys to exclude all fields e.g. `?cf_key_allowlist=`

Example:

**cf\_key\_blocklist (string) (optional)**

List of custom field keys to exclude from response. Add multiple for more than one key e.g. `?cf_key_blocklist=key1&cf_key_blocklist=key2`

Example:

## [hashtag](#example) Example

The following example is a cURL request to get an asset from the library.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains an asset library object.

[PreviousGetAssetsByGroupchevron-left](/attackforge-enterprise/modules/self-service-restful-api/getassetsbygroup)[NextGetAssetLibraryAssetschevron-right](/attackforge-enterprise/modules/self-service-restful-api/getassetsinlibrary)

Last updated 4 months ago
