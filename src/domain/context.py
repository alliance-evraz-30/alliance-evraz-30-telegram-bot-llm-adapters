from uuid import UUID, uuid4

from pydantic import BaseModel, Field

ContextId = UUID


class Context(BaseModel):
    id: ContextId = Field(default_factory=uuid4)
    content: str
