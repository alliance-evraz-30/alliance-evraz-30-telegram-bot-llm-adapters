import json
import re
from pathlib import Path
from typing import Callable, Any


def read_file(path: Path) -> str:
    try:
        # Use the detected encoding to read the entire file
        with open(path, 'r', encoding='utf-8') as file:
            result = file.read()
    except Exception as e:
        # Log or handle the exception as needed
        result = ""
    return result


def parse_project_structure(
        root: Path,
        exclude: set[str] = None,
        exclude_prefixes: set[str] = None,
) -> dict:
    if exclude is None:
        exclude = set()

    if exclude_prefixes is None:
        exclude_prefixes = set()

    structure = {}

    # Перебираем все элементы в директории
    for path in root.iterdir():
        if path.name in exclude:
            continue

        # Пропускаем элементы, имя которых начинается с исключенных префиксов
        if any(path.name.startswith(prefix) for prefix in exclude_prefixes):
            continue

        if path.is_dir():
            # Если это директория, рекурсивно собираем её содержимое
            structure[path.name] = parse_project_structure(path, exclude, exclude_prefixes)
        elif path.is_file():
            structure[path.name] = path
        else:
            raise TypeError

    return structure


def get_leaves_from_tree(data: dict):
    leaves = []

    def extract_leaves(subtree):
        if isinstance(subtree, dict):  # If the subtree is a dictionary
            for value in subtree.values():
                extract_leaves(value)
        else:  # If it's not a dictionary, it's a leaf
            leaves.append(subtree)

    extract_leaves(data)
    return leaves


def transform_tree_leaves(data, callback: Callable[[Any], Any]):
    if isinstance(data, dict):
        # Рекурсивно обходим словарь и применяем функцию к значениям
        return {key: transform_tree_leaves(value, callback) for key, value in data.items()}
    else:
        # Если это лист (не словарь), применяем callback
        return callback(data)


def print_project_structure(structure: dict, indent: int = 0):
    for key, value in structure.items():
        # Печатаем имя элемента с соответствующим отступом
        print('  ' * indent + str(key), )

        if isinstance(value, dict):
            print_project_structure(value, indent + 1)
        else:
            print('  ' * (1 + indent), value)


def extract_json(text):
    # Regular expression to match the text between START_JSON and END_JSON
    match = re.search(r"START_JSON\n({.*})\nEND_JSON", text, re.DOTALL)
    print(text)

    # Return the matched JSON text if found
    if match:
        result = match.group(1)
        result = json.loads(result)
        return result
    else:
        raise Exception


class PathConverter:
    def __init__(self):
        self._data = {}
        self._counter = 0

    def to_hash(self, path: Path) -> str:
        self._counter += 1
        key = str(self._counter)
        self._data[key] = path
        return key

    def from_hash(self, value: str) -> Path:
        return self._data[value]


def get_relative_path(root_path: Path, file_path: Path) -> str:
    """
    Возвращает относительный путь файла от корневой директории.

    :param root_path: Полный путь до корневой директории.
    :param file_path: Полный путь до конечного файла.
    :return: Относительный путь от корневой директории до файла.
    """
    root = root_path.resolve()
    file = file_path.resolve()
    try:
        # Получаем относительный путь
        relative_path = file.relative_to(root)
        return str(relative_path)
    except ValueError:
        # Если файл не находится внутри корневой директории
        raise ValueError("Файл находится вне корневой директории")


def clean_empty_keys(data, keys_to_remove=None):
    """
    Рекурсивно удаляет указанные ключи с пустыми значениями из словаря.

    :param data: Исходный словарь.
    :param keys_to_remove: Список ключей для удаления, если их значения пусты.
    :return: Новый словарь без удалённых ключей.
    """
    if keys_to_remove is None:
        keys_to_remove = {"imports", "classes", "methods", "functions"}

    if isinstance(data, dict):
        # Рекурсивно обрабатываем каждый ключ
        return {
            key: clean_empty_keys(value, keys_to_remove)
            for key, value in data.items()
            if not (key in keys_to_remove and isinstance(value, (list, dict)) and not value)
        }
    elif isinstance(data, list):
        # Если значение — список, рекурсивно обрабатываем его элементы
        return [clean_empty_keys(item, keys_to_remove) for item in data]
    else:
        # Возвращаем значение как есть, если оно не словарь и не список
        return data


