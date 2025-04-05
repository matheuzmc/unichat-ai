# Guia de Ambiente: UniChat

Este documento descreve como configurar o ambiente de desenvolvimento para o projeto UniChat.

## Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

- [Git](https://git-scm.com/) (2.30+)
- [Docker](https://www.docker.com/) (20.10+)
- [Docker Compose](https://docs.docker.com/compose/) (2.0+)
- [Node.js](https://nodejs.org/) (18.0+) - apenas para desenvolvimento frontend local
- [Python](https://www.python.org/) (3.10+) - apenas para desenvolvimento backend local

## Estrutura do Projeto

```
unichat-ai/
├── backend/            # Projeto Django
│   ├── api/            # Aplicação da API REST
│   ├── config/         # Configurações do Django
│   └── requirements.txt # Dependências Python
├── frontend/           # Projeto React/Vite
│   ├── public/         # Arquivos públicos
│   ├── src/            # Código-fonte React
│   ├── package.json    # Dependências NPM
│   └── vite.config.ts  # Configuração do Vite
├── llm/                # Serviço de LLM
│   ├── app/            # Código do serviço
│   └── requirements.txt # Dependências Python
├── docs/               # Documentação
├── docker-compose.yml  # Configuração dos containers
└── README.md           # Documentação raiz
```

## Configuração com Docker

O projeto utiliza Docker para isolamento e padronização do ambiente de desenvolvimento. Todos os serviços são definidos no arquivo `docker-compose.yml`.

### Passos para Inicialização

1. **Clonar o repositório:**

```bash
git clone https://github.com/seu-usuario/unichat-ai.git
cd unichat-ai
```

2. **Configurar variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
# Configurações do PostgreSQL
POSTGRES_DB=unichat
POSTGRES_USER=unichat_user
POSTGRES_PASSWORD=unichat_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Configurações do Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Configurações do LLM
LLM_MODEL_PATH=/app/models/model.bin
```

3. **Iniciar os serviços com Docker Compose:**

```bash
docker-compose up -d
```

Este comando iniciará os seguintes serviços:
- `db`: PostgreSQL
- `backend`: Django REST Framework
- `llm`: Serviço LLM
- `frontend`: Aplicação React/Vite

4. **Verificar o status dos serviços:**

```bash
docker-compose ps
```

5. **Acessar os serviços:**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/v1/
- Documentação da API: http://localhost:8000/api/docs/

## Desenvolvimento Local (Sem Docker)

### Backend (Django)

1. **Configurar ambiente virtual Python:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configurar variáveis de ambiente:**

Crie um arquivo `.env` no diretório `backend/` com conteúdo similar ao apresentado anteriormente.

3. **Aplicar migrações e iniciar servidor:**

```bash
python manage.py migrate
python manage.py runserver
```

### Frontend (React/Vite)

1. **Instalar dependências:**

```bash
cd frontend
npm install
```

2. **Iniciar servidor de desenvolvimento:**

```bash
npm run dev
```

### Serviço LLM

1. **Configurar ambiente virtual Python:**

```bash
cd llm
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Baixar modelo (se necessário):**

```bash
mkdir -p models
# Script para download do modelo será adicionado
```

3. **Iniciar serviço:**

```bash
python app/main.py
```

## Testes

### Backend

```bash
cd backend
python manage.py test
```

### Frontend

```bash
cd frontend
npm run test
```

## Comandos Úteis

### Docker Compose

```bash
# Iniciar todos os serviços
docker-compose up -d

# Parar todos os serviços
docker-compose down

# Ver logs
docker-compose logs -f [serviço]

# Reconstruir serviços
docker-compose build [serviço]

# Executar comando em um serviço
docker-compose exec [serviço] [comando]
```

### Django

```bash
# Criar migrações
docker-compose exec backend python manage.py makemigrations

# Aplicar migrações
docker-compose exec backend python manage.py migrate

# Criar superusuário
docker-compose exec backend python manage.py createsuperuser

# Alimentar banco com dados de teste
docker-compose exec backend python manage.py loaddata initial_data
```

## Configuração Especial para MacBooks M1/M2/M3

Os MacBooks com chips Apple Silicon (M1/M2/M3) possuem uma configuração especial para maximizar o desempenho do LLM através da API Metal.

### Inicialização com LLM Local

Para MacBooks com chips M1/M2/M3, é recomendado executar o serviço LLM localmente (fora do Docker) para aproveitar a aceleração de hardware, enquanto os demais serviços continuam em containers Docker.

1. **Usar o script de inicialização automática:**

```bash
./start_unichat.sh
```

Este script:
- Inicia os serviços Docker (backend, frontend, db)
- Configura e inicia o LLM localmente com suporte a Metal
- Detecta automaticamente o chip M1/M2/M3 e otimiza as configurações

2. **Configuração manual (se necessário):**

```bash
# Iniciar serviços Docker (exceto LLM)
docker-compose up -d db backend frontend

# Configurar e iniciar o LLM local
cd llm
./local_setup.sh
```

### Requisitos para LLM Local no M1/M2/M3

- O modelo `Phi-3-mini-4k-instruct-q4.gguf` deve estar no diretório `llm/models/`
- Python 3.10+ deve estar instalado no MacOS
- O Mac deve ter pelo menos 8GB de RAM (16GB recomendado)

### Verificação do Funcionamento

Para verificar se o LLM local está funcionando corretamente:

```bash
# Verificar se o processo está rodando
ps aux | grep uvicorn

# Testar o endpoint de saúde
curl http://localhost:8080/health
```

Resposta esperada:
```json
{"status":"ok","message":"UniChat LLM Service is running"}
```

## Solução de Problemas

### Problemas Comuns

1. **Erro ao conectar ao banco de dados:**
   - Verifique se o serviço `db` está em execução: `docker-compose ps`
   - Verifique as credenciais no arquivo `.env`
   - Verifique os logs: `docker-compose logs db`

2. **Erro ao iniciar o serviço LLM:**
   - Verifique se o modelo foi baixado corretamente
   - Verifique o caminho do modelo no arquivo `.env`
   - Aumentar a memória alocada para o Docker se o modelo for grande

3. **Frontend não conecta ao backend:**
   - Verifique as configurações de CORS no backend
   - Verifique se a URL da API está correta no frontend

## Próximos Passos

Este guia será atualizado à medida que o projeto evolui. Futuramente, incluiremos:
- Instruções para deploy em produção
- Configuração de CI/CD
- Monitoramento e logging 