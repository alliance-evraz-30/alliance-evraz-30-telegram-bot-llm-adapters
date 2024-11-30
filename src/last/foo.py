import datetime
import json
from enum import StrEnum

import requests
from pydantic import BaseModel

from src.last import prompts
from src.last.module_analys import analyze_module_structure
from src.last.services import *


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

    def print(self):
        print()
        for choice in self.choices:
            print(choice.message.content)

    def get_content(self):
        for choice in self.choices:
            return choice.message.content


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

    def send_prompts(self, data: list[str]) -> Response:
        messages = []
        for prompt in data:
            message = Message(role="user", content=prompt)
            messages.append(message)

        json_data = self._request(messages)
        response = Response(**json_data)
        return response


class Pipeline:
    def __init__(self, root: Path, excludes: set[str]):
        self._root = root
        self._excludes = excludes
        self._structure = {}
        self._paths = []

    def convert_path_to_simple_structure(self):
        self._structure = parse_project_structure(self._root, self._excludes)
        return self

    def parse_file_paths(self):
        _ = transform_tree_leaves(self._structure, lambda path: self._paths.append(path))
        llm = LLMAdapter()
        prompts_to_send = [
            prompts.ARCHITECTURE_CONTEXT_PROMPT,
            prompts.STRUCTURE_FROM_PATHS_ONLY,
            json.dumps([str(get_relative_path(self._root, x)) for x in self._paths])

        ]
        response = llm.send_prompts(prompts_to_send)
        response.print()

        return self

    def divide_simple_structure_into_layers(self):
        llm = LLMAdapter()
        structure = transform_tree_leaves(self._structure, lambda path: str(path))
        data = json.dumps(structure)

        prompts_to_send = [
            prompts.ARCHITECTURE_CONTEXT_PROMPT,
            prompts.DIVIDE_DOMAIN_LAYER_PROMPT,
            data,
        ]

        response = llm.send_prompts(prompts_to_send)
        content = response.get_content()
        domain_structure = extract_json(content)
        print(domain_structure, end="\n\n")

        prompts_to_send = [
            prompts.ARCHITECTURE_CONTEXT_PROMPT,
            prompts.DIVIDE_APPLICATION_LAYER_PROMPT,
            data,
        ]

        response = llm.send_prompts(prompts_to_send)
        content = response.get_content()
        application_structure = extract_json(content)
        print(application_structure, end="\n\n")

        return self

    def code_structure(self):
        self._structure = transform_tree_leaves(self._structure, lambda path: read_file(path))
        return self

    def get_structure(self):
        return self._structure


def main():
    project_path = Path("D:/hakatons/files/RESTfulAPI-master 2/RESTfulAPI-master")
    excludes = {
        ".idea",
        ".venv",
        ".git",
        ".gitignore",
        ".env",
        "__pycache__",
    }
    pipeline = Pipeline(project_path, excludes)

    structure = (
        pipeline
        .convert_path_to_simple_structure()
        # .divide_simple_structure_into_layers()
        .parse_file_paths()
        .get_structure()
    )


def converter(root: Path, excludes: set[str]) -> dict:
    structure = parse_project_structure(root, excludes)
    paths = get_leaves_from_tree(structure)

    result = {}
    for path in paths:
        relative_path = get_relative_path(root, path)
        code = read_file(path)
        if code:
            result[str(relative_path)] = analyze_module_structure(code)
    result = clean_empty_keys(result)
    print_project_structure(result)
    return result


def main2():
    project_path = Path("D:/hakatons/files/RESTfulAPI-master 2/RESTfulAPI-master")
    excludes = {
        ".idea",
        ".venv",
        ".git",
        ".gitignore",
        ".env",
        "__pycache__",
    }
    structure = converter(project_path, excludes)

    prompts_to_send = [
        prompts.ARCHITECTURE_CONTEXT_PROMPT,
        json.dumps(structure),
        *prompts.PROMPTS,
    ]

    llm = LLMAdapter()
    response = llm.send_prompts(prompts_to_send)
    content = response.get_content()

    response = llm.send_prompts(["Translate this text in russian: " + content])
    response.print()


if __name__ == "__main__":
    main2()
