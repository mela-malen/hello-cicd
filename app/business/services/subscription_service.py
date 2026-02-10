import re
from dataclasses import dataclass

from app.data.repositories.subscriber_repository import Subscriber, SubscriberRepository

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


@dataclass
class SubscriptionResult:
    success: bool
    error: str = ""
    subscriber: Subscriber | None = None


class SubscriptionService:
    def __init__(self, repository: SubscriberRepository | None = None):
        self._repository = repository or SubscriberRepository()

    def subscribe(self, email: str, name: str) -> SubscriptionResult:
        is_valid, error = self._validate_email(email)
        if not is_valid:
            return SubscriptionResult(success=False, error=error)

        normalized_email = self._normalize_email(email)
        normalized_name = self._normalize_name(name)

        subscriber = Subscriber(email=normalized_email, name=normalized_name)
        self._repository.save(subscriber)

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

    def get_all_subscribers(self):
        """
        Get all subscribers.

        Delegates to the repository for data access.

        Returns:
            List of all Subscriber instances, newest first
        """
        return self._repository.get_all()
