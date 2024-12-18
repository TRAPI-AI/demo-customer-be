from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
import time

# Initializing Flask app
app = Flask(__name__)
CORS(app)

load_dotenv()

# Define your routes and logic here
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the backend!"})

# Add more routes as needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
