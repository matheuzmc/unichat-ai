# Plano de Implementação MVP: UniChat

## 1. Definição do MVP

O MVP (Produto Mínimo Viável) do UniChat consistirá em uma aplicação de chat funcional capaz de responder a um conjunto limitado, porém representativo, de perguntas sobre dados acadêmicos e administrativos, utilizando um LLM open-source e uma API Django simplificada.

## 2. Objetivos do MVP

- Validar a viabilidade técnica da integração entre LLM e dados acadêmicos
- Obter feedback inicial sobre a qualidade e utilidade das respostas
- Estabelecer uma base sólida para desenvolvimento incremental
- Demonstrar valor para stakeholders antes da implementação completa

## 3. Escopo do MVP

### 3.1 Funcionalidades Incluídas

1. **Chat com Interface Básica**
   - Interface de usuário minimalista para entrada de perguntas e exibição de respostas
   - Histórico básico de conversas
   - Design responsivo para desktop e mobile

2. **Consultas Acadêmicas Limitadas**
   - Consulta de notas nas disciplinas
   - Consulta de horários de aulas
   - Consulta de situação de matrícula

3. **Consultas Administrativas Limitadas**
   - Consulta de informações financeiras básicas
   - Consulta de dados cadastrais do aluno

4. **Backend com Modelo de Dados Simplificado**
   - Implementação de modelo de dados para alunos, notas e horários
   - API REST com endpoints essenciais
   - Banco de dados com dados fictícios representativos

5. **Integração Básica com LLM**
   - Configuração de LLM open-source (ex.: GPT4All, Llama2)
   - Processamento básico de perguntas em linguagem natural
   - Geração de respostas contextualmente relevantes

### 3.2 Funcionalidades Excluídas do MVP (Para Futuras Iterações)

1. **Funcionalidades Avançadas de Chat**
   - Sugestões de perguntas
   - Feedback sobre qualidade das respostas
   - Personalização da interface

2. **Consultas Acadêmicas Complexas**
   - Histórico completo
   - Análise de desempenho
   - Frequência detalhada

3. **Consultas Administrativas Complexas**
   - Atividades extracurriculares
   - Biblioteca e empréstimos
   - Mensagens da coordenação

4. **Componentes Avançados**
   - Autenticação e autorização
   - Análise de sentimentos
   - Cache avançado e otimizações de performance

## 4. Arquitetura Técnica Simplificada

### 4.1 Componentes Essenciais

1. **Banco de Dados (PostgreSQL)**
   - Esquema simplificado com tabelas essenciais
   - Sem otimizações complexas

2. **Backend (Django REST Framework)**
   - API com endpoints mínimos necessários
   - Sem autenticação complexa
   - Sem cache avançado

3. **Serviço LLM**
   - Configuração básica do modelo
   - Integração simples via LangChain

4. **Frontend (React/Vite)**
   - Componentes UI essenciais
   - Estilização básica com Tailwind CSS
   - Validação básica com Zod

## 5. Cronograma de Desenvolvimento

### Semana 1: Configuração e Planejamento
- Configuração do ambiente de desenvolvimento com Docker
- Inicialização do projeto Django e React
- Definição detalhada dos modelos de dados e endpoints

### Semana 2: Desenvolvimento do Backend Inicial
- Implementação do modelo de dados básico
- Criação dos endpoints essenciais da API
- População do banco com dados ficticios representativos

### Semana 3: Integração do LLM
- Setup e configuração do LLM open-source
- Integração básica com LangChain
- Testes iniciais de geração de respostas

### Semana 4: Desenvolvimento do Frontend Básico
- Implementação da interface de chat
- Integração com a API do backend
- Estilização básica

### Semana 5: Testes e Refinamentos
- Testes end-to-end das funcionalidades
- Correção de bugs críticos
- Otimização do tempo de resposta

### Semana 6: Lançamento do MVP
- Documentação final
- Deploy em ambiente de demonstração
- Apresentação para stakeholders

## 6. Divisão de Tarefas por Semana

