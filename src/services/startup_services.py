from src.adapters.repos.prompt_repo import PromptRepo
from src.domain.prompt import Prompt
from src.enums import TargetLanguage

PROMPTS: list[Prompt] = [
    Prompt(
        title="Temp",
        value="prompt_string",
        importance=10,
        language=TargetLanguage.Python,
    )
]


class StartupService:
    def __init__(
            self,
            prompt_repo: PromptRepo,
    ):
        self._prompt_repo = prompt_repo

    async def _create_prompts(self):
        await self._prompt_repo.remove_all()
        if PROMPTS:
            await self._prompt_repo.add_many(PROMPTS)

    async def execute(self):
        await self._create_prompts()
