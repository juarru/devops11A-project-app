import pytest
from app import app, db
from unittest.mock import MagicMock, patch


@pytest.fixture
def client():
    """Creates a Flask test client"""
    app.config["TESTING"] = True

    # Mock Redis to return a fake counter value instead of connecting
    # to a real Redis server
    db.incr = MagicMock(return_value=1)

    with app.test_client() as client:
        yield client


def test_index_success(client):
    """Successful test: Verifies that the route '/' responds with
    status code 200
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "La página ha sido cargada" in response.get_data(as_text=True)


def test_index_exception(client):
    with patch("app.es.index", side_effect=Exception("Fallo en Index")):
        response = client.get("/")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Fallo en Index"


def test_not_found(client):
    """Failed test: Tries to access a non-existent route"""
    response = client.get("/notfound")
    assert response.status_code == 404


def test_health_success(client):
    """Successful test: Verifies that the route '/health' responds with
    status code 200
    """
    response = client.get("/health")
    assert response.status_code == 200


def test_health_exception(client):
    with patch("app.es.index", side_effect=Exception("Fallo en Health")):
        response = client.get("/health")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Fallo en Health"


def test_logs_success(client):
    """Successful test: Verifies that the route '/logs' responds with
    status code 200
    """
    response = client.get("/logs")
    assert response.status_code == 200


def test_logs_exception(client):
    with patch(
        "app.es.search",
        side_effect=Exception("Fallo en Elasticsearch")
    ):
        response = client.get("/logs")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert data["error"] == "Fallo en Elasticsearch"


# Test that always fails intentionally to see what happens in pytest.
# Uncomment to see the result.
# def test_forced():
#     """Test that always fails intentionally"""
#     assert False, "This test is designed to fail"

# Test to see what happens in coverage when a function is not tested.
# Uncomment to see the result.
# def test_no_tested_function():
#     return "This function is not tested"
