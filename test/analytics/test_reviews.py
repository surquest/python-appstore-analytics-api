import os
import datetime as dt

from surquest.utils.appstoreconnect.analytics.client import Client
from surquest.utils.appstoreconnect.analytics.reviews import Reviews
       

class TestReviews:

    client = Client(
        mayacinfo=os.getenv("MYACINFO", "")
        )
    
    reviews = Reviews(
        client=client
        )
    

    def test_fetch_reviews(self):
        
        reviews_count, reviews = self.reviews.fetch(
            app_id=os.getenv("APPID", ""),
            start_date=dt.datetime(2023, 7, 1),
            end_date=dt.datetime(2023, 7, 24)
            )

        assert isinstance(reviews, list), F"Expected type: list, got: {type(reviews)}."
        assert len(reviews) > 0, F"Expected reviews to not be empty, got: {reviews}."
        assert isinstance(reviews_count, int), F"Expected type: int, got: {type(reviews_count)}."
        assert reviews_count > 0, F"Expected reviews count to be greater than 0, got: {reviews_count}."
        assert len(reviews) == 29, F"Expected count of reviews is 29, got: {len(reviews)}"

    def test_fetch_reviews_last_known_id(self):

        reviews_count, reviews = self.reviews.fetch(
            app_id=os.getenv("APPID", ""),
            start_date=dt.datetime(2023, 7, 1),
            end_date=dt.datetime(2023, 7, 24),
            last_known_review_id=10166387055
            )
        
        assert isinstance(reviews, list), F"Expected type: list, got: {type(reviews)}."
        assert len(reviews) > 0, F"Expected reviews to not be empty, got: {reviews}."
        assert isinstance(reviews_count, int), F"Expected type: int, got: {type(reviews_count)}."
        assert reviews_count > 0, F"Expected reviews count to be greater than 0, got: {reviews_count}."
        assert len(reviews) == 2, F"Expected count of reviews is 2, got: {len(reviews)}"