from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

MOONRAKER_API_URL = "http://192.168.0.196:7125/printer/objects/query"

# Define the sensors and attributes to query
TEMPERATURE_SENSORS = {
    "extruder": ["temperature", "target"],
    "heater_bed": ["temperature", "target"],
    "heater_generic chamber": ["temperature"]  # Query chamber temperature from heater_generic
}

def fetch_temperature_data():
    """
    Fetch temperature and target data for all sensors from the Moonraker API.
    """
    try:
        # Query temperature objects
        payload = {"objects": TEMPERATURE_SENSORS}
        response = requests.post(MOONRAKER_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        # Parse sensor data
        sensors_data = data.get("result", {}).get("status", {})
        temperatures = {}
        for sensor, attributes in TEMPERATURE_SENSORS.items():
            sensor_data = sensors_data.get(sensor, {})
            # Use a display name of "Chamber" for "heater_generic chamber"
            display_name = "Chamber" if sensor == "heater_generic chamber" else sensor
            temperatures[display_name] = {attr: sensor_data.get(attr) for attr in attributes}

        return temperatures
    except requests.RequestException as e:
        print(f"Error fetching data from Moonraker API: {e}")
        return {}

@app.route("/temperatures")
def get_temperatures():
    """
    API endpoint to fetch temperature data for polling.
    """
    temperatures = fetch_temperature_data()
    return jsonify(temperatures)

@app.route("/")
def index():
    """
    Main route to display the temperature data on the frontend.
    """
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)

