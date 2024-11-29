from urllib.parse import urlparse

from async_pymongo import AsyncClient

from src import config
from src.adapters.repos.project_repo import ProjectRepo
from src.adapters.repos.prompt_repo import PromptRepo
from src.services.project_services import ProjectService
from src.services.startup_services import StartupService


class Bootstrap:
    def __init__(self):
        self._database = None
        self._project_repo = None
        self._prompt_repo = None
        self._project_service = None
        self._startup_service = None

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

    def startup_service(self) -> StartupService:
        if not self._startup_service:
            self._startup_service = StartupService(self.prompt_repo())
        return self._startup_service


container = Bootstrap()


def get_container():
    return container
