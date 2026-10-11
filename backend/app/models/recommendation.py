from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    predicted_success_prob = Column(Float, default=0.0, nullable=False)
    explanation_text = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Phase 2 Step 3 Concept-Level Recommendation Metadata
    recommendation_score = Column(Float, nullable=True)
    concept_gap = Column(Float, nullable=True)
    difficulty_fit = Column(Float, nullable=True)
    primary_weak_concept = Column(String(100), nullable=True)

    # Relationships
    user = relationship("User", back_populates="recommendations")
    problem = relationship("Problem", back_populates="recommendations")

    def __repr__(self) -> str:
        return (
            f"<Recommendation id={self.id} user_id={self.user_id} "
            f"problem_id={self.problem_id} active={self.is_active}>"
        )
