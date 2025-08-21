Projeto_Blog (Django)

![alt text](https://img.shields.io/badge/Django%205.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![alt text](https://img.shields.io/badge/Python%203.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![alt text](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![alt text](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![alt text](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)

Uma plataforma de blog completa e robusta desenvolvida com Django e totalmente containerizada com Docker. Permite aos usuários criar, editar, gerenciar e publicar posts de forma segura e intuitiva, com sistema de rascunhos, editor de texto avançado, categorias, tags e muito mais.

Status: Em processo

Funcionalidades Principais

Autenticação de Usuários: Sistema seguro de Login e Logout.

Gerenciamento Completo de Posts (CRUD): Crie, visualize, atualize e exclua posts.

Sistema de Rascunhos e Publicação: Salve posts como rascunhos e publique-os quando estiverem prontos. Apenas o autor pode visualizar e gerenciar seus próprios rascunhos.

Editor de Texto Avançado (WYSIWYG): Integração com django-summernote para formatação de texto, inclusão de links e upload de imagens diretamente no corpo do post.

Organização de Conteúdo: Sistema de Categorias e Tags para classificar os posts.

Geração Automática de Slugs: URLs amigáveis (/post/meu-primeiro-post) são geradas automaticamente a partir dos títulos, com tratamento para caracteres especiais.

Busca: Pesquisa de posts por título, resumo ou conteúdo.

Paginação: Navegação otimizada para listas de posts.

Segurança:

Apenas o autor de um post pode editá-lo ou excluí-lo.

Logout automático após período de inatividade.

Proteção contra brute-force com django-axes.

Ambiente de Desenvolvimento Otimizado: O projeto é 100% containerizado com Docker, garantindo um setup rápido, consistente e isolado.

Tecnologias Utilizadas

Backend: Python 3.10, Django 5.2

Banco de Dados: PostgreSQL (rodando em um container Docker)

Containerização: Docker, Docker Compose

Servidor WSGI: Gunicorn (utilizado no Dockerfile para prontidão de produção)

Frontend: HTML, CSS (com Variáveis CSS para fácil customização)

Bibliotecas Principais:

django-summernote: Editor de texto avançado (WYSIWYG).

Pillow: Manipulação e processamento de imagens.

python-dotenv: Gerenciamento de variáveis de ambiente.

unidecode: Tratamento de caracteres especiais para a geração de slugs.

django-axes: Segurança para controle de acesso e tentativas de login.

Pré-requisitos

Docker instalado

Docker Compose instalado

Configuração do Ambiente de Desenvolvimento

Siga os passos abaixo para configurar e rodar o projeto localmente usando Docker.

Clone o Repositório:

code
Bash
download
content_copy
expand_less

git clone https://github.com/arthurbleich/Projeto_Blog.git
cd Projeto_Blog

Crie o Arquivo de Variáveis de Ambiente:

Crie um arquivo chamado .env na raiz do projeto.

IMPORTANTE: O arquivo .gitignore já está configurado para ignorar o .env.

Adicione as seguintes variáveis, substituindo pelos seus valores:

code
Dotenv
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
# .env
SECRET_KEY='sua_chave_secreta_super_segura_aqui'
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1

# Configurações do Banco de Dados PostgreSQL (usadas pelo docker-compose)
POSTGRES_USER=blog_user
POSTGRES_PASSWORD=senha_super_forte
POSTGRES_DB=blog_db

Para gerar uma SECRET_KEY segura, você pode usar o seguinte comando Python:

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

Construa os Containers e Inicie a Aplicação:
Este comando irá construir a imagem do Django, baixar a imagem do PostgreSQL e iniciar todos os serviços em segundo plano.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
docker-compose up --build -d

Execute as Migrações do Banco de Dados:
Com os containers rodando, execute o comando abaixo para criar as tabelas no banco de dados.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
docker-compose exec djangoapp python manage.py migrate

Crie um Superusuário:
Para acessar a área administrativa do Django (/admin/), crie um superusuário:

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
docker-compose exec djangoapp python manage.py createsuperuser

Siga as instruções no terminal para definir seu nome de usuário, email e senha.

Executando a Aplicação

Se os containers não estiverem rodando, inicie-os com:

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
docker-compose up -d

Acesse o Blog: http://localhost:8000/

Acesse a Área Administrativa: http://localhost:8000/admin/

Deploy (Produção)

O Dockerfile deste projeto já está otimizado para produção, utilizando um multi-stage build para criar uma imagem final leve e segura. O servidor de aplicação utilizado é o Gunicorn.

Para um deploy real, os passos adicionais tipicamente envolvem:

Configurar um servidor (Ex: VPS na DigitalOcean, AWS EC2).

Configurar o Docker e Docker Compose no servidor.

Ajustar o docker-compose.yml para produção (remover volumes de código, por exemplo).

Configurar um Proxy Reverso como Nginx para servir arquivos estáticos/mídia e direcionar o tráfego para o Gunicorn.

Configurar o firewall (UFW).

Configurar um certificado HTTPS com Certbot (Let's Encrypt).

No settings.py (gerenciado por variáveis de ambiente), definir DEBUG=False e preencher ALLOWED_HOSTS com o domínio real.

Projeto desenvolvido como parte de um estudo aprofundado do framework Django e boas práticas de desenvolvimento web.
