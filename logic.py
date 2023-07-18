import time
import random
import math
from config import *

food_palete = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                for i in range(NUMBER_OF_COLORS)]
def random_color():
    return random.choice(food_palete)
def random_x():
    return random.randint(0,WIDTH)
def random_y():
    return random.randint(0,HEIGHT)

def dist(a,b):
    x1 = a['x']
    x2 = b['x']
    y1 = a['y']
    y2 = b['y']
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def run(db):
    for i in range(NUMBER_OF_FOOD):
        id = 'food{0}'.format(i)
        db.add(id, '', random_color(), random_x(), random_y())
        db.change_score(id, -60)
    
    while True:
        for user_id in list(db.data.keys()):
            user = db.data[user_id]
            if not user['alive']:
                del db.data[user_id]
                continue
            if user['name'] != '':
                new_x = user['x'] + SPEED*user['vector_x']
                new_y = user['y'] + SPEED*user['vector_y']
                radius = user['score']*1.5 + 100
                radius_to_wall = radius*GO_TO_WALL
                if ((radius_to_wall <= new_x or user['vector_x'] > 0) and
                   (new_x <= WIDTH-radius_to_wall or user['vector_x'] < 0)):
                    user['x'] = new_x
                if ((radius_to_wall <= new_y or user['vector_y'] > 0) and
                   (new_y <= HEIGHT-radius_to_wall or user['vector_y'] < 0)):
                    user['y'] = new_y
                for else_user_id in db.data.keys():
                    else_user = db.data[else_user_id]
                    if else_user['alive'] and else_user['name']=='' and dist(user, else_user) < radius + else_user['score']*1.5 + 100:
                        user['score']+=0.5
                        else_user['alive'] = False
        time.sleep(0.02)