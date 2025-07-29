from flask import request
from flask_restful import Resource

from models.user import User, db

class LoginResource(Resource):
    def post(self):
        data = request.get_json(force=True)
        email = data.get("email")
        senha = data.get("senha")
        if not email or not senha:
            return {"error": "Email e senha são obrigatórios"}, 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(senha):
            return {"error": "Email ou senha inválidos"}, 401

        return {"user": user.to_dict()}, 200
