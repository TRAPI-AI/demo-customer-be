import pytest
from httpx import AsyncClient
from fastapi import status
from main import app  # Assuming your FastAPI app is instantiated in main.py

@pytest.mark.asyncio
async def test_search_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/search", params={"query": "test"})
    assert response.status_code == status.HTTP_200_OK
    assert "data" in response.json()

@pytest.mark.asyncio
async def test_hotel_availability_endpoint():
    request_body = {
        "checkin": "2023-10-01",
        "checkout": "2023-10-10",
        "destination": "NYC",
        "guests": 2
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/hotelbeds-hotels-booking-hotel-availability", json=request_body)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert "message" in response_json
    assert response_json["message"] == "Request sent to Hotelbeds API"
    assert "headers" in response_json
    assert "body" in response_json
    assert response_json["body"] == request_body