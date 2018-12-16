# TypeTracker
by Szymon Krasuski and Hanna Nykowska

## Installation
Project is designed for Python2.7.
In order to install required packages use requirements.txt file.
Command:
```
pip install -r requirements.txt
```

## Running Listener
In order to run listener that should run during the time you want to collect data,
run run_listener.py script.
Ex.
```
python2 run_listener.py
```
Ex. Running script and pushing it to background process
```
python2 run_listener.py &
```
## Running Vizualization
In order to run dash server with vizualization use
viz_app.py script.
Ex.
```
python2 viz_app.py
```
Afterwards, in your web browser, enter 127.0.0.1:8050.
You should see UI to draw fantastic graphs.

## Testing code
In order to test code use tox module.
Command:
```
tox
```
