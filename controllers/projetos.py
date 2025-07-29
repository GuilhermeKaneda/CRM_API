from flask import request
from flask_restful import Resource
from sqlalchemy import func
from datetime import datetime, date

from models.projeto import Project, db

# mapa dos meses 
MESES_PT = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
    5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
    9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
}

class ProjectsResource(Resource):
    def get(self, projeto_id=None):
        # o if divide o endpoint em 4 partes
        # busca por ID (?projeto_id=123)
        if projeto_id:
            projeto = Project.query.get(projeto_id)
            if not projeto:
                return {"error": "Projeto não encontrado"}, 404
            return {"projeto": projeto.to_dict()}, 200

        # calculo de projetos feitos (?stats=1)
        stats = request.args.get("stats", type=str)
        if stats and stats.lower() in ("1", "true", "s", "sim"):
            rows = (
                db.session.query(
                    func.extract("year", Project.data_final).label("ano"),
                    func.extract("month", Project.data_final).label("mes"),
                    func.count(Project.projeto_id).label("done"),
                    func.coalesce(func.sum(Project.valor_total), 0).label("revenue")
                )
                .filter(Project.status == "feito")
                .group_by("ano", "mes")
                .order_by("ano", "mes")
                .all()
            )

            output = {}
            for ano, mes, done, revenue in rows:
                ano = int(ano); mes = int(mes)
                if ano not in output:
                    output[ano] = {
                        MESES_PT[m]: {"done": 0, "revenue": 0}
                        for m in range(1, 13)
                    }
                output[ano][MESES_PT[mes]] = {
                    "done": int(done),
                    "revenue": float(revenue)
                }
            return output, 200

        # busca por prestador (?prestador_id=123)
        prestador_id = request.args.get("prestador_id", type=int)
        if prestador_id:
            projetos = Project.query.filter_by(prestador_id=prestador_id).all()
            return {
                "prestador_id": prestador_id,
                "projetos": [p.to_dict() for p in projetos]
            }, 200

        # lista geral (/projects)
        projetos = Project.query.all()
        return {"projetos": [p.to_dict() for p in projetos]}, 200

    def post(self):
        data = request.get_json(force=True)

        try:
            data_solicitacao = datetime.fromisoformat(data["data_solicitacao"])
            data_inicial = date.fromisoformat(data["data_inicial"])
            data_final = date.fromisoformat(data["data_final"])

            projeto = Project(
                cliente_id = data["cliente_id"],
                prestador_id = data["prestador_id"],
                estado = data["estado"],
                data_solicitacao = data_solicitacao,
                data_inicial = data_inicial,
                data_final = data_final,
                prazo_dias = data["prazo_dias"],
                valor_prestador = data["valor_prestador"],
                valor_material = data["valor_material"],
                valor_assinatura = data["valor_assinatura"],
                valor_total = data["valor_total"],
                status = data["status"]
            )

            db.session.add(projeto)
            db.session.commit()

            return {"message": "Projeto criado com sucesso", "projeto": projeto.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Erro ao criar projeto: {str(e)}"}, 500

    def put(self, projeto_id):
        projeto = Project.query.get(projeto_id)
        if not projeto:
            return {"error": "Projeto não encontrado"}, 404

        data = request.get_json(force=True)

        # Busca cada coluna de projeto e verifica se essa coluna veio no payload. Se sim, atualiza no banco
        for attr in [
            "cliente_id",
            "prestador_id",
            "estado",
            "data_solicitacao",
            "data_inicial",
            "data_final",
            "prazo_dias",
            "valor_prestador",
            "valor_material",
            "valor_assinatura",
            "valor_total",
            "status",
        ]:
            if attr in data:
                setattr(projeto, attr, data[attr])

        db.session.commit()
        return {"message": "Projeto atualizado com sucesso", "projeto": projeto.to_dict()}, 200

    def delete(self, projeto_id):
        projeto = Project.query.get(projeto_id)
        if not projeto:
            return {"error": "Projeto não encontrado"}, 404

        db.session.delete(projeto)
        db.session.commit()
        return {"message": "Projeto excluído com sucesso"}, 200
