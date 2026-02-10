from dataclasses import dataclass


@dataclass
class Subscriber:
    email: str
    name: str


class SubscriberRepository:
    def __init__(self):
        self._subscribers: dict[str, Subscriber] = {}

    def save(self, subscriber: Subscriber) -> Subscriber:
        self._subscribers[subscriber.email] = subscriber
        return subscriber

    def find_by_email(self, email: str) -> Subscriber | None:
        return self._subscribers.get(email)

    def exists(self, email: str) -> bool:
        return email in self._subscribers
