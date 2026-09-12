from fastapi import FastAPI, HTTPException

from backend.database import test_database_connection

app = FastAPI(
    title="Cloud Data Platform API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "status": "online",
        "service": "Cloud Data Platform API"
    }


@app.get("/health")
def health():
    try:
        database_status = test_database_connection()

        if database_status == 1:
            return {
                "status": "healthy",
                "api": "online",
                "database": "connected"
            }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "api": "online",
                "database": "disconnected"
            }
        )