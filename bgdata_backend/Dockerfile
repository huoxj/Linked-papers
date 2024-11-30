FROM docker.io/python:3.12-slim

ENV MYSQL_URL mysql-jenkins
ENV MYSQL_USER root
ENV MYSQL_ROOT_PASSWORD root

ENV DATA_REMOTE_URL http://192.168.1.133:6666/

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y wget

RUN sed -i "s/password: .*/password: ${MYSQL_ROOT_PASSWORD}/" config/config.yaml
RUN sed -i "s/url: .*/url: ${MYSQL_URL}/" config/config.yaml

RUN mkdir data
RUN wget ${DATA_REMOTE_URL}/papers.csv -O data/papers.csv
RUN wget ${DATA_REMOTE_URL}/papers_pred.csv -O data/papers_pred.csv
RUN wget ${DATA_REMOTE_URL}/similar_papers.csv -O data/similar_papers.csv

CMD ["python", "scripts/load_data.py"]

RUN pip install --no-cache-dir -r requirements_runtime.txt

CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]