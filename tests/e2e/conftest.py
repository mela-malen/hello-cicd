import pytest
from playwright.sync_api import Browser, Playwright


@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def playwright():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        yield p
