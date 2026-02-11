import pytest
import subprocess
import time
import os
import sys


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def playwright():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def app_server():
    """Start Flask server for E2E tests."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env = os.environ.copy()
    env['FLASK_ENV'] = 'testing'
    env['PYTHONPATH'] = project_root

    process = subprocess.Popen(
        [sys.executable, '-m', 'flask', 'run', '--host', '0.0.0.0', '--port', '5000'],
        env=env,
        cwd=project_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(3)

    yield process

    process.terminate()
    process.wait()


@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def app_url():
    return "http://localhost:5000"


@pytest.fixture(scope="session")
def admin_user(app_server):
    """Create admin user for E2E tests."""
    import requests
    from app import create_app, db
    from app.data.models import User

    app = create_app()
    with app.app_context():
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
        yield {"username": "admin", "password": "admin123"}
