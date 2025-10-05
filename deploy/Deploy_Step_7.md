# ⚙️ Resumo — Configuração do Nginx para Django + Gunicorn

## 1. Conceito Geral

- **Nginx**: servidor web responsável por receber as requisições HTTP/HTTPS.
- **Gunicorn**: servidor WSGI que conecta o Nginx ao Django.
- **Socket Unix**: canal local que permite a comunicação entre Nginx e Gunicorn.
- Django não serve arquivos estáticos em produção — o Nginx faz isso.

## 2. Estrutura de Configuração
```bash
/etc/nginx/
│
├── sites-available/
│   └── curso_django
│
└── sites-enabled/
    └── curso_django → (link simbólico)
```

## 3. Criar Arquivo de Configuração do Nginx

```bash 
sudo nano /etc/nginx/sites-available/curso_django
```

**Conteúdo:**

```bash
server {
    listen 80;
    server_name SEU_IP_DO_SERVIDOR;

    # Caminho dos arquivos estáticos e de mídia
    location /static/ {
        alias /home/SEU_USUARIO/app_repo/static/;
    }

    location /media/ {
        alias /home/SEU_USUARIO/app_repo/media/;
    }

    # Comunicação com Gunicorn via socket
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/curso_django.sock;
    }

    # Logs
    access_log /var/log/nginx/curso_django_access.log;
    error_log /var/log/nginx/curso_django_error.log;
}
```

## 4. Criar Link Simbólico (Ativar Site)

```bash 
sudo ln -s /etc/nginx/sites-available/curso_django /etc/nginx/sites-enabled/
```

Remover configuração padrão:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

## 5. Testar e Reiniciar o Nginx

```bash 
sudo nginx -t
sudo systemctl restart nginx
```

Saída esperada:

```bash 
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

## 6. Verificar Funcionamento

Acesse no navegador:
```cpp
http://SEU_IP_DO_SERVIDOR
```
Se estiver tudo certo, verá sua página Django sendo servida.

⚠️ Se o site aparecer sem CSS, significa que os **arquivos estáticos não foram coletados ainda**.

## 7. Coletar Arquivos Estáticos

Dentro da pasta do seu projeto Django:

```bash
source venv/bin/activate
python manage.py collectstatic
```

Isso criará a pasta `/static/` com todos os arquivos estáticos, permitindo que o Nginx os sirva.

## 8. Configurações Opcionais

**Mudar o Timezone do servidor:**

```bash 
sudo timedatectl set-timezone America/Sao_Paulo
sudo reboot
```
**Logs de Erro:**

```bash 
sudo tail -f /var/log/nginx/curso_django_error.log
```

## 9. Estrutura Final de Comunicação

```mathematica
Usuario → Nginx → Socket Unix → Gunicorn → Django
```

## 10. Dicas Finais
- ✅ Use nomes simples (sem acentos ou espaços) para sockets e arquivos.
- ✅ Sempre teste a configuração (`sudo nginx -t`) antes de reiniciar.
- ✅ Reinicie Gunicorn e Nginx sempre que editar arquivos de configuração.
- ✅ HTTPS exige um domínio e certificado SSL (vamos usar só HTTP neste caso).