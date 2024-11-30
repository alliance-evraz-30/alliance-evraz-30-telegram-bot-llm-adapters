import ast
from pathlib import Path
from typing import Callable, Any

import chardet


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
        print('  ' * indent + str(key),)

        if isinstance(value, dict):
            print_project_structure(value, indent + 1)
        else:
            print('  ' * (1+ indent), value)

