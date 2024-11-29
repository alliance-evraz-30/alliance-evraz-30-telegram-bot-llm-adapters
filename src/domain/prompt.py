from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict

from src.enums import TargetLanguage

PromptId = UUID


class Prompt(BaseModel):
    id: PromptId = Field(default_factory=uuid4)
    title: str = "NotMatter"
    content: str
    importance: int = 0
    language: TargetLanguage = TargetLanguage.Python

    model_config = ConfigDict(frozen=True)

