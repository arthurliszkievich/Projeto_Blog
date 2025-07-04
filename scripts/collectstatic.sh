#!/bin/sh
# Coleta os arquivos estáticos
echo "Collecting Static Files..."
python manage.py collectstatic --noinput 