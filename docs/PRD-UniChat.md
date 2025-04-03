# PRD: UniChat - Sistema de Chat Inteligente para Atendimento Acadêmico

## 1. Visão do Produto

O UniChat é um sistema de chat inteligente que utiliza modelos de linguagem (LLM) e um Protocolo de Contexto de Modelo (MCP) personalizado para fornecer respostas contextualizadas e personalizadas aos alunos universitários, baseando-se em dados acadêmicos e administrativos armazenados em banco de dados.

## 2. Objetivos

- Desenvolver um ambiente de testes completo que simule um chat acadêmico inteligente
- Integrar um LLM open-source com uma API REST personalizada
- Fornecer respostas naturais e precisas sobre informações acadêmicas
- Criar uma interface moderna e responsiva para interação com os usuários

## 3. Escopo

### 3.1. Funcionalidades Principais

1. **Consulta de dados acadêmicos**
   - Notas e desempenho em disciplinas
   - Horários de aulas
   - Frequência em disciplinas
   - Situação de matrícula

2. **Consulta de dados administrativos**
   - Situação financeira
   - Informações cadastrais
   - Mensagens da coordenação
   - Atividades extracurriculares

3. **Interação natural por linguagem**
   - Processamento de perguntas em linguagem natural
   - Respostas contextualizadas e personalizadas
   - Sugestões baseadas no histórico do aluno

### 3.2. Fora do Escopo

- Autenticação e autorização avançadas
- Recomendações preditivas baseadas em IA
- Integração com sistemas externos (apenas simulação)
- Chatbot com reconhecimento de voz

## 4. Arquitetura Técnica

### 4.1. Componentes do Sistema

1. **Banco de Dados (PostgreSQL)**
   - Armazenamento de dados dos alunos
   - Tabelas relacionais para informações acadêmicas e administrativas

2. **Backend (Django Rest Framework)**
   - API RESTful para acesso aos dados
   - Endpoints específicos para cada tipo de informação
   - Implementação do MCP (Model Context Protocol)

3. **Serviço de LLM**
   - Modelo de linguagem open-source (GPT4All ou similar)
   - Integração via LangChain para processamento de consultas

4. **Frontend (React/Vite)**
   - Interface de chat responsiva
   - Componentes modernos com shadcn/ui
   - Estilização com Tailwind CSS
   - Validação com Zod e tipagem com TypeScript

### 4.2. Diagrama de Arquitetura

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐     ┌──────────────┐
│  Frontend   │     │     Backend      │     │     LLM      │     │  PostgreSQL  │
│ React/Vite  │◄───►│    Django REST   │◄───►│  + LangChain │     │   Database   │
│ Tailwind CSS│     │    Framework     │     │              │     │              │
└─────────────┘     └──────────────────┘◄───►└──────────────┘◄───►└──────────────┘
```

## 5. Requisitos Técnicos

### 5.1. Backend

- Django 4.2+
- Django REST Framework 3.14+
- PostgreSQL 14+
- Docker e Docker Compose
- Integração com LangChain 0.1.0+

### 5.2. Frontend

- React 18+
- TypeScript 5.0+
- Vite 4.0+
- Tailwind CSS 3.3+
- shadcn/ui
- Zod para validação

### 5.3. LLM e Integração

- LLM open-source (GPT4All, Llama2, etc.)
- LangChain para integração de fontes de dados
- API REST para comunicação entre componentes

## 6. Modelo de Dados

### 6.1. Entidades Principais

1. **Aluno**
   - Dados pessoais e identificação
   - Vínculo com curso e semestre

2. **Acadêmico**
   - Notas
   - Frequência
   - Horários
   - Matrículas
   - Histórico

3. **Administrativo**
   - Dados financeiros
   - Mensagens
   - Atividades extracurriculares
   - Biblioteca

### 6.2. Relacionamentos

- Um aluno possui múltiplas notas, matrículas, etc.
- Um aluno está associado a um conjunto de informações administrativas
- Todas as entidades possuem chaves estrangeiras para o aluno

## 7. Fluxos de Usuário

### 7.1. Consulta Acadêmica

1. Aluno acessa a interface de chat
2. Aluno digita pergunta (ex: "Qual minha nota em Matemática?")
3. Backend processa a pergunta e identifica o tipo de consulta
4. Sistema consulta o banco de dados através do MCP
5. LLM recebe os dados e gera uma resposta contextualizada
6. Resposta é exibida ao aluno no chat

### 7.2. Consulta Administrativa

1. Aluno acessa a interface de chat
2. Aluno digita pergunta (ex: "Quando vence minha próxima mensalidade?")
3. Backend processa a pergunta e identifica o tipo de consulta
4. Sistema consulta o banco de dados através do MCP
5. LLM recebe os dados e gera uma resposta contextualizada
6. Resposta é exibida ao aluno no chat

## 8. Critérios de Aceitação

1. O sistema deve processar e responder a consultas sobre todos os tipos de dados acadêmicos
2. As respostas devem ser contextualizadas e em linguagem natural
3. O tempo de resposta deve ser inferior a 3 segundos
4. A interface deve ser responsiva e funcionar em dispositivos móveis e desktop
5. Os dados fictícios devem ser representativos de um ambiente acadêmico real

## 9. Métricas de Sucesso

1. Precisão das respostas (correspondência com os dados reais)
2. Tempo médio de resposta
3. Naturalidade das respostas geradas pelo LLM
4. Cobertura dos diferentes cenários de consulta

## 10. Plano de Implementação

### 10.1. Fases de Desenvolvimento

1. **Configuração do Ambiente (Semana 1)**
   - Setup do Docker e containers
   - Configuração inicial do PostgreSQL

2. **Desenvolvimento do Backend (Semanas 2-3)**
   - Implementação dos modelos de dados
   - Criação da API REST com Django
   - População do banco com dados fictícios

3. **Integração do LLM (Semanas 4-5)**
   - Configuração do LLM open-source
   - Implementação da integração com LangChain
   - Testes de geração de respostas

4. **Desenvolvimento do Frontend (Semanas 6-7)**
   - Criação da interface de chat
   - Implementação dos componentes UI
   - Integração com o backend

5. **Testes e Refinamentos (Semana 8)**
   - Testes end-to-end
   - Ajustes de performance
   - Refinamento das respostas do LLM

## 11. Riscos e Mitigações

1. **Qualidade das respostas do LLM**
   - Mitigação: Refinamento do prompt e experimentação com diferentes modelos

2. **Performance do sistema**
   - Mitigação: Implementação de cache e otimização de consultas

3. **Complexidade da integração**
   - Mitigação: Abordagem modular e testes incrementais

4. **Limitações dos LLMs open-source**
   - Mitigação: Implementação de fallbacks e respostas predefinidas

## 12. Próximos Passos e Evolução

1. Implementação de autenticação e autorização
2. Expansão para outros domínios além do acadêmico
3. Melhoria contínua do modelo de linguagem
4. Adição de recursos de acessibilidade
5. Integração com sistemas reais de gestão acadêmica 