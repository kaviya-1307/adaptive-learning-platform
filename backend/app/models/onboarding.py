from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class OnboardingProfile(Base):
    __tablename__ = "onboarding_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    learning_goal = Column(String(100), nullable=False)  # e.g., 'placement_prep', 'interview_prep', 'learn_dsa', 'competitive_programming'
    experience_level = Column(String(50), nullable=False)  # 'beginner', 'intermediate', 'advanced'
    completed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="onboarding_profile")

    def __repr__(self) -> str:
        return f"<OnboardingProfile id={self.id} user_id={self.user_id} goal='{self.learning_goal}'>"
