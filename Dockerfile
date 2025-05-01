
FROM python:3.11-slim

WORKDIR /app

COPY service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY service/ .

EXPOSE 8000


CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
