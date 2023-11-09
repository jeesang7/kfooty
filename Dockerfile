FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py .
COPY *.json .

CMD ["python", "./main.py"]
