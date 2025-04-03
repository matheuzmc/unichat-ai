# Documentação do Projeto UniChat

Este diretório contém a documentação completa do projeto UniChat, um sistema de chat inteligente para atendimento acadêmico que utiliza LLM (Large Language Models) e um protocolo de contexto personalizado (MCP) para fornecer respostas contextualizadas aos alunos.

## Índice de Documentos

### 1. Documentos de Produto

- [PRD (Product Requirements Document)](PRD-UniChat.md) - Documento de requisitos do produto
- [Plano MVP](Plano-MVP-UniChat.md) - Plano detalhado de implementação do MVP (Produto Mínimo Viável)
- [Exemplos de Interação](Exemplos-Interacao.md) - Exemplos de perguntas e respostas esperadas no chat

### 2. Documentos Técnicos

- [API Blueprint](API-Blueprint.md) - Documentação da estrutura da API REST
- [Glossário Técnico](Glossario-Tecnico.md) - Definição de termos técnicos utilizados no projeto
- [Decisões Técnicas](Decisoes-Tecnicas.md) - Justificativas para as escolhas tecnológicas

### 3. Guias de Instalação e Configuração

- [Guia de Instalação Passo a Passo](Guia-Instalacao-Passo-a-Passo.md) - Instruções detalhadas para instalação e configuração
- [Guia de Ambiente](Guia-Ambiente.md) - Visão geral do ambiente de desenvolvimento
- [Problemas Comuns e Soluções](Guia-Instalacao-Problemas-Comuns.md) - Soluções para problemas frequentes durante a instalação

### 4. Documentos de Acompanhamento

- [Diário de Desenvolvimento](Diario-Desenvolvimento.md) - Registro cronológico do desenvolvimento do projeto

## Estrutura do Projeto

```
unichat-ai/
├── backend/            # Projeto Django (Backend)
│   ├── api/            # App da API REST 
│   ├── config/         # Configurações do Django
│   ├── Dockerfile      # Configuração do container
│   └── requirements.txt # Dependências Python
├── frontend/           # Projeto React/Vite (Frontend)
│   ├── src/            # Código fonte React
│   ├── Dockerfile      # Configuração do container
│   └── package.json    # Dependências NPM
├── llm/                # Serviço LLM
│   ├── app/            # Código da API FastAPI
│   ├── Dockerfile      # Configuração do container
│   └── requirements.txt # Dependências Python
├── docs/               # Documentação
├── docker-compose.yml  # Configuração Docker Compose
├── .env                # Variáveis de ambiente (UID/GID)
└── .gitignore          # Arquivos ignorados pelo Git
```

## Como Navegar na Documentação

1. **Novos membros da equipe devem começar pelo:**
   - [PRD](PRD-UniChat.md) para entender o escopo e objetivos
   - [Guia de Instalação](Guia-Instalacao-Passo-a-Passo.md) para configurar o ambiente

2. **Para desenvolvedores trabalhando no backend:**
   - [API Blueprint](API-Blueprint.md)
   - [Decisões Técnicas](Decisoes-Tecnicas.md)

3. **Para desenvolvedores trabalhando no frontend:**
   - [Exemplos de Interação](Exemplos-Interacao.md)

4. **Para desenvolvedores trabalhando na integração LLM:**
   - [Glossário Técnico](Glossario-Tecnico.md)
   - [Decisões Técnicas](Decisoes-Tecnicas.md) (seção LLM)

## Estado Atual do Projeto

O projeto está na fase inicial de configuração do ambiente de desenvolvimento. A estrutura básica foi implementada com:

- Containers Docker para todos os componentes
- Configuração inicial do Django para o backend
- Configuração de uma API FastAPI para simular o serviço LLM
- Configuração básica do frontend com React, Vite e Tailwind

A próxima fase incluirá o desenvolvimento dos modelos de dados, API REST no backend, e implementação da interface do chat no frontend.

Para acompanhar o progresso atual, consulte o [Diário de Desenvolvimento](Diario-Desenvolvimento.md). 