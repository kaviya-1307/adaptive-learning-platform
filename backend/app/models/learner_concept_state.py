"""
Learner Concept State Model (Phase 2 Step 2).
Persists granular concept-level knowledge states for learners across all real Codeforces learning concepts:
- Bayesian smoothed mastery (M_c)
- Weakness score (1.0 - M_c)
- Concept confidence (min(1.0, interactions / K))
- 5-tier weakness level
- Interaction and solved counts
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class LearnerConceptState(Base):
    __tablename__ = "learner_concept_states"
    __table_args__ = (
        UniqueConstraint("user_id", "concept", name="uq_user_concept_state"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    concept = Column(String(100), nullable=False, index=True)
    mastery_score = Column(Float, default=0.5, nullable=False)   # Bayesian smoothed M_c
    weakness_score = Column(Float, default=0.5, nullable=False)  # W_c = 1 - M_c
    confidence_score = Column(Float, default=0.0, nullable=False) # C_c = min(1.0, interactions / K)
    weakness_level = Column(String(20), default="Moderate", nullable=False) # Very Low, Low, Moderate, High, Very High
    interactions = Column(Integer, default=0, nullable=False)     # N_c
    solved_count = Column(Integer, default=0, nullable=False)     # S_c
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="concept_states")

    def __repr__(self) -> str:
        return (
            f"<LearnerConceptState id={self.id} user_id={self.user_id} "
            f"concept='{self.concept}' mastery={self.mastery_score:.2f} weakness={self.weakness_score:.2f}>"
        )
