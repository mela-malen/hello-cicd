import pytest


class TestSubscribeRoutes:
    def test_subscribe_page_loads(self, client):
        response = client.get("/subscribe")
        assert response.status_code == 200
        assert b"Subscribe" in response.data or b"Join" in response.data

    def test_subscribe_success(self, client, clean_db):
        response = client.post(
            "/subscribe/confirm",
            data={
                "email": "test1@example.com",
                "name": "Test User",
                "nl_kost": "1",
                "nl_mindset": "1",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Thank" in response.data or b"In!" in response.data

    def test_subscribe_with_all_newsletters(self, client, clean_db):
        response = client.post(
            "/subscribe/confirm",
            data={
                "email": "test2@example.com",
                "name": "Test User",
                "nl_kost": "1",
                "nl_mindset": "1",
                "nl_kunskap": "1",
                "nl_veckans_pass": "1",
                "nl_jaine": "1",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Thank" in response.data or b"In!" in response.data

    def test_subscribe_missing_email(self, client, clean_db):
        response = client.post(
            "/subscribe/confirm",
            data={
                "name": "Test User",
                "nl_kost": "1",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"Email is required" in response.data

    def test_subscribe_invalid_email(self, client, clean_db):
        response = client.post(
            "/subscribe/confirm",
            data={
                "email": "not-an-email",
                "name": "Test User",
                "nl_kost": "1",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"Invalid email format" in response.data

    def test_subscribe_preserves_form_data_on_error(self, client, clean_db):
        response = client.post(
            "/subscribe/confirm",
            data={
                "email": "",
                "name": "My Name",
                "nl_kost": "1",
            },
            follow_redirects=False,
        )
        assert response.status_code == 200
        assert b"My Name" in response.data


class TestPublicRoutes:
    def test_index_page(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_subscribe_link_exists(self, client):
        response = client.get("/")
        assert b"subscribe" in response.data.lower() or b"Subscribe" in response.data
