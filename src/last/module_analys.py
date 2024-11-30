import ast
from pathlib import Path

from src.last.services import parse_project_structure, transform_tree_leaves, read_file


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
    except SyntaxError as e:
        return "ParsingError"



