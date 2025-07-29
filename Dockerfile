FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5555
# Opcional: ativa o modo debug se for ambiente de dev
# ENV FLASK_ENV=development

EXPOSE 5555

CMD ["flask", "run"]
