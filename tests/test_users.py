from fastapi import FastAPI, HTTPException, status, Response

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