from pathlib import Path
from uuid import UUID, uuid4

from pydantic import Field, ConfigDict, BaseModel

from src.domain.context import ContextId
from src.enums import TargetLanguage

ProjectId = UUID


class Project(BaseModel):
    id: ProjectId = Field(default_factory=uuid4)
    title: str
    path: Path
    structure: dict
    language: TargetLanguage = TargetLanguage.Python
    context_id: ContextId

    model_config = ConfigDict(frozen=True)
