# 🧩 Resumo da Aula — Configuração de Banco de Dados e Deploy no Django

## 🎯 Objetivo Principal

Aprender como configurar corretamente o banco de dados no Django, separando as configurações locais e de produção, e entender boas práticas antes de enviar o projeto para o servidor.

## ⚙️ 1. Por que não usar o banco de dados local no servidor

- Durante o desenvolvimento, **não é necessário subir um banco de dados completo (como PostgreSQL)** na sua máquina se o projeto funciona com SQLite localmente.

- Isso **economiza recursos** e simplifica o ambiente de desenvolvimento.

- A ideia é usar **SQLite localmente** e **PostgreSQL (ou outro)** em produção.
  
## 🧱 2. Configuração de Banco de Dados no Django

- O arquivo padrão de configuração é o `settings.py`.

- Por padrão, o Django cria o banco com SQLite:

```python 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
```
- Para usar PostgreSQL (ou outro), você adicionaria:

```python 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_banco',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
## 🌍 3. Separando variáveis locais e de produção

- **Nunca mantenha informações sensíveis no código.**
- Use um arquivo `.env` (gerenciado com a biblioteca `python-dotenv`) para armazenar variáveis como:
  
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=meubanco
DB_USER=meuusuario
DB_PASSWORD=minhasenha
DB_HOST=localhost
DB_PORT=5432
```
- No `settings.py`, importe com:

## 🧩 4. Por que usar variáveis de ambiente

- Evita conflitos entre ambientes (local e servidor).

- Impede que credenciais sensíveis vazem para o repositório Git.

- Permite mudar configurações sem alterar o código-fonte.
  
## 🚫 5. Boas práticas com versionamento

- **Nunca edite diretamente o código no servidor.**
  
    - Faça alterações **no ambiente local**, teste, e envie **para o servidor via Git**.
    - Editar no servidor causa **conflitos e inconsistências** no controle de versão.

- Arquivos como `.env` devem estar no `.gitignore`, pois contêm senhas e dados privados.

## ✅ 6. Testes antes do deploy

- Sempre **rode os testes antes de enviar para produção.**
- Use:

```bash
python manage.py test
```
- Isso garante que a aplicação está funcionando corretamente antes do deploy.
- Evita que o site caia para os usuários ou que você precise “remendar” erros em produção.

## ☁️ 7. Banco de dados em produção

- Em produção, use bancos robustos como:
    - PostgreSQL ✅ (recomendado)
    - MySQL
    - MariaDB
    - Oracle (menos comum)
- Evite usar SQLite no servidor — ele é ideal apenas para desenvolvimento.

## 🚀 8. Processo de Deploy resumido

1. Editar e testar localmente.
2. Confirmar as mudanças no Git:

```bash 
git add .
git commit -m "Atualização da configuração do banco de dados"
git push origin main
```

3. No servidor:

```bash 
git pull origin main
sudo systemctl restart <seu_serviço>
```

4. Verificar se o servidor subiu corretamente.
   