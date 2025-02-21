from flask import Flask, render_template, jsonify
import aiohttp
import asyncio

app = Flask(__name__)

MOONRAKER_API_URL = "http://192.168.0.196:7125/printer/objects/query"

TEMPERATURE_SENSORS = {
    "extruder": ["temperature", "target"],
    "heater_bed": ["temperature", "target"],
    "heater_generic chamber": ["temperature"],
    "virtual_sdcard": ["progress"]
}

# Async function to fetch temperature data
async def fetch_temperature_data():
    try:
        payload = {"objects": TEMPERATURE_SENSORS}
        async with aiohttp.ClientSession() as session:
            async with session.post(MOONRAKER_API_URL, json=payload) as response:
                response.raise_for_status()
                data = await response.json()

        sensors_data = data.get("result", {}).get("status", {})
        temperatures = {}
        for sensor, attributes in TEMPERATURE_SENSORS.items():
            sensor_data = sensors_data.get(sensor, {})
            temperatures[sensor] = {attr: sensor_data.get(attr) for attr in attributes}

        return temperatures
    except aiohttp.ClientError as e:
        print(f"Error fetching data from Moonraker API: {e}")
        return {}

# Async function to fetch progress data
async def fetch_progress_data():
    # Fetch progress data using the virtual_sdcard progress
    try:
        progress = {
            "progress_percentage": round((TEMPERATURE_SENSORS.get("virtual_sdcard", {}).get("progress") or 0) * 100, 1)
        }
        return progress
    except Exception as e:
        print(f"Error fetching progress data: {e}")
        return {"progress_percentage": 0}

@app.route("/temperatures")
async def get_temperatures():
    temperatures = await fetch_temperature_data()
    return jsonify(temperatures)

@app.route("/progress")
async def get_progress():
    progress = await fetch_progress_data()
    return jsonify(progress)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # Run the app with async mode enabled
    app.run(host="127.0.0.1", port=5001, debug=False)
