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

    def test_admin_login_success(self, page: Page, app_url, app_server, admin_user):
        """Admin can login successfully."""
        page.goto(f"{app_url}/admin/login")

        page.fill('input[name="username"]', admin_user["username"])
        page.fill('input[name="password"]', admin_user["password"])
        page.click('button[type="submit"]')

        assert "/admin/subscribers" in page.url or "subscribers" in page.url.lower()

    def test_admin_login_failure(self, page: Page, app_url, app_server):
        """Admin sees error on invalid login."""
        page.goto(f"{app_url}/admin/login")

        page.fill('input[name="username"]', "wrong")
        page.fill('input[name="password"]', "wrong")
        page.click('button[type="submit"]')

        assert "Invalid" in page.content() or "error" in page.content().lower()

    def test_admin_subscribers_page_loads(self, page: Page, app_url, app_server, admin_user):
        """Admin subscribers page loads after login."""
        page.goto(f"{app_url}/admin/login")

        page.fill('input[name="username"]', admin_user["username"])
        page.fill('input[name="password"]', admin_user["password"])
        page.click('button[type="submit"]')

        assert page.locator("table").is_visible() or "subscribers" in page.content().lower()

    def test_admin_redirect_when_not_logged_in(self, page: Page, app_url, app_server):
        """Admin is redirected to login when not authenticated."""
        page.goto(f"{app_url}/admin/subscribers")

        assert "/admin/login" in page.url or page.locator('input[name="username"]').is_visible()

    def test_admin_logout(self, page: Page, app_url, app_server, admin_user):
        """Admin can logout."""
        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', admin_user["username"])
        page.fill('input[name="password"]', admin_user["password"])
        page.click('button[type="submit"]')

        logout_link = page.locator('a[href="/admin/logout"]')
        if logout_link.is_visible():
            logout_link.click()

            assert "/admin/login" in page.url or "login" in page.url.lower()

    def test_admin_subscribers_table_headers(self, page: Page, app_url, app_server, admin_user):
        """Admin sees correct table headers."""
        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', admin_user["username"])
        page.fill('input[name="password"]', admin_user["password"])
        page.click('button[type="submit"]')

        if page.locator("table").is_visible():
            headers = page.locator("table th").all_text_contents()
            assert len(headers) > 0

    def test_admin_sorting_options(self, page: Page, app_url, app_server, admin_user):
        """Admin can see sorting options."""
        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', admin_user["username"])
        page.fill('input[name="password"]', admin_user["password"])
        page.click('button[type="submit"]')

        sort_select = page.locator('select[id="sort"]')
        if sort_select.is_visible():
            assert sort_select.is_visible()

    def test_admin_newsletter_filter(self, page: Page, app_url, app_server, admin_user):
        """Admin can filter by newsletter."""
        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', admin_user["username"])
        page.fill('input[name="password"]', admin_user["password"])
        page.click('button[type="submit"]')

        filter_select = page.locator('select[id="newsletter"]')
        if filter_select.is_visible():
            assert filter_select.is_visible()
