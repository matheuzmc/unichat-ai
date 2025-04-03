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
- Criação da documentação inicial do projeto (PRD, MVP, glossário técnico)
- Implementação da estrutura inicial do projeto com Docker
- Configuração dos containers para backend, frontend, banco de dados e serviço LLM
- Implementação dos modelos de dados no backend (Django)
- Criação dos serializadores para converter objetos Django em JSON
- Implementação dos viewsets para APIs RESTful
- Configuração das rotas da API
- Registro dos modelos no painel administrativo
- Implementação de comandos para resetar e popular o banco de dados com dados fictícios
- Criação de superusuário para acesso administrativo
- Adição de documentação Swagger para API
- Padronização dos nomes de arquivos de documentação (remoção de acentos)

### Decisões Tomadas
- Escolha de Django REST Framework para o backend: maior produtividade e ecossistema maduro
- Escolha de React/Vite para o frontend: performance e experiência de desenvolvimento
- Decisão de usar LLM open-source: controle local e redução de custos
- Adoção do LangChain para integração de fontes de dados: simplificação da arquitetura
- Uso de volumes Docker nomeados para persistência de dados: melhor isolamento e portabilidade
- Implementação de verificação de saúde (healthcheck) para o PostgreSQL: garantir que o banco esteja pronto antes de iniciar o backend
- Armazenamento de UID/GID em arquivo .env: simplificar o uso em diferentes sessões de terminal
- Remoção da configuração de usuário para o container frontend: resolver problemas de permissão com node_modules
- Implementação de um serviço LLM simulado inicial: permitir desenvolvimento do frontend sem dependência de um LLM real
- Uso do padrão ModelViewSet para APIs: simplifica a criação de endpoints CRUD
- Implementação de ações personalizadas nas APIs (por exemplo, /api/alunos/{id}/detalhes/): facilita consultas específicas
- Implementação de filtros por aluno em cada endpoint (por exemplo, /api/notas/por_aluno/?aluno_id=1): melhora a usabilidade
- Utilização de Django Filters e SearchFilter: permite pesquisa e filtragem flexível
- Utilização de drf-yasg para documentação Swagger: documentação automática e interativa da API
- Padronização de nomenclatura sem acentos: evita problemas de codificação em sistemas diversos

### Problemas Encontrados
- Indefinição sobre qual LLM open-source específico utilizar: planejado um estudo comparativo entre GPT4All e Llama2
- Preocupações sobre performance local de LLMs: necessidade de testar em ambiente representativo
- Permissões de arquivos em volumes montados: resolvido com a configuração user: "${UID}:${GID}" nos serviços e uso de arquivo .env
- Problema específico no PostgreSQL com alteração de permissões: resolvido removendo a configuração de usuário do serviço db
- Conflito na indentação do docker-compose.yml: corrigido manualmente
- Erros no frontend relacionados a permissões em node_modules: resolvido usando um volume anônimo (/app/node_modules)
- Pacote curl não disponível no container backend: adicionado ao Dockerfile
- Erro na expansão das variáveis de ambiente UID/GID: corrigido usando o comando printf para criar corretamente o arquivo .env
- Problema de permissões nos containers: resolvido reconstruindo os containers com as IDs corretas do usuário
- Erros na manipulação de tipos Decimal e float: corrigido usando Decimal para todos os valores numéricos no cálculo de notas
- Duplicação de registros ao popular o banco: implementado um comando reset_db para limpar o banco antes de popular

### Próximos Passos
- Desenvolver o frontend com ReactJS
- Implementar a autenticação e autorização
- Criar as telas de login e cadastro
- Desenvolver o componente de chat
- Implementar a integração com o serviço LLM
- Realizar testes de integração do frontend com o backend
- Testar a performance do LLM em ambiente representativo
- Implementar o protocolo de contexto personalizado (MCP)

### Observações
O projeto teve um avanço significativo no primeiro dia de implementação. A infraestrutura básica está configurada, o backend possui uma API REST robusta com modelos de dados relacionais, e o ambiente de desenvolvimento está funcional com Docker. A estrutura do backend está bem definida e segue padrões RESTful, enquanto a documentação automática com Swagger facilita o entendimento e teste da API.

A configuração inicial com Docker provou ser mais complexa do que o esperado, especialmente em relação às permissões de arquivos, mas proporciona um ambiente de desenvolvimento isolado e consistente. Para a próxima fase, é importante focar no desenvolvimento do frontend e na integração com o LLM, que será o maior desafio técnico.

É essencial definir bem o escopo do MVP para garantir a entrega dentro do prazo de 6 semanas, priorizando funcionalidades críticas e deixando melhorias para iterações futuras.

## [Data: 2024-04-03]

### Atividades Realizadas
- Implementação da integração do serviço LLM com LangChain e GPT4All
- Desenvolvimento de interface baseada em prompt para processamento de contexto
- Criação de sistema de fallback para simulação de respostas quando o modelo não está disponível
- Implementação da interface de chat no frontend com React
- Criação de componentes reutilizáveis para o chat (ChatWindow, ChatMessage, ChatInput)
- Implementação de serviços de API para comunicação entre frontend e backend/LLM
- Documentação de melhorias futuras para o backend
- Correção de problemas de compatibilidade de versões no serviço LLM
- Ajustes nos Dockerfiles para garantir a instalação correta de dependências

### Decisões Tomadas
- Uso do modo de simulação para o LLM no MVP: evitar necessidade de baixar modelos grandes
- Implementação de um sistema de prompt baseado em dados do aluno: contextualização das respostas
- Design responsivo para a interface do chat: garantir usabilidade em diferentes dispositivos
- Integração com serviço LLM assíncrono: melhor experiência do usuário durante processamento
- Utilização do GPT4All na versão 0.1.7: compatibilidade com o ambiente atual
- Estruturação de TypeScript para o frontend: melhor manutenibilidade e detecção de erros
- Criação de um documento de melhorias futuras: facilitar evolução sistemática do projeto

### Problemas Encontrados
- Incompatibilidade de versões do GPT4All: necessidade de usar a versão 0.1.7 em vez da 2.0.3
- Dependências ausentes no container do frontend: resolvido adicionando-as explicitamente ao Dockerfile
- Dificuldades na geração de respostas contextualizadas: implementado sistema baseado em regras como fallback
- Incompatibilidade entre APIs do LangChain: resolução com importações específicas de versão

### Próximos Passos
- Implementar autenticação e perfis de usuário
- Adicionar testes automatizados para garantir qualidade
- Refinar o sistema de prompts para melhorar a qualidade das respostas
- Implementação de dados reais no banco de dados
- Explorar a integração com modelos LLM mais eficientes
- Melhorar o design e a experiência do usuário na interface de chat
- Adicionar funcionalidades como histórico persistente e filtros de consulta

### Observações
A implementação do MVP avançou significativamente, com uma arquitetura funcional que conecta todos os componentes do sistema. A abordagem de simulação para o LLM permitiu focar no desenvolvimento da interface e fluxos de dados sem depender de modelos grandes. A estrutura modular do serviço LLM permitirá fácil substituição por modelos mais avançados no futuro.

A interface de chat, embora simples, demonstra efetivamente o conceito e permitirá validar a utilidade do sistema com usuários reais. O próximo foco deve ser na melhoria da qualidade das respostas e na expansão das funcionalidades de acordo com o feedback dos usuários.

---

<!-- Novas entradas serão adicionadas acima desta linha --> 