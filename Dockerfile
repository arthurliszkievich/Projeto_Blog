# Modelo de Dockerfile para mim

# --- Estágio 1: "Builder" ---
FROM python:3.10-slim-bookworm AS builder

# Variáveis de ambiente para um build limpo e eficiente
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

# Instala as dependências do sistema necessárias para compilar pacotes Python
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev

# Cria um ambiente virual isolado dentro da imagem
RUN python -m venv /opt/venv
# Ativa o venv para os comandos subsequentes nesta etapa
ENV PATH="/opt/venv/bin:$PATH"

# Copia apenas o arquivo de requisitos para otimizar o cache
WORKDIR /app
COPY ./djangoapp/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# --- Estágio 2: "Runtime" ---
FROM python:3.10-slim-bookworm AS runtime

# Instala apenas as dependências de sistema necessárias para RODAR a aplicação
# `libpq5` é a bibilioteca de runtime para o PostgreSQL, muito menor que o `libpq-dev`
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Cria um usuário e grupo não-root para a aplicação
RUN addgroup --system django && adduser --system -ingroup django django

# Cria um diretório da aplicação
WORKDIR /home/django/web

# Copia o ambiente virtual do estágio de build
# A vantagem é que a imagem final não tem as ferramentas de build, apenas o ambiente virtual
COPY --from=builder /opt/venv /opt/venv

#Copia o script da entrypoint
COPY ./entrypoint.prod.sh /entrypoint.prod.sh
RUN sed -i 's/\r$//g' /entrypoint.prod.sh && chmod +x /entrypoint.prod.sh

# Copia o código da aplicação para o diretório de trabalho
COPY ./djangoapp .



# Define o dono de todos os arquivos para o usuário não-root 
# Isso é importante para evitar problemas de permissão
RUN chown -R django:django /home/django/web /entrypoint.prod.sh

# Muda para o usuário não-root
USER django

# Degine o PATH para que o sistema use o python e os pacotes do venv
ENV PATH="/opt/venv/bin:$PATH"

# Expõe a porta que o Gunicorn usará
EXPOSE 8000

# Define o entrypoint. Ele sera executado ANTES do CMD

# Comando padrão para rodar a aplicação (será executado pelo o entrypoint)
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]


