import io
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.bootstrap import Bootstrap
from src.domain.project import Project
from src.enums import TargetLanguage
from src.main import app


class MockBootstrap(Bootstrap):
    pass


mock_container = MockBootstrap()


def get_mock_container():
    return mock_container


@pytest.fixture
def client():
    return TestClient(app)


def create_test_zip() -> bytes:
    # Создаём архив в памяти
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("test.txt", "This is a test file content")
    zip_buffer.seek(0)
    return zip_buffer.read()


def test_upload_zip(client):
    # Создаём тестовый ZIP-файл
    test_zip_content = create_test_zip()
    test_zip_filename = "test.zip"

    # Отправка POST-запроса
    response = client.post(
        "/project/",
        files={"file": (test_zip_filename, test_zip_content, "application/zip")},
    )

    # Проверка результата
    assert response.status_code == 200
    assert isinstance(response.json(), str)


@pytest.mark.asyncio
async def test_get_one_by_id(client):
    expected = Project(
        title="AnyProject",
        path=Path("."),
        structure={},
        language=TargetLanguage.Python,
    )
    await get_mock_container().project_repo().add_one(expected)

    response = client.get(f"/project/{expected.id}/")
    assert response.status_code == 200
    real = Project(**response.json())
    assert real == expected
    assert isinstance(real.path, Path)
