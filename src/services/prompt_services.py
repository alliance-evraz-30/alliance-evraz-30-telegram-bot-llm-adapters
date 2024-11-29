from typing import Iterable

from src.adapters.repos.lllm_adapter import LLMAdapter
from src.adapters.repos.prompt_repo import PromptRepo
from src.domain.project import Project
from src.domain.prompt import Prompt
from src.domain.recommendation import Recommendation


class PromptService:
    def __init__(
            self,
            llm_adapter: LLMAdapter,
            prompt_repo: PromptRepo,
    ):
        self._llm_adapter = llm_adapter
        self._prompt_repo = prompt_repo

    async def send_project(self, project: Project):
        pass

    async def send_prompts(self, prompts: Iterable[Prompt]) -> list[Recommendation]:
        pass

    async def create_context(self, context_id: str):
        pass

    async def clear_context(self, context_id: str):
        pass
