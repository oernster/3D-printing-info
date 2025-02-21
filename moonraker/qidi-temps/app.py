from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

MOONRAKER_API_URL = "http://192.168.0.196:7125/printer/objects/query"

TEMPERATURE_SENSORS = {
    "extruder": ["temperature", "target"],
    "heater_bed": ["temperature", "target"],
    "heater_generic chamber": ["temperature"]
}

def fetch_temperature_data():
    try:
        payload = {"objects": TEMPERATURE_SENSORS}
        response = requests.post(MOONRAKER_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        sensors_data = data.get("result", {}).get("status", {})
        temperatures = {}
        for sensor, attributes in TEMPERATURE_SENSORS.items():
            sensor_data = sensors_data.get(sensor, {})
            temperatures[sensor] = {attr: sensor_data.get(attr) for attr in attributes}

        return temperatures
    except requests.RequestException as e:
        print(f"Error fetching data from Moonraker API: {e}")
        return {}
        
def fetch_progress_data():
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {
            "objects": {
                "print_stats": ["print_duration", "total_duration", "state"]
            }
        }

        # Send request to Moonraker API
        response = requests.post(MOONRAKER_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()

        status = data.get("result", {}).get("status", {})
        print_stats = status.get("print_stats", {})

        # Extract time-based data
        print_duration = print_stats.get("print_duration", 0) or 0
        total_duration = print_stats.get("total_duration", 1) or 1  # Avoid division by zero

        # Debug logs to check print_duration and total_duration
        print(f"DEBUG | print_duration: {print_duration}, total_duration: {total_duration}")

        # Calculate time-based progress
        time_progress = (print_duration / total_duration) * 100
        print(f"DEBUG | time_progress: {time_progress:.2f}%")

        # Final adjusted progress is simply time_progress
        adjusted_progress = min(round(time_progress, 2), 100)  # Cap at 100%

        # Final adjusted progress debug log
        print(f"DEBUG | Adjusted Progress: {adjusted_progress:.2f}%")

        return {"progress_percentage": adjusted_progress}

    except requests.RequestException as e:
        print(f"Error fetching progress data: {e}")
        return {"progress_percentage": 0}

@app.route("/temperatures")
def get_temperatures():
    temperatures = fetch_temperature_data()
    return jsonify(temperatures)

@app.route("/progress")
def get_progress():
    progress = fetch_progress_data()
    return jsonify(progress)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
