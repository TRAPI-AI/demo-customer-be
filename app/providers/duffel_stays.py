"""duffel_stays.py"""

import os
import requests
from flask import jsonify, Response

def fetch_duffel_stays(transformed_request):
    """
    Fetch hotel availability from Duffel Stays API.
    """
    try:
        api_endpoint = "https://api.duffel.com/stays/search"
        headers = {
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Duffel-Version": "v2",
            "Authorization": f"Bearer {os.getenv('DUFFEL_STAYS_API_KEY')}",
        }

        response = requests.post(
            api_endpoint,
            headers=headers,
            json=transformed_request,
            timeout=10,
        )
        print(f"Duffel Stays response status: {response.status_code}")
        print(f"Duffel Stays response content (truncated): {str(response.content)[:200]}...")
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Duffel Stays API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}