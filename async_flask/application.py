"""
Demo flask application to stream in real time JSON files 
Example modified from https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/
Code by: Diego Pinochet  -  November 2019
"""

# Start with a basic flask app webpage and import Numpy and JSON
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import numpy as np 
import json

__author__ = 'dp'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

def randomNumberGenerator():
    """
    Generate a random number every .001 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of Json
    while not thread_stop_event.isSet():
        number = round(random()*10, 3)

        # x =  { "name":"Lukas", "age":number, "Country":"Austria"}
        # x["age"]=number
        x= np.random.rand(3,2)
        y = json.dumps(x.tolist())
        # y[1]= number
        print(y)
        socketio.emit('newnumber', {'number': y}, namespace='/test')
        socketio.sleep(0.001)


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
