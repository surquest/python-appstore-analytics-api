#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file contains the Analytics class which is used to retrieve analytics data from the App Store Connect API.
import json
from typing import List, Optional, Callable
import datetime as dt
from .enums import Measure, Group, Frequency
from .formatter import Formatter
    

class Analytics:

    def __init__(self, client):
        """Initializes the Analytics class."""

        self.client = client

    def get_time_series(
        self,
        app_ids: List[str],
        measure: Measure,
        start_date: dt.date,
        end_date: dt.date,
        grouping: Optional[Group] = Group.TOTAL,
        frequency: str = Frequency.DAY,
        dimension_filters: Optional[List] = None,
        formatter: Optional[Callable] = Formatter.run
    ):
        """Method to retrieve the time series data for the specified measure and grouping.

        :param app_id: The App Store Connect app ID.
        :type app_id: str
        :param measure: The measure to retrieve data for.
        :type measure: Measure
        :param start_date: The start date for the time series data.
        :type start_date: dt.date
        :param end_date: The end date for the time series data.
        :type end_date: dt.date
        :param grouping: The grouping to retrieve data for.
        :type grouping: Group
        :param frequency: The frequency to retrieve data for.
        :type frequency: Frequency
        :param dimension_filters: The dimension filters to apply to the data.
        :type dimension_filters: List
        :param formatter: The formatter to apply to the data.
        :type formatter: Callable

        :return: The time series data.
        """

        # Get the endpoint for the request.
        url = self.client.get_endpoint(
            subject="time-series",
        )

        # Do the request.
        payload = {
            "adamId": [app_ids] if isinstance(app_ids, str) else app_ids,
            "measures":[measure.value],
            "frequency": frequency.value,
            "startTime": start_date.strftime("%Y-%m-%d")+"T00:00:00Z",
            "endTime":end_date.strftime("%Y-%m-%d")+"T00:00:00Z"
        }

        if grouping != Group.TOTAL:
            payload["group"] = self._get_group(
                grouping=grouping, 
                measure=measure
            )

        print("payload: ", json.dumps(payload))

        data = self.client.request(
            url=url,
            method="POST",
            data=payload
        )

        return formatter(
            data=data,
            grouping=grouping,
            measure=measure
        )
    
    @staticmethod
    def _get_group(grouping, measure):

        return {
            "dimension": grouping.value,
            "metric": measure.value,
            "rank": "DESCENDING",
            "limit": 10,
        }