# TypeTracker
by Szymon Krasuski and Hanna Nykowska

# Idea
This project contain 2 pretty independent apps.

First app is typing listener. Every minute it logs total number of characters pressed on keyboard and buttons pressed on mouse.
App does not register order of typed character - only summarized counts of every character and saves it to .csv file.
Ex. of basic data log:
```
| Date               | Key | Counts |Type|
| ------------------ | --- | ------ |----|
|16-12-2018 15:00:00 | k   | 30     |  k |
|16-12-2018 15:00:00 | e   | 43     |  k |
|16-12-2018 15:00:00 | 5   | 12     |  k |
|16-12-2018 15:01:00 | k   | 22     |  k |
|16-12-2018 15:01:00 | 1   | 4      |  k |
|16-12-2018 15:01:00 | =   | 123    |  k |
```

Second app is a vizualization website hosted with Flask and Dash. 
Application works as http server on localhost.
![GUI](https://github.com/Dysproz/TypeTracker/blob/master/images/gui1.png)
![GUI](https://github.com/Dysproz/TypeTracker/blob/master/images/gui2.png)
Choose date that you want to analize and range of time.
Afterwards you should see two graphs.
One graph shows characters per minute - how many character you typed every minute, so it's possible to measure work performance.
Second graph show how often was used every key. For example for writting in English the most common letter is 'e'.

Although, there's summary section where you can check on average how many characters per minute you type and how you use keyboard and mouse in percents.


## Installation
Project is designed for Python2.7.
In order to install required packages use requirements.txt file.
Command:
```
pip install -r requirements.txt
```

## Running Listener
In order to run listener that should run during the time you want to collect data,
run listener_app.py script.
Ex.
```
python2 listener_app.py
```
Ex. Running script and pushing it to background process
```
nohup python2 listener_app.py &
```
## Running Vizualization
In order to run dash server with vizualization use
visualization_app.py script.
Ex.
```
python2 visualization_app.py
```
Afterwards, in your web browser, enter 127.0.0.1:8050.
You should see UI to draw fantastic graphs.

## Testing code
In order to test code use tox module.
Command:
```
tox
```
