import socket
import logic
import json
from _thread import *
from config import *


class Data:
    def __init__(self):
        self.data = {}
    def get_byid(self,id):
        return self.data[id]
    def get_all(self):
        return json.dumps(self.data)
    def del_byid(self, id):
        pass
    def add(self, id, name, color, x, y):
        self.data[id] = {'name': name, 
                         'color':color, 
                         'x':float(x), 
                         'y':float(y), 
                         'vector_x':0., 
                         'vector_y':0., 
                         'score': 0,
                         'alive': True}
        return True
    def change_vector(self, id, vector_x, vector_y):
        self.data[id]['vector_x'] = float(vector_x)
        self.data[id]['vector_y'] = float(vector_y)
        return True
    def change_xy(self, id, x, y):
        self.data[id]['x'] = float(x)
        self.data[id]['y'] = float(y)
        return True
    def change_score(self, id, score):
        self.data[id]['score'] = score

def command_interpreter(db, r):
    r_command = r.split()[0]
    r_args = r.split()[1:]
    if r_command == 'add':
        db.add(*r_args)
    elif r_command == 'change_vector':
        db.change_vector(*r_args)
    elif r_command == 'get_all':
        return db.get_all()
    return "all done, sir"


def serv_run():
    db = Data()
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        soc.bind((DS_HOST, DS_PORT))
    except socket.error as e:
        print(e)

    soc.listen(2)
    print("Data Server Waiting for connections")

    def treaded_client(conn):
        conn.send(str.encode("Connected"))
        reply = ""
        while True:
            try:
                get_recv = conn.recv(2048)
                get_recv_decode = get_recv.decode("utf-8")

                if not get_recv:
                    print("Disconnected from Data Server")
                    break
                else:
                    reply = command_interpreter(db, get_recv_decode)
                conn.sendall(str.encode(reply))
            except:
                break
        print("lost connections to Data Server")
        conn.close()
    start_new_thread(logic.run, (db,))
    while True:
        conn, addr = soc.accept()
        print("Data Server Connected to ", addr)
        start_new_thread(treaded_client, (conn,))

if __name__ == "__main__":
    serv_run()