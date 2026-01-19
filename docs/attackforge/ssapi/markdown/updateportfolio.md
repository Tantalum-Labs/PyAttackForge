# UpdatePortfolio

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/updateportfolio

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# UpdatePortfolio

This method can be used for the following functionality: Update a Portfolio

## [hashtag](#parameters) Parameters

The following URL, Headers and Parameters are required for requests to this API endpoint. Where a parameter is optional, it will be indicated. Otherwise treat all parameters as mandatory.

### [hashtag](#headers) Headers

Copy

```
PUT /api/ss/portfolio/:id HTTP/1.1
Host: demo.attackforge.com
X-SSAPI-KEY: APIKey
Content-Type: application/json
Connection: close
```

### [hashtag](#body) Body

**name** ***(string)***

Name of the portfolio.

Example:

Copy

```
{
   "name": "..."
}
```

**code** ***(string) (optional)***

Portfolio code.

Example:

**description** ***(string) (optional)***

Portfolio description.

Example:

**level\_1\_owner** ***(string) (optional)***

Portfolio level 1 owner.

Example:

**level\_2\_owner** ***(string) (optional)***

Portfolio level 2 owner.

Example:

**level\_3\_owner** ***(string) (optional)***

Portfolio level 3 owner.

Example:

**users\_with\_view\_access** ***(array of strings) (optional)***

Users Ids for users who will have View access to this Portfolio.

Example:

**groups\_with\_view\_access** ***(array of strings) (optional)***

Group Ids for users who will have View access to this Portfolio.

Example:

**users\_with\_link\_access** ***(array of strings) (optional)***

Users Ids for users who will have Link access to this Portfolio.

Example:

**groups\_with\_link\_access** ***(array of strings) (optional)***

Group Ids for users who will have Link access to this Portfolio.

Example:

**streams** ***(array of objects) (optional)***

Create Streams on the Portfolio.

* id - Stream Id
* name - Stream name ***(optional)***
* projects - Project Ids to link to the Stream ***(optional)***
* users\_with\_view\_access - Users Ids for users who will have View access to this Portfolio. ***(optional)***
* users\_with\_link\_access - Users Ids for users who will have Link access to this Portfolio. ***(optional)***
* groups\_with\_view\_access - Group Ids for groups who will have View access to this Portfolio. ***(optional)***
* groups\_with\_link\_access - Group Ids for groups who will have Link access to this Portfolio. ***(optional)***
* sort\_order - sort order for the Streams ***(optional)***

Example:

**tags** ***(array of strings) (optional)***

Portfolio tags.

Example:

**custom\_fields (*****array of objects*****) (*****optional*****)**

Custom fields. Must include a key and value. Key must be unique and letters, number and underscores only.

For more information visit [https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apisarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/custom-fields-and-forms#using-custom-fields-with-apis)

Example:

## [hashtag](#example) Example

The following example is a cURL request to create a new portfolio.

### [hashtag](#request) Request

Include API Token instead of stars in 'X-SSAPI-KEY: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*' parameter.

### [hashtag](#response) Response

Response contains a portfolio object.

[PreviousUpdateGroupchevron-left](/attackforge-enterprise/modules/self-service-restful-api/updategroup)[NextUpdateProjectByIdchevron-right](/attackforge-enterprise/modules/self-service-restful-api/updateproject)

Last updated 1 year ago
