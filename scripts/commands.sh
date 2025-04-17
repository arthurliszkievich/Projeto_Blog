#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Espera o PostgreSQL iniciar
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2 # Pequeno sleep para não sobrecarregar
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

# Aplica as migrações do banco de dados
echo "Applying Database Migrations..."
python manage.py migrate --noinput

# Coleta os arquivos estáticos
echo "Collecting Static Files..."
python manage.py collectstatic --noinput 

# Inicia o servidor de desenvolvimento Django
# IMPORTANTE: Este deve ser o ÚLTIMO comando, pois ele não termina
# a menos que seja interrompido (Ctrl+C ou docker stop)
echo "Starting Django Development Server..."
python manage.py runserver 0.0.0.0:8000