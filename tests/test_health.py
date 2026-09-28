from fastapi import FastAPI, HTTPException, status, Response

def test_heath(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status" : "ok"}
