# 🚀 Resumo — Aula: Configuração de Repositório e Deploy Django no Servidor

## 🧠 Objetivo da Aula

Aprender a:

1. Criar e configurar repositórios Git locais e remotos (no próprio servidor).
2. Conectar o projeto Django a esse repositório interno.
3. Criar e ativar ambiente virtual.
4. Instalar dependências e configurar PostgreSQL.
5. Subir o projeto Django e preparar o servidor para produção.

## 🏗️ 1. Criação de Repositório no Servidor (Git Bare)

O **repositório “bare” (BR)** é um repositório sem arquivos do projeto, apenas com histórico Git. Ele serve como ponto central de envio e recebimento de código — similar ao GitHub, mas hospedado no próprio servidor.

```bash 
# Criar pasta para o repositório “bare”
mkdir -p ~/app_repo.git
cd ~/app_repo.git

# Inicializar repositório bare
git init --bare
```

**📘 Conceito**:

O repositório bare funciona como “hub de código” — ele **não contém os arquivos**, apenas o histórico. O código é baixado em outro diretório.

## 📂 2. Criar Diretório para a Aplicação

```bash 
mkdir -p ~/app_repo
cd ~/app_repo
git init
```
Agora você tem dois repositórios:

- `app_repo.git` → repositório remoto (bare)
- `app_repo` → repositório de trabalho (onde ficam os arquivos do projeto)
  
Conecte o repositório de trabalho ao bare:

```bash 
git remote add origin ~/app_repo.git
```

## 💻 3. Configurar Repositório Local (No Seu Computador)

No computador, adicione o servidor como remoto adicional:

```bash 
git remote add server user@ip_do_servidor:~/app_repo.git
```

(ou, se estiver usando SSH com nome personalizado, algo como `ssh cursodjango '...'`)

Envie o código:

```bash
git push server main
```
💡 Dica: O nome origin normalmente é o GitHub, e server é o seu servidor.

## 🔧 4. No Servidor — Clonar o Código
Depois do push, acesse o servidor e baixe o código:

```bash 
cd ~
git clone ~/app_repo.git app_repo
```

Agora o diretório `app_repo` contém o código Django.

## 🐍 5. Criar Ambiente Virtual e Instalar Dependências

```bash 
cd ~/app_repo

# Criar ambiente virtual
python3.9 -m venv venv

# Ativar
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

💡 **Se não existir o arquivo** requirements.txt, gere-o no seu ambiente local:

```bash 
pip freeze > requirements.txt
```

## 🗄️ 6. Configurar Banco de Dados

Crie e configure seu `.env` baseado no exemplo:

```bash 
cp .env.example .env
nano .env
```

Ajuste:

```ini
DEBUG=False
DATABASE_NAME=base_de_dados
DATABASE_USER=usuario
DATABASE_PASSWORD=senha
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## 🧩 7. Testar o Projeto Django

```bash 
python manage.py runserver 0.0.0.0:8000
```

Se funcionar, rode as migrações:

```bash 
python manage.py makemigrations
python manage.py migrate
```

## 🐘 8. Instalar e Configurar PostgreSQL (se ainda não tiver feito)

```bash 
sudo apt install postgresql postgresql-contrib libpq-dev
```

Crie o banco e o usuário dentro do PostgreSQL:

```bash
sudo -u postgres psql
CREATE DATABASE base_de_dados;
CREATE USER usuario WITH PASSWORD 'senha';
ALTER ROLE usuario SET client_encoding TO 'utf8';
ALTER ROLE usuario SET default_transaction_isolation TO 'read committed';
ALTER ROLE usuario SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE base_de_dados TO usuario;
\q
```

## 🦄 9. Instalar Gunicorn e Configurar Servidor

Gunicorn faz a ponte entre o Django e o Nginx.

```bash 
pip install gunicorn psycopg2-binary
```

Testar manualmente:

```bash 
gunicorn app_repo.wsgi:application
```

## 🌐 10. Conectar com Nginx (nas próximas etapas)
O Nginx será configurado para:
- Servir o site via HTTPS.
- Repassar requisições ao Gunicorn.

## 🧭 11. Dicas Importantes

- Sempre **entenda o que o comando faz**, não apenas copie.
- Erros fazem parte do processo — leia e interprete as mensagens.
- “Programar” é 30% código e 70% resolver problemas e entender erros.
- Mantenha um arquivo `README.md` com todos os comandos que usou (ótimo para revisões futuras).


## 🗂️ Resumo Rápido de Comandos

| Etapa                  | Comando / Ação                         |
| ---------------------- | -------------------------------------- |
| Criar repositório bare | `git init --bare ~/app_repo.git`       |
| Criar app repo normal  | `git init ~/app_repo`                  |
| Adicionar remoto       | `git remote add origin ~/app_repo.git` |
| Push para o servidor   | `git push server main`                 |
| Criar venv             | `python3.9 -m venv venv`               |
| Ativar venv            | `source venv/bin/activate`             |
| Instalar dependências  | `pip install -r requirements.txt`      |
| Criar .env             | `cp .env.example .env`                 |
| Rodar migrações        | `python manage.py migrate`             |
| Testar app             | `python manage.py runserver`           |
| Instalar Gunicorn      | `pip install gunicorn`                 |
