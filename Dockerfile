# 1. Versão estável do Linux (Bookworm)
FROM python:3.11-slim-bookworm

# 2. Configurações
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Pasta de trabalho
WORKDIR /app

# 4. Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Instala Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia o código
COPY . /app/

# 7. Coleta estáticos (COM O TRUQUE DA CHAVE FALSA)
# Definimos valores fake apenas para este comando funcionar no build
RUN SECRET_KEY=django-insecure-build-key \
    DATABASE_URL=sqlite:///db.sqlite3 \
    python manage.py collectstatic --noinput

# 8. Inicia o servidor
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
