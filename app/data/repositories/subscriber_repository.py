from datetime import datetime
from app.data.models import db, Subscriber


class SubscriberRepository:
    def save(self, email: str, name: str) -> Subscriber:
        subscriber = Subscriber(email=email, name=name)
        db.session.add(subscriber)
        db.session.commit()
        return subscriber

    def find_by_email(self, email: str) -> Subscriber | None:
        return Subscriber.query.filter_by(email=email).first()

    def find_by_id(self, subscriber_id: int) -> Subscriber | None:
        return Subscriber.query.get(subscriber_id)

    def exists(self, email: str) -> bool:
        return Subscriber.query.filter_by(email=email).first() is not None

    def get_all(self, sort_by: str = "date_desc") -> list[Subscriber]:
        query = Subscriber.query
        if sort_by == "date_asc":
            query = query.order_by(Subscriber.subscribed_at.asc())
        elif sort_by == "date_desc":
            query = query.order_by(Subscriber.subscribed_at.desc())
        elif sort_by == "name_asc":
            query = query.order_by(Subscriber.name.asc())
        elif sort_by == "name_desc":
            query = query.order_by(Subscriber.name.desc())
        elif sort_by == "email_asc":
            query = query.order_by(Subscriber.email.asc())
        elif sort_by == "email_desc":
            query = query.order_by(Subscriber.email.desc())
        else:
            query = query.order_by(Subscriber.subscribed_at.desc())
        return query.all()

    def update(self, subscriber_id: int, email: str, name: str) -> Subscriber | None:
        subscriber = self.find_by_id(subscriber_id)
        if subscriber:
            subscriber.email = email
            subscriber.name = name
            db.session.commit()
        return subscriber

    def delete(self, subscriber_id: int) -> bool:
        subscriber = self.find_by_id(subscriber_id)
        if subscriber:
            db.session.delete(subscriber)
            db.session.commit()
            return True
        return False
