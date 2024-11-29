from typing import Iterable, Optional

from src.adapters.repos.context_repo import ContextRepo
from src.adapters.repos.lllm_adapter import LLMAdapter
from src.domain.context import Context, ContextId
from src.domain.project import Project
from src.domain.prompt import Prompt
from src.domain.recommendation import Recommendation


class ContextService:
    def __init__(
            self,
            context_repo: ContextRepo,
    ):
        self._context_repo = context_repo

    async def create_one(self, context: Context):
        await self._context_repo.add_one(context)

    async def get_one_by_id(self, context_id: ContextId) -> Context:
        return await self._context_repo.get_one_by_id(context_id)

    async def update_one(self, context: Context) -> None:
        await self._context_repo.update_one(context)

    async def clear_one(self, context_id: ContextId):
        try:
            target = await self._context_repo.get_one_by_id(context_id)
            target.content = ""
            await self._context_repo.update_one(target)
        except LookupError:
            pass


class ContextLLMService:
    def __init__(
            self,
            llm_adapter: LLMAdapter,
    ):
        self._llm_adapter = llm_adapter

    async def summarize(self, context: Context) -> Context:
        raise NotImplemented

    async def combine_context_with_prompts(self, context: Context, prompts: Iterable[Prompt]) -> Context:
        raise NotImplemented

    async def combine_context_with_recommendations(self, context: Context, recs: list[Recommendation]) -> Context:
        new_value = context.content
        for rec in recs:
            new_value = new_value + "\n" + rec.content
        return Context(id=context.id, content=new_value)

    async def send_prompts_with_context(
            self,
            prompts: Iterable[Prompt],
            context: Optional[Context] = None
    ) -> list[Recommendation]:
        result = await self._llm_adapter.send_prompts_with_context(prompts, context)
        return result

    async def send_project(self, project: Project) -> Context:
        pass
