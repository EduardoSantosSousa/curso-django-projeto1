# Resumo — Configuração Nginx + HTTPS (Let's Encrypt) — guia rápido

## Objetivo
Configurar Nginx para servir a aplicação Django com HTTPS usando **Let's Encrypt (Certbot)**, além de boas práticas (timezone, segurança, certificados).

---

## 1. Principais passos (visão geral)
1. Parar o Nginx temporariamente.
2. Gerar / obter certificado com Certbot (Let's Encrypt).
3. Atualizar a configuração do Nginx para usar os certificados.
4. Criar link simbólico e reiniciar Nginx.
5. Verificar certificado no navegador e testar renovação.

---

## 2. Parar Nginx (temporariamente)
```bash
sudo systemctl stop nginx
```

Necessário porque o Certbot (modo standalone) precisa usar porta 80/443 para validar domínio.

## 3. Gerar certificado com Certbot (modo standalone)

- Exemplo (domínio `curso-django.example.com`):

```bash 
sudo certbot certonly --standalone -d curso-django.example.com
```

- Durante o processo:
    - Informe email (para avisos/renovação).
    - Aceite os termos.
    - Certbot criará os arquivos (`/etc/letsencrypt/live/<domínio>/fullchain.pem` e `privkey.pem`).

**Nota sobre chaves RSA**:

- `--rsa-key-size 4096` é mais seguro, mas leva mais tempo para gerar.
- `2048` é mais rápido e aceitável para muitos casos. Exemplo:

```bash 
sudo certbot certonly --standalone --rsa-key-size 2048 -d curso-django.example.com
```

## 4. Exemplo de bloco Nginx para HTTPS

Edite `/etc/nginx/sites-available/curso_django` e inclua (ou substitua) a versão HTTPS:

```ngix
server {
    listen 443 ssl;
    server_name curso-django.example.com;

    ssl_certificate /etc/letsencrypt/live/curso-django.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/curso-django.example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location /static/ {
        alias /home/seu_usuario/app_repo/static/;
    }

    location /media/ {
        alias /home/seu_usuario/app_repo/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/curso_django.sock;
    }

    access_log /var/log/nginx/curso_django_access.log;
    error_log  /var/log/nginx/curso_django_error.log;
}

# Opcional: redirecionar HTTP -> HTTPS
server {
    listen 80;
    server_name curso-django.example.com;
    return 301 https://$host$request_uri;
}
```
Depois de editar:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

## 5. Verificar certificado

- Abra no navegador `https://curso-django.example.com` e verifique:
    - Cadeado seguro
    - Emissor: R3 / Let's Encrypt
    - Data de expiração

## 6. Renovação automática
Let's Encrypt vence a cada 90 dias. Para renovar automaticamente:

- Certbot normalmente instala um timer systemd ou cron job.
- Teste a renovação:

```bash 
sudo certbot renew --dry-run
```

- Se preferir, crie um cron ou rely on systemd timer.

## 7. Portas / Firewall

- Certifique-se de liberar portas 80 e 443 no firewall e na cloud:
    - GCP: permitir tráfego HTTP (80) e HTTPS (443)
- Se usar modo `standalone` do Certbot, porta 80 precisa estar livre no momento da validação.

## 8. Timezone (opcional, recomendado)

Defina timezone do servidor (ex.: São Paulo):

```bash 
sudo timedatectl set-timezone America/Sao_Paulo
sudo reboot   # se necessário
```

## 9. Boas práticas / segurança

- Use senha forte para contas do servidor e para superuser do Django.
- Mantenha sistema atualizado:

```bash 
sudo apt update && sudo apt upgrade -y
```

- Monitore logs (`/var/log/nginx/...`, `journalctl -u curso_django.service`).
- Habilite regrar de firewall/IPS se necessário e minimize serviços expostos.
- Entenda que servidores públicos recebem tentativas de ataque — invista em segurança.


## 10. Problemas comuns
- Conexão recusada após parar Nginx: esperado até reiniciar.
- Certbot falha se porta 80/443 não estiver disponível (outro serviço ocupando).
- Certificado não aparece: certifique-se de usar caminhos corretos (`/etc/letsencrypt/live/...`).