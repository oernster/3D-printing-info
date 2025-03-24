from flask import Flask, render_template, jsonify
import aiohttp
import asyncio
import logging
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SensorConfig:
    """Configuration for a temperature sensor"""
    name: str
    attributes: List[str]
    display_name: str


class APIClient:
    """Client for interacting with the 3D printer API"""
    
    def __init__(self, api_url: str, timeout: int = 10):
        self.api_url = api_url
        self.timeout = timeout
    
    async def _make_request(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make a request to the API with the given payload"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url, 
                    json=payload, 
                    timeout=self.timeout
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"API request error: {e}")
            return None
        except asyncio.TimeoutError:
            logger.error(f"API request timed out after {self.timeout} seconds")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during API request: {e}")
            return None


class PrinterDataService:
    """Service for fetching and processing printer data"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        
        # Define temperature sensors configuration
        self.temperature_sensors = [
            SensorConfig("extruder", ["temperature", "target"], "Extruder"),
            SensorConfig("heater_bed", ["temperature", "target"], "Bed"),
            SensorConfig("heater_generic chamber", ["temperature"], "Chamber")
        ]
        
        # Build the sensors query object
        self.sensors_query = {
            sensor.name: sensor.attributes for sensor in self.temperature_sensors
        }
    
    async def get_temperatures(self) -> Dict[str, Any]:
        """Get temperature data for all configured sensors"""
        payload = {"objects": self.sensors_query}
        data = await self.api_client._make_request(payload)
        
        if not data:
            return {sensor.name: {} for sensor in self.temperature_sensors}
        
        sensors_data = data.get("result", {}).get("status", {})
        temperatures = {}
        
        for sensor in self.temperature_sensors:
            sensor_data = sensors_data.get(sensor.name, {})
            temperatures[sensor.name] = {
                attr: sensor_data.get(attr) for attr in sensor.attributes
            }
        
        return temperatures
    
    async def get_progress(self) -> Dict[str, Any]:
        """Get print job progress data"""
        payload = {
            "objects": {
                "virtual_sdcard": [
                    "file_path", 
                    "progress", 
                    "is_active", 
                    "file_position", 
                    "file_size"
                ]
            }
        }
        
        data = await self.api_client._make_request(payload)
        
        if not data:
            return {"progress_percentage": 0, "is_active": False}
        
        logger.debug("Progress API response: %s", data)
        
        progress_data = data.get("result", {}).get("status", {}).get("virtual_sdcard", {})
        
        return {
            "progress_percentage": round((progress_data.get("progress") or 0) * 100, 1),
            "file_path": progress_data.get("file_path", "N/A"),
            "is_active": progress_data.get("is_active", False),
            "file_position": progress_data.get("file_position", 0),
            "file_size": progress_data.get("file_size", 0)
        }


class PrinterDashboardApp:
    """Flask application for the 3D printer dashboard"""
    
    def __init__(self, data_service: PrinterDataService):
        self.app = Flask(__name__)
        self.data_service = data_service
        self._register_routes()
        
        # Configure template folder if running in development mode
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "templates")):
            self.app.template_folder = "."
    
    def _register_routes(self):
        """Register all Flask routes"""
        
        @self.app.route('/temperatures')
        async def get_temperatures():
            temperatures = await self.data_service.get_temperatures()
            return jsonify(temperatures)
            
        @self.app.route('/progress')
        async def get_progress():
            progress = await self.data_service.get_progress()
            return jsonify(progress)
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
    
    def run(self, host: str = "127.0.0.1", port: int = 5001, debug: bool = False):
        """Run the Flask application"""
        self.app.run(host=host, port=port, debug=debug)


def create_app(config: Dict[str, Any] = None) -> PrinterDashboardApp:
    """Factory function to create and configure the application"""
    if config is None:
        config = {}
    
    api_url = config.get("api_url", "http://localhost:7125/printer/objects/query")
    timeout = config.get("timeout", 10)
    
    # Create the API client
    api_client = APIClient(api_url, timeout)
    
    # Create the data service
    data_service = PrinterDataService(api_client)
    
    # Create and return the application
    return PrinterDashboardApp(data_service)


# Main application entry point
if __name__ == "__main__":
    # Configuration
    config = {
        "api_url": os.environ.get(
            "MOONRAKER_API_URL", 
            "http://192.168.0.196:7125/printer/objects/query"
        ),
        "timeout": int(os.environ.get("API_TIMEOUT", "10"))
    }
    
    # Debug level from environment
    if os.environ.get("DEBUG", "").lower() in ("1", "true", "yes"):
        logger.setLevel(logging.DEBUG)
    
    # Create and run the application
    app = create_app(config)
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5001")),
        debug=os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    )
