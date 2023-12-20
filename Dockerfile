FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py .
COPY *.json .
COPY fixtures ./fixtures/
COPY static ./static/

CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
