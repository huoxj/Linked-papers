FROM docker.io/python:3.12-slim

ENV MYSQL_URL mysql-jenkins
ENV MYSQL_USER root
ENV MYSQL_ROOT_PASSWORD root

WORKDIR /app

COPY . .

RUN sed -i "s/password: .*/password: ${MYSQL_ROOT_PASSWORD}/" config/config.yaml
RUN sed -i "s/url: .*/url: ${MYSQL_URL}/" config/config.yaml

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app"]