from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class UserRole:
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"
    ALL_ROLES = {STUDENT, ADMIN}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default=UserRole.STUDENT, server_default=UserRole.STUDENT, nullable=False)
    diagnostic_completed = Column(Boolean, default=False, server_default='0', nullable=False)
    diagnostic_exempt = Column(Boolean, default=True, server_default='0', nullable=False)
    diagnostic_score = Column(Integer, nullable=True)
    diagnostic_total = Column(Integer, nullable=True)
    diagnostic_completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    onboarding_profile = relationship("OnboardingProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    diagnostic_attempts = relationship("DiagnosticAttempt", back_populates="user", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    knowledge_states = relationship("LearnerKnowledgeState", back_populates="user", cascade="all, delete-orphan")
    concept_states = relationship("LearnerConceptState", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.id} email='{self.email}'>"
