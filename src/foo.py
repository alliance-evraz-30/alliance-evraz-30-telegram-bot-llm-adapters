import datetime
import time
from enum import StrEnum
from pathlib import Path
from typing import Callable

import requests
from pydantic import BaseModel


def print_project_structure(structure: dict, indent: int = 0):
    for key, value in structure.items():
        # Печатаем имя элемента с соответствующим отступом
        print('  ' * indent + str(key))

        # Если значение - это путь (объект Path), то пропускаем
        if isinstance(value, Path):
            pass

        # Если значение - это вложенный словарь, рекурсивно вызываем функцию для вложенной структуры
        elif isinstance(value, dict):
            print_project_structure(value, indent + 1)


def read_file(path: Path) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            result = file.read()
    except Exception as e:
        # Если не удаётся прочитать файл, записываем ошибку
        result = f"Error reading file: {e}"
    return result


def parse_project_structure(
        root: Path,
        callback: Callable[[dict, Path], None],
        exclude: set[str] = None,
        exclude_prefixes: set[str] = None,
) -> dict:
    if exclude is None:
        exclude = set()

    if exclude_prefixes is None:
        exclude_prefixes = set()

    structure = {}

    # Перебираем все элементы в директории
    for item in root.iterdir():
        if item.name in exclude:
            continue

        # Пропускаем элементы, имя которых начинается с исключенных префиксов
        if any(item.name.startswith(prefix) for prefix in exclude_prefixes):
            continue

        if item.is_dir():
            # Если это директория, рекурсивно собираем её содержимое
            structure[item.name] = parse_project_structure(item, callback, exclude, exclude_prefixes)
        elif item.is_file():
            callback(structure, item)
        else:
            raise TypeError

    return structure


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
            exclude: set[Path] = None,
            exclude_prefixes: set[Path] = None,
    ):
        self._path = path
        self._exclude = exclude if exclude else set()
        self._exclude_prefixes = exclude_prefixes if exclude_prefixes else set()

        self._full_structure = {}  # Текст файла в конце
        self._short_structure = {}  # Путь к файлу в конце
        self._module_layer: dict[Path, LayerName] = {}

    @staticmethod
    def short_structure_callback(structure, path):
        structure[path.name] = path

    @staticmethod
    def full_structure_callback(structure, path):
        structure[path.name] = read_file(path)

    @staticmethod
    def module_layer_callback(_structure, path):
        print(f"Узнаем к какому слою принадлежит: {path}")
        content = read_file(path)
        prompt = "Tell me which layer of the hexagonal architecture this file belongs to. Return layer name and reason only"
        llm = LLMAdapter()

        response = llm.send_prompts([prompt, content])
        for choice in response.choices:
            print(f"Файл принадлежит слою {choice.message.content}")
        print()
        time.sleep(3)

    def build(self):
        parse_project_structure(self._path, self.module_layer_callback)
        # self._short_structure = parse_project_structure(self._path, self.short_structure_callback)
        # self._full_structure = parse_project_structure(self._path, self.short_structure_callback)

    def print_short_structure(self):
        print_project_structure(self._short_structure)


def main():
    project_path = Path("D:/market/user")
    excludes = {
        Path("D:/market/user/.idea"),
        Path("D:/market/user/.venv"),
        Path("D:/market/user/.gitignore"),
        Path("D:/market/user/.git"),

    }

    # builder = GodService(project_path, exclude=excludes)
    # builder.build()
    # builder.print_short_structure()


    llm = LLMAdapter()
    response = llm.send_prompts([
        "I have a python project. I use hexagonal architecture. I need code review. "
        "I want to know what architectural mistakes I have done. Tell me about algorythm should I use for the task"
    ])

    print()
    print("Results")
    for x in response.choices:
        print(x.message.content)


if __name__ == "__main__":
    main()
