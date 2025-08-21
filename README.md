Projeto_Blog: Uma Plataforma de Blog Completa com Django

Este é um projeto de blog full-stack desenvolvido com Django e containerizado com Docker. A aplicação permite que usuários criem, editem, gerenciem e publiquem posts de forma segura e intuitiva, contando com um editor de texto avançado, sistema de rascunhos, categorias, tags e muito more.

![alt text](https://github.com/arthurbleich/Projeto_Blog/assets/101886835/9564f331-50e5-47e9-a764-a74578b94f1c)

✨ Features

Gerenciamento Completo de Posts (CRUD): Crie, visualize, atualize e exclua posts.

Autenticação de Usuários: Sistema seguro de login e logout.

Sistema de Rascunhos e Publicação: Salve posts como rascunhos e publique-os quando estiverem prontos. Apenas o autor pode visualizar seus próprios rascunhos.

Editor de Texto Avançado (WYSIWYG): Integrado com django-summernote para permitir formatação de texto, inclusão de links e upload de imagens diretamente no corpo do post.

Upload de Imagens: Suporte para imagem de capa e imagens no conteúdo.

Organização de Conteúdo: Sistema de Categorias e Tags para classificar os posts.

Geração Automática de Slugs: URLs amigáveis são geradas automaticamente a partir dos títulos, com suporte a caracteres especiais (ex: "Programação" → programacao).

Funcionalidade de Busca: Pesquise posts por título, resumo ou conteúdo.

Paginação: Navegue facilmente por listas longas de posts.

Segurança: Apenas o autor de um post pode editá-lo ou excluí-lo.

Logout Automático: A sessão do usuário expira após um período de inatividade, aumentando a segurança.

Ambiente Containerizado: O projeto é totalmente configurado para rodar com Docker e Docker Compose, garantindo um setup de desenvolvimento rápido e consistente.

🛠️ Tecnologias Utilizadas

Backend: Python, Django

Frontend: HTML, CSS (com Variáveis CSS para fácil customização)

Banco de Dados: PostgreSQL (rodando em um container Docker)

Editor de Texto: django-summernote

Containerização: Docker, Docker Compose

Servidor de Produção: Gunicorn

🚀 Configuração do Ambiente Local

Para rodar este projeto localmente, você precisará ter o Docker e o Docker Compose instalados.

1. Clone o Repositório
code
Bash
download
content_copy
expand_less

git clone https://github.com/SEU_USUARIO/Projeto_Blog.git
cd Projeto_Blog
2. Crie o Arquivo de Variáveis de Ambiente

O projeto utiliza um arquivo .env para gerenciar as configurações sensíveis. Crie um arquivo chamado .env na raiz do projeto e adicione o seguinte conteúdo. Substitua os valores conforme necessário.

code
Env
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
# Configurações do Banco de Dados PostgreSQL
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydb

# Chave Secreta do Django (IMPORTANTE: Gere uma nova chave)
# Você pode gerar uma usando o comando: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY='sua_chave_secreta_aqui'

# Configurações do Django
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
3. Construa os Containers e Inicie a Aplicação

Com o Docker em execução, execute o seguinte comando na raiz do projeto. Ele irá construir as imagens, baixar o PostgreSQL e iniciar todos os serviços.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
docker-compose up --build -d
4. Aplique as Migrações do Banco de Dados

Com os containers rodando, aplique as migrações para criar as tabelas no banco de dados.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
docker-compose exec djangoapp python manage.py migrate
5. Crie um Superusuário

Para acessar a área administrativa, crie um superusuário.

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
docker-compose exec djangoapp python manage.py createsuperuser

Siga as instruções no terminal para definir um nome de usuário, email e senha.

💻 Uso da Aplicação

Acessar o Blog: Abra seu navegador e acesse http://localhost:8000

Acessar a Área Administrativa: Acesse http://localhost:8000/admin/ e faça login com o superusuário que você criou.

A partir daí, você pode usar o botão "Criar Post" para começar a publicar seu conteúdo!

📁 Estrutura do Projeto
code
Code
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
.
├── docker-compose.yml     # Orquestra os containers
├── Dockerfile             # Define a imagem do container da aplicação Django
├── requirements.txt       # Lista de dependências Python
├── .env                   # Arquivo de variáveis de ambiente (local)
└── djangoapp/             # Diretório contendo todo o código-fonte do Django
    ├── blog/              # A app principal do blog (models, views, etc.)
    ├── project/           # Configurações do projeto Django (settings.py, urls.py)
    └── manage.py          # Utilitário de linha de comando do Django

Parabéns por desenvolver um projeto tão completo
