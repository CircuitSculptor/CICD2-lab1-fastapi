from fastapi import FastAPI

app = FastAPI(title="Lab 1 - FastAPI User API")

@app.get("/health")
def health():
    return{"status": "ok"}