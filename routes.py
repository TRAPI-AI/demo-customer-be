from fastapi import APIRouter, HTTPException
from src.services.aggregator import aggregate_data

router = APIRouter()

@router.get("/search")
async def search(query: str):
    try:
        aggregated_data = await aggregate_data(query)
        return {"data": aggregated_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))