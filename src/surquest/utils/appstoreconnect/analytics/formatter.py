#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as dt


class Formatter(object):
    """
    A class for formatting data from the App Store Connect Analytics API.
    """

    @staticmethod
    def run(data, grouping, measure):
        """
        Formats data from the App Store Connect Analytics API.

        :param data: The data to format.
        :type data: dict
        :param grouping: The grouping to use for the data.
        :type grouping: str
        :param measure: The measure to use for the data.
        :type measure: str
        :return: The formatted data.
        :rtype: list
        """

        out = []

        for item in data.get("results"):
            app_id = item.get("adamId")
            segmentation = grouping
            segment = (
                "<total>"
                if item.get("group") is None
                else item.get("group").get("title")
            )
            segmentation_name = (
                "<total>" if segmentation.value is None else segmentation.name
            )

            for record in item.get("data"):
                out.append(
                    {
                        "date": str(record.get("date")).split("T")[0],
                        "app_id": app_id,
                        "segmentation_name": segmentation_name,
                        "segment": segment,
                        measure: None
                        if record.get(measure.value) == -1.0
                        else record.get(measure),
                        "__record_month": int(dt.datetime.utcnow().strftime("%Y%m")),
                        "__record_create_date": dt.datetime.utcnow().strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                    }
                )

        return out

    @staticmethod
    def retentions(data, grouping) -> list:
        """
        Formats data from the App Store Retentions API.

        :param data: List of retentions kpis.
        :type data: dict
        :param grouping: The grouping to use for the data.
        :type grouping: list
        :return: The formatted data.
        :rtype: list
        """

        out = []

        segmentation_name = "<total>"
        segment_name = "<total>"

        if isinstance(grouping, list) and len(grouping) > 0:
            segmentation_name = str(grouping[0].get("dimensionKey"))
            segment_name = ",".join(grouping[0].get("optionKeys"))

        for purchase_day in data.get("results"):

            for date in purchase_day.get("data"):
                out.append(
                    {
                        "purchasedAt": dt.datetime.strptime(
                            purchase_day.get("appPurchase"), "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "date": dt.datetime.strptime(
                            date.get("date"), "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "appId": purchase_day.get("adamId"),
                        "segmentationName": segmentation_name,
                        "segment": segment_name,
                        "retentionPercentage": date.get("retentionPercentage"),
                        "retentionCount": date.get("value"),
                    }
                )

        return out

    @staticmethod
    def reviews(data):
        """
        Formats data from the App Store Reviews API.

        :param data: List of reviews.
        :type data: dict
        :return: The formatted data.
        :rtype: list
        """

        return data
