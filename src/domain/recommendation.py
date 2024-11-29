from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

RecommendationId = UUID


class Recommendation(BaseModel):
    id: RecommendationId = Field(default_factory=uuid4)
    importance: int
    content: str

    model_config = ConfigDict(frozen=True)
