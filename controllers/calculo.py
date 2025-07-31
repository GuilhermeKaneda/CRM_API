from flask import request
from flask_restful import Resource

from models.administrador import Administrador
from models.material import Material


class CalcResource(Resource):

    def calcular_qtd_paineis(self, consumo_mensal: int, horas_sol: int):
        return round((consumo_mensal * 1000) / (horas_sol * 30 * 585))

    def post(self) -> dict:
        data = request.get_json(force=True)

        # Definir com vinicius como vamos obter esses valores!!
        consumo_mensal = data.get("consumo_mensal")
        horas_sol = data.get("horas_sol")

        assinatura_prestador = data.get("valor_prestador")

        materiais = Material.query.one()
        admin = Administrador.query.one()

        if not materiais or not admin:
            return {"error": f"Dados de {"materiais" if not materiais else "admin"} não encontrados no banco"}, 404

        if horas_sol:
            calculo_total = (
                (
                    self.calcular_qtd_paineis(
                        consumo_mensal=consumo_mensal, horas_sol=horas_sol
                    )
                    * materiais.valor_placa
                )
                + admin.valor_assinatura
                + materiais.valor_diversos
                + assinatura_prestador
            )
            return {"resultado": calculo_total}, 200
        else:
            return {"resultado": "Valor inválido: divisão por zero."}, 400
