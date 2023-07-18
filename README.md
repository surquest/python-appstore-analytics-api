![GitHub](https://img.shields.io/github/license/surquest/python-appstore-analytics-api?style=flat-square)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/surquest/python-appstore-analytics-api/test.yml?branch=main&style=flat-square)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/surquest/6e25c317000917840152a5e702e71963/raw/python-appstore-analytics-api.json&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/surquest-GCP-logger?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/surquest-GCP-logger)

# Introduction

This is a Python library for the AppStore Analytics API and allows you to easily access the analytics data of your python apps.

# Installation

```bash
pip install surquest-utils-appstoreconnect-analytics-api
```

# Usage

```python

from surquest.utils.appstoreconnect.analytics import (
    Client as AppStoreConnectClient,
    Analytics as AppStoreConnectAnalytics,
)

# Create client
client = AppStoreConnectClient(
    key_id="KEY_ID",
    issuer_id="ISSUER_ID",
    key_file_path="KEY_FILE_PATH",
    key_file_password="KEY_FILE_PASSWORD",
)

# Create analytics object
analytics = AppStoreConnectAnalytics(
    client=client
)

# Get time series data
data = analytics.get_time_series(

)

```

# Development

```
docker build `
     --tag surquest/utils/appstoreconnect:dev `
     --file package.base.dockerfile `
     --target test .

docker run --rm -it `
 -v "${pwd}:/opt/project" `
 -w "/opt/project/test" `
 -e "APPID={ADD-YOUR-APP-ID}" `
 -e "MYACINFO={ADD-YOUR-MYACINFO}" `
 surquest/utils/appstoreconnect:dev pytest
```

# License

This project is licensed under the terms of the MIT license.