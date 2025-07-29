import requests

"""
url = "http://127.0.0.1:5555/users"

data = {
    "nome": "Pedro Alvez",
    "email": "pedro.alvez@example.com",
    "senha": "SenhaForte!23",
    "telefone": "(11) 99999-8888",
    "tipo": "cliente",
    "documento_identidade": "12345678901",
    "endereco": "Rua das Flores, 123, São Paulo, SP, 01234-567",
    "conta_energia_url": 125.75,
    "conta_kilowatts": 320.40
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
try:
    print("JSON Response:", response.json())
except Exception:
    print("Resposta não é JSON:", response.text)
"""

url = "http://127.0.0.1:5555/projetos"

data = {
    "cliente_id": 2,
    "prestador_id": 1,
    "estado": "SP",
    "data_solicitacao": "2025-07-29T14:30:00",
    "data_inicial": "2025-08-01",
    "data_final": "2025-08-15",
    "prazo_dias": 15,
    "valor_prestador": 5000.00,
    "valor_material": 1500.00,
    "valor_assinatura": 200.00,
    "valor_total": 6700.00,
    "status": "feito"
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
try:
    print("JSON Response:", response.json())
except Exception:
    print("Resposta não é JSON:", response.text)