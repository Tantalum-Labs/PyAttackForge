# EXPORTING TO CSV

Source: https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/exporting-to-csv

---

copyCopychevron-down

1. [Core & Enterprise](/attackforge-enterprise)chevron-right
2. [Modules](/attackforge-enterprise/modules)chevron-right
3. [Self-Service RESTful API](/attackforge-enterprise/modules/self-service-restful-api)

# EXPORTING TO CSV

## [hashtag](#getting-started) Getting Started

This page will help you with exporting your Self-Service RESTful API data to CSV format.

This is useful if you need to analyze the data, create reports, or import the data into other tools that require CSV format.

It is possible to programmatically parse the output from the AttackForge Self-Service RESTful API into CSV format using various tools such as [JQarrow-up-right](https://stedolan.github.io/jq).

JQ is a lightweight and flexible command-line JSON processor.

JQ is supported on multiple operating systems (Linux, OSX, Windows) & is freely available. It is written in C and has no runtime dependencies.

This tutorial will show you how to install JQ and use it to convert AttackForge Self-Service RESTful API data into CSV format.

## [hashtag](#installing-jq-on-linux) Installing JQ on Linux

1. From command line, type following command: `sudo apt-get install jq`
2. Other install options are available from [https://stedolan.github.io/jq/download/arrow-up-right](https://stedolan.github.io/jq/download/)

## [hashtag](#installing-jq-on-windows) Installing JQ on Windows

1. From command line, type following command: `winget install jqlang.jq`
2. Other install options are available from [https://stedolan.github.io/jq/download/arrow-up-right](https://stedolan.github.io/jq/download/)

## [hashtag](#creating-csv-using-api-data) Creating CSV Using API Data

For this tutorial, we are going to focus on the [getVulnerabilitiesarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/getvulnerabilities) API method. You can however use this approach for any of the Self-Service RESTful API methods.

Open a command window / terminal.

Run the following command (replacing your tenant name & API Key). Make sure you have access to the getVulnerabilities API (see [https://support.attackforge.com/attackforge-enterprise/modules/users#managing-access-to-self-service-apiarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/users#managing-access-to-self-service-api))

The command above will produce a CSV titled **filtered\_vulns.csv** in the working directory where you had run the command from.

The CSV will include the following details for each vulnerability:

* **Id**
* **Title** (e.g. Blind SQL Injection)
* **Created** (time/date)
* **Priority** (Critical/High/Medium/Low/Info)
* **Status** (Open/Closed)
* **Status Updated** (time/date)
* **Affected Asset Name** (e.g. attackforge.com)
* **Affected Assets** - if vulnerability is using Grouped Assets, show each asset name
* **Retest** (Yes/No)
* **Project Name** (e.g. Web App Pentest)
* **Description**
* **Attack Scenario**
* **Remediation Recommendation**
* **Steps to Reproduce**

## [hashtag](#changing-fields-and-re-ordering-fields) **Changing Fields & Re-Ordering Fields**

If you would like to change the existing fields in the CSV, or re-order the fields in the CSV – adjust everything between **[.vulnerability\_created, ... , .vulnerability\_id]**:

## [hashtag](#adding-additional-fields) **Adding Additional Fields**

If you would like to add additional fields to the CSV, you can use any of the fields available in the API (see [https://support.attackforge.com/attackforge-enterprise/modules/self-service-api/getvulnerabilitiesarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/self-service-api/getvulnerabilities))

For example, the command below will also include the **Vulnerability SLA (.vulnerability\_sla)** in the CSV:

## [hashtag](#including-column-names) **Including Column Names**

If you would like to include column names in the CSV, you can set the columns using the command below – see **[\"Id\", ... , \"Steps To Reproduce\"]**:

Note the backslashes **\"** are necessary to escape the quotation marks for each CSV column title. If you do not include the backslashes, you may get a compilation error.

## [hashtag](#filtering-vulnerabilities) **Filtering Vulnerabilities**

If you would like to filter the vulnerabilities, you can use any of the existing filters supported in the API (see [https://support.attackforge.com/attackforge-enterprise/modules/users#managing-access-to-self-service-apiarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/users#managing-access-to-self-service-api))

For example, the command below will limit the vulnerabilities retrieved from the API to Open vulnerabilities only using the Advanced Query Filter ([https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filterarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filter)) **--data-urlencode "q={status:{$eq:\"Open\"}}"**:

## [hashtag](#advanced-examples) **Advanced Examples**

### [hashtag](#example-1-get-all-closed-vulnerabilities-and-reason-why-closed) **Example 1 - Get All Closed Vulnerabilities and Reason Why Closed**

Vulnerability Id

Created

Priority

Title

Status

Status Last Updated

Affected Asset

Affected Assets

Project Name

Project Id

Last Closed Reason

Last Closed On

Last Closed By

65bc9d9a4534bd000e50db3f

2024-02-02T07:45:30.179Z

Critical

Out-of-date Version

Closed

2024-02-02T09:36:41.513Z

https://attackforge.com

Test Project 1

65af64ec07bd34000fbac60d

Issue Closed: Risk accepted

2024-02-02T09:36:41.513Z

Admin Test

65b56ceff8b879000f887c7e

2024-01-27T20:51:59.346Z

Critical

Out-of-date Version

Closed

2024-02-02T05:33:38.928Z

https://portal.attackforge.com, https://app.attackforge.com

Test Project 1

65af64ec07bd34000fbac60d

Issue Closed: Issue has been fixed

2024-02-02T05:33:38.928Z

Admin Test

## [hashtag](#wrapping-up) **Wrapping up**

You can now use the JQ utility for any of the AttackForge Self-Service APIs, to extract any desired information for your reporting purposes.

You can check all the of the available APIs from our support site:
[https://support.attackforge.com/attackforge-enterprise/modules/self-service-apiarrow-up-right](https://support.attackforge.com/attackforge-enterprise/modules/self-service-api)

## [hashtag](#troubleshooting) **Troubleshooting**

### [hashtag](#id-1.-test-jq-utility-is-available) **1. Test jq utility is available**

This should result in info/help output in the terminal. This will test to confirm jq utility has been installed & configured successfully on your host.

### [hashtag](#id-2.-test-curl-works--piping-passing-json-data-to-jq) **2. Test cURL works + piping/passing JSON data to jq**

This should output JSON data to the terminal.

### [hashtag](#id-3.-test-csv-is-working) **3. Test @csv is working**

It should print "https://api.github.com/repos/stedolan/jq/commits/d18b2d078c2383d9472d0a0a226e07009025574f" in the terminal

### [hashtag](#id-4.-try-output-data-into-csv-file) **4. Try output data into csv file**

This should create a file **output.csv** in the directory you are currently running commands from in command terminal, the contents of the file will be https://api.github.com/repos/stedolan/jq/commits/d18b2d078c2383d9472d0a0a226e07009025574f

### [hashtag](#id-5.-store-attackforge-getvulnerabilities-data-in-a-json-file) **5. Store AttackForge getVulnerabilities data in a JSON file**

This should create a file vulns.json in the directory you are currently running commands from in terminal, the contents of this file will be vulnerabilities which match the query parameter.

### [hashtag](#id-6.-try-running-jq-on-vulns.json) **6. Try running JQ on vulns.json**

This should output csv data in the terminal.

### [hashtag](#id-7.-try-exporting-vulns.json-to-csv) **7. Try exporting vulns.json to csv**

This should create a file **filtered\_vulns.csv** in the directory you are currently running commands from in terminal, the contents of this file will be vulnerabilities which match the specified fields in the JQ command.

If you get to Step 7 above and it is all working correctly, there should be no restrictions from running the original command (see below):

[PreviousGETTING STARTEDchevron-left](/attackforge-enterprise/modules/self-service-restful-api/getting-started)[NextADVANCED QUERY FILTERchevron-right](/attackforge-enterprise/modules/self-service-restful-api/advanced-query-filter)

Last updated 9 months ago
