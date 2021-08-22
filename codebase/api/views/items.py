from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.users import Users, user_schema, users_schema

#Cadastrar usuário
def post_user():
    username = request.json['username']
    password = request.json['password']
    pass_hash = generate_password_hash(password)
    user = Users(username, pass_hash)
    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message':'Usuario cadastrado com sucesso', 'data': result}),201
    except Exception as e:
        print(e)
        return jsonify({'message':'Erro ao cadastrar usuario.','data':{}}),500

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