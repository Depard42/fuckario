import socket
import json
from config import *

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = DS_HOST
        self.port = DS_PORT
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
    def sendBIG(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048*60).decode()
        except socket.error as e:
            print(e)

n = Network()

def get_byid(id):
    return n.send("get_byid {0}".format(id))
def get_all():
    res = n.sendBIG("get_all")
    return json.loads(res)
def del_byid(id):
    return n.send("del_byid {0}".format(id))
def add(id, name, color, x, y):
    return n.send("add {0} {1} {2} {3} {4}".format(id, name, color, x, y))
def change_vector(id, vector_x, vector_y):
    return n.send("change_vector {0} {1} {2}".format(id, vector_x, vector_y))
def change_xy(id, x, y):
    return n.send("change_vector {0} {1} {2}".format(id, x, y))