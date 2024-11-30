import datetime
from enum import StrEnum
from pathlib import Path

import requests
from pydantic import BaseModel

from src.last.services import parse_project_structure, print_project_structure, transform_tree_leaves, read_file, \
    analyze_module_structure


class LayerName(StrEnum):
    Domain = "Domain"
    Ports = "Ports"
    Adapters = "Adapters"
    Infrastructure = "Infrastructure"


class Message(BaseModel):
    role: str
    content: str

    def __str__(self):
        return f"Message({self.content}) from role={self.role}"


class Usage(BaseModel):
    prompt_tokens: int
    total_tokens: int
    tokens_per_second: float
    completion_tokens: int


class Timestamps(BaseModel):
    request_time: datetime.datetime
    start_time_generation: datetime.datetime
    end_time_generation: datetime.datetime
    queue_wait_time: float
    generation_time: float


class Choice(BaseModel):
    index: int
    message: Message


class Response(BaseModel):
    request_id: int
    response_id: int
    model: str
    provider: str
    choices: list[Choice]
    usage: Usage
    timestamps: Timestamps


class Request(BaseModel):
    model: str = "mistral-nemo-instruct-2407"
    messages: list[Message]
    max_tokens: int = 1_000
    temperature: float = 0.3


class LLMAdapter:
    def __init__(self):
        self._BASE_URL = "http://84.201.152.196:8020/v1/completions"
        self._headers = {
            "Authorization": "IoC25C2J4Efw6V2g1t74CxewKFzaXkdS",
            "Content-Type": "application/json",
        }

    def _request(self, messages: list[Message]):
        request = Request(messages=messages)
        url = self._BASE_URL
        data = request.model_dump(mode="json")
        response = requests.post(url, json=data, headers=self._headers)
        response.raise_for_status()
        return response.json()

    def send_prompts(self, prompts: list[str], ) -> Response:
        messages = [
            # Message(role="user",
            #         content="Do you know what is Hexagonal architecture (also known as the Ports and Adapters Architecture)?"),
            # Message(role="user",
            #         content="If I send you a Python file, can you analyze which layer the code belongs to in the hexagonal architecture?"),

        ]
        for prompt in prompts:
            message = Message(role="user", content=prompt)
            messages.append(message)

        json_data = self._request(messages)
        response = Response(**json_data)
        return response


class GodService:
    def __init__(
            self,
            path: Path,
            exclude: set[str] = None,
            exclude_prefixes: set[str] = None,
    ):
        self._path = path
        self._exclude = exclude if exclude else set()
        self._exclude_prefixes = exclude_prefixes if exclude_prefixes else set()

        self._full_structure = {}  # Текст файла в конце
        self._short_structure = {}  # Путь к файлу в конце
        self._module_layer: dict[Path, LayerName] = {}

    def build(self):
        structure = parse_project_structure(self._path, self._exclude, self._exclude_prefixes)
        structure_with_inside = transform_tree_leaves(structure, lambda x: analyze_module_structure(read_file(x)))

        self._short_structure = structure
        self._full_structure = structure_with_inside

    def print_short_structure(self):
        print_project_structure(self._full_structure)


def main():
    project_path = Path("D:/market/user")
    excludes = {
        ".idea",
        ".venv",
        ".git",
        ".gitignore",
        ".env",
    }

    builder = GodService(project_path, exclude=excludes)
    builder.build()
    builder.print_short_structure()

    # llm = LLMAdapter()
    # response = llm.send_prompts([
    #     "I have a python project. I use hexagonal architecture. I need code review. "
    #     "I want to know what architectural mistakes I have done. Tell me about algorythm should I use for the task"
    # ])
    #
    # print()
    # print("Results")
    # for x in response.choices:
    #     print(x.message.content)


if __name__ == "__main__":
    main()


