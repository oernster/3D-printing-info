from flask import Flask, render_template, jsonify
import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

MOONRAKER_API_URL = "http://192.168.0.196:7125/printer/objects/query"

TEMPERATURE_SENSORS = {
    "extruder": ["temperature", "target"],
    "heater_bed": ["temperature", "target"],
    "heater_generic chamber": ["temperature"],
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
    try:
        payload = {"objects": {"virtual_sdcard": ["file_path", "progress", "is_active", "file_position", "file_size"]}}
        async with aiohttp.ClientSession() as session:
            async with session.post(MOONRAKER_API_URL, json=payload) as response:
                response.raise_for_status()
                data = await response.json()

        logging.debug("API response: %s", data)

        progress_data = data.get("result", {}).get("status", {}).get("virtual_sdcard", {})
        progress = {
            "progress_percentage": round((progress_data.get("progress") or 0) * 100, 1),
            "file_path": progress_data.get("file_path", "N/A"),
            "is_active": progress_data.get("is_active", False),
            "file_position": progress_data.get("file_position", 0),
            "file_size": progress_data.get("file_size", 0)
        }
        return progress
    except aiohttp.ClientError as e:
        logging.error("Error fetching data from Moonraker API: %s", e)
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
    app.run(host="127.0.0.1", port=5001, debug=True)
