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

def dist(a,b): #растояние между двумя точками на плоскости
    x1 = a['x']
    x2 = b['x']
    y1 = a['y']
    y2 = b['y']
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

eaten_food_ids = []
def eat(who, whom):
    who['score'] += whom['score']
    who['radius'] += whom['score'] * INCREMENT_RADIUS_PER_SCORE
    whom['alive'] = False

def gen_food(db, id):
    db.add(id, FOOD_NAME, random_color(), random_x(), random_y())
    db.change_score(id, FOOD_SCORE)
    db.change_radius(id, FOOD_RADIUS)

def run(db):
    for i in range(NUMBER_OF_FOOD):
        gen_food(db, 'food{0}'.format(i))
    
    while True:
        if eaten_food_ids != []:
            gen_food(db, eaten_food_ids.pop(0))
        for user_id in list(db.data.keys()):
            user = db.data[user_id]
            if not user['alive']:
                if user['name'] ==FOOD_NAME:
                    eaten_food_ids.append(user_id)
                db.delete_byId(user_id)
                continue
            if user['name'] != '':
                new_x = user['x'] + SPEED*user['vector_x']
                new_y = user['y'] + SPEED*user['vector_y']
                radius = user['radius']
                radius_to_wall = radius*GO_TO_WALL
                if ((radius_to_wall <= new_x or user['vector_x'] > 0) and
                   (new_x <= WIDTH-radius_to_wall or user['vector_x'] < 0)):
                    user['x'] = new_x
                if ((radius_to_wall <= new_y or user['vector_y'] > 0) and
                   (new_y <= HEIGHT-radius_to_wall or user['vector_y'] < 0)):
                    user['y'] = new_y
                for else_user_id in db.data.keys():
                    else_user = db.data[else_user_id]
                    if else_user['alive']  and dist(user, else_user) < radius + else_user['radius']:# and else_user['name']==FOOD_NAME:
                        if user['radius'] / else_user['radius'] > 1.3:
                            eat(user, else_user)
                        elif else_user['radius'] / user['radius'] > 1.3:
                            eat( else_user,user)
        time.sleep(0.0166)