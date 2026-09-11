FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py wsgi.py ./
COPY templates/ templates/
COPY static/ static/
COPY assets/ assets/
COPY migrations/ migrations/

RUN mkdir -p data

EXPOSE 5000

CMD ["sh", "-c", "flask db upgrade && gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 4 --timeout 60 wsgi:app"]
