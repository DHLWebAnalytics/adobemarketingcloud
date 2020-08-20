# Adobe Experience Cloud APIs Client for Python
This Project tries to implement all Adobe Experience Cloud APIs for Python under one umbrella. Create an integration,
select an authentication method and call your desired API.

*Note: In the current stage not all APIs and authentication methods are implemented*

## How to install
Either clone this repository and run the setup script or take the more convenient path and get it via pip:
```python
pip install experiencecloudapis
```

## Authentication Methods
Currently only the JWT Service Account method is implemented. In order to get authenticated, you need to create
an integration with Adobe I/O first. You can read how to create a integration [here](https://www.adobe.io/authentication/auth-methods.html#!AdobeDocs/adobeio-auth/master/AuthenticationOverview/ServiceAccountIntegration.md).
When creating the JWT client, you need to specify the path to your service account json file, private key file and company id.
The service account json file nowadays can be easily retrieved from your Adobe I/O console. In order to do so, navigate to your
Intergration and click on the top right **Download JSON** button. The authentication client is configured to read and understand this
file out of the box. When creating your integration, either via the command line or via the **Generate a public/private key pair** method in
your Adobe I/O integration, you can retrieve the private key file.

```python
from experiencecloud.authentication import JWT

path_to_service_account_json = "/path/to/file.json"
path_to_private_key = "/path/to/private.key"
company_id = "company_id"

jwt_client = JWT(path_to_service_account_json, path_to_private_key, company_id)
```

## Request an API
Requesting an API is easy after you managed to create the integration. Plug the authentication client into any of the
APIs you want to request and call the respective method.

Currently implemented APIs:
- [Analytics](https://adobedocs.github.io/analytics-2.0-apis) (All Analytics 2.0 APIs are implemented and missing ones from 1.4 as Classifications)

```python
# setup the Analytics API Client and request the metrics method
from experiencecloud import Analytics

# report suite id is required for getting metrics
rsid = "rsid"

analytics_client = Analytics(jwt_client)
response = analytics_client.get_metrics(rsid)
```

## Adobe Analytics Report
In order to work easily with the Adobe Analytics Reports API, a helper Class requests and resolves labels automatically.
Currently this helper class works only with the Analytics Debugger JSON object, which can be extracted in Analytics Workspace
via the Debugger option. Copy and Paste the request payload into your script and execute the request. The class has
been designed to transform the response into a pandas DataFrame in order to make it as versatile as possible. See the
example below:

```python
from experiencecloud import AnalyticsReport

payload = {...} # Copy from Analytics Debugger

report_client = AnalyticsReport(jwt_client)
report_client.request_report(payload)
# now you have many options how to represent the response
report_client.to_dataframe() # pandas.DataFrame
report_client.to_csv() # csv string
report_client.to_json() # json string
report_client.to_dict() # dict
```