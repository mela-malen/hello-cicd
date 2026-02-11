#!/usr/bin/env python3
"""Quick production smoke test using Playwright."""
import sys
from playwright.sync_api import sync_playwright

def test_production(url):
    """Test production environment."""
    print(f"Testing production: {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Test homepage
        print("  Testing homepage...")
        page.goto(url)
        assert "CM Corp" in page.title(), "Homepage title not found"
        print("  ✓ Homepage loads")
        
        # Test subscribe page
        print("  Testing subscribe page...")
        page.goto(f"{url}/subscribe")
        assert page.locator('input[name="email"]').is_visible(), "Email input not visible"
        assert page.locator('input[name="name"]').is_visible(), "Name input not visible"
        print("  ✓ Subscribe page loads")
        
        # Test form submission
        import uuid
        email = f"test-{uuid.uuid4().hex[:8]}@example.com"
        print(f"  Testing form submission with {email}...")
        page.fill('input[name="email"]', email)
        page.fill('input[name="name"]', "Test User")
        page.click('label:has(input[name="nl_kost"])')
        page.click('button[type="submit"]')
        
        # Should show thank you page
        assert "You're In" in page.title() or "In!" in page.text_content("h1"), "Thank you page not shown"
        print(f"  ✓ Form submission works")
        
        browser.close()
        print("\n✅ All production tests passed!")
        return True

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    try:
        test_production(url)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
