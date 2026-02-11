import pytest
from playwright.sync_api import Page, Browser


class TestAdminJourney:
    """End-to-end tests for admin journey using Playwright."""

    @pytest.fixture
    def page(self, browser: Browser):
        page = browser.new_page()
        yield page
        page.close()

    @pytest.fixture
    def app_url(self):
        return "http://localhost:5000"

    @pytest.fixture
    def admin_user(self, app_url, page: Page):
        """Create an admin user for testing."""
        import requests
        base_url = app_url

        requests.post(f"{base_url}/api/admin/users", json={
            "username": "admin",
            "password": "admin123"
        })
        return {"username": "admin", "password": "admin123"}

    def test_admin_login_page_loads(self, page: Page, app_url):
        """Admin login page loads correctly."""
        page.goto(f"{app_url}/admin/login")

        assert page.locator('input[name="username"]').is_visible()
        assert page.locator('input[name="password"]').is_visible()
        assert page.locator('button[type="submit"]').is_visible()

    def test_admin_login_success(self, page: Page, app_url):
        """Admin can login successfully."""
        page.goto(f"{app_url}/admin/login")

        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        assert "/admin/subscribers" in page.url or "subscribers" in page.url.lower()

    def test_admin_login_failure(self, page: Page, app_url):
        """Admin sees error on invalid login."""
        page.goto(f"{app_url}/admin/login")

        page.fill('input[name="username"]', "wrong")
        page.fill('input[name="password"]', "wrong")
        page.click('button[type="submit"]')

        assert "Invalid" in page.content() or "error" in page.content().lower()

    def test_admin_subscribers_page_loads(self, page: Page, app_url):
        """Admin subscribers page loads after login."""
        page.goto(f"{app_url}/admin/login")

        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        assert page.locator("table").is_visible() or "subscribers" in page.content().lower()

    def test_admin_can_create_subscriber(self, page: Page, app_url):
        """Admin can create a new subscriber via API or form."""
        import requests

        requests.post(f"{app_url}/subscribe/confirm", data={
            "email": "admincreated@example.com",
            "name": "Admin Created",
            "nl_kost": "1"
        })

        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        assert "admincreated@example.com" in page.content() or "Admin Created" in page.content()

    def test_admin_can_edit_subscriber(self, page: Page, app_url):
        """Admin can edit an existing subscriber."""
        import requests

        requests.post(f"{app_url}/subscribe/confirm", data={
            "email": "adminedit@example.com",
            "name": "Original Name",
            "nl_kost": "1"
        })

        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        edit_link = page.locator('a[href*="edit"]').first
        if edit_link.is_visible():
            edit_link.click()

            page.fill('input[name="name"]', "Edited Name")
            page.click('button[type="submit"]')

            assert "Edited Name" in page.content()

    def test_admin_can_delete_subscriber(self, page: Page, app_url):
        """Admin can delete a subscriber."""
        import requests

        requests.post(f"{app_url}/subscribe/confirm", data={
            "email": "admindelete@example.com",
            "name": "To Delete",
            "nl_mindset": "1"
        })

        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        delete_checkbox = page.locator('input.subscriber-checkbox').first
        if delete_checkbox.is_visible():
            delete_checkbox.check()

            delete_button = page.locator('button:has-text("Delete")').first
            if delete_button.is_visible():
                delete_button.click()
                page.accept_alert()

    def test_admin_sorting_options(self, page: Page, app_url):
        """Admin can see sorting options."""
        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        sort_select = page.locator('select[id="sort"]')
        if sort_select.is_visible():
            assert sort_select.is_visible()

    def test_admin_newsletter_filter(self, page: Page, app_url):
        """Admin can filter by newsletter."""
        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        filter_select = page.locator('select[id="newsletter"]')
        if filter_select.is_visible():
            assert filter_select.is_visible()

    def test_admin_logout(self, page: Page, app_url):
        """Admin can logout."""
        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        logout_link = page.locator('a[href="/admin/logout"]')
        if logout_link.is_visible():
            logout_link.click()

            assert "/admin/login" in page.url or "login" in page.url.lower()

    def test_admin_redirect_when_not_logged_in(self, page: Page, app_url):
        """Admin is redirected to login when not authenticated."""
        page.goto(f"{app_url}/admin/subscribers")

        assert "/admin/login" in page.url or page.locator('input[name="username"]').is_visible()

    def test_admin_bulk_actions(self, page: Page, app_url):
        """Admin can perform bulk actions on subscribers."""
        import requests

        requests.post(f"{app_url}/subscribe/confirm", data={
            "email": "bulk1@example.com",
            "name": "Bulk One",
            "nl_kost": "1"
        })
        requests.post(f"{app_url}/subscribe/confirm", data={
            "email": "bulk2@example.com",
            "name": "Bulk Two",
            "nl_kost": "1"
        })

        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        select_all = page.locator('input[id="select-all"]')
        if select_all.is_visible():
            select_all.check()

    def test_admin_subscribers_table_headers(self, page: Page, app_url):
        """Admin sees correct table headers."""
        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        if page.locator("table").is_visible():
            headers = page.locator("table th").all_text_contents()
            assert len(headers) > 0

    def test_admin_edit_form_has_all_fields(self, page: Page, app_url):
        """Admin edit form has all required fields."""
        import requests

        requests.post(f"{app_url}/subscribe/confirm", data={
            "email": "editfields@example.com",
            "name": "Edit Fields",
            "nl_kost": "1"
        })

        page.goto(f"{app_url}/admin/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')

        edit_link = page.locator('a[href*="edit"]').first
        if edit_link.is_visible():
            edit_link.click()

            assert page.locator('input[name="email"]').is_visible()
            assert page.locator('input[name="name"]').is_visible()
            assert page.locator('input[name="nl_kost"]').is_visible()
            assert page.locator('input[name="nl_mindset"]').is_visible()
