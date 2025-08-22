<div align="center">
  <h1>
    📝<br>Blog do Rocha
  </h1>
  <p><strong>Um blog completo e moderno construído com Django e Docker.</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.10-blue.svg" alt="Python 3.10">
    <img src="https://img.shields.io/badge/Django-5.2-green.svg" alt="Django 5.2">
    <img src="https://img.shields.io/badge/PostgreSQL-16-blue.svg" alt="PostgreSQL 16">
    <img src="https://img.shields.io/badge/Docker-Ready-blue.svg?logo=docker" alt="Docker Ready">
  </p>
</div>

---

### 📖 Tabela de Conteúdos

- [Sobre o Projeto](#-sobre-o-projeto)
- [✅ Features](#-features)
- [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [🚀 Como Executar o Projeto](#-como-executar-o-projeto)
- [📂 Estrutura de Commits](#-estrutura-de-commits)
- [👨‍💻 Autor](#-autor)

---

### 📌 Sobre o Projeto

O **Blog do Rocha** é uma aplicação web full-stack desenvolvida como um projeto de estudo aprofundado do framework Django. A plataforma permite a criação, edição, publicação e gerenciamento de posts, com um sistema de autenticação completo, rascunhos, categorias, tags e um ambiente de produção containerizado com Docker.

O projeto foi estruturado para seguir as melhores práticas de desenvolvimento, incluindo um sistema de slug automático, tratamento de imagens, e uma interface de usuário interativa com AJAX para uma melhor experiência.

---

### ✅ Features

-   **Autenticação Completa:**
    -   [x] Página de Login e Logout.
    -   [x] Página de Registro para novos usuários.
    -   [x] Logout automático por inatividade.
-   **Gerenciamento de Posts (CRUD):**
    -   [x] Criar, Ler, Atualizar e Excluir posts.
    -   [x] Editor de texto avançado (WYSIWYG) com `django-summernote`.
    -   [x] Suporte para imagem de capa (cover) com redimensionamento automático.
-   **Sistema de Publicação:**
    -   [x] Salvar posts como **Rascunho** ou **Publicado**.
    -   [x] Página "Meus Rascunhos" para o usuário logado.
-   **Organização de Conteúdo:**
    -   [x] Sistema de **Categorias** e **Tags**.
    -   [x] Criação de categorias dinamicamente na página do post via **AJAX**, sem recarregar a página.
-   **Navegação e UX:**
    -   [x] Botão de ação dinâmico no cabeçalho ("Criar Post" / "Editar Post").
    -   [x] Busca por título, resumo ou conteúdo dos posts.
    -   [x] Paginação nas listagens de posts.
-   **Infraestrutura:**
    -   [x] Ambiente de desenvolvimento e produção totalmente containerizado com **Docker** e **Docker Compose**.
    -   [x] Banco de dados **PostgreSQL** persistente.
    -   [x] Servidor de produção **Gunicorn**.

---

### 🛠️ Tecnologias Utilizadas

O projeto foi construído utilizando as seguintes tecnologias:

-   **Backend:** Python, Django
-   **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
-   **Banco de Dados:** PostgreSQL
-   **Editor de Texto:** `django-summernote`
-   **Containerização:** Docker, Docker Compose
-   **Servidor de Produção:** Gunicorn

---

### 🚀 Como Executar o Projeto

Siga os passos abaixo para executar o projeto em seu ambiente local.

#### Pré-requisitos

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/products/docker-desktop/)
-   [Docker Compose](https://docs.docker.com/compose/)

#### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/arthurtobieich/Projeto_Blog.git
    cd Projeto_Blog
    ```

2.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto, copiando o exemplo abaixo. Substitua os valores conforme necessário.
    ```env
    # .env
    SECRET_KEY='sua-chave-secreta-super-forte-aqui'
    DEBUG=True
    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=psql
    ```

3.  **Construa e suba os containers Docker:**
    Este comando irá construir a imagem do Django e iniciar os serviços.
    ```bash
    docker-compose up -d --build
    ```

4.  **Execute as migrações do banco de dados:**
    ```bash
    docker-compose exec djangoapp python manage.py migrate
    ```

5.  **Crie um superusuário para acessar o Admin:**
    ```bash
    docker-compose exec djangoapp python manage.py createsuperuser
    ```
    Siga as instruções no terminal para criar seu usuário administrador.

6.  **Acesse a aplicação:**
    🎉 Pronto! Abra seu navegador e acesse `http://localhost:8000`.

---

### 📂 Estrutura de Commits

Este projeto adota o padrão de **Conventional Commits** para manter um histórico de versões limpo, organizado e legível. Os tipos de commits utilizados incluem:

-   `feat`: Para novas funcionalidades.
-   `fix`: Para correção de bugs.
-   `refactor`: Para mudanças no código que não alteram a funcionalidade.
-   `chore`: Para tarefas de manutenção (ex: atualizar `.gitignore`).
-   `docs`: Para mudanças na documentação.

---

### 👨‍💻 Autor

-   **Arthur Liskievich**
-   **GitHub:** [arthurtobieich](https://github.com/arthurliszkievich)

---
