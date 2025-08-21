# Dockerfile Final - Padrão Ouro para Produção e Desenvolvimento

# --- Estágio 1: "Builder" ---
# Este estágio compila e instala todas as dependências em um ambiente limpo.
FROM python:3.10-slim-bookworm AS builder

# Variáveis de ambiente para otimizar o build e o runtime do Python.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala as dependências do sistema operacional necessárias para COMPILAR pacotes Python.
# build-essential: Compiladores C/C++.
# libpq-dev: Headers para a biblioteca do PostgreSQL.
# libgeoip-dev: Headers para a biblioteca GeoIP, necessária para o django-axes.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libgeoip-dev

# Cria um ambiente virtual Python isolado.
RUN python -m venv /opt/venv

# Adiciona o venv ao PATH do sistema.
ENV PATH="/opt/venv/bin:$PATH"

# Define o diretório de trabalho.
WORKDIR /app

# Copia apenas o arquivo de requisitos primeiro para aproveitar o cache do Docker.
COPY requirements.txt .

# Instala as dependências Python.
RUN pip install --no-cache-dir -r requirements.txt


# --- Estágio 2: "Runtime" ---
# Este estágio cria a imagem final, que é leve e segura.
FROM python:3.10-slim-bookworm AS runtime

# Instala apenas as dependências de sistema necessárias para a EXECUÇÃO.
# libpq5: Cliente do PostgreSQL.
# libgeoip1: Biblioteca GeoIP, necessária para o django-axes em runtime.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libgeoip1 \
    && rm -rf /var/lib/apt/lists/*

# Cria um usuário e grupo de sistema com privilégios limitados.
RUN addgroup --system django && adduser --system --ingroup django django

# Define o diretório de trabalho.
WORKDIR /app

# Copia o ambiente virtual com as dependências JÁ INSTALADAS do estágio "builder".
COPY --from=builder /opt/venv /opt/venv

# Copia o código da aplicação.
COPY ./djangoapp .

# Criação dos diretórios de mídia e estáticos.
RUN mkdir -p /app/media /app/staticfiles

# Define o dono de todos os arquivos da aplicação para o usuário `django`.
RUN chown -R django:django /app

# Muda o contexto de execução para o nosso usuário não-root.
USER django

# Define o PATH para que o sistema use o Python e os pacotes do venv.
ENV PATH="/opt/venv/bin:$PATH"

# Expõe a porta 8000.
EXPOSE 8000

# Define o comando padrão para iniciar o servidor de produção Gunicorn.
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
