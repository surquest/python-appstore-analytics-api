import json
from typing import List, Optional, Callable
import datetime as dt
from .enums import Measure, Group, Frequency
from .formatter import Formatter


class Analytics:
    """
    The Analytics class is used to retrieve analytics data from the App Store Connect API.
    """

    def __init__(self, client):
        """
        Initializes the Analytics class.

        :param client: The client to use for the requests.
        :type client: AppStoreConnectClient
        """
        self.client = client

    def get_time_series(
        self,
        app_id: str,
        measure: Measure,
        start_date: dt.date,
        end_date: dt.date,
        grouping: Optional[Group] = Group.TOTAL,
        frequency: Frequency = Frequency.DAY,
        dimension_filters: Optional[List] = None,
        formatter: Callable = Formatter.run,
    ):
        """
        Method to retrieve the time series data for the specified measure and grouping.

        :param app_id: The App Store Connect app IDs.
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
        :rtype: dict
        """
        # Get the endpoint for the request.
        url = self.client.get_endpoint(
            subject="time-series",
        )

        # Do the request.
        payload = {
            "adamId": [str(app_id)],
            "measures": [measure.value],
            "frequency": frequency.value,
            "startTime": start_date.strftime("%Y-%m-%d") + "T00:00:00Z",
            "endTime": end_date.strftime("%Y-%m-%d") + "T00:00:00Z",
        }

        if grouping != Group.TOTAL:
            payload["group"] = self._get_group(grouping=grouping, measure=measure)

        data = self.client.request(url=url, method="POST", data=payload)

        return formatter(data=data, grouping=grouping, measure=measure)
    

    def get_retentions(self,
            app_id: str,
            start_date: dt.datetime = dt.datetime.utcnow() - dt.timedelta(days=7),
            end_date: dt.datetime = dt.datetime.utcnow(),
            frequency: Frequency = Frequency.DAY,
            dimension_filters: list = [],
            formatter: Callable = Formatter.retentions
            ) -> list:
        """Method to retrieve the retentions data for the specified app, time range and if passed, dimension filters.

        :param app_id: The App Store Connect app ID.
        :type app_id: str
        :param start_date: The start date for the retentions data.
        :type start_date: dt.datetime
        :param end_date: The end date for the retentions data.
        :type end_date: dt.datetime
        :param frequency: The frequency to retrieve data for.
        :type frequency: Frequency
        :param dimension_filters: The dimension filters to apply to the data. (default: []), example: 
[{dimensionKey: "source", optionKeys: ["Search"]}]
        :type dimension_filters: list
        :param formatter: The formatter to apply to the data.
        :type formatter: Callable

        :return: The retentions data.
        :rtype: list
        """

        # Get the endpoint for the request.
        url = self.client.get_endpoint(
            subject="retention",
        )

        # Do the request.
        payload = {
            "adamId": [str(app_id)],
            "frequency": frequency.value,
            "startTime": start_date.strftime("%Y-%m-%d") + "T00:00:00Z",
            "endTime": end_date.strftime("%Y-%m-%d") + "T00:00:00Z",
            "dimensionFilters": dimension_filters
        }

        data = self.client.request(url=url, method="POST", data=payload)

        return formatter(data=data, grouping=dimension_filters)


    @staticmethod
    def _get_group(grouping, measure):
        """
        Returns the group for the request.

        :param grouping: The grouping to retrieve data for.
        :type grouping: Group
        :param measure: The measure to retrieve data for.
        :type measure: Measure

        :return: The group for the request.
        :rtype: dict
        """
        return {
            "dimension": grouping.value,
            "metric": measure.value,
            "rank": "DESCENDING",
            "limit": 10,
        }
