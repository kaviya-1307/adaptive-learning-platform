from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    code = Column(Text, nullable=False)
    language = Column(String(20), default="python", nullable=False)
    status = Column(String(50), nullable=False)  # 'Accepted', 'Wrong Answer', 'Runtime Error', 'Time Limit Exceeded'
    passed_test_cases = Column(Integer, default=0, nullable=False)
    total_test_cases = Column(Integer, default=0, nullable=False)
    execution_time_ms = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")

    def __repr__(self) -> str:
        return f"<Submission id={self.id} user_id={self.user_id} problem_id={self.problem_id} status='{self.status}'>"
