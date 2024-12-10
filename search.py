from flask import Flask, request, jsonify
from providers.hotelbeds import transform_request as transform_hotelbeds_request, call_api as call_hotelbeds_api, normalize_response as normalize_hotelbeds_response
# Import additional providers here as needed

app = Flask(__name__)

@app.route("/unified-endpoint", methods=["POST"])
def unified_endpoint():
    frontend_payload = request.get_json()
    
    responses = []
    
    # Hotelbeds Provider
    try:
        hb_transformed_request = transform_hotelbeds_request(frontend_payload)
        hb_response = call_hotelbeds_api(hb_transformed_request)
        hb_normalized = normalize_hotelbeds_response(hb_response)
        responses.append(hb_normalized)
    except Exception as e:
        # Handle errors (logging can be added here)
        pass
    
    # Call additional providers similarly
    # Example:
    # try:
    #     providerX_transformed_request = transform_providerX_request(frontend_payload)
    #     providerX_response = call_providerX_api(providerX_transformed_request)
    #     providerX_normalized = normalize_providerX_response(providerX_response)
    #     responses.append(providerX_normalized)
    # except Exception as e:
    #     pass
    
    unified_response = {
        "hotels": responses,
        "total": len(responses)
    }
    
    return jsonify(unified_response)