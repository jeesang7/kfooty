FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py .
COPY *.json .
COPY fixtures ./fixtures/

CMD ["python", "-m", "gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "--log-level", "debug", "main:app"]
