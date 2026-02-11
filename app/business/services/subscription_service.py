import re
from dataclasses import dataclass

from app.data.models import Subscriber
from app.data.repositories.subscriber_repository import SubscriberRepository

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


@dataclass
class SubscriptionResult:
    success: bool
    error: str = ""
    subscriber: Subscriber | None = None


class SubscriptionService:
    def __init__(self, repository: SubscriberRepository | None = None):
        self._repository = repository or SubscriberRepository()

    def subscribe(self, email: str, name: str, newsletters: dict[str, bool] | None = None) -> SubscriptionResult:
        is_valid, error = self._validate_email(email)
        if not is_valid:
            return SubscriptionResult(success=False, error=error)

        normalized_email = self._normalize_email(email)
        normalized_name = self._normalize_name(name)

        if self._repository.exists(normalized_email):
            return SubscriptionResult(success=False, error="Email already subscribed")

        subscriber = self._repository.save(normalized_email, normalized_name, newsletters)
        return SubscriptionResult(success=True, subscriber=subscriber)

    def _validate_email(self, email: str) -> tuple[bool, str]:
        if not email or not email.strip():
            return False, "Email is required"
        if not re.match(EMAIL_PATTERN, email.strip()):
            return False, "Invalid email format"
        return True, ""

    def _normalize_email(self, email: str) -> str:
        return email.lower().strip()

    def _normalize_name(self, name: str | None) -> str:
        if not name or not name.strip():
            return "Subscriber"
        return name.strip()

    def get_all_subscribers(self, sort_by: str = "date_desc", newsletter_filter: str | None = None) -> list[Subscriber]:
        return self._repository.get_all(sort_by, newsletter_filter)

    def get_subscriber(self, subscriber_id: int) -> Subscriber | None:
        return self._repository.find_by_id(subscriber_id)

    def update_subscriber(self, subscriber_id: int, email: str, name: str, newsletters: dict[str, bool] | None = None) -> SubscriptionResult:
        is_valid, error = self._validate_email(email)
        if not is_valid:
            return SubscriptionResult(success=False, error=error)

        normalized_email = self._normalize_email(email)
        normalized_name = self._normalize_name(name)

        existing = self._repository.find_by_email(normalized_email)
        if existing and existing.id != subscriber_id:
            return SubscriptionResult(success=False, error="Email already in use")

        subscriber = self._repository.update(subscriber_id, normalized_email, normalized_name, newsletters)
        if subscriber:
            return SubscriptionResult(success=True, subscriber=subscriber)
        return SubscriptionResult(success=False, error="Subscriber not found")

    def update_newsletters_bulk(self, subscriber_ids: list[int], newsletters: dict[str, bool | None]) -> int:
        return self._repository.update_newsletters_bulk(subscriber_ids, newsletters)

    def delete_subscriber(self, subscriber_id: int) -> bool:
        return self._repository.delete(subscriber_id)
