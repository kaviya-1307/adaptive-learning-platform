from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False, nullable=False)
    order_index = Column(Integer, default=0, nullable=False)

    # Relationships
    problem = relationship("Problem", back_populates="test_cases")

    def __repr__(self) -> str:
        return f"<TestCase id={self.id} problem_id={self.problem_id} is_hidden={self.is_hidden}>"
