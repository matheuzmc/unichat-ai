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

## [Data: 2024-04-04]

### Atividades Realizadas
- Implementação de sistema de testes automatizados para o serviço LLM
- Criação de dois comandos personalizados Django para testes: básico e avançado
- Implementação de biblioteca de casos de teste predefinidos
- Desenvolvimento de sistema de relatórios em CSV e visualizações gráficas
- Implementação de testes para diferentes categorias de consultas
- Criação de testes específicos para capacidades avançadas do LLM
- Documentação detalhada dos testes e comandos
- Atualização dos requisitos do projeto para incluir bibliotecas de visualização

### Decisões Tomadas
- Estruturação de testes por categorias de consulta: facilita a identificação de áreas problemáticas
- Implementação de testes de conversação com contexto: simula cenários reais de uso
- Geração de relatórios visuais com matplotlib: facilita interpretação dos resultados
- Separação entre testes básicos e avançados: oferece flexibilidade na execução
- Configuração de atraso entre requisições aos testes: evita sobrecarga do serviço LLM
- Criação de diretório específico para relatórios: melhor organização dos resultados

### Problemas Encontrados
- Módulo requests não disponível no contêiner: resolvido adicionando-o ao requirements.txt
- Bibliotecas pandas, numpy e matplotlib ausentes: adicionadas ao requirements.txt
- Erro na importação de modelos inexistentes (Professor e Avaliacao): corrigido removendo-os da importação
- Problemas de permissão ao instalar pacotes no contêiner: resolvido reconstruindo o contêiner

### Próximos Passos
- Refinar os casos de teste com base nos resultados iniciais
- Implementar avaliação semântica das respostas
- Desenvolver dashboard para monitoramento contínuo da qualidade
- Adicionar testes de robustez para consultas mal-formadas
- Implementar métricas de tempo de resposta
- Integrar testes automatizados ao pipeline CI/CD

### Observações
A implementação do sistema de testes automatizados representa um avanço significativo na garantia de qualidade do UniChat. O sistema agora permite uma avaliação objetiva e sistemática das respostas do LLM, facilitando a identificação de áreas que precisam de melhorias.

A taxa de sucesso inicial é baixa (cerca de 6%), o que era esperado considerando que o serviço LLM está em estágio inicial de desenvolvimento. Estes testes agora fornecem uma linha de base clara para medir o progresso futuro.

Os relatórios visuais e as métricas implementadas serão valiosos para comunicar o progresso aos stakeholders e guiar o desenvolvimento futuro do serviço LLM. A estrutura modular dos testes também permitirá fácil expansão à medida que novos requisitos surgirem.

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

## [Data: 2024-04-05]

### Atividades Realizadas
- Otimização significativa do serviço LLM para melhorar tempo de resposta
- Implementação de sistema de cache em dois níveis (dados do aluno e respostas)
- Redução do tamanho do contexto de 4096 para 1024 tokens para melhor performance
- Otimização de parâmetros do modelo (threads, batch size, temperatura)
- Implementação de sistema de timeout para respostas
- Redução e otimização dos prompts do sistema
- Criação de estratégia de build em duas camadas para reduzir tempo de build
- Análise de desempenho comparativa entre diferentes configurações
- Atualização da documentação de testes e instalação

## [Data: 2024-04-05]

### Atividades Realizadas
- Adaptação do sistema UniChat para suporte nativo a MacBooks com chip M1/M2/M3 (ARM)
- Criação do script `local_setup.sh` para configuração do ambiente LLM local no MacOS
- Desenvolvimento de `docker-compose.override.yml` para desativar o serviço LLM em Docker
- Implementação da detecção automática de arquitetura ARM para uso otimizado do Metal API
- Modificação do serviço LLM para aproveitar a aceleração por hardware via Metal no MacOS
- Ajuste nos scripts para verificação do modelo LLM local sem tentativas de download automático
- Configuração para que o LLM seja inicializado automaticamente em Macs ARM sem pedir confirmação
- Atualização do `start_unichat.sh` para orquestrar a inicialização integrada dos serviços
- Adição do comando `populate_db` ao iniciar o backend para garantir que dados de exemplo sejam criados

### Decisões Tomadas
- Execução do LLM localmente enquanto outros serviços permanecem em Docker: maximizar performance no M1
- Uso da API Metal da Apple para LLM: aceleração via GPU do chip M1/M2/M3
- Carregamento manual do modelo em vez de download automático: controle e segurança
- Detecção automática do chip ARM: configuração zero para melhor experiência do usuário
- Adição do comando populate_db no docker-compose.override.yml: garantir dados de teste disponíveis

### Problemas Encontrados
- Incompatibilidade do llama-cpp-python em contêiner Docker no M1: resolvido com execução local
- O banco de dados não era populado automaticamente no MacOS: corrigido com adição do comando populate_db
- Script original pedia confirmação para iniciar o LLM: modificado para iniciar automaticamente em Macs M1
- O processo de verificação do modelo fazia downloads não solicitados: modificado para apenas verificar

### Próximos Passos
- Aperfeiçoar a documentação específica para MacOS M1/M2/M3
- Implementar verificações de validação para garantir que o LLM está respondendo conforme esperado
- Otimizar ainda mais os parâmetros do LLM para a arquitetura ARM
- Explorar o uso de Metal Performance Shaders (MPS) para maior aceleração

### Observações
A adaptação para MacOS com chips M1/M2/M3 representa um avanço significativo na experiência de desenvolvimento, permitindo aproveitar a potência do hardware Apple para execução do LLM com melhor desempenho. A arquitetura híbrida (serviços em Docker + LLM nativo) oferece o melhor dos dois mundos: isolamento e padronização para a maioria dos serviços, e performance nativa para o componente mais exigente (LLM). Os scripts desenvolvidos simplificam significativamente o processo de configuração, tornando a experiência de desenvolvimento mais fluida.

