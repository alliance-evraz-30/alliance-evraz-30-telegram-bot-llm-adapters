import datetime
from typing import Optional, Iterable

import aiohttp
from pydantic import BaseModel

from src.domain.context import Context
from src.domain.prompt import Prompt
from src.domain.recommendation import Recommendation


class MessageSchema(BaseModel):
    role: str
    content: str

    def __str__(self):
        return f"Message({self.content}) from role={self.role}"




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
    model: str = "mistral-nemo-instruct-2407"
    messages: list[MessageSchema]
    max_tokens: int = 1_000
    temperature: float = 0.3

    @classmethod
    def from_context(cls, context: Context):
        messages = [
            MessageSchema(role="system", content="Response in russian language only"),
            MessageSchema(role="user", content=context.content),
        ]
        return RequestSchema(
            messages=messages
        )


class LLMAdapter:
    def __init__(self):
        self._BASE_URL = "http://84.201.152.196:8020/v1/completions"
        self._headers = {
            "Authorization": "IoC25C2J4Efw6V2g1t74CxewKFzaXkdS",
            "Content-Type": "application/json",
        }

    async def _request(self, request: RequestSchema):
        url = self._BASE_URL
        data = request.model_dump(mode="json")
        async with aiohttp.ClientSession() as session:
            async with session.request("POST", url, json=data, headers=self._headers) as response:
                response.raise_for_status()
                return await response.json()

    async def send_prompts_with_context(
            self,
            prompts: Prompt | Iterable[Prompt],
            context=Optional[Context],
    ) -> list[Recommendation]:
        if isinstance(prompts, Prompt):
            prompts = [prompts]

        messages = [
            MessageSchema(role="system", content="Response in russian language only")
        ]
        if context and context.content:
            messages.append(
                MessageSchema(role="system", content=f"Use this context for answer: {context.content}")
            )

        for prompt in prompts:
            messages.append(
                MessageSchema(role="user", content=prompt.content)
            )

        self._log(messages)

        schema = RequestSchema(
            messages=messages
        )
        json_data = await self._request(schema)
        response = ResponseSchema(**json_data)
        result = []
        for choice in response.choices:
            result.append(Recommendation(content=choice.message.content))
        return result

    async def send_context(self, context: Context) -> list[Recommendation]:
        json_data = await self._request(
            RequestSchema.from_context(context)
        )
        response = ResponseSchema(**json_data)
        result = []
        for choice in response.choices:
            result.append(Recommendation(content=choice.message.content))
        return result

    @staticmethod
    def _log(messages: list[MessageSchema]):
        print()
        print("Отправляю следующие сообщения в модель:")
        for msg in messages:
            print(f" - {msg}")
        print()
