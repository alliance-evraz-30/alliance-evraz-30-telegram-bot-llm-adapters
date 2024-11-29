from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from src.bootstrap import Bootstrap
from src.domain.project import Project
from src.domain.prompt import Prompt
from src.domain.recommendation import Recommendation
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


CONTEXT_ID = UUID("cf08492e-1984-4f0b-bf61-fde6e4f4e4ad")

MESSAGE = "А дальше?"


@pytest.mark.asyncio
async def test_foo(client):
    # ОЧИЩАЕМ КОНТЕКСТ, ИНАЧЕ КОММЕНТИРУЕМ СЛЕДУЮУЮ СТРОКУ
    client.post(f"/context/{CONTEXT_ID}/clear")

    prompt = Prompt(content=MESSAGE)
    data = [prompt.model_dump(mode="json")]

    response = client.post(f"/context/{CONTEXT_ID}/prompt", json=data)
    assert response.status_code == 200

    recs = [Recommendation(**x) for x in response.json()]
    print()
    print()
    for rec in recs:
        print(rec.content)


