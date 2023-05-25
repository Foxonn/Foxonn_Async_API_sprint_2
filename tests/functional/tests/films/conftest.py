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
async def fixture_es_restart_movies(fixture_aiohttp: ClientSession, fixture_elastic: AsyncElasticsearch) -> None:
    es_settings = settings.plugins.elastic
    es_url = f'http://{es_settings.host}:{es_settings.port}/'
    schema = orjson.loads(Path(SCHEMAS_DIRECTORY / 'movies_schema.json').read_text(encoding='utf-8'))
    movies_url = es_url + 'movies/'

    await fixture_aiohttp.delete(url=es_url + 'movies/')
    await fixture_aiohttp.put(url=movies_url, json=schema)

    operations = []
    data_movies = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': round(random.uniform(1.0, 10.0), 1),
        'genre': 'Sci-Fi',
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],
    } for _ in range(60)]
    data_movies.append({
        'id': 'c7adaab9-6c6c-4e12-8c53-d0ecfd3f6890',
        'imdb_rating': 5.5,
        'genre': 'Horror',
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ]
    })
    for item in data_movies:
        operations.append({"index": {'_index': 'movies', '_id': item['id']}})
        operations.append(item)
    result = await fixture_elastic.bulk(body=operations)
    if result['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')
