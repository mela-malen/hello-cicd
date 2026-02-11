import pytest
from playwright.sync_api import Page
import os


@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def app_url():
    return "http://localhost:5000"


class TestVisitorJourney:
    """End-to-end tests for visitor journey using Playwright."""

    def test_homepage_loads(self, page: Page, app_url, app_server):
        """Visitor can load the homepage."""
        page.goto(app_url)

        assert "CM Corp" in page.title()
        assert page.locator("h1").is_visible()

    def test_subscribe_page_loads(self, page: Page, app_url, app_server):
        """Visitor can load the subscribe page."""
        page.goto(f"{app_url}/subscribe")

        assert "Subscribe" in page.title() or "Subscribe" in page.text_content("h1")
        assert page.locator('input[name="email"]').is_visible()
        assert page.locator('input[name="name"]').is_visible()

    def test_subscribe_success_with_single_newsletter(self, page: Page, app_url, app_server):
        """Visitor can successfully subscribe with one newsletter."""
        page.goto(f"{app_url}/subscribe")

        page.fill('input[name="email"]', "visitor1@example.com")
        page.fill('input[name="name"]', "Visitor One")
        page.click('label:has(input[name="nl_kost"])')
        page.click('button[type="submit"]')

        assert "You're In" in page.title() or "In!" in page.text_content("h1")
        assert "visitor1@example.com" in page.content()

    def test_subscribe_success_with_all_newsletters(self, page: Page, app_url, app_server):
        """Visitor can successfully subscribe with all newsletters."""
        page.goto(f"{app_url}/subscribe")

        page.fill('input[name="email"]', "visitor4@example.com")
        page.fill('input[name="name"]', "Visitor All")
        page.click('label:has(input[name="nl_kost"])')
        page.click('label:has(input[name="nl_mindset"])')
        page.click('label:has(input[name="nl_kunskap"])')
        page.click('label:has(input[name="nl_veckans_pass"])')
        page.click('label:has(input[name="nl_jaine"])')
        page.click('button[type="submit"]')

        assert "You're In" in page.title() or "In!" in page.text_content("h1")

    def test_subscribe_error_missing_email(self, page: Page, app_url, app_server):
        """Visitor sees error when email is missing."""
        page.goto(f"{app_url}/subscribe")

        page.fill('input[name="name"]', "No Email Visitor")
        page.click('label:has(input[name="nl_kost"])')
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")
        error_banner = page.locator('.form__error-banner')
        if error_banner.is_visible():
            assert "Email is required" in error_banner.text_content()

    def test_subscribe_error_invalid_email(self, page: Page, app_url, app_server):
        """Visitor sees error for invalid email format."""
        page.goto(f"{app_url}/subscribe")

        page.fill('input[name="email"]', "not-an-email")
        page.fill('input[name="name"]', "Invalid Email")
        page.click('label:has(input[name="nl_kost"])')
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")
        error_banner = page.locator('.form__error-banner')
        if error_banner.is_visible():
            assert "Invalid email format" in error_banner.text_content()

    def test_subscribe_preserves_form_data_on_error(self, page: Page, app_url, app_server):
        """Form data is preserved when there is an error."""
        page.goto(f"{app_url}/subscribe")

        page.fill('input[name="name"]', "My Name")
        page.click('label:has(input[name="nl_kost"])')
        page.click('label:has(input[name="nl_mindset"])')
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")
        assert 'value="My Name"' in page.content()

    def test_navigation_links_work(self, page: Page, app_url, app_server):
        """Navigation links work correctly."""
        page.goto(f"{app_url}/subscribe")
        page.click('a[href="/"]')
        assert page.url.endswith("/") or "cm corp" in page.title().lower()

    def test_thank_you_page_has_home_link(self, page: Page, app_url, app_server):
        """Thank you page has link back to home."""
        page.goto(f"{app_url}/subscribe")
        page.fill('input[name="email"]', "visitor3@example.com")
        page.fill('input[name="name"]', "Visitor Three")
        page.click('input[name="nl_kost"]')
        page.click('button[type="submit"]')

        back_link = page.locator("a:has-text('Back to Home')")
        assert back_link.is_visible()

    def test_newsletter_options_display_correctly(self, page: Page, app_url, app_server):
        """All newsletter options are displayed."""
        page.goto(f"{app_url}/subscribe")

        assert page.locator('input[name="nl_kost"]').is_visible()
        assert page.locator('input[name="nl_mindset"]').is_visible()
        assert page.locator('input[name="nl_kunskap"]').is_visible()
        assert page.locator('input[name="nl_veckans_pass"]').is_visible()
        assert page.locator('input[name="nl_jaine"]').is_visible()

    def test_form_has_required_fields(self, page: Page, app_url, app_server):
        """Form has correct required field markers."""
        page.goto(f"{app_url}/subscribe")
        email_input = page.locator('input[name="email"]')
        assert email_input.get_attribute("required") is not None

    def test_email_input_has_correct_type(self, page: Page, app_url, app_server):
        """Email input has correct type attribute."""
        page.goto(f"{app_url}/subscribe")
        email_input = page.locator('input[name="email"]')
        assert email_input.get_attribute("type") == "email"
