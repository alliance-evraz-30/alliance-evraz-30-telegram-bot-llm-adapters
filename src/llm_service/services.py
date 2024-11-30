import ast
from pathlib import Path


class ModuleAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.structure = {
            "imports": [],
            "classes": {},
            "functions": []
        }
        self.current_class = None  # Переменная для отслеживания текущего класса

    def visit_Import(self, node):
        # Добавляем импортированные модули
        for alias in node.names:
            self.structure["imports"].append(alias.name)

    def visit_ImportFrom(self, node):
        # Добавляем импорты из конкретного модуля
        for alias in node.names:
            self.structure["imports"].append(f"from {node.module} import {alias.name}")

    def visit_ClassDef(self, node):
        # При нахождении класса, инициализируем словарь для его методов
        self.current_class = node.name  # Запоминаем имя текущего класса
        self.structure["classes"][self.current_class] = {"methods": []}
        # Применяем visit для всех методов в классе
        self.generic_visit(node)
        self.current_class = None  # После завершения обработки класса сбрасываем контекст

    def visit_FunctionDef(self, node):
        # Если текущий узел — это функция, то проверяем, если она в классе или нет
        if self.current_class:
            # Если функция внутри класса, то это метод
            self.structure["classes"][self.current_class]["methods"].append(node.name)
        else:
            # Если это свободная функция
            self.structure["functions"].append(node.name)

    def visit(self, node):
        # Рекурсивно обрабатываем все дочерние узлы
        super().visit(node)


def analyze_module_structure(module_code: str):
    try:
        tree = ast.parse(module_code)

        analyzer = ModuleAnalyzer()
        analyzer.visit(tree)

        return analyzer.structure
    except SyntaxError:
        return "ParsingError"


def print_project_structure(structure: dict, indent: int = 0):
    for key, value in structure.items():
        # Печатаем имя элемента с соответствующим отступом
        print('  ' * indent + str(key), )

        if isinstance(value, dict):
            print_project_structure(value, indent + 1)
        else:
            print('  ' * (1 + indent), value)


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


def read_file(path: Path) -> str:
    try:
        # Use the detected encoding to read the entire file
        with open(path, 'r', encoding='utf-8') as file:
            result = file.read()
    except Exception:
        # Log or handle the exception as needed
        result = ""
    return result


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


def get_relative_path(root_path: Path, file_path: Path) -> str:
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
    if keys_to_remove is None:
        keys_to_remove = {"imports", "classes", "methods", "functions"}

    if isinstance(data, dict):
        return {
            key: clean_empty_keys(value, keys_to_remove)
            for key, value in data.items()
            if not (key in keys_to_remove and isinstance(value, (list, dict)) and not value)
        }
    elif isinstance(data, list):
        return [clean_empty_keys(item, keys_to_remove) for item in data]
    else:
        return data


def convert_path_to_structure(root: Path, excludes: set[str]) -> dict:
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
