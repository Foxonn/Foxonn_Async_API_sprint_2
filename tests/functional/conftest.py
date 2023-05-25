from asyncio import AbstractEventLoop
from asyncio import get_event_loop_policy
from pathlib import Path
from typing import AsyncGenerator
from typing import Generator

import pytest
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch

from tests.functional.utils.settings import settings

__all__ = [
    'fixture_elastic',
    'fixture_aiohttp',
    'SCHEMAS_DIRECTORY',
]

SCHEMAS_DIRECTORY = Path(__file__).parent / 'assets' / 'elastic'


@pytest.fixture(scope='session')
async def fixture_elastic() -> Generator[AsyncElasticsearch, None, None]:
    es = AsyncElasticsearch(hosts=f'{settings.plugins.elastic.host}:{settings.plugins.elastic.port}')
    yield es
    await es.close()


@pytest.fixture(scope='session')
async def fixture_aiohttp() -> Generator[ClientSession, None, None]:
    session = ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='session', autouse=True)
def event_loop() -> AsyncGenerator[None, AbstractEventLoop]:
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
