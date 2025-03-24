# How to setup OBS Studio with live temperature reporting on a Voron - see the pic for an example.
![VoronTemps](https://github.com/user-attachments/assets/ecf71b62-7b15-4671-b5b7-617109fb210e)

## 1) Download req.txt, app.py and the templates directory to your machine.

## 1a) Adjust the IP address in app.py to be the IP address of your Voron here: MOONRAKER_API_URL = "http://(your ip without angled brackets):7125/printer/objects/query"

## 2) Install Python 3 (https://www.python.org); ensure you add the PYTHONPATH on windows during install.

## 3) Install pip for python

```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```

## 4) Install virtualenv

```python -m pip install virtualenv```

```python -m virtualenv venv```

```venv\scripts\activate```

```python -m pip install --upgrade pip```

```python -m pip install -r req.txt```

```python app.py```

## 5) As a test go to 127.0.0.1:5000 in your browser; you should see the temps at the bottom live for your Voron/Klipper printer.

## 6) Launch OBS Studio (https://obsproject.com/)

## 7) Add a scene.

## Add a browser source and call it something like 'VoronTridentTemps'

## In the browser source untick local file and define the URL as 127.0.0.1:5000


# Customisations: Study app.py; my setup will be different from yours.
## Specifically, extruder, heater_bed and temperature_fan variables are defined in TEMPERATURE_SENSORS.
## TEMPERATURE_SENSOR_VARIABLES defines your temperature_sensor variables from printer.cfg.

# What if you want to do this on boot?

## Hit Windows key + R, then type ```shell:startup```

## Add a VoronTemps.bat file (edit in notepad or notepad++ for example) like this: 

```@echo off
cd <path to your Voron temps directory where you downloaded my files above>
call venv\Scripts\activate
python app.py
```

# Multiple printers: Create multiple virtual environments and choose a different port in app.py instead e.g. 5001, or other port for each printer.
