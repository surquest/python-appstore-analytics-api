import os
import time
import pytest
import json
import datetime as dt

from surquest.utils.appstoreconnect.analytics.client import Client
from surquest.utils.appstoreconnect.analytics.analytics import Analytics
from surquest.utils.appstoreconnect.analytics.enums import Measure, Group, Frequency

class Params:

    @staticmethod
    def get():

        params = []
        combi = {
            Measure.ACTIVE_DEVICES: [
                    Group.TOTAL, 
                    Group.APP_VERSION, 
                    Group.COUNTRY, 
                    Group.DEVICE, 
                    Group.OS_VERSION, 
                    Group.SOURCE
                ],
            Measure.CRASHES: [
                    Group.TOTAL, 
                    Group.APP_VERSION, 
                    Group.DEVICE, 
                    Group.OS_VERSION
                ],
            Measure.INSTALLS: [
                    Group.TOTAL, 
                    Group.APP_VERSION, 
                    Group.COUNTRY, 
                    Group.DEVICE, 
                    Group.OS_VERSION, 
                    Group.SOURCE
                ],
            Measure.OPT_IN_RATE: [
                    Group.TOTAL
                ],
            Measure.SALES: [
                    Group.TOTAL, 
                    Group.COUNTRY, 
                    Group.DEVICE, 
                    Group.OS_VERSION, 
                    Group.PRODUCT,
                    Group.SOURCE
                ],
            Measure.UNINSTALLS: [
                    Group.TOTAL, 
                    Group.APP_VERSION,
                    Group.COUNTRY, 
                    Group.DEVICE, 
                    Group.OS_VERSION,
                    Group.SOURCE
            ],
            Measure.UNITS: [
                    Group.TOTAL, 
                    Group.COUNTRY, 
                    Group.DEVICE, 
                    Group.OS_VERSION,
                    Group.SOURCE
            ],
            Measure.VISITS: [
                    Group.TOTAL, 
                    Group.COUNTRY, 
                    Group.DEVICE, 
                    Group.OS_VERSION,
                    Group.SOURCE
            ]
        }

        for key in combi.keys():
                
                for value in combi.get(key):
    
                    params.append(
                         ({
                            "appId": os.getenv("APPID"),
                            "measure": key,
                            "startDate": dt.date(2023, 6, 16),
                            "endDate": dt.date(2023, 6, 18),
                            "grouping": value,
                            "frequency": Frequency.DAY
                        },{
                            "type": list,
                            "length": 3,
                        })
                    )

        return params
        

class TestAnalytics:

    client = Client(
        mayacinfo=os.getenv("MYACINFO")
        )
    
    analytics = Analytics(
        client=client
        )
    

    # do parameterized tests
    # https://docs.pytest.org/en/6.2.x/parametrize.html#parametrize-basics
    @pytest.mark.parametrize(
        "inputs,expected",
        Params.get()
    )
    def test_get_time_series_simple(self, inputs, expected):
        
        measure = inputs.get("measure")
        grouping = inputs.get("grouping")
        frequency = inputs.get("frequency")
        start_date = inputs.get("startDate")
        end_date = inputs.get("endDate")
        app_ids = str(inputs.get("appId"))

        data = self.analytics.get_time_series(
            app_ids=app_ids,
            measure=measure,
            start_date=start_date,
            end_date=end_date,
            grouping=grouping,
            frequency=frequency
            )

        # write out data into a json file
        with open(F"../data/sample/output.{measure.name}.{grouping.name}.{frequency.name}.json", "w") as f:
            json.dump(data, f, indent=4)

        # check if data is a list
        assert isinstance(data, list), F"Expected type: list, got: {type(data)}."

        # check if data is not empty
        assert data != [], F"Expected data to not be empty, got: {data}."

        # check the length of the data
        assert len(data) >= expected.get("length"), F"Expected length should be greater or equal: {expected.get('length')}, got: {len(data)}."