### Semana 1: Configuração e Planejamento
- **Dia 1-2:** Configuração do Docker e ambiente de desenvolvimento
- **Dia 3-4:** Criação do projeto Django e configuração do PostgreSQL
- **Dia 5:** Inicialização do projeto React/Vite

### Semana 2: Desenvolvimento do Backend Inicial
- **Dia 1-2:** Implementação dos modelos Django (Aluno, Notas, Horários)
- **Dia 3-4:** Desenvolvimento dos serializers e views da API
- **Dia 5:** Script para população do banco com dados de teste

### Semana 3: Integração do LLM
- **Dia 1-2:** Setup e configuração do LLM escolhido
- **Dia 3-4:** Integração com LangChain e criação de prompts iniciais
- **Dia 5:** Testes e ajustes na geração de respostas

### Semana 4: Desenvolvimento do Frontend Básico
- **Dia 1-2:** Implementação dos componentes básicos do chat
- **Dia 3-4:** Integração com endpoints da API
- **Dia 5:** Estilização com Tailwind CSS

### Semana 5: Testes e Refinamentos
- **Dia 1-2:** Testes integrados de todos os componentes
- **Dia 3-4:** Correção de bugs e problemas identificados
- **Dia 5:** Otimização de performance e tempo de resposta

### Semana 6: Lançamento do MVP
- **Dia 1-2:** Finalização da documentação
- **Dia 3-4:** Deploy em ambiente de demonstração
- **Dia 5:** Apresentação do MVP para stakeholders

## 7. Métricas de Sucesso do MVP

### 7.1 Métricas Técnicas
- Tempo médio de resposta < 5 segundos
- Taxa de perguntas corretamente interpretadas > 80%
- Uptime do sistema > 95% durante período de testes

### 7.2 Métricas de Usuário
- Taxa de satisfação com as respostas > 70%
- Taxa de perguntas que recebem respostas úteis > 75%
- Número médio de consultas por sessão > 3

## 8. Critérios de Aceitação

1. O sistema deve responder corretamente às consultas de notas e horários
2. O tempo de resposta não deve exceder 5 segundos
3. As respostas devem ser gramaticalmente corretas e contextualmente relevantes
4. A interface deve funcionar em dispositivos desktop e mobile
5. O sistema deve lidar graciosamente com perguntas fora do escopo

## 9. Estratégia de Testes

1. **Testes Unitários**
   - Cobertura mínima de 60% para o backend
   - Testes dos principais componentes do frontend

2. **Testes de Integração**
   - Verificação da comunicação entre todos os componentes
   - Validação do fluxo completo de perguntas e respostas

3. **Testes de Usuário**
   - Sessões de teste com 5-10 usuários representativos
   - Coleta estruturada de feedback

## 10. Riscos e Mitigações para o MVP

1. **Qualidade insuficiente das respostas do LLM**
   - Mitigação: Implementar respostas pré-definidas para perguntas comuns

2. **Tempo de resposta alto**
   - Mitigação: Limitar o escopo das consultas e otimizar prompts

3. **Dificuldades na integração LLM/API**
   - Mitigação: Desenvolver uma camada intermediária simplificada

4. **Problemas de usabilidade da interface**
   - Mitigação: Focar em design minimalista e intuitivo

## 11. Próximos Passos Pós-MVP

1. Expansão do conjunto de consultas suportadas
2. Melhorias na interface de usuário e experiência
3. Otimizações de performance
4. Implementação de autenticação e personalização
5. Análise de dados de uso para identificar oportunidades de melhoria

## 12. Recursos Necessários

1. **Equipe**
   - 1 Desenvolvedor Backend
   - 1 Desenvolvedor Frontend
   - 1 Especialista em LLM/NLP
   - 1 Testador

2. **Infraestrutura**
   - Servidor para PostgreSQL
   - Servidor para aplicação Django
   - Servidor para LLM
   - Ambiente de desenvolvimento local com Docker

3. **Ferramentas**
   - Repositório Git
   - Sistema de CI/CD
   - Ferramentas de monitoramento
   - Plataforma para coleta de feedback 