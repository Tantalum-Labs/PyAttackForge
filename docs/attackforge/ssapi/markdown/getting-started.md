# GETTING STARTED

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getting-started

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# GETTING STARTED

## [hashtag](#overview) Overview

This page will help you to get started with using the Self-Service RESTful API.

## [hashtag](#authentication) Authentication

Access to the Self-Service RESTful API is controlled using an [User API Keyarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/manage-user#user-key).

In order to access the Self-Service RESTful API, you must meet the following conditions:

* You must have a valid [User API Keyarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/manage-user#user-key);
* You must be provided with access to RESTful API methods by the Administrators; and
* Your [User API Keyarrow-up-right](https://support.attackforge.com/attackforge-enterprise/getting-started/manage-user#user-key) is supplied in the Header **X-SSAPI-KEY** for each request to the API endpoint.

All requests to the API must be made over HTTPS. Calls made over plain HTTP will fail. You must authenticate all requests.

## [hashtag](#accessing-the-restful-api) Accessing the RESTful API

Access to the RESTful API, including scope of data available, is restricted to the users' data within the application.

By default, every user in the system does not have access to any of the RESTful API methods - including Administrators. Access to the RESTful API must be provided explicitly by an Administrator, and is controlled on an individual method basis.

A user can see their access to the RESTful SSAPI by viewing the SSAPI module in the application.

The following warning and padlock indicate that the RESTful API Method is not available:

![](https://support.attackforge.com/~gitbook/image?url=https%3A%2F%2F372186556-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-M8s1QY2Q6YTHB4a6DMu%252Fuploads%252FCVm1MT7XQHHUHGO167KB%252FScreenshot%25202025-06-24%2520at%252012.48.10%25E2%2580%25AFpm.png%3Falt%3Dmedia%26token%3D43c3d3f2-fd99-4a88-8ea3-2be3ae7ba761&width=768&dpr=4&quality=100&sign=348c80d3&sv=2)

An Administrator can provide a user with access to the RESTful SSAPI by accessing `Users > (select user) > Access > Self-Service RESTful API > Add Access`

![](https://support.attackforge.com/~gitbook/image?url=https%3A%2F%2F372186556-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-M8s1QY2Q6YTHB4a6DMu%252Fuploads%252FTK3BikVaiUTSN8gwXYQM%252FScreenshot%25202025-06-24%2520at%252012.49.38%25E2%2580%25AFpm.png%3Falt%3Dmedia%26token%3D1c55b60a-98e9-435e-b03c-ea5716f96eba&width=768&dpr=4&quality=100&sign=4f90ff58&sv=2)

[PreviousSelf-Service RESTful APIchevron-left](/attackforge-enterprise/modules/self-service-restful-api)[NextEXPORTING TO CSVchevron-right](/attackforge-enterprise/modules/self-service-restful-api/exporting-to-csv)

Last updated 6 months ago
