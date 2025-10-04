## 🧩 Resumo da Aula — Arquivos estáticos, collectstatic e configurações de produção

## 🎯 Objetivo 

Explicar o papel do `collectstatic`, como servir arquivos estáticos em produção, e as alterações obrigatórias em `settings.py` ao preparar a aplicação Django para deploy (DEBUG, ALLOWED_HOSTS, etc.).

## 📁 1. O que é collectstatic e por que é importante

- `python manage.py collectstatic` copia todos os arquivos estáticos das apps (pastas `static/` de cada app) e do diretório de projeto para uma pasta central (`STATIC_ROOT`).
  
- Essa pasta única é a que o servidor web em produção (Nginx, Apache, etc.) vai servir — não o servidor de desenvolvimento do Django.

- Sempre rode `collectstatic` **antes de publicar** se você alterou CSS, JS, imagens ou templates que referenciam arquivos estáticos.

## ⚙️ 2. Configurações relevantes em settings.py

- Defina `STATIC_URL` e `STATIC_ROOT`:
  
```python 
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   # onde collectstatic vai juntar tudo
```

- Se estiver em desenvolvimento, mantenha `STATICFILES_DIRS` apontando para suas pastas locais:

```python 
STATICFILES_DIRS = [BASE_DIR / 'static']
```

- Não servir arquivos estáticos com o servidor de desenvolvimento em produção — use Nginx/Apache (ou Whitenoise para soluções simples).
  

## 🔒 3. Segurança e configurações de produção

- `DEBUG = False` em produção — isso evita exibir erros sensíveis para usuários.
  
- `ALLOWED_HOSTS` deve conter somente os domínios/IPs que irão acessar a aplicação:
  
```python
DEBUG = False
ALLOWED_HOSTS = ['meudominio.com', '34.132.3.125']  # ou domínios reais do servidor
```
- Colocar `ALLOWED_HOSTS = ['*']` funciona, mas **não é seguro** (apenas para testes temporários).
  
## 🚫 4. Boas práticas com chaves e versionamento

- **Nunca** comite chaves privadas (SSH/private keys) no repositório.

- Adicione a chave pública ao servidor/Git host (GitHub/GitLab) e, se precisar, mantenha instruções no README sobre configurar chaves.

- Use `.gitignore` para `.env`, arquivos de chave privada e `staticfiles` gerados localmente.
  
## 🖥️ 5. Servidor web e arquivos estáticos

- Em produção a arquitetura comum:
    - Gunicorn (app WSGI) + Nginx (reverse proxy + serve static).
    - Nginx serve a pasta `STATIC_ROOT` diretamente (mais rápido e eficiente).

- Alternativa simples: **Whitenoise** permite ao Gunicorn servir estáticos sem Nginx (bom para projetos menores).

## ✅ 6. Passos práticos para publicar (deploy básico)

1. Garantir que todos os testes passaram localmente:

```bash 
python manage.py test
```

2. Atualizar `settings.py`:

- `DEBUG = False`
- `ALLOWED_HOSTS = ['seu_dominio', 'IP_do_servidor']`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`

3. Rodar migrations (no servidor):

```bash 
python manage.py migrate
```

4. Rodar collectstatic (gera a pasta de estáticos):

```bash 
python manage.py collectstatic --noinput
```

5. Ajustar permissões da pasta staticfiles e propriedade (ex.: usuário do webserver):

```bash
sudo chown -R www-data:www-data /caminho/para/staticfiles
sudo chmod -R 755 /caminho/para/staticfiles
```

6. Reiniciar processos (Gunicorn / systemd) e Nginx:

```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

7. Testar no domínio/IP.

## 🧾 7. Trecho de `settings.py` (exemplo claro)
```python 

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False
ALLOWED_HOSTS = ['meudominio.com', '34.132.3.125']

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']  # apenas em dev se usar

```

## 🔁 8. Integração com Git / fluxo recomendado

- Faça as mudanças localmente → teste → commit → push.
  
- No servidor: `git pull origin main` → rodar `migrate` → `collectstatic` → reiniciar serviços.
  
- Nunca edite o código em produção diretamente; alterações devem vir do repositório.
  
## ⚠️ 9. Avisos importantes

- Se `DEBUG = False` e `ALLOWED_HOSTS` não contiver seu domínio/IP, Django retornará erro 400. Configure corretamente antes do deploy.

- Não confunda `STATIC_ROOT` (destino do collectstatic) com `STATICFILES_DIRS` (fontes locais).

- Não comite `.env` nem chaves privadas. Documente como configurar variáveis de ambiente no README.