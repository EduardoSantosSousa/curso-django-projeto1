# 🧩 Resumo — Aula sobre “Arquivos Estáticos, Git e Sincronização Local/Servidor”

## 🎯 Objetivo

Resolver o problema de arquivos estáticos (CSS não carregando) em produção e definir boas práticas de versionamento e deploy entre o computador local e o servidor.

## 🧱 1. Entendimento do Problema

- Ao rodar o projeto Django no servidor, o CSS e outros arquivos estáticos **não apareciam**.
- O motivo: Django não serve arquivos estáticos em produção — eles devem ser coletados e servidos pelo **Nginx**.
- A solução é usar o comando:
  
```bash 
python manage.py collectstatic
```

## ⚠️ 2. Boas Práticas — Git e Sincronização

**❌ Nunca:**

- Fazer alterações **diretamente no servidor** e depois **puxar (git pull)** para o computador local.
- Versionar pastas que **são geradas automaticamente**, como:

```cpp
static/
db.sqlite3
gunicorn.sock
```

*Isso gera conflitos e inconsistências entre ambiente local e remoto.*

**✅ Sempre:**

- Trabalhar no computador local e enviar as alterações para o servidor (nunca o contrário).
- Usar `.gitignore` para ignorar arquivos/pastas geradas automaticamente:


```cpp
static/
db.sqlite3
*.sock
```

## 🔧 3. Fluxo Correto de Trabalho (Git)

**No seu computador local:**
```bash 
# Atualizar o repositório local
git add .
git commit -m "atualização do código"
git push origin main
```

**No servidor:**
```bash
cd ~/app_repo
git pull origin main
```
Agora o servidor está sincronizado com seu código mais recente.

## 🧹 4. Coletar Arquivos Estáticos no Servidor
Depois de atualizar o código:

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Coletar arquivos estáticos
python manage.py collectstatic
```
Isso cria a pasta `/static/` no servidor (não versionada pelo Git), com os arquivos CSS/JS organizados.

## 🌐 5. Testar no Navegador

Acesse:
```cpp
http://SEU_IP_DO_SERVIDOR
```
O site agora deve aparecer com o CSS e imagens corretos, servidos diretamente pelo Nginx.

## 🚫 6. Evitar Conflitos Futuros

- Trabalhe **sempre local** → **servidor**, nunca o contrário.
- Nunca edite o código diretamente no servidor (exceto para emergências).
- Confirme que `.gitignore` contém todos os arquivos que não devem trafegar via Git.

## 🧠 7. Resumo Conceitual

| Item                           | Deve estar no Git? | Gerado no servidor? |
| ------------------------------ | ------------------ | ------------------- |
| Código Python (app Django)     | ✅                  | ❌                   |
| Arquivos estáticos (`static/`) | ❌                  | ✅                   |
| Banco local (`db.sqlite3`)     | ❌                  | ✅                   |
| Socket Gunicorn (`.sock`)      | ❌                  | ✅                   |
