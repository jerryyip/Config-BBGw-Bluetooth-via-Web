#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode =None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import time
import subprocess
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template('index.html')

@socketio.on('pair event', namespace='/test')
def pair_message(message):
#    scan = True
	session['receive_count'] = session.get('receive_count', 0) + 1     
#     	pair_a=message['data']+'\n'    
#	pair_a=''
#   data = 1 or 2
	pair_a=message['data']
#	pair_p = subprocess.Popen("python /home/debian/bin/bluetoothtest.py",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#	pair_p.stdin.write(pair_a)
#	pair_b=''
#	for line in pair_p.stdout.readlines():
#        pair_b = pair_b + line + '\n\r'
    if (pair_a == '1'): 
        emit('my response',{'data': "add" , 'count': session['receive_count']})
        print("receive add command")
    if (pair_a == '2'): 
        emit('my response',{'data': "minus" , 'count': session['receive_count']})
        print("receive minus command")
        
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', debug=False)
