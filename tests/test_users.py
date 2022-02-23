import pytest

@pytest.mark.usefixtures("create_items")
class TestUserRouters:
    @pytest.fixture
    def login(self, client):
        response = client.post("/login", json={"login": "admin", "password": "admin"})
        assert response.status_code == 200, response.text
        yield

    def test_get_current_user_auth(self, client, login):
        response = client.get("/users/current")
        assert response.status_code == 200, response.text
