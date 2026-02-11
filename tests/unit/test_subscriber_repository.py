import pytest
from app.data.models import Subscriber
from app.data.repositories.subscriber_repository import SubscriberRepository
from app.business.services.subscription_service import SubscriptionService


class TestSubscriberRepository:
    def test_save_creates_subscriber(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            subscriber = repo.save(
                email="test1@example.com",
                name="Test User",
                newsletters={'kost': True, 'mindset': False}
            )

            assert subscriber.id is not None
            assert subscriber.email == "test1@example.com"
            assert subscriber.name == "Test User"
            assert subscriber.nl_kost is True
            assert subscriber.nl_mindset is False

    def test_find_by_email_returns_subscriber(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            repo.save(
                email="findme@example.com",
                name="Find Me",
                newsletters={'kunskap': True}
            )

            found = repo.find_by_email("findme@example.com")

            assert found is not None
            assert found.email == "findme@example.com"
            assert found.name == "Find Me"

    def test_find_by_email_returns_none_for_nonexistent(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            found = repo.find_by_email("nonexistent@example.com")

            assert found is None

    def test_exists_returns_true_for_existing_email(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            repo.save(
                email="exists@example.com",
                name="Exists",
                newsletters={}
            )

            assert repo.exists("exists@example.com") is True
            assert repo.exists("notexists@example.com") is False

    def test_find_by_id_returns_subscriber(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            saved = repo.save(
                email="byid@example.com",
                name="By ID",
                newsletters={}
            )
            found = repo.find_by_id(saved.id)

            assert found is not None
            assert found.id == saved.id
            assert found.email == "byid@example.com"

    def test_find_by_id_returns_none_for_nonexistent(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            found = repo.find_by_id(99999)

            assert found is None

    def test_get_all_returns_all_subscribers(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            repo.save("user1@example.com", "User 1", {})
            repo.save("user2@example.com", "User 2", {})
            repo.save("user3@example.com", "User 3", {})

            subscribers = repo.get_all()

            assert len(subscribers) == 3

    def test_get_all_sorts_by_date_desc(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            repo.save("user1@example.com", "User 1", {})
            repo.save("user2@example.com", "User 2", {})
            repo.save("user3@example.com", "User 3", {})

            subscribers = repo.get_all(sort_by="date_desc")

            assert len(subscribers) == 3

    def test_get_all_sorts_by_name_asc(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            repo.save("zuser@example.com", "Zebra User", {})
            repo.save("auser@example.com", "Alpha User", {})
            repo.save("muser@example.com", "Middle User", {})

            subscribers = repo.get_all(sort_by="name_asc")

            assert subscribers[0].name == "Alpha User"
            assert subscribers[1].name == "Middle User"
            assert subscribers[2].name == "Zebra User"

    def test_get_all_filters_by_newsletter(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            repo.save("kost@example.com", "Kost User", {'kost': True})
            repo.save("both@example.com", "Both User", {'kost': True, 'mindset': True})
            repo.save("none@example.com", "None User", {})

            subscribers = repo.get_all(newsletter_filter="kost")

            assert len(subscribers) == 2
            for s in subscribers:
                assert s.nl_kost is True

    def test_update_subscriber(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            saved = repo.save(
                email="update@example.com",
                name="Original Name",
                newsletters={'kost': True}
            )

            updated = repo.update(
                saved.id,
                email="updated@example.com",
                name="New Name",
                newsletters={'mindset': True, 'kunskap': True}
            )

            assert updated.email == "updated@example.com"
            assert updated.name == "New Name"
            assert updated.nl_kost is False
            assert updated.nl_mindset is True
            assert updated.nl_kunskap is True

    def test_update_with_none_newsletters_preserves_existing(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            saved = repo.save(
                email="preserve@example.com",
                name="Preserve",
                newsletters={'kost': True, 'mindset': False}
            )

            updated = repo.update(
                saved.id,
                email="preserve@example.com",
                name="Preserve Updated",
                newsletters=None
            )

            assert updated.nl_kost is True
            assert updated.nl_mindset is False

    def test_delete_subscriber(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            saved = repo.save(
                email="delete@example.com",
                name="To Delete",
                newsletters={}
            )
            subscriber_id = saved.id

            result = repo.delete(subscriber_id)

            assert result is True
            assert repo.find_by_id(subscriber_id) is None

    def test_delete_nonexistent_returns_false(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            result = repo.delete(99999)

            assert result is False

    def test_update_newsletters_bulk(self, app, clean_db):
        with app.app_context():
            repo = SubscriberRepository()
            s1 = repo.save("bulk1@example.com", "Bulk 1", {'kost': False})
            s2 = repo.save("bulk2@example.com", "Bulk 2", {'kost': False})
            s3 = repo.save("bulk3@example.com", "Bulk 3", {'kost': False})

            updated = repo.update_newsletters_bulk(
                [s1.id, s2.id],
                {'kost': True}
            )

            assert updated == 2

            s1_updated = repo.find_by_id(s1.id)
            s2_updated = repo.find_by_id(s2.id)
            s3_unchanged = repo.find_by_id(s3.id)

            assert s1_updated.nl_kost is True
            assert s2_updated.nl_kost is True
            assert s3_unchanged.nl_kost is False
