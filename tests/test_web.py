import httpx
import pytest


@pytest.mark.asyncio
async def test_success(client):
    query = {
        "count": 3,
        "price": 4000,
        "state": "NV",
    }
    response = await client.post("/calculate", json=query)
    response.raise_for_status()
    data = response.json()
    assert data == {"calculated_price": (3 * 4000) * 0.9 * 1.08}


@pytest.mark.asyncio
async def test_bad_state(client):
    query = {
        "count": 3,
        "price": 4000,
        "state": "UFO",
    }
    response = await client.post("/calculate", json=query)
    assert response.status_code == httpx.codes.UNPROCESSABLE_ENTITY
    details = response.json()
    assert len(details["detail"]) == 1
    assert details["detail"][0]["msg"] == "value is not a valid enumeration member; " \
                                          "permitted: 'UT', 'NV', 'TX', 'AL', 'CA'"
