from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_tenant_lists_only_own_rows() -> None:
    response = client.get("/v1/matters", headers={"X-Tenant-Id": "1"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["tenant_id"] == 1


def test_cross_tenant_lookup_returns_404() -> None:
    response = client.get("/v1/matters/2", headers={"X-Tenant-Id": "1"})
    assert response.status_code == 404
