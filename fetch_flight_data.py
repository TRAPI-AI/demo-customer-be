from flask import Flask, request
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore client
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/fetch-flight-data', methods=['GET'])
def fetch_flight_data():
    # Get parameters from request
    acid = request.args.get('acid')
    outdate = request.args.get('outdate')
    indate = request.args.get('indate')
    username = "trAPI"
    password = "EP5lGF8r5W"
    url = "https://xml.flightview.com/FlightStatusJsonDemo/fvxml.exe"

    # Prepare parameters for the request
    params = {
        "acid": acid,
        "outdate": outdate,
        "indate": indate,
        "A": username,
        "B": password
    }

    # Make the request to the external API
    response = requests.get(url, params=params)
    print('JSON Response:', response.text)
    response_dict = response.json()

    # Check if the response contains multiple flights
    flights = response_dict.get("Flights", [])
    flight_data_list = []
    for flight in flights:
        flight_data = {
            "FlightNumber": flight["Acid"]["FlightNumber"],
            "AirlineCode": flight["Acid"]["Airline"]["Code"],
            "DepartureAirportCode": flight["DepartureAirport"]["Code"],
            "ArrivalAirportCode": flight["ArrivalAirport"]["Code"],
            "ScheduledDeparture": flight["ScheduledDeparture"]["Local"],
            "ScheduledArrival": flight["ScheduledArrival"]["Local"],
            "Status": flight["Status"],
            "ServiceType": flight["ServiceType"],
            "DepartureTerminal": flight["DepartureTerminal"],
            "ArrivalTerminal": flight["ArrivalTerminal"],
        }
        flight_data_list.append(flight_data)

    # Generate a datetime string for the document name
    datetime_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    document_name = f"flight_info_v2_req_{datetime_str}"

    # Create a single document with all flights data
    doc_ref = db.collection('flightViewCalls').document(document_name)
    doc_ref.set({"flights": flight_data_list})

    return {"flights": flight_data_list}

if __name__ == '__main__':
    app.run(debug=True)

# Legacy Endpoint CURL: curl "http://localhost:5000/fetch-flight-data?acid=WN1&depdate=20241010"
