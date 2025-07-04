#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Espera o banco de dados ficar pronto (opcional, mas recomendado)
# Use o mesmo laço que você já tem em commands.sh se quiser.

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Executa o comando passado para o script (o "CMD" do Dockerfile)
# O `exec` é importante para que o Gunicorn se torne o processo principal (PID 1)
# e receba os sinais do Docker corretamente (ex: para parar o container).
exec "$@"