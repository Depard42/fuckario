#from multiprocessing import Process
from app.app import app, socketio
from config import *



if __name__ == "__main__":
    socketio.run(app, debug=False, host=HOST, port=PORT)