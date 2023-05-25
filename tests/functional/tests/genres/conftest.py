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
async def fixture_es_restart_genres(fixture_aiohttp: ClientSession, fixture_elastic: AsyncElasticsearch) -> None:
    es_settings = settings.plugins.elastic
    es_url = f'http://{es_settings.host}:{es_settings.port}/'
    schema = orjson.loads(Path(SCHEMAS_DIRECTORY / 'genres_schema.json').read_text(encoding='utf-8'))
    url = es_url + 'genres/'

    await fixture_aiohttp.delete(url=url)
    await fixture_aiohttp.put(url=url, json=schema)

    operations = []
    data = [{
        'id': str(uuid.uuid4()),
        'name': 'Horror',
        'description': '',
    } for _ in range(60)]
    data.append({
        'id': '66acaffc-6e37-4763-a0b4-6c67087c9d3f',
        'name': 'Action',
        'description': '',
    })
    for item in data:
        operations.append({"index": {'_index': 'genres', '_id': item['id']}})
        operations.append(item)
    result = await fixture_elastic.bulk(body=operations)
    if result['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')
