from datetime import datetime
from app.data.models import db, Subscriber


class SubscriberRepository:
    def save(self, email: str, name: str, newsletters: dict[str, bool] | None = None) -> Subscriber:
        subscriber = Subscriber(
            email=email,
            name=name,
            nl_kost=newsletters.get('kost', False) if newsletters else False,
            nl_mindset=newsletters.get('mindset', False) if newsletters else False,
            nl_kunskap=newsletters.get('kunskap', False) if newsletters else False,
            nl_veckans_pass=newsletters.get('veckans_pass', False) if newsletters else False,
            nl_jaine=newsletters.get('jaine', False) if newsletters else False,
        )
        db.session.add(subscriber)
        db.session.commit()
        return subscriber

    def find_by_email(self, email: str) -> Subscriber | None:
        return Subscriber.query.filter_by(email=email).first()

    def find_by_id(self, subscriber_id: int) -> Subscriber | None:
        return Subscriber.query.get(subscriber_id)

    def exists(self, email: str) -> bool:
        return Subscriber.query.filter_by(email=email).first() is not None

    def get_all(self, sort_by: str = "date_desc", newsletter_filter: str | None = None) -> list[Subscriber]:
        query = Subscriber.query

        # Filter by newsletter
        if newsletter_filter:
            if newsletter_filter == 'kost':
                query = query.filter(Subscriber.nl_kost == True)
            elif newsletter_filter == 'mindset':
                query = query.filter(Subscriber.nl_mindset == True)
            elif newsletter_filter == 'kunskap':
                query = query.filter(Subscriber.nl_kunskap == True)
            elif newsletter_filter == 'veckans_pass':
                query = query.filter(Subscriber.nl_veckans_pass == True)
            elif newsletter_filter == 'jaine':
                query = query.filter(Subscriber.nl_jaine == True)

        # Sort
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

    def update(self, subscriber_id: int, email: str, name: str, newsletters: dict[str, bool] | None = None) -> Subscriber | None:
        subscriber = self.find_by_id(subscriber_id)
        if subscriber:
            subscriber.email = email
            subscriber.name = name
            if newsletters is not None:
                subscriber.nl_kost = newsletters.get('kost', False)
                subscriber.nl_mindset = newsletters.get('mindset', False)
                subscriber.nl_kunskap = newsletters.get('kunskap', False)
                subscriber.nl_veckans_pass = newsletters.get('veckans_pass', False)
                subscriber.nl_jaine = newsletters.get('jaine', False)
            db.session.commit()
        return subscriber

    def update_newsletters_bulk(self, subscriber_ids: list[int], newsletters: dict[str, bool | None]) -> int:
        """Update newsletters for multiple subscribers. None means don't change."""
        updated = 0
        for sid in subscriber_ids:
            subscriber = self.find_by_id(sid)
            if subscriber:
                if newsletters.get('kost') is not None:
                    subscriber.nl_kost = newsletters['kost']
                if newsletters.get('mindset') is not None:
                    subscriber.nl_mindset = newsletters['mindset']
                if newsletters.get('kunskap') is not None:
                    subscriber.nl_kunskap = newsletters['kunskap']
                if newsletters.get('veckans_pass') is not None:
                    subscriber.nl_veckans_pass = newsletters['veckans_pass']
                if newsletters.get('jaine') is not None:
                    subscriber.nl_jaine = newsletters['jaine']
                updated += 1
        db.session.commit()
        return updated

    def delete(self, subscriber_id: int) -> bool:
        subscriber = self.find_by_id(subscriber_id)
        if subscriber:
            db.session.delete(subscriber)
            db.session.commit()
            return True
        return False
