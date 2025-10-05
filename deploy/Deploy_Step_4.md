# 🧠 Resumo — Configuração Inicial do Servidor (Google Cloud / Ubuntu)

## 🧩 1. Ambiente e referências

- O servidor pode ser criado no **Google Cloud Platform**, mas também é possível usar **VirtualBox** ou VMware/Parallels localmente.

- Crie um arquivo `README.md` (ou `server_setup.md`) no seu projeto para guardar:
  
    - IP do servidor (ou nome do host SSH)
    - Instruções de acesso
    - Passos de configuração e comandos executados

## 🔐 2. Acesso SSH

- Gere uma **chave SSH** se ainda não tiver:

```bash 
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```

- Copie a **chave pública** (`id_rsa.pub`) para o servidor (na seção de **metadados** → **SSH Keys** do Google Cloud).

- Acesse o servidor:

```bash 
ssh usuario@IP_DO_SERVIDOR
```

- (Opcional) Configure o arquivo `~/.ssh/config` para conexões rápidas:

```bash
Host curso-django
    HostName 34.xxx.xxx.xxx
    User usuario
    IdentityFile ~/.ssh/id_rsa
```

Agora é possível acessar com:

```bash 
ssh curso-django
```

## ⚙️ 3. Atualizar e preparar o servidor

Execute esses comandos em sequência (podem levar alguns minutos):

```bash 
# Atualizar lista de pacotes
sudo apt update

# Atualizar pacotes instalados
sudo apt upgrade -y

# Remover dependências antigas
sudo apt autoremove -y

# Instalar pacotes essenciais para compilar e construir dependências
sudo apt install build-essential libssl-dev libffi-dev python3-dev -y
```

## 🐍 4. Instalar Python, Nginx e PostgreSQL

```bash 
# Instalar Python 3.9 (ou 3.10 se disponível)
sudo apt install python3.9 python3.9-venv python3.9-dev -y

# Instalar Nginx (servidor web)
sudo apt install nginx -y

# Instalar Certbot (para HTTPS/SSL)
sudo apt install certbot python3-certbot-nginx -y

# Instalar PostgreSQL e bibliotecas necessárias
sudo apt install postgresql postgresql-contrib libpq-dev -y

# Instalar Git (para versionamento do código)
sudo apt install git -y
```

## 💾 5. Boas práticas

- **Desligue a VM** quando não estiver usando (para evitar cobrança).
- **Reserve o IP** como **estático** se quiser mantê-lo fixo entre reinicializações.
- Guarde todos os comandos executados no seu `README.md` para referência futura.
- Pequenos “erros vermelhos” no terminal (como avisos de pacotes não críticos) são normais — continue o processo
  
## 🧰 Próximos passos
- Configurar **Nginx** + **Gunicorn** para rodar o Django em modo produção.
- Gerar e aplicar **certificados SSL (HTTPS)** com o Certbot.
- Fazer o **deploy da aplicação Django** e configurar o **PostgreSQL** como banco de dados.