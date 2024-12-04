from fastapi import APIRouter, HTTPException
from src.services.aggregator import aggregate_data

router = APIRouter()

@router.get("/search")
async def search(query: str):
    """
    Search route that aggregates data from multiple providers based on the query.
    """
    try:
        # Call the aggregator service to get data from providers
        aggregated_data = await aggregate_data(query)
        return {"data": aggregated_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    