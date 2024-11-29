from uuid import UUID

from pydantic import BaseModel, ConfigDict

RecommendationId = UUID


class Recommendation(BaseModel):
    id: RecommendationId

    model_config = ConfigDict(frozen=True)

