import pytest

from src.bootstrap import Bootstrap
from src.domain.context import Context


class MockBootstrap(Bootstrap):
    pass


mock_container = MockBootstrap()


def get_mock_container():
    return mock_container


client = get_mock_container().llm_adapter()

msg = """
Карл у Клары украл кораллы. А дальше?
"""


@pytest.mark.asyncio
async def test_foo():
    context = Context(content=msg)
    recs = await client.send_context(context)
    print()
    print()
    for rec in recs:
        print(rec.content)
    print()
    print()
