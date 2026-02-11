import pytest
from app.business.services.subscription_service import SubscriptionService
from app.data.models import Subscriber
from app.data.repositories.subscriber_repository import SubscriberRepository


class TestRegressionIssues:
    """Regression tests for previously fixed issues."""

    def test_email_normalization_preserves_local_part(self, app):
        """Regression: Email normalization should preserve local part before @."""
        with app.app_context():
            service = SubscriptionService()
            normalized = service._normalize_email("Test.User@Example.COM")
            assert normalized == "test.user@example.com"

    def test_email_normalization_trims_whitespace(self, app):
        """Regression: Email normalization should trim whitespace."""
        with app.app_context():
            service = SubscriptionService()
            normalized = service._normalize_email("  test@example.com  ")
            assert normalized == "test@example.com"

    def test_empty_name_becomes_subscriber(self, app):
        """Regression: Empty name should become 'Subscriber'."""
        with app.app_context():
            service = SubscriptionService()
            normalized = service._normalize_name("")
            assert normalized == "Subscriber"

    def test_whitespace_name_becomes_subscriber(self, app):
        """Regression: Whitespace-only name should become 'Subscriber'."""
        with app.app_context():
            service = SubscriptionService()
            normalized = service._normalize_name("   ")
            assert normalized == "Subscriber"

    def test_valid_name_preserved(self, app):
        """Regression: Valid name should be preserved with whitespace trimmed."""
        with app.app_context():
            service = SubscriptionService()
            normalized = service._normalize_name("  John Doe  ")
            assert normalized == "John Doe"

    def test_duplicate_email_prevents_duplicate_subscribers(self, app):
        """Regression: Same email cannot subscribe twice."""
        with app.app_context():
            service = SubscriptionService()

            result1 = service.subscribe(
                email="unique@example.com",
                name="First",
                newsletters={'kost': True}
            )
            assert result1.success is True

            result2 = service.subscribe(
                email="unique@example.com",
                name="Second",
                newsletters={'mindset': True}
            )
            assert result2.success is False
            assert result2.error == "Email already subscribed"

    def test_subscriber_get_newsletters_returns_list(self, app):
        """Regression: get_newsletters should return a list."""
        with app.app_context():
            repo = SubscriberRepository()
            subscriber = repo.save(
                email="newsletters@example.com",
                name="Test",
                newsletters={
                    'kost': True,
                    'mindset': True,
                    'kunskap': False,
                    'veckans_pass': False,
                    'jaine': True
                }
            )

            newsletters = subscriber.get_newsletters()

            assert isinstance(newsletters, list)
            assert 'kost' in newsletters
            assert 'mindset' in newsletters
            assert 'jaine' in newsletters
            assert 'kunskap' not in newsletters
            assert 'veckans_pass' not in newsletters

    def test_subscriber_get_newsletter_count(self, app):
        """Regression: get_newsletter_count should return correct count."""
        with app.app_context():
            repo = SubscriberRepository()
            subscriber = repo.save(
                email="count@example.com",
                name="Test",
                newsletters={
                    'kost': True,
                    'mindset': True,
                    'kunskap': True,
                    'veckans_pass': True,
                    'jaine': True
                }
            )

            count = subscriber.get_newsletter_count()

            assert count == 5

    def test_subscriber_without_newsletters(self, app):
        """Regression: Subscriber with no newsletters should work correctly."""
        with app.app_context():
            repo = SubscriberRepository()
            subscriber = repo.save(
                email="none@example.com",
                name="No Newsletters",
                newsletters={}
            )

            assert subscriber.nl_kost is False
            assert subscriber.nl_mindset is False
            assert subscriber.nl_kunskap is False
            assert subscriber.nl_veckans_pass is False
            assert subscriber.nl_jaine is False
            assert subscriber.get_newsletters() == []
            assert subscriber.get_newsletter_count() == 0

    def test_subscriber_with_all_newsletters(self, app):
        """Regression: Subscriber with all newsletters should work correctly."""
        with app.app_context():
            repo = SubscriberRepository()
            subscriber = repo.save(
                email="all@example.com",
                name="All Newsletters",
                newsletters={
                    'kost': True,
                    'mindset': True,
                    'kunskap': True,
                    'veckans_pass': True,
                    'jaine': True
                }
            )

            newsletters = subscriber.get_newsletters()

            assert len(newsletters) == 5
            assert 'kost' in newsletters
            assert 'mindset' in newsletters
            assert 'kunskap' in newsletters
            assert 'veckans_pass' in newsletters
            assert 'jaine' in newsletters

    def test_email_validation_rejects_empty(self, app):
        """Regression: Email validation should reject empty string."""
        with app.app_context():
            service = SubscriptionService()
            is_valid, error = service._validate_email("")

            assert is_valid is False
            assert error == "Email is required"

    def test_email_validation_rejects_whitespace_only(self, app):
        """Regression: Email validation should reject whitespace-only."""
        with app.app_context():
            service = SubscriptionService()
            is_valid, error = service._validate_email("   ")

            assert is_valid is False
            assert error == "Email is required"

    def test_email_validation_rejects_invalid_format(self, app):
        """Regression: Email validation should reject invalid format."""
        with app.app_context():
            service = SubscriptionService()
            is_valid, error = service._validate_email("not-an-email")

            assert is_valid is False
            assert error == "Invalid email format"

    def test_email_validation_accepts_valid_email(self, app):
        """Regression: Email validation should accept valid email."""
        with app.app_context():
            service = SubscriptionService()
            is_valid, error = service._validate_email("user@example.com")

            assert is_valid is True
            assert error == ""

    def test_email_validation_accepts_complex_email(self, app):
        """Regression: Email validation should accept complex valid email."""
        with app.app_context():
            service = SubscriptionService()
            is_valid, error = service._validate_email("user.name+tag@example.co.uk")

            assert is_valid is True
            assert error == ""

    def test_update_nonexistent_subscriber_fails(self, app):
        """Regression: Updating nonexistent subscriber should fail gracefully."""
        with app.app_context():
            service = SubscriptionService()
            result = service.update_subscriber(
                subscriber_id=99999,
                email="test@example.com",
                name="Test",
                newsletters={'kost': True}
            )

            assert result.success is False
            assert result.error == "Subscriber not found"

    def test_delete_nonexistent_subscriber_returns_false(self, app):
        """Regression: Deleting nonexistent subscriber should return False."""
        with app.app_context():
            service = SubscriptionService()
            result = service.delete_subscriber(99999)

            assert result is False

    def test_get_nonexistent_subscriber_returns_none(self, app):
        """Regression: Getting nonexistent subscriber should return None."""
        with app.app_context():
            service = SubscriptionService()
            result = service.get_subscriber(99999)

            assert result is None

    def test_update_existing_email_to_own_email_succeeds(self, app):
        """Regression: Updating subscriber to same email should succeed."""
        with app.app_context():
            service = SubscriptionService()
            result = service.subscribe(
                email="same@example.com",
                name="Same Email",
                newsletters={'kost': True}
            )
            assert result.success is True

            subscriber = result.subscriber
            update_result = service.update_subscriber(
                subscriber_id=subscriber.id,
                email="same@example.com",
                name="Updated Name",
                newsletters={'mindset': True}
            )

            assert update_result.success is True
            assert update_result.subscriber.name == "Updated Name"
