from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Calculator Agent" in response.text


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_calculate_percentage() -> None:
    response = client.post(
        "/api/calculate",
        json={"query": "calculate 20% of 8500"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "task": "percentage calculation",
        "tool": "calculator",
        "answer": 1700,
        "expression": "(20 / 100) * 8500",
        "error": None,
    }


def test_calculate_returns_agent_error() -> None:
    response = client.post("/api/calculate", json={"query": "write me a poem"})
    assert response.status_code == 200
    assert response.json()["answer"] is None
    assert response.json()["error"]
