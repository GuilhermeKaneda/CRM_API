from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(15), unique=True, nullable=False)
    senha = db.Column(db.String(25), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    tipo = db.Column(db.String(10), nullable=False)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.senha, raw_password)

    def set_password(self, raw_password: str):
        self.senha = generate_password_hash(raw_password)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "nome": self.nome,
            "email": self.email,
            # não expoe a senha_hash
            "telefone": self.telefone,
            "tipo": self.tipo,
        }
