from enum import Enum

class Measure(str, Enum):

    CRASHES = "crashes"
    INSTALLS = "installs"
    UNINSTALLS = "uninstalls"
    UNITS = "units"
    SALES = "sales"
    ACTIVE_DEVICES = "rollingActiveDevices"
    VISITS = "pageViewUnique"
    OPT_IN_RATE = "optin"


class Group(str, Enum):

    TOTAL = None
    APP_VERSION = "appVersion"
    COUNTRY = "storefront"
    DEVICE = "platform"
    OS_VERSION = "platformVersion"
    PRODUCT = "purchase"
    SOURCE = "source"
    


class Frequency(str, Enum):

    DAY = "day"
    WEEK = "week"
    MONTH = "month"