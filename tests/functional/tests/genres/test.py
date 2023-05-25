from asyncio import sleep
from http.client import NOT_FOUND

from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch

from tests.functional.utils.settings import settings

URL = settings.plugins.api.url


async def test_cache(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/genres'

    await sleep(2)
    await fixture_aiohttp.get(url, raise_for_status=True)
    response = await fixture_aiohttp.get(url, raise_for_status=True)

    assert 'Cache-Control' in response.headers


async def test_get_over_limit(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/genres'
    query_data = {"page_size": 500}

    await sleep(2)
    async with fixture_aiohttp.get(url, params=query_data) as response:
        text = await response.text()

    assert 'ensure this value is less than or equal to 75' in text


async def test_get_less_limit(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/genres'
    query_data = {"page_size": -1}

    await sleep(2)
    async with fixture_aiohttp.get(url, params=query_data) as response:
        text = await response.text()

    assert 'ensure this value is greater than or equal to 1' in text


async def test_get_all(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/genres'

    await sleep(2)
    async with fixture_aiohttp.get(url, raise_for_status=True) as response:
        body = await response.json()

    assert len(body) == 25


async def test_get_target(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/genres/66acaffc-6e37-4763-a0b4-6c67087c9d3f'
    data = {
        'id': '66acaffc-6e37-4763-a0b4-6c67087c9d3f',
        'name': 'Action',
    }

    await sleep(2)
    async with fixture_aiohttp.get(url, raise_for_status=True) as response:
        body = await response.json()

    assert body == data


async def test_get_404(
    fixture_elastic: AsyncElasticsearch,
    fixture_aiohttp: ClientSession,
):
    url = URL + 'v1/genres/66acaffc-6e37-4763-a0b4-6c67087c9d3t'

    await sleep(2)
    response = await fixture_aiohttp.get(url)

    assert response.status == NOT_FOUND
