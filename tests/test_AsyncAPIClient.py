import asyncio

import pytest
from aioresponses import aioresponses
from aiohttp import ClientSession
from AsyncAPIClient import AsyncAPIClient  # Replace with the actual module name


@pytest.fixture
def api_client():
    api_url = "https://example.com/api/"
    headers = {"Authorization": "Bearer token"}
    return AsyncAPIClient(api_url, headers)


@pytest.mark.asyncio
async def test_fetch_success(api_client):
    index = 1
    expected_data = {"data": {"ads": ["ad1", "ad2"]}}

    with aioresponses() as m:
        m.get(f"{api_client.api_url}{index}", payload=expected_data)

        async with ClientSession() as session:
            result = await api_client.fetch(session, index)
            assert result == expected_data["data"]["ads"]


@pytest.mark.asyncio
async def test_fetch_failure(api_client):
    index = 1

    with aioresponses() as m:
        m.get(f"{api_client.api_url}{index}", status=404)

        async with ClientSession() as session:
            result = await api_client.fetch(session, index)
            assert result == {"error": "Failed to fetch data (status: 404)"}


@pytest.mark.asyncio
async def test_fetch_timeout(api_client):
    index = 1

    with aioresponses() as m:
        m.get(f"{api_client.api_url}{index}", exception=asyncio.TimeoutError)

        async with ClientSession() as session:
            result = await api_client.fetch(session, index)
            assert result == {"error": "Request timed out"}


@pytest.mark.asyncio
async def test_get_data(api_client):
    expected_data = [{"data": {"ads": ["ad1", "ad2"]}} for _ in range(954)]

    with aioresponses() as m:
        for index in range(954):
            m.get(f"{api_client.api_url}{index}", payload=expected_data[index])

        results = await api_client.get_data()
        for result, expected in zip(results, expected_data):
            assert result == expected["data"]["ads"]
