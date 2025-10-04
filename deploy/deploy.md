# Resumo da Aula: Criando e Acessando um Servidor no Google Cloud Platform (GCP)

## 1. Contexto
- Objetivo: Criar um servidor para hospedar a aplicação Django.
- Ferramenta: Google Cloud Platform (GCP), usando uma conta gratuita ou paga.
- Alternativas: VirtualBox, Parallels ou outro provedor de nuvem.

## 2. Criação da Instância no GCP

1. Acesse o menu Compute Engine → Instâncias de VM.
2. Clique em Criar instância.
3. Configurações principais:
    - Nome: Use letras minúsculas e números, sem caracteres especiais.
    - Localização: Escolha região/zone (ex.: São Paulo ou US Central).
    - Tipo de máquina:
        - Inicialmente: 2 vCPU, 4 GB RAM (mais rápido, mas mais caro).
        - Sugestão para economia: e2-micro (2 vCPU, 1 GB RAM) ou menor.
    - Disco de inicialização: Ubuntu Server 20.04 LTS.
    - Firewall: Permitir tráfego HTTP (porta 80). HTTPS será configurado depois (porta 443).
  
4. Criação do servidor: leva alguns minutos.

## 3. Endereço IP

- IP externo: usado para acessar a instância.
- Atenção: IP pode ser dinâmico (muda quando o servidor é desligado).
- Para manter o IP fixo, use a opção “**Reservar IP estático**” no GCP.

## 4. Configuração de Acesso via SSH

1.Gere uma chave SSH (se não tiver):
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519
```

- `-t ed25519`: tipo da chave.
-  `-f`: caminho do arquivo.
-  Senha: opcional, mas aumenta a segurança.

2. Copie a chave pública (`.pub`) e cole em Metadados → Chaves SSH no GCP.
3. Salve e aguarde o acesso autorizado.
4. Conexão SSH:
   
```bash
ssh -i ~/.ssh/id_ed25519 usuario@IP_DO_SERVIDOR
```
1. Dica: Para facilitar futuras conexões, configure um alias no `~/.ssh/config`:
```text
Host curso-django
    HostName IP_DO_SERVIDOR
    User usuario
    IdentityFile ~/.ssh/id_ed25519
    Port 22
```

- Agora basta usar `ssh curso-django`.

## 5. Boas práticas
- Sempre desligue o servidor quando não estiver usando para evitar cobranças.
- Ajuste o tipo de máquina de acordo com a performance necessária.
- Use Ubuntu LTS para estabilidade e suporte prolongado.
- Reserve o IP se quiser que ele permaneça constante.
- Use comentários nas chaves SSH para identificar usuários e máquinas.

## 6. Próximos Passos

- Atualizar pacotes do servidor.
- Instalar dependências necessárias para o Django.
- Configurar firewall adicional (HTTPS, etc.).
- Preparar o ambiente para deploy da aplicação