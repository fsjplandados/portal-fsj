# 1. Imagem base do Python
FROM python:3.11-slim

# 2. Configurações de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Define pasta de trabalho
WORKDIR /app

# 4. Instala dependências do sistema (para Postgres)
RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean

# 5. Instala bibliotecas Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia o projeto
COPY . /app/

# 7. Roda o comando de coleta de estáticos (cria a pasta staticfiles)
RUN python manage.py collectstatic --noinput

# 8. Comando para iniciar o servidor (Porta padrão do Render é 10000, mas o Django usa 8000 internamente)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]