from flask import jsonify
from app import db
from app.models import User
from app.api import bp
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from app.api.auth import basic_auth

token_auth = HTTPTokenAuth()

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None