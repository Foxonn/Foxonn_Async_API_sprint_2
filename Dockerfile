FROM python:3.10

COPY api api
COPY requirements.txt .

RUN  pip install -r requirements.txt

COPY /services/api /services/api:ro

ENTRYPOINT supervisord -c /services/api/supervisord.conf -n