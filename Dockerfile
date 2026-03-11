FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && app-get install -y \
    libpq-dev \
    gcc \
    gettext \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cahce-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py migrate && gunicorn reverence.wsgi.application --bind 0.0.0.0:8000"]