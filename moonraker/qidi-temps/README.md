# How to setup OBS Studio with live temperature reporting on a Qidi - see the jpg for an example.

![QidiTemps](https://github.com/user-attachments/assets/934ac6c8-f1c0-49f2-95ad-e5aa604acede)

## 1) Download req.txt, app.py and the templates directory to your machine.

## 1a) Adjust the IP address in app.py to be the IP address of your Qidi here: MOONRAKER_API_URL = "http://(your ip without brackets):7125/printer/objects/query"

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

## 5) As a test go to 127.0.0.1:5001 in your browser; you should see the temps at the bottom live for your Qidi.

## 6) Launch OBS Studio (https://obsproject.com/)

## 7) Add a scene.

## Add a browser source and call it something like 'QidiTemps'

## In the browser source untick local file and define the URL as 127.0.0.1:5001

# What if you want to do this on boot?

## Hit Windows key + R, then type ```shell:startup```

## Add a QidiTemps.bat file (edit in notepad or notepad++ for example) like this: 

```@echo off
cd <path to your qidi temps directory where you downloaded my files above>
call venv\Scripts\activate
python app.py
```

