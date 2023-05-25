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
    url = URL + 'v1/persons/search'
    data = {'query': 'ford', 'page_size': 25}

    await sleep(2)
    response = await fixture_aiohttp.get(url, params=data, raise_for_status=True)
    data = await response.json()

    assert len(data) == 25


async def test_search_cache(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/persons/search'
    data = {'query': 'ord', 'page_size': 21}

    await sleep(2)
    await fixture_aiohttp.get(url, params=data, raise_for_status=True)
    response = await fixture_aiohttp.get(url, params=data, raise_for_status=True)

    assert 'Cache-Control' in response.headers


async def test_cache(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/persons'
    await sleep(2)
    await fixture_aiohttp.get(url, raise_for_status=True)
    response = await fixture_aiohttp.get(url, raise_for_status=True)

    assert 'Cache-Control' in response.headers


async def test_get_over_limit(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/persons'
    query_data = {"page_size": 500}

    await sleep(2)
    async with fixture_aiohttp.get(url, params=query_data) as response:
        text = await response.text()

    assert 'ensure this value is less than or equal to 75' in text


async def test_get_less_limit(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/persons'
    query_data = {"page_size": -1}

    await sleep(2)
    async with fixture_aiohttp.get(url, params=query_data) as response:
        text = await response.text()

    assert 'ensure this value is greater than or equal to 1' in text


async def test_get_all(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/persons'

    await sleep(2)
    async with fixture_aiohttp.get(url, raise_for_status=True) as response:
        body = await response.json()

    assert len(body) == 25


async def test_get_target(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/persons/eb4b7d6e-fa43-4c6b-89c6-7045318689ae'
    data = {
        'id': 'eb4b7d6e-fa43-4c6b-89c6-7045318689ae',
        'full_name': 'Down Jones',
        'films': [
            {'id': 'dea9e2ab-23b4-4a26-99d1-7b55c5072111', 'roles': ['Actor', 'Writer']}
        ],
    }

    await sleep(2)
    async with fixture_aiohttp.get(url, raise_for_status=True) as response:
        body = await response.json()

    assert body == data


async def test_get_404(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/persons/eb4b7d6e-fa43-4c6b-89c6-7045318689hh'

    await sleep(2)
    response = await fixture_aiohttp.get(url)

    assert response.status == NOT_FOUND
