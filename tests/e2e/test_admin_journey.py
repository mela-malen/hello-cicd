import pytest
from playwright.sync_api import Page


class TestAdminJourney:
    """End-to-end tests for admin journey using Playwright."""

    def test_admin_login_page_loads(self, page: Page, app_url, app_server):
        """Admin login page loads correctly."""
        page.goto(f"{app_url}/admin/login")

        assert page.locator('input[name="username"]').is_visible()
        assert page.locator('input[name="password"]').is_visible()
        assert page.locator('button[type="submit"]').is_visible()

    def test_admin_login_failure(self, page: Page, app_url, app_server):
        """Admin sees error on invalid login."""
        page.goto(f"{app_url}/admin/login")

        page.fill('input[name="username"]', "wrong")
        page.fill('input[name="password"]', "wrong")
        page.click('button[type="submit"]')

        assert "Invalid" in page.content() or "error" in page.content().lower()

    def test_admin_redirect_when_not_logged_in(self, page: Page, app_url, app_server):
        """Admin is redirected to login when not authenticated."""
        page.goto(f"{app_url}/admin/subscribers")

        assert "/admin/login" in page.url or page.locator('input[name="username"]').is_visible()
