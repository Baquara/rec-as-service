import csv
from io import StringIO
from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.users import Users, user_schema, users_schema
from werkzeug import datastructures
from sqlalchemy import *

engine = create_engine('sqlite:///./db1.db?check_same_thread=False')

#Insert item


def get_items():
    result = engine.execute('SELECT * FROM items').fetchall()
    return jsonify(result)

def get_item():
    item = request.get_json()
    result = engine.execute('SELECT * FROM items WHERE itemId = :itemId', item).fetchone()
    return jsonify(result)

def post_item(content):
    if isinstance(content, datastructures.FileStorage):
        data = content.stream.read()
        stream = StringIO(data.decode("UTF8"), newline=None)
        dict_reader = csv.DictReader(stream)
        lis = []
        for row in dict_reader:
            lis.append(row)
        for x in lis:
            if '\ufeffitemId' in x and 'title' in x and 'description' in x and 'tag' in x:
                engine.execute('INSERT INTO items (itemId, title, description, tag) VALUES (:itemId, :title, :description, :tag)', x)
                return {'status': 201, 'message': 'Created Items'}
            else:
                return {'status': 400, 'message': 'Bad Request'}
    for x in content:
        if isinstance(content, list):
            if 'itemId' in x and 'title' in x and 'description' in x and 'tag' in x:
                engine.execute('INSERT INTO items (itemId, title, description, tag) VALUES (:itemId, :title, :description, :tag)', x)
                return {'status': 201, 'message': 'Created Items'}
            else:
                return {'status': 400, 'message': 'Bad Request'}
        else:
            break
    if isinstance(content, dict):
        if 'itemId' in content and 'title' in content and 'description' in content and 'tag' in content:
            engine.execute('INSERT INTO items (itemId, title, description, tag) VALUES (:itemId, :title, :description, :tag)', x)
            return {'status': 201, 'message': 'Created Item'}
        else:
            return {'status': 400, 'message': 'Bad Request'}
    return {'status': 400, 'message': 'Bad Request'}


            

'''  elif isinstance(content, str):
        try:
            reader = csv.DictReader(StringIO(content))
            for row in reader:
                if 'itemId' in row and 'title' in row and 'description' in row and 'tag' in row:
                    return {'status': 201, 'message': 'Created Item'}
                else:
                    return {'status': 400, 'message': 'Bad Request'}
        except:
            return {'status': 400, 'message': 'Bad Request'}
    else:
        return {'status': 400, 'message': 'Bad Request'}'''

'''
#Insert item
def post_item():
    username = request.json['username']
    password = request.json['password']
    pass_hash = generate_password_hash(password)
    user = Items(username, pass_hash)
    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message':'Usuario cadastrado com sucesso', 'data': result}),201
    except Exception as e:
        print(e)
        return jsonify({'message':'Erro ao cadastrar usuario.','data':{}}),500

        '''

#Atualizar/editar usuário
def update_user(id):
    username = request.json['username']
    password = request.json['password']
    
    user = Users.query.get(id)

    if not user:
        return jsonify({'message':"Usuario nao existe.",'data':{}}), 404

    pass_hash = generate_password_hash(password)

    try:
        user.username = username
        user.password = pass_hash
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message':'Cadastro atualizado com sucesso.', 'data': result}),201
    except Exception as e:
        print(e)
        return jsonify({'message':'Erro ao atualizar cadastro.','data':{}}),500

#Coletar dados de usuário
def get_user(id):
    user = Users.query.get(id)
    if user:
        result = user_schema.dump(user)
        return jsonify({'message':'succesfully fetched','data':result}), 201

    return jsonify({'message':"user don't exist",'data':{}}), 404

#Deletar o usuário
def delete_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message':"O usuario nao existe.",'data':{}}),404
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            result = user_schema.dump(user)
            return jsonify({'message':'Cadastro deletado com sucesso.','data':result}), 200
        except:
            return jsonify({'message':'Erro ao deletar o cadastro.','data':{}}),500

#Função auxiliar para localizar usuário
def user_by_username(username):
    try:
        return Users.query.filter(Users.username == username).one()
    except:
        return None
