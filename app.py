# ********************************************************************
## app.py       Author: Llewellyn (Cassie) VanDelinder
## Module 4: Assignment 1
# Build a RESTful application that talks to an external API with Async Fetch
# ********************************************************************

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


# ------------------------------------------------------------------
# 1️⃣  GET endpoint that fetches data from a remote API
@app.route("/items", methods=["GET"])
def get_items():
    """
      Calls an external REST API
    • Making a GET request with `requests`.
    • Parsing JSON.
    • Basic error handling.
    """
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleVariableList?format=json"
    try:
        resp = requests.get(url, timeout=5)  # 5‑second timeout
        resp.raise_for_status()  # raise for HTTP errors
        data = resp.json()  # parse JSON into Python list/dict

        filtered = [
            item
            for item in data["Results"]
            if item["GroupName"] == "Active Safety System"
        ]

        return jsonify(filtered), 200  # Flask will set Content‑Type: application/json
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error: {http_err}"}), resp.status_code
    except requests.exceptions.RequestException as err:
        return jsonify({"error": f"Network error: {err}"}), 503


# ------------------------------------------------------------------
# 2️⃣  POST endpoint that forwards data to a remote API
@app.route("/items", methods=["POST"])
def create_item():
    """
    Accepts JSON from the client, forwards it to an external API,
    and returns the response. Demonstrates:
      • Reading JSON body (`request.get_json()`).
      • Sending JSON payload with `json=` argument.
      • Handling non‑200 responses.
    """
    payload = request.get_json() or {}
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleVariableList?format=json"

    try:
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        return jsonify(resp.json()), 201
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error: {http_err}"}), resp.status_code
    except requests.exceptions.RequestException as err:
        return jsonify({"error": f"Network error: {err}"}), 503


# ------------------------------------------------------------------
if __name__ == "__main__":
    # Run the Flask development server on http://localhost:5000
    app.run(debug=True, port=5000)
