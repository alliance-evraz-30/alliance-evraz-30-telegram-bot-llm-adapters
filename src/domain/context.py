from pydantic import BaseModel

ContextId = int


class Context(BaseModel):
    id: ContextId
    value: str
