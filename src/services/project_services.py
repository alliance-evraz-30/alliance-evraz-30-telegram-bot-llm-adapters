import shutil
import zipfile
from pathlib import Path

from fastapi import UploadFile

from src.adapters.repos.project_repo import ProjectRepo
from src.domain.project import Project
from src.enums import TargetLanguage


def unpack_upload_file(upload_file: UploadFile, destination_dir: Path) -> Path:
    # Определяем имя директории на основе имени файла
    base_name = Path(upload_file.filename).stem  # Без расширения
    unpack_dir = destination_dir / base_name

    # Проверяем уникальность имени директории
    counter = 0
    while unpack_dir.exists():
        counter += 1
        unpack_dir = destination_dir / f"{base_name}_{counter}"

    unpack_dir.mkdir(parents=True, exist_ok=True)

    # Сохраняем файл временно на диск
    temp_file_path = unpack_dir / upload_file.filename
    with temp_file_path.open("wb") as temp_file:
        shutil.copyfileobj(upload_file.file, temp_file)

    # Проверяем, является ли файл zip-архивом
    if not zipfile.is_zipfile(temp_file_path):
        temp_file_path.unlink()  # Удаляем временный файл
        unpack_dir.rmdir()  # Удаляем созданную директорию
        raise ValueError(f"The uploaded file {upload_file.filename} is not a valid zip archive.")

    # Распаковываем содержимое архива
    with zipfile.ZipFile(temp_file_path, 'r') as archive:
        archive.extractall(unpack_dir)

    # Удаляем временный файл
    temp_file_path.unlink()

    return unpack_dir


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


def parse_project_structure(
        root: Path,
        exclude: set[str] = None,
) -> dict:
    structure = {}
    if exclude is None:
        exclude = set()

    # Перебираем все элементы в директории
    for item in root.iterdir():
        if item.name in exclude:
            continue

        if item.is_dir():
            # Если это директория, рекурсивно собираем её содержимое
            structure[item.name] = parse_project_structure(item)
        elif item.is_file():
            # Если это файл, добавляем его в структуру
            structure[item.name] = item

    return structure


class ProjectService:
    def __init__(
            self,
            repo: ProjectRepo,
            base_project_dir: Path,
    ):
        self._repo = repo
        self._base_project_dir = base_project_dir

    async def create_project_from_upload_file(self, file: UploadFile) -> Project:
        path = unpack_upload_file(file, self._base_project_dir)
        result = Project(
            title=path.name,
            path=path,
            structure=parse_project_structure(path),
            language=TargetLanguage.Python,
        )
        await self._repo.add_one(result)
        return result

    async def create_project_from_project_root(self, project_root: Path) -> Project:
        result = Project(
            title=project_root.name,
            path=project_root,
            structure=parse_project_structure(project_root),
            language=TargetLanguage.Python,
        )
        await self._repo.add_one(result)
        return result
