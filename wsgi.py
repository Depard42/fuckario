#from multiprocessing import Process
from app.app import app, socketio
from config import *



if __name__ == "__main__":
    socketio.run(app, debug=True, host=HOST, port=PORT)