from typing import Callable
import datetime as dt
from .formatter import Formatter


class Reviews:
    """
    The Reviews class is used to retrieve reviews from the App Store Connect API.
    """

    def __init__(self, client):
        """
        Initializes the Reviews class.

        :param client: The client to use for the requests.
        :type client: AppStoreConnectClient
        """
        self.client = client

    def fetch(
        self,
        app_id: str,
        start_date: dt.datetime = dt.datetime(2020, 1, 1),
        end_date: dt.datetime = dt.datetime(2050, 12, 31),
        country: str | None = None,
        last_known_review_id: int | None = None,
        formatter: Callable = Formatter.reviews,
    ):
        """
        Method to retrieve reviews of the AppStore app.

        :param app_id: The App Store Connect app ID.
        :type app_id: str
        :param start_date: The start date for the reviews.
        :type start_date: dt.date
        :param end_date: The end date for the reviews.
        :type end_date: dt.date
        :param formatter: The formatter to apply to the data.
        :type formatter: Callable

        :return: List of reviews.
        :rtype: dict
        """

        # Output variable with all reviews
        reviews = []
        reviews_count = 0
        has_next = True
        index = 0

        unix_start_date = int(start_date.timestamp()) * 1000
        unix_end_date = int(end_date.timestamp()) * 1000

        while has_next is True:
            # Get the endpoint for the request.
            url = self.client.get_endpoint(
                subject="reviews",
            ).format(app_id=app_id, index=index)

            if country is not None:
                url += f"&storefront={country}"

            # Do the request.
            data = self.client.request(url=url, method="GET").get("data")

            # Set total reviews count
            reviews_count = data.get("reviewCount")

            # loop in reviews and check if the review is in the date range
            # or if the review is the last known review
            for item in data.get("reviews"):

                review = item.get("value")
                print("-> review:", review)

                if int(review.get("id")) == last_known_review_id:
                    print("--> excluding due to last_known_review_id")
                    has_next = False
                    break

                if unix_start_date <= int(review.get("lastModified")) < unix_end_date:
                    reviews.append(review)

                else:
                    print("--> excluding due to date range")
                    has_next = False

            if has_next is True:
                index += 1

        return reviews_count, formatter(data=reviews)
