# 🧾 Resumo da Aula — Testes Finais no Servidor e Uploads no Django

## 🧩 1. Testando a Aplicação no Servidor

- Acesse a aplicação pelo IP (ou domínio, se configurado).
- O painel administrativo pode ser acessado via `/admin/`.
- Se o login falhar, é necessário criar um **usuário administrador (superuser)** no servidor.


## 👤 2. Criando o Superusuário
```bash 
# Ativar ambiente virtual
source venv/bin/activate

# Criar superusuário
python manage.py createsuperuser
```

- Utilize um e-mail válido e uma senha forte, pois o servidor está exposto à internet.

- A senha simples só é aceitável em ambiente de testes.

## 🗂️ 3. Diferença entre Banco Local e Banco no Servidor

- Local: SQLite (db.sqlite3) — usado para desenvolvimento.
- Servidor: PostgreSQL — mais robusto e seguro para produção.
- Não misturar bancos entre os ambientes.

## 🧠 4. Boas Práticas de Sincronização
- Nunca altere código diretamente no servidor.
- Sempre faça modificações no ambiente local → git push → pull no servidor.
- Isso evita conflitos e perda de histórico Git.

## 🖼️ 5. Problema de Upload de Arquivos Grandes (Erro 413)

- O erro HTTP 413 indica que o arquivo enviado excede o limite permitido pelo servidor.
- A solução é ajustar o limite de upload no Nginx:

```bash 
sudo nano /etc/nginx/sites-available/meusite
```

Adicione (ou altere) dentro do bloco `server`:
```ngix
client_max_body_size 20M;
```

Depois, reinicie o Nginx:

```bash 
sudo systemctl restart nginx
```
*💡 20 MB é um limite seguro, mas evite imagens grandes — elas prejudicam o desempenho do site.*


## ⚙️ 6. Otimização de Imagens

- Sempre **otimize** imagens antes de enviá-las (ex: 720p e < 500 KB).
- Imagens muito grandes tornam o site lento.
- Pode-se usar o Photoshop, TinyPNG ou ferramentas CLI para compressão.

## ✅ 7. Verificação Final
- Testar upload e exibição de imagens.
- Verificar se as categorias, receitas e layout estão carregando corretamente.
- Confirmar que o site carrega rápido e sem erros.

## 🚀 8. Próximos Passos

- Configurar **domínio próprio** e **SSL (HTTPS)**.
- Testar acessos externos e realizar pequenos ajustes de segurança.

