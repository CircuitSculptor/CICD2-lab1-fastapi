from fastapi import FastAPI, HTTPException, status, Response
import pytest

def user_payload(
    #uid=1,
    name="Bartek",
    email="bartek@atu.ie",
    age=21,
    student_id="G1234567", # Using G as we are in Galway, not Sligo
):
    return {
        #"user_id": uid,
        "name": name,
        "email": email,
        "age": age,
        "student_id": student_id,
    }
    

def test_create_user_returns_201(client):
    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 201
    data = response.json()
    # Valid data
    #assert data["user_id"] == 1
    assert data["name"] == "Bartek"
    assert data["email"] == "bartek@atu.ie"

    # Invalid data
    #assert data["user_id"] == 10
    #assert data["name"] == "B"
    #assert data["email"] == "bk@atu.ie"


def test_duplicate_user_id_returns_409(client):
    client.post("/api/users", json=user_payload()) #uid=2

    response = client.post("/api/users", json=user_payload()) #uid=2

    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()


@pytest.mark.parametrize(
    "bad_student_id",
    ["1234567", "g1234567", "G123", "G12345678"],
)
def test_bad_student_id_returns_422(client, bad_student_id):
    response = client.post(
        "/api/users",
        json=user_payload(student_id=bad_student_id),
    )

    assert response.status_code == 422


def test_get_users_return_created_users(client):
    client.post("/api/users", json=user_payload(name="Bob", email="bob@atu.ie")) #uid=10

    response = client.get("/api/users")
    user_id = response.json()[0]["id"]
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == user_id
    assert data[0]["name"] == "Bob"


def test_get_existing_user_returns_200(client):
    data = client.post("/api/users", json=user_payload()) #uid=11
    user_id = data.json()["id"]
    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_missing_user_returns_404(client):
    response = client.get("/api/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_existing_user_returns_204(client):
    data = client.post("/api/users", json=user_payload()) #uid=20
    user_id = data.json()["id"]
    response = client.delete(f"/api/users/{user_id}")

    assert response.status_code == 204
    assert response.content == b''

def test_delete_missing_user_returns_404(client):
    response = client.delete("/api/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_deleted_user_can_no_longer_be_retrieved(client):
    data = client.post("/api/users", json=user_payload()) #uid=21
    user_id = data.json()["id"]

    client.delete(f"/api/users/{user_id}")
    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 404


def test_get_users(client):
    client.post("/api/users", json=user_payload())

    response = client.get("/api/users")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["student_id"] == "G1234567"

def test_get_user_by_id(client):
    created = client.post(
        "/api/users",
        json=user_payload(),
    ).json()
    user_id = created["id"]

    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["email"] == "bartek@atu.ie"


def test_get_missiing_user_returns_404(client):
    response = client.get("/api/users/999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_user(client):
    created = client.post(
        "/api/users",
        json=user_payload(),
    ).json()

    user_id = created["id"]

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 404


def test_delete_missing_user_returns_404(client):
    response = client.delete("/api/users/999")

    assert response.status_code == 404