from urllib.parse import urlparse

from async_pymongo import AsyncClient

from src import config
from src.adapters.repos.context_repo import ContextRepo
from src.adapters.repos.lllm_adapter import LLMAdapter
from src.adapters.repos.project_repo import ProjectRepo
from src.adapters.repos.prompt_repo import PromptRepo
from src.services.context_service import ContextService, ContextLLMService
from src.services.project_services import ProjectService
from src.services.prompt_services import PromptService
from src.services.startup_services import StartupService


class Bootstrap:
    def __init__(self):
        self._database = None
        self._project_repo = None
        self._prompt_repo = None
        self._llm_adapter = None
        self._prompt_service = None
        self._project_service = None
        self._startup_service = None
        self._context_service = None
        self._context_llm_service = None
        self._context_repo = None

    def database(self):
        if not self._database:
            parsed_url = urlparse(config.DB_URL)
            username = parsed_url.username
            password = parsed_url.password
            host = parsed_url.hostname
            port = parsed_url.port
            client = AsyncClient(host=host, port=port, username=username, password=password)
            self._database = client["evraz_back"]
        return self._database

    def project_repo(self) -> ProjectRepo:
        if not self._project_repo:
            self._project_repo = ProjectRepo(self.database())
        return self._project_repo

    def project_service(self) -> ProjectService:
        if not self._project_service:
            self._project_service = ProjectService(self.project_repo(), config.EXTRACT_DIR)
        return self._project_service

    def prompt_repo(self) -> PromptRepo:
        if not self._prompt_repo:
            self._prompt_repo = PromptRepo(self.database())
        return self._prompt_repo

    def llm_adapter(self) -> LLMAdapter:
        if not self._llm_adapter:
            self._llm_adapter = LLMAdapter()
        return self._llm_adapter

    def startup_service(self) -> StartupService:
        if not self._startup_service:
            self._startup_service = StartupService(self.prompt_repo())
        return self._startup_service

    def prompt_service(self) -> PromptService:
        if not self._prompt_service:
            self._prompt_service = PromptService(self.llm_adapter(), self.prompt_repo())
        return self._prompt_service

    def context_service(self) -> ContextService:
        if not self._context_service:
            self._context_service = ContextService(self.context_repo())
        return self._context_service

    def context_repo(self):
        if not self._context_repo:
            self._context_repo = ContextRepo(self.database())
        return self._context_repo

    def context_llm_service(self) -> ContextLLMService:
        if not self._context_llm_service:
            self._context_llm_service = ContextLLMService(self.llm_adapter())
        return self._context_llm_service


container = Bootstrap()


def get_container():
    return container
