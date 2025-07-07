#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Espera o PostgreSQL iniciar
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2 # Pequeno sleep para não sobrecarregar
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"
