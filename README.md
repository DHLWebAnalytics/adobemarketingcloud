# Adobe Experience Cloud APIs for Python

[![Build Status](https://travis-ci.org/DHLWebAnalytics/experiencecloudapis.svg?branch=master)](https://travis-ci.org/DHLWebAnalytics/experiencecloudapis)
[![PyPI version](https://badge.fury.io/py/experiencecloudapis.svg)](https://badge.fury.io/py/experiencecloudapis)

This Project tries to implement all Adobe Experience Cloud APIs for Python under one umbrella. Create an integration,
select an authentication method and call your desired API.

*Note: In this stage not all APIs and authentication methods are implemented*

## How to install
Either clone this repository and run the setup script or install it via pip:
```python
pip install experiencecloudapis
```

## Authentication Methods
Currently only the Service Account (JWT) client is implemented.
- [Service Account (JWT)](https://www.adobe.io/authentication/auth-methods.html#!AdobeDocs/adobeio-auth/master/AuthenticationOverview/AuthenticationGuide.md)

## Service Account (JWT)
In order to get authenticated, you need to create an integration with [Adobe I/O](https://console.adobe.io/) first. You can read how to create a integration [here](https://www.adobe.io/authentication/auth-methods.html#!AdobeDocs/adobeio-auth/master/AuthenticationOverview/ServiceAccountIntegration.md).
When creating the JWT client, you need to specify the path to your **service account json** file, **private key** file and **company id**.
The service account json file nowadays can be easily retrieved from your Adobe I/O console. In order to do so, navigate to your
intergration and click on the top right **Download JSON** button. The authentication client is configured to read and understand this
file out of the box. When creating your integration, you have to upload a private/public key pair to your integration in order to make it work.
This can be done either via the command line or via the **Generate a public/private key pair** method in your Adobe I/O integration. After your key pair is generated, save the private key safely on your computer and use it for the authentication.
Retrieving the company id is rather a hard nut. In order to achieve it, we logged in into the [Adobe Analytics API Swagger UI](https://adobedocs.github.io/analytics-2.0-apis) and executed an API method, then retrieved the company id from the request URL, which looks something like this:
`https://analytics.adobe.io/api/{COMPANY_ID}/calculatedmetrics`

```python
# JWT authentication example
from experiencecloudapis.authentication import JWT

path_to_service_account_json = "/path/to/file.json"
path_to_private_key = "/path/to/private.key"
company_id = "company_id"

# if everything works well, you have created your jwt client and can inject it into your API client
jwt_client = JWT(path_to_service_account_json, path_to_private_key, company_id)
```

## Supported APIs
Currently implemented APIs:
- [Analytics](https://adobedocs.github.io/analytics-2.0-apis) (All Analytics 2.0 APIs are implemented and missing ones from 1.4 as Classifications)

## Request Analytics API
Requesting an API is easy after you managed to create the integration. Plug the authentication client into any of the
APIs you want to request and call the respective method.


```python
# setup the Analytics API Client and request the metrics method
from experiencecloudapis import Analytics

# report suite id is required for getting metrics
rsid = "rsid"

# inject the authentication client into your API
analytics_client = Analytics(jwt_client)
response = analytics_client.get_metrics(rsid)
```

## Adobe Analytics Report Class
Requesting Adobe Analytics Reports is a common task and in order to ease the way to retrieve and process the response, we have created a helper class.
In order to work easily with the Adobe Analytics Reports API, a helper Class requests and processes responses automatically.
Adobe Reports API responses come in a rather generic format, which needs to be processed in order to be useful for further analysis.
This class processes the response and resolves the data into an intermediate table which can be transformed further into famous formats as pandas.DataFrame, json or csv.
Currently this helper class works only with the Analytics Debugger JSON object, which can be extracted in Analytics Workspace via the Debugger option.
Copy and Paste the request payload into your script and execute the request.
See the example below:

```python
from experiencecloudapis import AnalyticsReport

payload = {...} # Copy from Analytics Debugger

report_client = AnalyticsReport(jwt_client)
report_client.request_report(payload)
# now you have many options how to represent the response
report_client.to_dataframe() # pandas.DataFrame
report_client.to_csv() # csv string
report_client.to_json() # json string
report_client.to_dict() # dict
```