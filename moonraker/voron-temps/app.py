from flask import Flask, render_template, jsonify
import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)

class PrinterDataFetcher:
    """Class responsible for fetching data from the 3D printer API."""
    
    def __init__(self, api_url):
        self.api_url = api_url
        self.temperature_sensors = {
            "extruder": ["temperature", "target"],
            "heater_bed": ["temperature", "target"],
            "temperature_fan MCU_Fans": ["temperature"],
        }
        self.temperature_sensor_variables = ["CHAMBER", "Internals", "NucBox", "NH36", "Cartographer"]
    
    async def fetch_temperature_data(self):
        """Fetch temperature data from all sensors."""
        temperatures = {}

        async with aiohttp.ClientSession() as session:
            try:
                # Fetch standard sensors
                payload_standard = {"objects": self.temperature_sensors}
                async with session.post(self.api_url, json=payload_standard) as response:
                    response.raise_for_status()
                    data_standard = await response.json()

                sensors_data = data_standard.get("result", {}).get("status", {})
                for sensor, attributes in self.temperature_sensors.items():
                    sensor_data = sensors_data.get(sensor, {})
                    display_name = "MCU" if sensor == "temperature_fan MCU_Fans" else sensor.title().replace("_", " ")
                    temperatures[display_name] = {attr: sensor_data.get(attr, "N/A") for attr in attributes}

                # Fetch temperature_sensor variables
                payload_variables = {"objects": {f"temperature_sensor {sensor}": ["temperature"] 
                                                for sensor in self.temperature_sensor_variables}}
                async with session.post(self.api_url, json=payload_variables) as response:
                    response.raise_for_status()
                    data_variables = await response.json()

                sensor_variables_data = data_variables.get("result", {}).get("status", {})
                for sensor in self.temperature_sensor_variables:
                    sensor_key = f"temperature_sensor {sensor}"
                    temperature = sensor_variables_data.get(sensor_key, {}).get("temperature", "N/A")
                    temperatures[sensor] = {"temperature": temperature, "target": "N/A"}

            except aiohttp.ClientError as e:
                logging.error(f"Error fetching temperature data from Moonraker API: {e}")

        return temperatures

    async def fetch_progress_data(self):
        """Fetch print job progress data."""
        try:
            payload = {"objects": {"virtual_sdcard": ["file_path", "progress", "is_active", "file_position", "file_size"]}}
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload) as response:
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
            logging.error(f"Error fetching progress data from Moonraker API: {e}")
            return {"progress_percentage": 0}

    async def fetch_fan_data(self):
        """
        Fetch cooling fan speed data. 
        Returns fan speed as a percentage (0-100).
        """
        fan_data = {"fan_speed": 0}
        payload = {"objects": {"fan": ["speed"]}}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.api_url, json=payload) as response:
                    response.raise_for_status()
                    data = await response.json()
                    fan_status = data.get("result", {}).get("status", {}).get("fan", {})
                    speed_fraction = fan_status.get("speed", 0)
                    # Convert 0.0-1.0 to 0-100%
                    fan_data["fan_speed"] = round(speed_fraction * 100, 1)
            except aiohttp.ClientError as e:
                logging.error(f"Error fetching fan data from Moonraker API: {e}")

        return fan_data


class PrinterDashboardApp:
    """Class that defines the Flask application for the 3D printer dashboard."""
    
    def __init__(self, api_url):
        self.app = Flask(__name__)
        self.data_fetcher = PrinterDataFetcher(api_url)
        self._register_routes()
    
    def _register_routes(self):
        """Register all the Flask routes."""
        
        @self.app.route('/progress')
        async def get_progress():
            progress = await self.data_fetcher.fetch_progress_data()
            return jsonify(progress)
            
        @self.app.route("/temperatures")
        async def get_temperatures():
            temperatures = await self.data_fetcher.fetch_temperature_data()
            return jsonify(temperatures)

        @self.app.route('/fan')
        async def get_fan_speed():
            """Return the current fan speed in percentage."""
            fan_data = await self.data_fetcher.fetch_fan_data()
            return jsonify(fan_data)

        @self.app.route('/')
        async def index():
            # Fetch basic data to display
            temperatures = await self.data_fetcher.fetch_temperature_data()
            fan_data = await self.data_fetcher.fetch_fan_data()
            return render_template('index.html', temperatures=temperatures, fan_data=fan_data)
    
    def run(self, host="127.0.0.1", port=5000, debug=True, use_reloader=False):
        """Run the Flask application."""
        self.app.run(host=host, port=port, debug=debug, use_reloader=use_reloader)


# Main application entry point
if __name__ == "__main__":
    # Configuration
    MOONRAKER_API_URL = "http://192.168.0.80:7125/printer/objects/query"
    
    # Initialize and run the application
    app = PrinterDashboardApp(MOONRAKER_API_URL)
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
