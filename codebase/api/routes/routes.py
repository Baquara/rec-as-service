from app import app
from flask import jsonify, render_template
from ..views import users, helper, items, events, train

#Insert a user
@app.route('/user', methods=['POST'])
def post_user():
    return users.post_user()

#Delete a user
@app.route('/user', methods=['DELETE'])
def delete_user():
    return users.delete_user()

#Returns a user
@app.route('/user', methods=['GET'])
def get_user():
    return users.get_user()

#Returns similar users
@app.route('/user/neighbors', methods=['GET'])
def get_similar_users():
    return users.get_similar_users()

#Returns all users
@app.route('/users', methods=['GET'])
def get_users():
    return users.get_users()

#Returns the events of a user
@app.route('/user/events', methods=['GET'])
def get_events():
    return users.get_events()

#Insert an item
@app.route('/item', methods=['POST'])
def post_item():
    return items.post_item()

#Delete an item
@app.route('/item', methods=['DELETE'])
def delete_item():
    return items.delete_item()

#Returns an item
@app.route('/item', methods=['GET'])
def get_item():
    return items.get_item()

#Returns similar items
@app.route('/item/neighbors', methods=['GET'])
def get_similar_items():
    return items.get_similar_items()

#Returns all items
@app.route('/items', methods=['GET'])
def get_items():
    return items.get_items()

#Returns the events of an item
@app.route('/item/events', methods=['GET'])
def get_item_events():
    return items.get_events()

#Add an event
@app.route('/event', methods=['POST'])
def post_event():
    return events.add_event()

#Return an event
@app.route('/event', methods=['GET'])
def get_event():
    return events.get_event()

#Returns recommendations of an user
@app.route('/user/recommendations', methods=['GET'])
def get_user_rec():
    return users.get_user_rec()

#Train the recommender
@app.route('/train', methods=['POST'])
def post_user_rec():
    return train.train_rec()

#Get system statistics
@app.route('/statistics', methods=['GET'])
def get_statisctics():
    return train.train_rec()