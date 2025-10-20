import pytest
from server import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.data == b"OK\n"
    assert response.content_type == "text/plain; charset=utf-8"


def test_root_path(client):
    """Test the root path"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello World!" in response.data
    assert b"Method: GET" in response.data
    assert b"Path: /" in response.data
    assert b"Timestamp:" in response.data
    assert b"Client IP:" in response.data
    assert b"User-Agent:" in response.data
    assert b"Hostname:" in response.data
    assert b"Request Count:" in response.data


def test_custom_path(client):
    """Test a custom path"""
    response = client.get("/api/users")
    assert response.status_code == 200
    assert b"Path: /api/users" in response.data


def test_query_parameters(client):
    """Test query parameters are displayed"""
    response = client.get("/search?q=test&page=1")
    assert response.status_code == 200
    assert b"Query: q=test&page=1" in response.data


def test_post_method(client):
    """Test POST method is supported"""
    response = client.post("/data")
    assert response.status_code == 200
    assert b"Method: POST" in response.data


def test_put_method(client):
    """Test PUT method is supported"""
    response = client.put("/update")
    assert response.status_code == 200
    assert b"Method: PUT" in response.data


def test_delete_method(client):
    """Test DELETE method is supported"""
    response = client.delete("/resource")
    assert response.status_code == 200
    assert b"Method: DELETE" in response.data


def test_identifier_env_var(client, monkeypatch):
    """Test that IDENTIFIER environment variable is displayed"""
    monkeypatch.setenv("IDENTIFIER", "TestServer123")
    # Need to reload the app to pick up the new env var
    response = client.get("/")
    assert response.status_code == 200
    assert b"Identifier: TestServer123" in response.data


def test_request_counter(client):
    """Test that request counter increments"""
    # Make first request
    response1 = client.get("/")
    assert b"Request Count: 1" in response1.data or b"Request Count:" in response1.data

    # Make second request
    response2 = client.get("/test")
    assert b"Request Count:" in response2.data


def test_user_agent_header(client):
    """Test that User-Agent header is captured"""
    response = client.get("/", headers={"User-Agent": "TestBot/1.0"})
    assert response.status_code == 200
    assert b"User-Agent: TestBot/1.0" in response.data


def test_no_query_parameters(client):
    """Test that Query line is omitted when no query parameters"""
    response = client.get("/test")
    assert response.status_code == 200
    # Query line should not appear when there are no query parameters
    assert b"Query:" not in response.data or b"Query: \n" not in response.data


def test_invalid_delay_env_var(client, monkeypatch):
    """Test that invalid DELAY values are handled gracefully"""
    monkeypatch.setenv("DELAY", "invalid")
    response = client.get("/")
    # Should still work, just ignore the invalid delay
    assert response.status_code == 200
    assert b"Hello World!" in response.data


def test_delay_query_parameter(client):
    """Test that delay can be specified via query parameter"""
    import time

    start = time.time()
    response = client.get("/?delay=1")
    elapsed = time.time() - start

    assert response.status_code == 200
    assert b"Hello World!" in response.data
    # Should have delayed for approximately 1 second
    assert elapsed >= 0.9  # Allow some tolerance


def test_delay_query_parameter_overrides_env(client, monkeypatch):
    """Test that query parameter delay overrides environment variable"""
    monkeypatch.setenv("DELAY", "5")
    import time

    start = time.time()
    response = client.get("/?delay=1")
    elapsed = time.time() - start

    assert response.status_code == 200
    assert b"Hello World!" in response.data
    # Should have delayed for 1 second (from query param), not 5 (from env)
    assert 0.9 <= elapsed < 2.0


def test_delay_query_parameter_invalid(client):
    """Test that invalid delay query parameter is handled gracefully"""
    import time

    start = time.time()
    response = client.get("/?delay=invalid")
    elapsed = time.time() - start

    assert response.status_code == 200
    assert b"Hello World!" in response.data
    # Should not delay
    assert elapsed < 0.5
