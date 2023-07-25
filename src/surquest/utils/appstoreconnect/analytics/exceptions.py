#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Collection of exceptions for the App Store Connect Analytics API


class AppStoreConnectAnalyticsError(Exception):

    """Base class for exceptions in this module."""

    pass


class AppStoreConnectAnalyticsRequestError(AppStoreConnectAnalyticsError):

    """Exception raised for errors in the request to the App Store Connect Analytics API.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message
