import requests
import json
from datetime import datetime

# Configuration
macro_name = 'PRINT_END_SOUND'
moonraker_api_url = f'http://0.0.0.0:7125/printer/gcode/script?script={macro_name}'

# Get the current hour
current_hour = datetime.now().hour

# Check if the current time is not between 1 AM and 8 AM
if not (1 <= current_hour < 8):
    # Send a request to Klipper to execute the macro

    payload = {
    "jsonrpc": "2.0",
    "method": "printer.gcode.script",
    "params": {
        "script": f"{macro_name}"
    },
    "id": 7466}
    
    try:
        response = requests.post(moonraker_api_url, data=json.dumps(payload))
        response.raise_for_status()
        print(f'Successfully executed macro: {macro_name}')
    except requests.exceptions.RequestException as e:
        print(f'Failed to execute macro: {macro_name}. Error: {e}')
else:
    print(f'Time is between 1 AM and 8 AM. Skipping macro execution.')
