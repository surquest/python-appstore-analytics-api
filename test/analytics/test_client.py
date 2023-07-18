import os
import pytest

from surquest.utils.appstoreconnect.analytics.client import Client

class TestClient:
    """
    This class contains unit tests for the Client class in the appstoreconnect.analytics package.
    """

    client = Client(
        mayacinfo=os.getenv("MYACINFO")
        )

    def test_get_endpoint(self):
        """
        Test the get_endpoint method of the Client class.
        """
        expected = "https://appstoreconnect.apple.com/analytics/api/v1/data/test"
        actual = Client.get_endpoint(subject="test")

        assert actual == expected, F"Expected URL: {expected}, got: {actual}."

    def test_request(self):
        """
        Test the request method of the Client class.
        """
        data = self.client.request(
            url="https://appstoreconnect.apple.com/analytics/api/v1/data/time-series", 
            method="POST",
            data={
                "adamId":[os.getenv("APPID")],
                "measures":["impressionsTotal"],
                "frequency":"day",
                "startTime":"2023-06-17T00:00:00Z",
                "endTime":"2023-07-16T00:00:00Z",
                "group":None
                }
            )
        
        # check if data is a dictionary
        assert isinstance(data, dict), F"Expected type: dict, got: {type(data)}."

        # check if data is not empty
        assert data != {}, F"Expected data to not be empty, got: {data}."


    def test__get_apple_widget_key(self):
        """
        Test the _get_apple_widget_key method of the Client class.
        """
        apple_widget_key = self.client._get_apple_widget_key()

        # check if the Apple Widget Key is a string
        assert isinstance(apple_widget_key, str), F"Expected type: str, got: {type(apple_widget_key)}."

        # check if the Apple Widget Key is not empty
        assert apple_widget_key != "", F"Expected Apple Widget Key to not be empty, got: {apple_widget_key}."

        # check if the Apple Widget Key is 32 characters long
        assert len(apple_widget_key) == 64, F"Expected Apple Widget Key to be 64 characters long, got: {len(apple_widget_key)}."

    def test__get_itctx(self):
        """
        Test the _get_itctx method of the Client class.
        """
        itctx = self.client._get_itctx()

        # check if the itctx is a string
        assert isinstance(itctx, str), F"Expected type: str, got: {type(itctx)}."

        # check if the itctx is not empty
        assert itctx != "", F"Expected itctx to not be empty, got: {itctx}."

        # check if the itctx is 32 characters long
        assert len(itctx) >= 32, F"Expected itctx to be at least 32 characters long, got: {len(itctx)}."