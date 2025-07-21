from flask import Flask
from flask_restful import Api
from models.user import db as db_model
from controllers.user import UsersResource

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db_model.init_app(app)

    # pelo q entendi, recria as tabelas quando nao existem
    with app.app_context():
        db_model.create_all()

    api = Api(app)
    # rotas
    api.add_resource(UsersResource, '/users', '/users/<int:user_id>', endpoint='users')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
