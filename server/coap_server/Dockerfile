FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY config.py .
COPY database.py .
COPY server.py .

CMD ["python", "server.py"]