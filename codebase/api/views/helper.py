import datetime
from functools import wraps
from app import app
from flask import request, jsonify
from .users import user_by_username
import jwt
from werkzeug.security import check_password_hash


# Gerando token com base na Secret key do app e definindo expiração com 'exp'
def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Nao pode ser verificado.', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401
    user = user_by_username(auth.username)
    if not user:
        return jsonify({'message': 'Usuario nao encontrado.', 'data': []}), 401

    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.now() + datetime.timedelta(hours=12) },
                           app.config['SECRET_KEY'])
        return jsonify({'message': 'Logado com sucesso.', 'token': token.decode('UTF-8'),
                        'exp': datetime.datetime.now() + datetime.timedelta(hours=12)})

    return jsonify({'message': 'Nao pode ser verificado.', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401 


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            headers = request.headers
            bearer = headers.get('Authorization')
            token = bearer.split()[1]
        except:
            return jsonify({'message': 'Token nao encontrado.', 'data': []}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user_by_username(username=data['username'])
        except:
            return jsonify({'message': 'Token invalido ou expirado.', 'data': []}), 401
        return f(current_user, *args, **kwargs)
    return decorated


