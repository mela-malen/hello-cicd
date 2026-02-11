from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Newsletter subscriptions
    nl_kost = db.Column(db.Boolean, default=False)
    nl_mindset = db.Column(db.Boolean, default=False)
    nl_kunskap = db.Column(db.Boolean, default=False)
    nl_veckans_pass = db.Column(db.Boolean, default=False)
    nl_jaine = db.Column(db.Boolean, default=False)

    def get_newsletters(self) -> list[str]:
        """Return list of subscribed newsletter names."""
        newsletters = []
        if self.nl_kost:
            newsletters.append('kost')
        if self.nl_mindset:
            newsletters.append('mindset')
        if self.nl_kunskap:
            newsletters.append('kunskap')
        if self.nl_veckans_pass:
            newsletters.append('veckans_pass')
        if self.nl_jaine:
            newsletters.append('jaine')
        return newsletters

    def get_newsletter_count(self) -> int:
        """Return number of subscribed newsletters."""
        return len(self.get_newsletters())
