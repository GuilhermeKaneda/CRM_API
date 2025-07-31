from models.user import db


class Material(db.Model):
    __tablename__ = "material"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor_diversos = db.Column(db.Float, nullable=False)
    valor_placa = db.Column(db.Float, nullable=False)
