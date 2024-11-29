from typing import Iterable

from src.domain.context import Context, ContextId
from src.domain.prompt import Prompt
from src.domain.recommendation import Recommendation


class ContextService:
    async def create_one(self, context: Context):
        pass

    async def get_one_by_id(self, context_id: ContextId) -> Context:
        pass

    async def update_one(self, context: Context) -> None:
        pass

    async def clear_one(self, context_id: ContextId):
        pass


class ContextLLMService:
    async def summarize(self, context: Context) -> Context:
        pass

    async def combine_context_with_prompts(self, context: Context, prompts: Iterable[Prompt]) -> Context:
        pass

    async def combine_context_with_recommendations(self, context: Context, recs: list[Recommendation]) -> Context:
        pass

    async def send_context(self, context: Context) -> list[Recommendation]:
        pass
