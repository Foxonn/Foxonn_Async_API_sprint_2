from asyncio import sleep
from http.client import NOT_FOUND

from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch

from tests.functional.utils.settings import settings

URL = settings.plugins.api.url


async def test_search(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/films/search'
    query_data = {"query": "The Star"}

    await sleep(2)
    async with fixture_aiohttp.get(url, params=query_data, raise_for_status=True) as response:
        body = await response.json()

    assert len(body) == 25


async def test_search_with_cache(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/films/search'
    query_data = {"query": "star", 'page_size': 13}

    await sleep(2)
    await fixture_aiohttp.get(url, params=query_data, raise_for_status=True)
    async with fixture_aiohttp.get(url, params=query_data, raise_for_status=True) as response:
        body = await response.json()

    assert 'Cache-Control' in response.headers
    assert len(body) == 13


async def test_limit(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/films?sort=-imdb_rating'
    query_data = {"page_size": 8}

    await sleep(2)
    async with fixture_aiohttp.get(url, params=query_data, raise_for_status=True) as response:
        body = await response.json()

    assert len(body) == 8


async def test_over_limit(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/films'
    query_data = {"page_size": 500}

    await sleep(2)
    async with fixture_aiohttp.get(url, params=query_data) as response:
        text = await response.text()

    assert 'ensure this value is less than or equal to 75' in text


async def test_less_limit(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/films'
    query_data = {"page_size": -1}

    await sleep(2)
    async with fixture_aiohttp.get(url, params=query_data) as response:
        text = await response.text()

    assert 'ensure this value is greater than or equal to 1' in text


async def test_all(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/films'

    await sleep(2)
    async with fixture_aiohttp.get(url, raise_for_status=True) as response:
        body = await response.json()

    assert len(body) == 25


async def test_get_target(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    data = {
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
    }
    url = URL + 'v1/films/c7adaab9-6c6c-4e12-8c53-d0ecfd3f6890'

    await sleep(2)
    async with fixture_aiohttp.get(url, raise_for_status=True) as response:
        body = await response.json()

    assert body == data


async def test_get_404(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/films/66acaffc-6e37-4763-a0b4-6c67087c9d3t'

    await sleep(2)
    response = await fixture_aiohttp.get(url)

    assert response.status == NOT_FOUND
