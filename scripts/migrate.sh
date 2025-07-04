#!/bin/sh
# Aplica as migrações do banco de dados
echo "Applying Database Migrations..."
python manage.py migrate --noinput
