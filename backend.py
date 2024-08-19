import xml.etree.ElementTree as ET
from lxml import etree
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

@app.route('/silverrail-shop-tickets', methods=['POST'])
def silverrail_shop_tickets():
    headers = {
        "Content-Type": "text/xml"
    }
    cert_path = "combined_unencrypted.pem"
    try:
        response = requests.post(
            "https://xml-cert-nex.railgds.net/shopping-ws/services/Shopping/v2",
            data=request.data,
            headers=headers,
            cert=cert_path,
        )
        response.raise_for_status()
        return Response(response.content, mimetype="text/xml")
    except requests.exceptions.RequestException as e:
        error_message = f"<error>Failed to fetch data from SilverRail API: {e}</error>"
        print(error_message)
        return Response(error_message, status=500, mimetype="text/xml")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
