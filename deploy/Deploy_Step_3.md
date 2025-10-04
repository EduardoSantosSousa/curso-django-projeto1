# 🧩 Resumo – Criando e Acessando um Servidor no Google Cloud Platform (GCP)

## 🎯 Objetivo

Criar uma máquina virtual (VM) no **Google Cloud Platform (GCP)** para hospedar uma aplicação Django com ambiente Ubuntu configurado para deploy.

## 🏗️ 1. Escolha da Plataforma

- A aula utiliza o **Google Cloud Platform (GCP)**, mas seria possível usar:
    - **VirtualBox**, **VMWare**, **Parallels**, **AWS**, **Azure**, etc.

- O professor usa uma **conta paga**, mas quem possui **créditos gratuitos (300 USD / 90 dias)** pode seguir normalmente.

## ⚙️ 2. Criando a Instância (Servidor Virtual)

1. **Acesse o GCP Console** → menu lateral → **Compute Engine** → **Instâncias de VM**.
2. Clique em “**Criar Instância**”.

**Configurações principais:**

| Parâmetro                         | Descrição / Valor sugerido                                                            |
| --------------------------------- | ------------------------------------------------------------------------------------- |
| **Nome**                          | `curso-django` (somente letras minúsculas e números)                                  |
| **Região/Zona**                   | Pode deixar padrão ou escolher **South America (São Paulo)** (geralmente mais barato) |
| **Tipo de máquina**               | `e2-micro` (2 vCPUs e 1 GB de RAM) — suficiente para projetos iniciais                |
| **Sistema operacional**           | **Ubuntu Server 20.04 LTS**                                                           |
| **Tamanho do disco**              | 10 GB é suficiente para iniciar                                                       |
| **Firewall**                      | ✅ Marcar **“Permitir tráfego HTTP”** (porta 80)                                       |
| *(HTTPS será configurado depois)* |                                                                                       |

## 💰 3. Custos e Créditos

- O custo estimado aparece na lateral.
    - Exemplo: `e2-micro` ≈ US$7/mês
    - Com créditos gratuitos, **não há cobrança**.
- Caso o servidor não esteja em uso, **pare a instância** para não gerar custos.

## 🌐 4. Endereço IP

- Após criada a VM, o GCP gera um:
    - **IP interno** (uso interno entre VMs)
    - **IP externo** (usado para acessar pela Internet)

**⚠️ IP temporário**

- O IP muda se a VM for desligada. → Vá em “**Ver detalhes da rede**” → “**Endereços IP externos**” → “**Reservar endereço estático**”
- Dê um nome, por exemplo: `curso-django-ip` → **Reservar**
- Assim, o IP se torna **fixo** (estático).

## 🔑 5. Configurando Acesso SSH

**Criar chave SSH (caso ainda não tenha)**

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```
*(Pressione Enter para deixar sem senha, se desejar)*

**Copiar chave pública**

```bash 
cat ~/.ssh/id_rsa.pub
```

**Adicionar no GCP**

- Vá até **Metadados** → **Chaves SSH** → **Adicionar item**
- Cole o conteúdo copiado da sua chave pública
- Clique em **Salvar**
  
## 💻 6. Conectando via SSH

Com a chave configurada, conecte-se:

```bash
ssh usuario@IP_DO_SERVIDOR
```

O “usuário” é o nome que aparece no final da sua chave pública (ex: `eduardo@notebook` → usuário = `eduardo`).

**Caso sua chave tenha outro nome (ex: `~/.ssh/minhachave`)**

Use:

```bash 
ssh -i ~/.ssh/minhachave usuario@IP_DO_SERVIDOR
```

## 🧩 7. Corrigindo Erros Comuns de SSH

- **Erro “Permission denied (publickey)”**:
  
    - Verifique se a chave usada localmente é a mesma adicionada no GCP.
  
    - Veja se o usuário do final da chave coincide com o esperado
  
- Se precisar, **gere uma nova chave SSH** e adicione novamente nos metadados.

## ⚙️ 8. Configurando arquivo `~/.ssh/config`

Para simplificar conexões SSH:

1. Edite ou crie o arquivo:

```bash 
nano ~/.ssh/config
```

2. Adicione:

```bash 
Host curso-django
    HostName 34.132.3.125   # (seu IP público)
    User eduardo             # (usuário conforme sua chave)
    Port 22
    IdentityFile ~/.ssh/id_rsa

```
Agora você pode conectar apenas digitando:

```bash 
ssh curso-django
```

**🧠 Resumo conceitual**

| Conceito                    | Função                                             |
| --------------------------- | -------------------------------------------------- |
| **Compute Engine (VM)**     | Cria um servidor virtual na nuvem                  |
| **Ubuntu Server 20.04 LTS** | Sistema operacional para hospedar o Django         |
| **Firewall (porta 80)**     | Libera o acesso HTTP                               |
| **SSH Key**                 | Autenticação segura entre sua máquina e o servidor |
| **IP Estático**             | Mantém o mesmo endereço mesmo após reiniciar       |
| **Arquivo `~/.ssh/config`** | Simplifica conexões SSH personalizadas             |

**🚀 Próximos Passos**

Na próxima etapa (próxima aula), serão realizados:

- Atualização dos pacotes do Ubuntu (`sudo apt update && sudo apt upgrade`)
- Instalação de dependências para Django (Python, pip, venv)
- Preparação para deploy (Gunicorn + Nginx)