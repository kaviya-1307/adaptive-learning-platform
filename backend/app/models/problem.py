from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    difficulty = Column(String(20), nullable=False)  # 'Easy', 'Medium', 'Hard'
    description_markdown = Column(Text, nullable=False)
    constraints_markdown = Column(Text, nullable=True)
    starter_code_python = Column(Text, nullable=False)
    reference_solution_python = Column(Text, nullable=True)
    starter_code_java = Column(Text, nullable=True)
    reference_solution_java = Column(Text, nullable=True)
    starter_code_cpp = Column(Text, nullable=True)
    reference_solution_cpp = Column(Text, nullable=True)
    starter_code_javascript = Column(Text, nullable=True)
    reference_solution_javascript = Column(Text, nullable=True)
    order_index = Column(Integer, default=0, nullable=False)
    is_diagnostic = Column(Boolean, default=False, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @property
    def supported_languages(self) -> list:
        langs = ["python"]
        if self.starter_code_java:
            langs.append("java")
        if self.starter_code_cpp:
            langs.append("cpp")
        if self.starter_code_javascript:
            langs.append("javascript")
        return langs

    # Relationships
    topic = relationship("Topic", back_populates="problems")
    test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="problem", cascade="all, delete-orphan")
    diagnostic_attempts = relationship("DiagnosticAttempt", back_populates="problem", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="problem", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Problem id={self.id} title='{self.title}' difficulty='{self.difficulty}'>"
