# Diário de Desenvolvimento: UniChat

Este documento serve como um registro cronológico do desenvolvimento do projeto UniChat. Aqui serão documentadas decisões importantes, alterações significativas, problemas encontrados e lições aprendidas durante o processo de desenvolvimento.

## Template de Entrada

```
## [Data: AAAA-MM-DD]

### Atividades Realizadas
- Descrição da atividade 1
- Descrição da atividade 2

### Decisões Tomadas
- Decisão 1: justificativa
- Decisão 2: justificativa

### Problemas Encontrados
- Problema 1: como foi resolvido ou plano para resolução
- Problema 2: como foi resolvido ou plano para resolução

### Próximos Passos
- Tarefa planejada 1
- Tarefa planejada 2

### Observações
Quaisquer observações adicionais, insights ou ideias para o futuro.
```

## Entradas do Diário

## [Data: 2023-04-03]

### Atividades Realizadas
- Criação da documentação inicial do projeto
- Definição do PRD (Product Requirements Document)
- Elaboração do plano de implementação MVP
- Criação do glossário técnico e outros documentos de suporte

### Decisões Tomadas
- Escolha de Django REST Framework para o backend: maior produtividade e ecossistema maduro
- Escolha de React/Vite para o frontend: performance e experiência de desenvolvimento
- Decisão de usar LLM open-source: controle local e redução de custos
- Adoção do LangChain para integração de fontes de dados: simplificação da arquitetura

### Problemas Encontrados
- Indefinição sobre qual LLM open-source específico utilizar: planejado um estudo comparativo entre GPT4All e Llama2
- Preocupações sobre performance local de LLMs: necessidade de testar em ambiente representativo

### Próximos Passos
- Configurar ambiente de desenvolvimento com Docker
- Implementar estrutura básica do projeto Django
- Definir modelos de dados e criar migrações iniciais
- Inicializar projeto React/Vite com configuração de Tailwind e TypeScript

### Observações
O projeto parece promissor, mas será importante definir bem o escopo do MVP para garantir entrega dentro do prazo de 6 semanas. A integração com LLM local será o maior desafio técnico e deve ser priorizada para validação inicial.

## [Data: 2023-04-04]

### Atividades Realizadas
- Implementação da estrutura inicial do projeto com Docker
- Configuração dos containers para banco de dados (PostgreSQL)
- Configuração do backend com Django REST Framework
- Configuração do serviço LLM simulado com FastAPI
- Configuração do frontend com React, Vite e Tailwind CSS
- Integração inicial entre os serviços

### Decisões Tomadas
- Uso de volumes Docker nomeados para persistência de dados: melhor isolamento e portabilidade
- Implementação de verificação de saúde (healthcheck) para o PostgreSQL: garantir que o banco esteja pronto antes de iniciar o backend
- Armazenamento de UID/GID em arquivo .env: simplificar o uso em diferentes sessões de terminal
- Remoção da configuração de usuário para o container frontend: resolver problemas de permissão com node_modules
- Implementação de um serviço LLM simulado inicial: permitir desenvolvimento do frontend sem dependência de um LLM real

### Problemas Encontrados
- Permissões de arquivos em volumes montados: resolvido com a configuração user: "${UID}:${GID}" nos serviços e uso de arquivo .env
- Problema específico no PostgreSQL com alteração de permissões: resolvido removendo a configuração de usuário do serviço db
- Conflito na indentação do docker-compose.yml: corrigido manualmente
- Erros no frontend relacionados a permissões em node_modules: resolvido usando um volume anônimo (/app/node_modules)
- Pacote curl não disponível no container backend: adicionado ao Dockerfile

### Próximos Passos
- Implementar modelos de dados do Django conforme PRD
- Desenvolver endpoints da API REST
- Implementar telas principais do frontend
- Integrar um LLM real ao serviço simulado
- Desenvolver a lógica de processamento de perguntas com LangChain

### Observações
A configuração inicial com Docker provou ser mais complexa do que o esperado, especialmente em relação às permissões de arquivos, mas proporciona um ambiente de desenvolvimento isolado e consistente. Para a próxima fase, é importante focar na implementação das funcionalidades centrais definidas no MVP.

---

<!-- Novas entradas serão adicionadas acima desta linha --> 