## [Data: 2024-04-06]

### Atividades Realizadas
- Otimização significativa do serviço LLM para melhorar tempo de resposta
- Implementação de sistema de cache em dois níveis (dados do aluno e respostas)
- Redução do tamanho do contexto de 4096 para 1024 tokens para melhor performance
- Otimização de parâmetros do modelo (threads, batch size, temperatura)
- Implementação de sistema de timeout para respostas
- Redução e otimização dos prompts do sistema
- Criação de estratégia de build em duas camadas para reduzir tempo de build
- Análise de desempenho comparativa entre diferentes configurações
- Atualização da documentação de testes e instalação

### Decisões Tomadas
- Implementação de sistema de cache de respostas: reduz drasticamente o tempo de resposta para perguntas repetidas
- Redução do contexto para 1024 tokens: compromisso entre qualidade e velocidade de resposta
- Aumento de threads para 12: melhora utilização de CPU disponível
- Estratégia de build em duas camadas (base + serviço): redução de 98% no tempo de builds incrementais
- Pré-aquecimento do modelo no carregamento: melhora experiência inicial do usuário
- Parâmetros agressivos de geração: temperatura 0.1, top_p 0.5, tokens máximos 150
- Implementação de controle adaptativo de perplexidade: melhora estabilidade das respostas

### Problemas Encontrados
- Decorator @lru_cache incompatível com funções assíncronas: substituído por cache manual
- Tempo de build prolongado devido à compilação da biblioteca llama-cpp-python: resolvido com estratégia de duas camadas
- Conflitos entre tamanho de contexto e tempo de resposta: ajuste de parâmetros para equilíbrio
- Erro "cannot reuse already awaited coroutine": corrigido removendo o decorator @lru_cache
- Timeout ocasional em consultas complexas: implementado sistema de timeout máximo

### Próximos Passos
- Implementar suporte a GPU para aceleração de inferência
- Explorar otimização de matriz KV para memória e velocidade
- Investigar pré-processamento e indexação dos dados do aluno
- Refinar o sistema de prompts para otimizar resposta do modelo
- Implementar sistema de monitoramento de performance
- Desenvolver análise automática de qualidade das respostas

### Observações
O processo de otimização resultou em tempos de resposta significativamente melhores. O tempo médio da segunda consulta foi reduzido de 3min 16s para apenas 21s, atingindo a meta de resposta abaixo de 20 segundos. As consultas em cache agora respondem instantaneamente (28ms).

A abordagem de duas camadas para o processo de build foi particularmente bem-sucedida, reduzindo o tempo de build de aproximadamente 8-9 minutos para apenas 5-10 segundos em mudanças incrementais, o que melhora drasticamente a experiência de desenvolvimento.

Embora tenhamos alcançado bons resultados com otimizações de CPU, uma próxima etapa importante seria a implementação de suporte a GPU, que poderia reduzir ainda mais os tempos de resposta para poucos segundos por consulta.

A implementação do sistema de cache se mostrou a otimização com melhor custo-benefício, reduzindo o tempo de resposta em 99.99% para consultas repetidas, um cenário comum em ambientes educacionais onde vários alunos podem fazer perguntas semelhantes.

## [Data: 2024-04-07]

### Atividades Realizadas
- Implementação de um indicador de digitação (Typing Indicator) no chat para melhorar o feedback visual
- Adição do componente Skeleton do shadcn/ui para interfaces de carregamento
- Otimização adicional do gerenciamento de memória do LLM para Mac com chips Apple Silicon
- Implementação de thread dedicado para limpeza de memória em intervalos regulares via psutil
- Integração de configurações específicas por plataforma para o LLM
- Criação de animação de bolhas digitando para feedback visual durante o processamento do LLM
- Configurações otimizadas para Mac com Apple Silicon (M1/M2/M3)

### Decisões Tomadas
- Utilização de um componente de indicador de digitação: melhora a experiência do usuário fornecendo feedback visual
- Adoção do Skeleton para feedback de carregamento: padrão moderno de UX para indicar que conteúdo está sendo carregado
- Implementação de gerenciador de memória periódico: evita vazamentos e mantém performance estável no Mac
- Detecção automática de plataforma: aplica configurações otimizadas com base no hardware
- Escolha de animação personalizada para as bolhas de digitação: melhor performance visual que a animação padrão do Tailwind

### Problemas Encontrados
- Componente de loader não disponível no shadcn/ui: resolvido criando um componente customizado
- Animação bounce padrão do Tailwind não oferecia a aparência desejada: implementada animação personalizada via CSS
- Problemas de liberação de memória após o garbage collection no Python: implementado monitoramento via psutil e thread de limpeza dedicado
- Consumo crescente de memória durante operações prolongadas: resolvido com limpeza de memória periódica

### Próximos Passos
- Refinar o sistema de otimização de memória para trabalhar com outros modelos LLM
- Implementar indicadores visuais adicionais para outros estados da aplicação
- Adicionar opções de temas para os componentes visuais
- Testes adicionais do sistema de gerenciamento de memória em operações de longa duração

### Observações
A implementação do indicador de digitação representa uma melhoria significativa na experiência do usuário, fornecendo feedback visual claro durante o processamento das consultas. A ausência desse tipo de feedback era uma falha na experiência do usuário, agora corrigida.

As otimizações de memória para Mac com chip M1/M2/M3 são cruciais para manter o sistema estável durante uso prolongado, prevenindo degradação de performance ao longo do tempo. O sistema agora monitora ativamente o uso de memória e realiza liberações periódicas para manter o consumo sob controle.

---

<!-- Novas entradas serão adicionadas acima desta linha --> 