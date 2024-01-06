FROM python:3.10

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y install redis-server

COPY src src
COPY app.py app.py
COPY settings.py settings.py
COPY run.sh run.sh

EXPOSE 8080

ENTRYPOINT ["bash", "run.sh"]
