import httpx
from app.main import app
from app.product_client import get_product_fetcher

def fake_fetch_product(product_id: int) -> dict:
    return {"id": product_id, "name": "Laptop", "price": 899.0}

def provide_fake_product():
    return fake_fetch_product

def test_remote_product_success(client):
    app.dependency_overrides[get_product_fetcher] = provide_fake_product
    try:
        response = client.get("/api/products/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Laptop"
    finally:
        app.dependency_overrides.pop(get_product_fetcher, None)