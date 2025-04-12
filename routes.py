from fastapi import APIRouter, HTTPException, Request
from src.services.aggregator import aggregate_data
import hashlib, time

router = APIRouter()

@router.get("/search")
async def search(query: str):
    try:
        aggregated_data = await aggregate_data(query)
        return {"data": aggregated_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hotelbeds-hotels-booking-hotel-availability")
async def hotel_availability(request: Request):
    try:
        body = await request.json()
        api_key = "HOTELBEDS_HOTEL_API_KEY"
        secret = "HOTELBEDS_HOTEL_SECRET"
        timestamp = str(int(time.time()))
        signature = hashlib.sha256((api_key + secret + timestamp).encode('utf-8')).hexdigest()
        headers = {
            'Accept': 'application/json',
            'Api-key': api_key,
            'X-Signature': signature,
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'
        }
        # Here you would typically make the request to the Hotelbeds API using an HTTP client
        # response = requests.post("https://api.test.hotelbeds.com/hotel-api/v1/hotels", json=body, headers=headers)
        # return response.json()
        return {"message": "Request sent to Hotelbeds API", "headers": headers, "body": body}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))