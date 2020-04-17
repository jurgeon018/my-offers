import pytest


@pytest.mark.asyncio
async def test_ping(http_client):
    await http_client.request('GET', '/ping/', expected_status=200)
