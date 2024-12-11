"""aggregator.py"""

import asyncio
from flask import jsonify
from . import providers

async def call_provider(provider_func, transformed_request):
    return await provider_func(transformed_request)

def get_unified_response(frontend_data):
    """Aggregate responses from multiple providers and return a unified response."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    tasks = []
    # Transform and call each provider
    hotelbeds_request = providers.hotelbeds_hotels.transform_to_hotelbeds_request(frontend_data)
    tasks.append(loop.create_task(providers.hotelbeds_hotels.get_hotel_availability_async(hotelbeds_request)))
    
    duffel_request = providers.duffel_stays.transform_to_duffel_request(frontend_data)
    tasks.append(loop.create_task(providers.duffel_stays.search_duffel_stays_async(duffel_request)))
    
    responses = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
    loop.close()
    
    unified_results = {"hotels": []}
    
    for response in responses:
        if isinstance(response, Exception):
            # Handle exceptions from providers
            continue
        unified_results["hotels"].extend(response.get("hotels", []))
    
    return jsonify(unified_results), 200