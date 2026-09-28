from fastapi import FastAPI, HTTPException, status, Response
import pytest

def user_payload(
    uid=1,
    name="Bartek",
    email="bartek@atu.ie",
    age=21,
    student_id="G1234567", # Using G as we are in Galway, not Sligo
):
    return {
        "user_id": uid,
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
    assert data["user_id"] == 1
    assert data["name"] == "Bartek"
    assert data["email"] == "bartek@atu.ie"

    # Invalid data
    #assert data["user_id"] == 10
    #assert data["name"] == "B"
    #assert data["email"] == "bk@atu.ie"


def test_duplicate_user_id_returns_409(client):
    client.post("/api/users", json=user_payload(uid=2))

    response = client.post("/api/users", json=user_payload(uid=2))

    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()


@pytest.mark.parametrize(
    "bad_student_id",
    ["1234567", "g1234567", "G123", "G12345678"],
)
def test_bad_student_id_returns_422(client, bad_student_id):
    response = client.post(
        "/api/users",
        json=user_payload(uid=3, student_id=bad_student_id),
    )

    assert response.status_code == 422