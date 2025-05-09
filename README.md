# Sistema de Autenticação e Resumo com IA (Vue.js + Flask)

Este projeto é uma aplicação web simples que demonstra um sistema de autenticação de usuário usando Vue.js no frontend e Flask no backend, integrado com um banco de dados PostgreSQL hospedado no Supabase e a API Google Gemini para resumir o conteúdo de arquivos.

## Descrição

A aplicação permite que novos usuários se registrem, façam login e, após a autenticação, acessem uma área protegida (Dashboard). Na Dashboard, os usuários podem fazer upload de arquivos de texto (`.txt`) ou PDF (`.pdf`). O backend processa o arquivo, extrai o texto, envia o texto para a API Google Gemini para gerar um resumo e, em seguida, cria um novo arquivo PDF contendo o resumo, que o usuário pode baixar.

## Funcionalidades

* Cadastro de novos usuários.
* Login de usuários existentes (autenticação via JWT).
* Rotas protegidas no backend que exigem um token JWT válido.
* Logout (remoção do token JWT no frontend).
* Upload de arquivos `.txt` e `.pdf` para o backend.
* Extração de texto de arquivos `.txt` e `.pdf`.
* Geração de resumo de texto utilizando a API Google Gemini (`gemini-2.0-flash`).
* Criação de arquivo PDF contendo o resumo gerado.
* Download do arquivo PDF de resumo pelo frontend.

## Tecnologias Utilizadas

**Frontend (Vue.js)**

* Vue.js 3
* Vue Router
* Axios (para requisições HTTP)

**Backend (Flask)**

* Python 3
* Flask
* Flask-SQLAlchemy (ORM para interação com o banco de dados)
* Flask-JWT-Extended (para autenticação via JWT)
* Flask-CORS (para lidar com requisições entre diferentes origens)
* python-dotenv (para carregar variáveis de ambiente)
* Werkzeug.security (para hashing de senha)
* psycopg2-binary (driver PostgreSQL)
* google-generativeai (SDK Python para API Google Gemini)
* PyPDF2 (para leitura de PDF)
* fpdf2 (para criação de PDF)

**Banco de Dados**

* Supabase (PostgreSQL hospedado)

**Inteligência Artificial**

* Google Gemini API (`gemini-2.0-flash`)

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

* [Python 3.x](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installation/) (gerenciador de pacotes do Python)
* [Node.js e npm](https://nodejs.org/en/download/)
* [Vue CLI](https://cli.vuejs.org/guide/installation.html) 

## Configuração e Execução

Siga os passos abaixo para configurar e rodar o projeto localmente.

### 1. Configuração no Supabase

1.  Crie um novo projeto no [Supabase](https://supabase.com/).
2.  Vá para **Project Settings -> Database** e copie a **Connection string (URI)**.
3.  Vá para **Table Editor** e crie uma nova tabela chamada `users` com as colunas `id` (serial/bigint, Primary Key, Is Identity), `username` (text/varchar, Unique, Not Null) e `password_hash` (text/varchar, Not Null).

### 2. Obtenha sua Chave de API do Google Gemini

1.  Vá para [Google AI Studio](https://aistudio.google.com/).
2.  Crie ou obtenha sua chave de API para o Google Gemini.

### 3. Backend (Flask)

1.  Clone o repositório:
    ```bash
    git clone <url_do_repositorio>
    cd <nome_da_pasta_do_seu_projeto>/backend-flask
    ```
2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```
3.  Instale as dependências do backend:
    ```bash
    pip install -r requirements.txt
    ```
4.  Crie um arquivo `.env` na pasta `backend-flask` e configure as variáveis com suas credenciais:
    ```env
    DATABASE_URL='postgresql://postgres:[SUA-SENHA-SUPABASE]@<host>:<port>/<database-name>'
    JWT_SECRET_KEY='sua_chave_secreta_bem_longa_e_aleatoria_para_jwt'
    GOOGLE_API_KEY='SUA_CHAVE_API_DO_GOOGLE_GEMINI_AQUI'
    SECRET_KEY='outra_chave_secreta_bem_longa_e_aleatoria'
    ```
    Substitua os valores entre `[]` e `<>` pelas suas credenciais.
5.  Rode o servidor Flask:
    ```bash
    flask run
    ```
    O backend estará rodando em `http://localhost:5000/`.

### 4. Frontend (Vue.js)

1.  Em um **novo terminal** (mantenha o do Flask rodando), navegue para a pasta do frontend:
    ```bash
    cd <nome_da_pasta_do_seu_projeto>/frontend-vue
    ```
2.  Instale as dependências do frontend:
    ```bash
    npm install
    # ou
    yarn install
    ```
3. Edite a variavel const API_URL = ''; nos arquivos /frontend-vue/src/views/UserDashboard.vue , UserLogin.vue e UserRegister.vue e coloque o url do backend, http://localhost5000 possivelmente.

4.  Rode o servidor de desenvolvimento do Vue:
    ```bash
    npm run serve
    # ou
    yarn serve
    ```
    O frontend estará rodando em `http://localhost:8080/` .

## Como Usar

1.  Abra seu navegador e vá para `http://localhost:8080/`. Você será redirecionado para a página de Login.
2.  Clique no link para a página de Cadastro (`/register`).
3.  Preencha as informações de usuário/senha e clique em "Cadastrar". Você deve receber uma mensagem de sucesso.
4.  Vá para a página de Login (`/login`), insira as credenciais cadastradas e clique em "Login".
5.  Se o login for bem-sucedido, você será redirecionado para a Dashboard (`/dashboard`).
6.  Na Dashboard, você verá a opção de fazer upload de arquivo. Selecione um arquivo `.txt` ou `.pdf`.
7.  Clique no botão "Upload e Resumir". Aguarde o processamento (pode levar alguns segundos dependendo do tamanho do arquivo e da resposta da API Gemini).
8.  Se o processamento for bem-sucedido, uma mensagem de sucesso aparecerá junto com um link para baixar o arquivo "resumo\_gerado.pdf".
9.  Clique no link para baixar o PDF com o resumo.
10. Para sair, clique no botão "Sair".