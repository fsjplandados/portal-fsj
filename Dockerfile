# MUDE DISSO:
# FROM python:3.11-slim-bookworm

# PARA ISSO (Versão 3.12):
FROM python:3.12-slim-bookworm

# ... (Mantenha o resto do arquivo EXATAMENTE igual, inclusive o truque da SECRET_KEY)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# O truque da chave falsa continua aqui, é essencial
RUN SECRET_KEY=django-insecure-build-key \
    DATABASE_URL=sqlite:///db.sqlite3 \
    python manage.py collectstatic --noinput

CMD python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000
