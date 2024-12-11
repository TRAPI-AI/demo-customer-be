from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv

# Initializing Flask app
app = Flask(__name__)
CORS(app)

load_dotenv()

SIMTEX_API_KEY = os.getenv('SIMTEX_API_KEY')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the backend!"})

@app.route('/simtex-esim-search', methods=['POST'])
def simtex_esim_search():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    headers = {
        'X-Api-Key': SIMTEX_API_KEY,
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    response = requests.post(
        'https://api.simtex.io/Quotes?currencyCode=USD',
        headers=headers,
        json=data
    )
    return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])