# 🚀 Resumo — Configuração do Gunicorn e Socket para Django

## 1. Conceito Geral

- **Nginx** = servidor web.
- **Gunicorn** = WSGI server que conecta o Nginx à aplicação Django.
- **Socket Unix** = canal de comunicação entre Nginx ↔ Gunicorn.
- Django não deve usar o servidor interno (`runserver`) em produção


## 2. Estrutura de Arquivos no Servidor

```perl
/etc/systemd/system/
│
├── curso_django.socket   ← socket (canal de comunicação)
└── curso_django.service  ← serviço do Gunicorn
```

## 3. Criar o Socket
```bash 
sudo nano /etc/systemd/system/curso_django.socket
```

**Conteúdo:**
```init
[Unit]
Description=Gunicorn socket for Django app

[Socket]
ListenStream=/run/curso_django.sock

[Install]
WantedBy=sockets.target
```

## 4. Criar o Serviço (Systemd)

```bash 
sudo nano /etc/systemd/system/curso_django.service
```

**Conteúdo:**

```init 
[Unit]
Description=Gunicorn daemon for Django app
Requires=curso_django.socket
After=network.target

[Service]
User=seu_usuario
Group=www-data
WorkingDirectory=/home/seu_usuario/app_repo
ExecStart=/home/seu_usuario/app_repo/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/curso_django.sock \
          app_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

## 5. Comandos Principais

**Ativar e iniciar:**

```bash 
sudo systemctl start curso_django.socket
sudo systemctl enable curso_django.socket
```

**Verificar status:**

```bash 
sudo systemctl status curso_django.socket
sudo systemctl status curso_django.service
```

**Deve aparecer:**
```makefile
Active: active (listening)
```

**Testar o socket:**
```bash
sudo apt install curl
curl --unix-socket /run/curso_django.sock localhost
```
Se o Gunicorn estiver rodando corretamente, você verá o HTML retornado pelo Django.

## 6. Reiniciar ou recarregar serviços

```bash
sudo systemctl daemon-reload
sudo systemctl restart curso_django.service
sudo systemctl restart curso_django.socket
```
Dica 💡:
Sempre execute daemon-reload após editar .service ou .socket.

## 7. Logs e Debug

Ver logs do serviço:

```bash
sudo journalctl -u curso_django.service
```

Verificar erros:

```bash 
cat /run/curso_django.sock
```
ou acesse o arquivo de log definido no Gunicorn (caso exista).

## 8. Dicas Finais

- Mantenha nomes simples e sem acentos (ex: `curso_django`).
- Verifique sempre os caminhos do **venv** e do **wsgi.py**.
- Use o grupo `www-data` para o Gunicorn.
- Após atualizar o código do projeto, reinicie o serviço.