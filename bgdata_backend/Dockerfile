FROM docker.io/python:3.12-slim

ENV MYSQL_USER root
ENV MYSQL_ROOT_PASSWORD root

WORKDIR /app

COPY . .

RUN sed -i 's/password: .*/password: root/' config/config.yaml

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app"]