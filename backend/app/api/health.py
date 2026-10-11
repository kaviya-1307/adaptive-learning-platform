from fastapi import APIRouter
from app.core.database import check_database_connection

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check endpoint to verify backend service availability.
    """
    db_status = check_database_connection()
    return {
        "status": "ok",
        "service": "adaptive-learning-platform",
        "database": db_status["message"]
    }
