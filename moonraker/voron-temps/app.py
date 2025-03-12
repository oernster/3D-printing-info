from flask import Flask, render_template, jsonify
import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

MOONRAKER_API_URL = "http://192.168.0.104:7125/printer/objects/query"

TEMPERATURE_SENSORS = {
    "extruder": ["temperature", "target"],
    "heater_bed": ["temperature", "target"],
    "temperature_fan MCU_Fans": ["temperature"],
}

TEMPERATURE_SENSOR_VARIABLES = ["CHAMBER", "Internals", "Pi", "EBB36"]

async def fetch_temperature_data():
    temperatures = {}

    async with aiohttp.ClientSession() as session:
        try:
            # Fetch standard sensors
            payload_standard = {"objects": TEMPERATURE_SENSORS}
            async with session.post(MOONRAKER_API_URL, json=payload_standard) as response:
                response.raise_for_status()
                data_standard = await response.json()

            sensors_data = data_standard.get("result", {}).get("status", {})
            for sensor, attributes in TEMPERATURE_SENSORS.items():
                sensor_data = sensors_data.get(sensor, {})
                display_name = "MCU" if sensor == "temperature_fan MCU_Fans" else sensor.title().replace("_", " ")
                temperatures[display_name] = {attr: sensor_data.get(attr, "N/A") for attr in attributes}

            # Fetch temperature_sensor variables
            payload_variables = {"objects": {f"temperature_sensor {sensor}": ["temperature"] for sensor in TEMPERATURE_SENSOR_VARIABLES}}
            async with session.post(MOONRAKER_API_URL, json=payload_variables) as response:
                response.raise_for_status()
                data_variables = await response.json()

            sensor_variables_data = data_variables.get("result", {}).get("status", {})
            for sensor in TEMPERATURE_SENSOR_VARIABLES:
                sensor_key = f"temperature_sensor {sensor}"
                temperature = sensor_variables_data.get(sensor_key, {}).get("temperature", "N/A")
                temperatures[sensor] = {"temperature": temperature, "target": "N/A"}

        except aiohttp.ClientError as e:
            logging.error(f"Error fetching data from Moonraker API: {e}")

    return temperatures

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

@app.route('/progress')
async def get_progress():
    progress = await fetch_progress_data()
    return jsonify(progress)
    
@app.route("/temperatures")
async def get_temperatures():
    temperatures = await fetch_temperature_data()
    return jsonify(temperatures)

@app.route("/")
async def index():
    temperatures = await fetch_temperature_data()
    return render_template("index.html", temperatures=temperatures)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
