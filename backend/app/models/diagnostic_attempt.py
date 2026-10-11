from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class DiagnosticAttempt(Base):
    __tablename__ = "diagnostic_attempts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    is_solved = Column(Boolean, default=False, nullable=False)
    attempts_count = Column(Integer, default=1, nullable=False)
    time_spent_seconds = Column(Integer, default=0, nullable=False)
    code_submitted = Column(Text, nullable=True)
    language = Column(String(20), default="python", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="diagnostic_attempts")
    problem = relationship("Problem", back_populates="diagnostic_attempts")

    def __repr__(self) -> str:
        return f"<DiagnosticAttempt id={self.id} user_id={self.user_id} problem_id={self.problem_id} solved={self.is_solved}>"
