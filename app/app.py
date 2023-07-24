from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from uuid import uuid4

from flask import session
from flask_session import Session

from engineio.payload import Payload
Payload.max_decode_packets = 50

import data_connector as data_client
from config import *
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app)

mes = ['']*10

@app.route("/", methods=["GET", "POST"])
def func():
    if request.method == 'POST':
        session['id'] = uuid4().hex
        session['username'] = str(request.form['username'])
        session['color'] = str(request.form['color'])
        session['last_update_vector'] = datetime.datetime.now()
        data_client.add(session['id'], session['username'], session['color'], x=100, y=100)
        print(session['username'], "connected with color", session["color"])
        return render_template("game.html", mes=mes, WIDTH=WIDTH, HEIGHT=HEIGHT, FOOD_NAME=FOOD_NAME, START_RADIUS=START_RADIUS)
    return render_template("index.html")



@socketio.on('connect')
def connect():
    session['sid'] = request.sid

@socketio.on('disconnect')
def disconnect():
    print("discon!!!!!")

@socketio.on('vector')
def new_vector(data):
    curr_time = datetime.datetime.now()
    if (curr_time-session['last_update_vector']).total_seconds() > 0.25:
        data_client.change_vector(session['id'], data['x'], data['y'])
        session['last_update_vector']=datetime.datetime.now()

@socketio.on('send_mes')
def send_mes(data):
    global mes
    mes.pop(0)
    mes.append(session['username']+": "+data['mes'])
    socketio.emit('take_mes', {'mes': mes[-1]})

last_update_time = datetime.datetime.now()
last_update_data = 0
@socketio.on('get update')
def get_update(data):
    global last_update_time
    global last_update_data
    curr_time = datetime.datetime.now()
    if (curr_time-last_update_time).total_seconds() > 0.0166:
        last_update_data = data_client.get_all()
        last_update_time = curr_time
    last_update_data['curr_id'] = session['id']
    socketio.emit('update', last_update_data, room=session['sid'])