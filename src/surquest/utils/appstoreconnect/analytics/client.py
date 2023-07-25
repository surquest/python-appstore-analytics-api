#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
from typing import Dict, Optional
from .exceptions import AppStoreConnectAnalyticsRequestError


class Client:
    """
    A class for interacting with the App Store Connect API.
    """

    BASE_URL = "https://appstoreconnect.apple.com"

    def __init__(self, mayacinfo: str):
        """
        Initializes the Client class.

        :param mayacinfo: The myacinfo cookie value for the App Store Connect API.
        :type mayacinfo: str
        """

        self.__mayacinfo = mayacinfo
        self.__apple_widget_key = None
        self.__itctx = None

    @staticmethod
    def get_endpoint(
        subject: str = "time-series",
        group: str = "data",
    ) -> str:
        """
        Returns the API endpoint URL for the specified subject and type.

        :param subject: The subject of the API endpoint (default: "time-series").
        :type subject: str
        :param group: The type of the API endpoint (default: "data").
        :type group: str
        :return: The API endpoint URL.
        :rtype: str
        """

        endpoint = None

        if subject == "retention":
            endpoint = "/analytics/api/v1/data/retention"

        if subject == "reviews":
            endpoint = "/WebObjects/iTunesConnect.woa/ra/apps/{app_id}/platforms/ios/reviews?index={index}&sort=REVIEW_SORT_ORDER_MOST_RECENT"

        if subject == "time-series":
            endpoint = f"/analytics/api/v1/{group}/{subject}"

        if endpoint is None:

            raise ValueError(f"Invalid subject: {subject}")

        return Client.BASE_URL + endpoint

    def request(
        self,
        url: str,
        method: str = "POST",
        data: Optional[Dict] = None,
    ) -> requests.Response:
        """
        Sends a request to the App Store Connect API.

        :param url: The URL of the API endpoint.
        :type url: str
        :param method: The HTTP method to use (default: "POST").
        :type method: str
        :param data: The request data (default: None).
        :type data: Optional[Dict]
        :return: The API response.
        :rtype: requests.Response
        """

        iteration = 0
        response = self.do_request(url=url, method=method, data=data)

        while response.status_code == 429 and iteration < 5:
            iteration += 1
            sleep = iteration * 3
            print("-> Too many requests. Waiting for {sleep} seconds.")
            time.sleep(sleep)

            response = self.do_request(url=url, method=method, data=data)

        if response.status_code != 200:
            message = (
                f"--> Request failed with status code: {response.status_code}. "
                + f"Response: {response.text}"
            )

            print(message)

            raise AppStoreConnectAnalyticsRequestError(message=message)

        return response.json()

    def do_request(
        self,
        url: str,
        method: str = "POST",
        data: Optional[Dict] = None,
    ) -> requests.Response:
        """
        Sends a request to the App Store Connect API.

        :param url: The URL of the API endpoint.
        :type url: str
        :param method: The HTTP method to use (default: "POST").
        :type method: str
        :param data: The request data (default: None).
        :type data: Optional[Dict]
        :return: The API response.
        :rtype: requests.Response
        """

        print("-" * 50)
        print(f"Requesting URL: {url}")

        response = requests.request(
            method=method,
            url=url,
            json=data,
            headers={
                "Content-Type": "application/json",
                "X-Apple-Widget-Key": self._get_apple_widget_key(),
                "Accept": "application/json, text/plain, */*",
                "X-Requested-By": "analytics.itunes.apple.com",
            },
            cookies={"itctx": self._get_itctx(), "myacinfo": self.__mayacinfo},
        )

        return response

    def _get_apple_widget_key(self) -> str:
        """
        Retrieves the authentication service key for the App Store Connect API.

        :return: The authentication service key.
        :rtype: str
        """

        if self.__apple_widget_key is not None:
            return self.__apple_widget_key

        url = (
            Client.BASE_URL + "/olympus/v1/app/config?hostname=itunesconnect.apple.com"
        )

        response = requests.get(url=url)

        self.__apple_widget_key = response.json().get("authServiceKey")

        return self.__apple_widget_key

    def _get_itctx(self) -> str:
        """
        Retrieves the itctx cookie for the App Store Connect API.

        :return: The itctx cookie value.
        :rtype: str
        """

        if self.__itctx is not None:
            return self.__itctx

        url = Client.BASE_URL + "/olympus/v1/session"

        headers = {
            "Content-Type": "application/json",
            "X-Apple-Widget-Key": self._get_apple_widget_key(),
            "X-Requested-By": "dev.apple.com    ",
            "Accept": "application/json, text/plain, */*",
            "Referrer": "https://appstoreconnect.apple.com/login",
            "Cookie": "myacinfo=" + self.__mayacinfo,
        }

        response = requests.get(url=url, headers=headers)

        self.__itctx = response.cookies.get_dict().get("itctx")

        return self.__itctx
