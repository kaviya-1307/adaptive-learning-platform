from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class LearnerKnowledgeState(Base):
    __tablename__ = "learner_knowledge_state"
    __table_args__ = (
        UniqueConstraint("user_id", "topic_id", name="uq_user_topic_knowledge"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    mastery_score = Column(Float, default=0.0, nullable=False)  # Range: [0.0, 1.0]
    confidence_score = Column(Float, default=0.0, nullable=False)  # Range: [0.0, 1.0]
    total_interactions = Column(Integer, default=0, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="knowledge_states")
    topic = relationship("Topic", back_populates="knowledge_states")

    def __repr__(self) -> str:
        return (
            f"<LearnerKnowledgeState id={self.id} user_id={self.user_id} "
            f"topic_id={self.topic_id} mastery={self.mastery_score:.2f}>"
        )
