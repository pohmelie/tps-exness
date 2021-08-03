FROM python:3.8-slim

COPY requirements/production.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./ /tps-exness
RUN pip install -e /tps-exness

CMD ["python", "-m", "tps_exness"]
