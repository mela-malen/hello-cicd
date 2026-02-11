import pytest
from app.business.services.subscription_service import SubscriptionService, SubscriptionResult


class TestSubscriptionService:
    def test_subscribe_valid_email(self, app, clean_db):
        with app.app_context():
            service = SubscriptionService()
            result = service.subscribe(
                email="test1@example.com",
                name="Test User",
                newsletters={'kost': True, 'mindset': False}
            )

            assert result.success is True
            assert result.error == ""
            assert result.subscriber is not None
            assert result.subscriber.email == "test1@example.com"
            assert result.subscriber.name == "Test User"
            assert result.subscriber.nl_kost is True
            assert result.subscriber.nl_mindset is False

    def test_subscribe_empty_email(self, app, clean_db):
        with app.app_context():
            service = SubscriptionService()
            result = service.subscribe(
                email="",
                name="Test User",
                newsletters={'kost': True}
            )

            assert result.success is False
            assert result.error == "Email is required"
            assert result.subscriber is None

    def test_subscribe_invalid_email_format(self, app, clean_db):
        with app.app_context():
            service = SubscriptionService()
            result = service.subscribe(
                email="invalid-email",
                name="Test User",
                newsletters={'kost': True}
            )

            assert result.success is False
            assert result.error == "Invalid email format"
            assert result.subscriber is None

    def test_subscribe_duplicate_email(self, app, clean_db):
        with app.app_context():
            service = SubscriptionService()

            result1 = service.subscribe(
                email="duplicate@example.com",
                name="First User",
                newsletters={'kost': True}
            )
            assert result1.success is True

            result2 = service.subscribe(
                email="duplicate@example.com",
                name="Second User",
                newsletters={'mindset': True}
            )
            assert result2.success is False
            assert result2.error == "Email already subscribed"

    def test_subscribe_without_newsletters(self, app, clean_db):
        with app.app_context():
            service = SubscriptionService()
            result = service.subscribe(
                email="no-newsletters@example.com",
                name="Test User"
            )

            assert result.success is True
            assert result.subscriber.nl_kost is False
            assert result.subscriber.nl_mindset is False
            assert result.subscriber.nl_kunskap is False
            assert result.subscriber.nl_veckans_pass is False
            assert result.subscriber.nl_jaine is False

    def test_subscribe_all_newsletters(self, app, clean_db):
        with app.app_context():
            service = SubscriptionService()
            result = service.subscribe(
                email="all-newsletters@example.com",
                name="Test User",
                newsletters={
                    'kost': True,
                    'mindset': True,
                    'kunskap': True,
                    'veckans_pass': True,
                    'jaine': True
                }
            )

            assert result.success is True
            assert result.subscriber.get_newsletters() == ['kost', 'mindset', 'kunskap', 'veckans_pass', 'jaine']
            assert result.subscriber.get_newsletter_count() == 5

    def test_normalize_email(self, app, clean_db):
        with app.app_context():
            service = SubscriptionService()
            normalized = service._normalize_email("TEST@EXAMPLE.COM")
            assert normalized == "test@example.com"

    def test_normalize_name_empty(self, app, clean_db):
        with app.app_context():
            service = SubscriptionService()
            normalized = service._normalize_name("")
            assert normalized == "Subscriber"

    def test_normalize_name_with_value(self, app, clean_db):
        with app.app_context():
            service = SubscriptionService()
            normalized = service._normalize_name("  Test User  ")
            assert normalized == "Test User"
