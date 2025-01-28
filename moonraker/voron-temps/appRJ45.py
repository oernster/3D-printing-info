from flask import Flask, render_template, jsonify

import requests

app = Flask(__name__)

MOONRAKER_API_URL = "http://192.168.0.103:7125/printer/objects/query"

# Define the sensors and attributes to query
TEMPERATURE_SENSORS = {
    "extruder": ["temperature", "target"],
    "heater_bed": ["temperature", "target"],
    "temperature_fan MCU_Fans": ["temperature"],  # Query the temperature_fan MCU_Fans temperature
}

TEMPERATURE_SENSOR_VARIABLES = ["CHAMBER", "Internals", "Pi"]  # Additional temperature sensors if needed

def fetch_temperature_data():
    """
    Fetch temperature and target data for all sensors from the Moonraker API.
    """
    try:
        # Query standard temperature objects
        payload = {"objects": TEMPERATURE_SENSORS}
        response = requests.post(MOONRAKER_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        # Parse standard sensors
        sensors_data = data.get("result", {}).get("status", {})
        temperatures = {}
        for sensor, attributes in TEMPERATURE_SENSORS.items():
            sensor_data = sensors_data.get(sensor, {})
            # Use a display name of "MCU" for "temperature_fan MCU_Fans"
            display_name = "MCU" if sensor == "temperature_fan MCU_Fans" else sensor
            temperatures[display_name] = {attr: sensor_data.get(attr) for attr in attributes}

        # Query `temperature_sensor` variables
        if TEMPERATURE_SENSOR_VARIABLES:
            payload = {"objects": {f"temperature_sensor {sensor}": ["temperature"] for sensor in TEMPERATURE_SENSOR_VARIABLES}}
            response = requests.post(MOONRAKER_API_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            # Parse `temperature_sensor` variables
            sensor_data = data.get("result", {}).get("status", {})
            for sensor in TEMPERATURE_SENSOR_VARIABLES:
                temperature = sensor_data.get(f"temperature_sensor {sensor}", {}).get("temperature")
                if temperature is not None:
                    temperatures[sensor] = {"temperature": temperature}

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
    temperatures = fetch_temperature_data()
    return render_template("index.html", temperatures=temperatures)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

