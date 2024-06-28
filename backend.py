# demo-customer-be Importing necessary libraries
import xml.etree.ElementTree as ET
from lxml import etree
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json

# Initializing Flask app
app = Flask(__name__)
CORS(app)


# Running the app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
