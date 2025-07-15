# Dockerfile Final - Padrão Ouro para Produção e Desenvolvimento

# --- Estágio 1: "Builder" ---
# Este estágio compila e instala todas as dependências em um ambiente limpo.
FROM python:3.10-slim-bookworm AS builder

# Variáveis de ambiente para otimizar o build e o runtime do Python.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala as dependências do sistema operacional necessárias para COMPILAR pacotes
# Python complexos, como o `psycopg2`.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev

# Cria um ambiente virtual Python isolado. Isso evita conflitos com o Python do sistema.
RUN python -m venv /opt/venv

# Adiciona o venv ao PATH do sistema para que os comandos usem o Python e o pip do venv.
ENV PATH="/opt/venv/bin:$PATH"

# Define o diretório de trabalho para os próximos comandos.
WORKDIR /app

# Copia apenas o arquivo de requisitos primeiro. Isso aproveita o cache do Docker:
# o passo de instalação só será re-executado se este arquivo mudar.
COPY ./djangoapp/requirements.txt .

# Instala as dependências Python usando o pip do nosso venv.
RUN pip install --no-cache-dir -r requirements.txt


# --- Estágio 2: "Runtime" ---
# Este estágio cria a imagem final, que é leve e segura, contendo apenas o
# necessário para RODAR a aplicação.
FROM python:3.10-slim-bookworm AS runtime

# Instala apenas as dependências de sistema necessárias para a execução,
# como o cliente do PostgreSQL (`libpq5`). É muito menor que o `libpq-dev`.
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Cria um usuário e grupo de sistema com privilégios limitados para rodar a aplicação.
# Esta é uma prática de segurança fundamental.
RUN addgroup --system django && adduser --system --ingroup django django

# Define o diretório de trabalho final da nossa aplicação.
WORKDIR /app

# Copia o ambiente virtual com as dependências JÁ INSTALADAS do estágio "builder".
# A grande vantagem: a imagem final não contém as pesadas ferramentas de build.
COPY --from=builder /opt/venv /opt/venv

# Copia o código da aplicação do seu computador para o diretório de trabalho na imagem.
COPY ./djangoapp .

# Criação dos diretórios de mídia e estáticos DENTRO do workdir
RUN mkdir -p /app/media /app/staticfiles

# Define o dono de todos os arquivos da aplicação para o nosso usuário `django`.
# Isso garante que o processo da aplicação tenha permissão para ler seus próprios arquivos.
RUN chown -R django:django /app

# Muda o contexto de execução para o nosso usuário não-root.
USER django

# Define o PATH para que o sistema use o Python e os pacotes do nosso venv.
ENV PATH="/opt/venv/bin:$PATH"

# Expõe a porta 8000, informando ao Docker que o container escutará nesta porta.
EXPOSE 8000

# Define o comando padrão para iniciar o servidor de produção Gunicorn.
# Este comando pode ser sobrescrito pelo `docker-compose.yml` para desenvolvimento.
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]