# 1. FIXAMOS a versão 'bookworm' (Estável) para evitar erros do Trixie
FROM python:3.11-slim-bookworm

# 2. Configurações de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Define pasta de trabalho
WORKDIR /app

# 4. Instala dependências do sistema
# Adicionamos --no-install-recommends para baixar menos coisas
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Instala bibliotecas Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia o projeto
COPY . /app/

# 7. Coleta arquivos estáticos
RUN python manage.py collectstatic --noinput

# 8. Inicia o servidor
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
