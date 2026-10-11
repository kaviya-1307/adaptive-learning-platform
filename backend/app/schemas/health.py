from typing import Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="ok", description="Service health status")
    service: str = Field(default="adaptive-learning-platform", description="Service identifier")
    database: Optional[str] = Field(default=None, description="Database connection status detail")
    version: str = Field(default="1.0.0", description="API version")
