import datetime
from typing import Iterable

from pydantic import BaseModel

from src.domain.project import Project
from src.domain.prompt import Prompt
from src.domain.recommendation import Recommendation


class MessageSchema(BaseModel):
    role: str
    content: str


class UsageSchema(BaseModel):
    prompt_tokens: int
    total_tokens: int
    tokens_per_second: float
    completion_tokens: int


class TimestampsSchema(BaseModel):
    request_time: datetime.datetime
    start_time_generation: datetime.datetime
    end_time_generation: datetime.datetime
    queue_wait_time: float
    generation_time: float


class ChoiceSchema(BaseModel):
    index: int
    message: MessageSchema


class ResponseSchema(BaseModel):
    request_id: int
    response_id: int
    model: str
    provider: str
    choices: list[ChoiceSchema]
    usage: UsageSchema
    timestamps: TimestampsSchema


class RequestSchema(BaseModel):
    model: str = "mistral-nemoinstruct-2407"
    messages: list[MessageSchema]
    max_tokens: int = 1_000
    temperature: float = 0.3


class LLMAdapter:
    async def send_project(self, project: Project):
        pass

    async def send_prompts(self, prompts: Iterable[Prompt]) -> list[Recommendation]:
        pass

    async def create_context(self, context_id: str):
        pass

    async def clear_context(self, context_id: str):
        pass
