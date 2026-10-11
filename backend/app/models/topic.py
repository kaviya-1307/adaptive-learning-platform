from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    order_index = Column(Integer, default=0, nullable=False)

    # Relationships
    problems = relationship("Problem", back_populates="topic", cascade="all, delete-orphan")
    knowledge_states = relationship("LearnerKnowledgeState", back_populates="topic", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Topic id={self.id} name='{self.name}'>"
