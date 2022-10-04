from app import app
from flask import jsonify, render_template, request
from ..views import users, helper, items
from ..apis import collaborative_filtering_rec
from ..apis import content_based_rec
import time
import json
from sqlalchemy import *
import os

engine = create_engine('sqlite:///./db1.db?check_same_thread=False')


#Insert a user
@app.route('/user', methods=['POST'])
def post_user():
    user = request.get_json()
    engine.execute('INSERT INTO users (userId, itemId, rating, timestamp) VALUES (:userId, :itemId, :rating, :timestamp)', user)
    return jsonify(user)
    #return users.post_user()

def delete_user():
    user = request.get_json()
    engine.execute('DELETE FROM users WHERE userId = :userId', user)
    return jsonify(user)
    #return users.delete_user()

#Returns a user
@app.route('/user', methods=['GET'])
def get_user():
    user = request.get_json()
    result = engine.execute('SELECT * FROM users WHERE userId = :userId', user).fetchone()
    return jsonify(result)

#Returns all users
@app.route('/users', methods=['GET'])
def get_users():
    result = engine.execute('SELECT * FROM users').fetchall()
    return jsonify(result)

#Returns the events of a user
@app.route('/user/events', methods=['GET'])
def get_events():
    user = request.get_json()
    result = engine.execute('SELECT * FROM events WHERE userId = :userId', user).fetchall()
    return jsonify(result)

#Insert an item
#Returns an item
@app.route('/item', methods=['POST','GET'])
def post_item():
    if request.is_json:
        content = request.get_json()
    elif request.args:
        content = dict(request.args)
    elif request.files['csv']:
        content = request.files['csv']
    elif request.method == 'GET':
        return items.get_item()

    return items.post_item(content)

#Delete an item
@app.route('/item', methods=['DELETE'])
def delete_item():
    item = request.get_json()
    engine.execute('DELETE FROM items WHERE itemId = :itemId', item)
    return jsonify(item)
    #return items.delete_item()


#Returns similar items
@app.route('/item/neighbors', methods=['GET'])
def get_similar_items():
    itemno = 1
    nitems = 3
    try:
        jso = request.get_json()
        if jso["itemno"]:
            itemno = int(jso["itemno"])
    except:
        pass
    try:
        jso = request.get_json()
        if jso["nitems"]:
            nitems = int(jso["nitems"])
    except:
        pass
    lis = []
    start = time.perf_counter()
    dict = {}
    dict["Item_number"] = str(1)
    lis = content_based_rec.start(1,itemno,nitems)
    end = time.perf_counter() - start
    dict["API_exec_time"] = str(end)
    lis.append(dict)
    return jsonify(items=lis)

#Returns all items
@app.route('/items', methods=['GET'])
def get_items():
    return items.get_items()

#Returns the events of an item
@app.route('/item/events', methods=['GET'])
def get_item_events():
    item = request.get_json()
    result = engine.execute('SELECT * FROM events WHERE itemId = :itemId', item).fetchall()
    return jsonify(result)

#Add an event
@app.route('/event', methods=['POST'])
def post_event():
    event = request.get_json()
    engine.execute('INSERT INTO events (userId, itemId, rating, timestamp) VALUES (:userId, :itemId, :rating, :timestamp)', event)
    return jsonify(event)


#Returns all events
@app.route('/events', methods=['GET'])
def get_events():
    result = engine.execute('SELECT * FROM events').fetchall()
    return jsonify(result)

#Returns recommendations of an user - COLLABORATIVE FILTERING
@app.route('/user/recommendations', methods=['GET'])
def get_user_rec():
    #return users.get_user_rec()
    nrec = request.args.get('nrec')
    sel_item = request.args.get('sel_item')
    start = time.perf_counter()
    results = collaborative_filtering_rec.start(nrec,sel_item)
    end = time.perf_counter() - start
    print("API EXECUTION TIME: "+str(end))
    return results

#Train the recommender
@app.route('/train', methods=['POST'])
def post_user_rec():
    return train.train_rec()

@app.route('/system', methods=['GET'])
def get_system():
    uptime = os.system("uptime")
    total_ram = os.system("free -m | awk 'NR==2{print $2}'")
    available_ram = os.system("free -m | awk 'NR==2{print $7}'")
    cpu_model = os.system("cat /proc/cpuinfo | grep 'model name' | uniq | awk -F: '{print $2}'")
    cpu_clock = os.system("cat /proc/cpuinfo | grep 'cpu MHz' | uniq | awk -F: '{print $2}'")
    database_size = os.system("du -sh /path/to/database")
    return jsonify({'uptime': uptime, 'total_ram': total_ram, 'available_ram': available_ram, 'cpu_model': cpu_model, 'cpu_clock': cpu_clock, 'database_size': database_size})
