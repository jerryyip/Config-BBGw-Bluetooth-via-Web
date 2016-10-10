#!/usr/bin/env python


import time
from led1 import myledon, myledoff
from mywificar import goFront, goBack, stop
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

def background_thread(): 
     """Example of how to send server generated events to clients.""" 
     count = 0 
     while True: 
         socketio.sleep(10) 
         count += 1 
         socketio.emit('my_response', 
                       {'data': 'Server generated event', 'count': count}, 
                       namespace='/test') 


@app.route('/')
def index():
    return render_template('index.html',async_mode=socketio.async_mode)

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('add_event', namespace='/test')
def add_message():
    session['receive_count'] = session.get('receive_count', 0) + 1
    print("get addd")
    myledon()
    emit('my response',{'data': "add" , 'count': session['receive_count']})

@socketio.on('minus_event', namespace='/test')
def minus_message():
    session['receive_count'] = session.get('receive_count', 0) + 1
    print("get minus")
    myledoff()
    emit('my response',{'data': "minus" , 'count': session['receive_count']})

        
if __name__ == '__main__':
    socketio.run(app,host='192.168.7.48', debug=False)
