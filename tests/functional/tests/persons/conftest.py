import random
import uuid
from pathlib import Path

import orjson
import pytest
from aiohttp import ClientSession
from tests.functional.utils.settings import settings
from elasticsearch import AsyncElasticsearch

from tests.functional.conftest import SCHEMAS_DIRECTORY


@pytest.fixture(scope='session', autouse=True)
async def fixture_es_restart_persons(fixture_aiohttp: ClientSession, fixture_elastic: AsyncElasticsearch) -> None:
    es_settings = settings.plugins.elastic
    es_url = f'http://{es_settings.host}:{es_settings.port}/'
    schema = orjson.loads(Path(SCHEMAS_DIRECTORY / 'persons_schema.json').read_text(encoding='utf-8'))
    url = es_url + 'persons/'

    await fixture_aiohttp.delete(url=url)
    await fixture_aiohttp.put(url=url, json=schema)

    operations = []
    data = [{
        'id': str(uuid.uuid4()),
        'full_name': 'Harrison Ford',
        'films': [
            {'id': str(uuid.uuid4()), 'roles': ['Actor', 'Writer']}
        ],
    } for _ in range(60)]
    data.append({
        'id': 'eb4b7d6e-fa43-4c6b-89c6-7045318689ae',
        'full_name': 'Down Jones',
        'films': [
            {'id': 'dea9e2ab-23b4-4a26-99d1-7b55c5072111', 'roles': ['Actor', 'Writer']}
        ],
    })
    for item in data:
        operations.append({"index": {'_index': 'persons', '_id': item['id']}})
        operations.append(item)
    result = await fixture_elastic.bulk(body=operations)
    if result['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')
