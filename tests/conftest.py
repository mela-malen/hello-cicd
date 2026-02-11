import pytest
from app import create_app
from app.data.models import db


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()


@pytest.fixture
def clean_db(app):
    """Clean database before and after test."""
    with app.app_context():
        from app.data.models import Subscriber, User
        Subscriber.query.delete()
        User.query.delete()
        db.session.commit()
        yield
        Subscriber.query.delete()
        User.query.delete()
        db.session.commit()
