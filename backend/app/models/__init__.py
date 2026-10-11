"""
SQLAlchemy models module.
Exports all database tables for metadata discovery and migrations.
"""
from app.core.database import Base
from app.models.user import User
from app.models.onboarding import OnboardingProfile
from app.models.topic import Topic
from app.models.problem import Problem
from app.models.test_case import TestCase
from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.submission import Submission
from app.models.learner_knowledge_state import LearnerKnowledgeState
from app.models.learner_concept_state import LearnerConceptState
from app.models.recommendation import Recommendation

__all__ = [
    "Base",
    "User",
    "OnboardingProfile",
    "Topic",
    "Problem",
    "TestCase",
    "DiagnosticAttempt",
    "Submission",
    "LearnerKnowledgeState",
    "LearnerConceptState",
    "Recommendation",
]
