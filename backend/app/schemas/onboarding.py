from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

LearningGoalType = Literal[
    "placement_prep",
    "interview_prep",
    "learn_dsa",
    "competitive_programming"
]

ExperienceLevelType = Literal[
    "beginner",
    "intermediate",
    "advanced"
]


class OnboardingCreate(BaseModel):
    learning_goal: str = Field(
        ...,
        description="Target DSA learning goal (placement_prep, interview_prep, learn_dsa, competitive_programming)"
    )
    experience_level: str = Field(
        ...,
        description="Self-reported coding experience level (beginner, intermediate, advanced)"
    )


class OnboardingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    learning_goal: str
    experience_level: str
    completed_at: datetime
    initial_mastery_applied: float = 0.5
