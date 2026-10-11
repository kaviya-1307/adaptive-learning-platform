"""
API routes package.
"""
from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.onboarding import router as onboarding_router
from app.api.problems import router as problems_router
from app.api.diagnostic import router as diagnostic_router
from app.api.submissions import router as submissions_router
from app.api.knowledge_state import router as knowledge_state_router
from app.api.recommendations import router as recommendations_router
from app.api.dashboard import router as dashboard_router
from app.api.roadmap import router as roadmap_router
from app.api.admin import router as admin_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(onboarding_router, prefix="/onboarding", tags=["Onboarding"])
api_router.include_router(problems_router, prefix="/problems", tags=["Problems"])
api_router.include_router(diagnostic_router, prefix="/diagnostic", tags=["Diagnostic"])
api_router.include_router(submissions_router, prefix="/submissions", tags=["Submissions"])
api_router.include_router(knowledge_state_router, prefix="/knowledge-state", tags=["Knowledge State"])
api_router.include_router(recommendations_router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(roadmap_router, prefix="/roadmap", tags=["Roadmap"])
api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])

__all__ = ["api_router"]
