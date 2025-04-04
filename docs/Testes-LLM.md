# Testes Automatizados para Qualidade do LLM

Este documento descreve a infraestrutura de testes automatizados implementada para avaliar a qualidade das respostas geradas pelo serviço LLM (Large Language Model) utilizado no UniChat.

## Arquitetura dos Testes

O sistema de testes foi construído como comandos personalizados do Django, localizados em `backend/api/management/commands/`. A arquitetura permite testes em diferentes níveis de complexidade e com diferentes opções de execução.

### Arquivos Principais

- **test_llm_responses.py**: Teste básico que verifica a qualidade das respostas do LLM para consultas simples.
- **test_llm_avancado.py**: Teste avançado com suporte a relatórios, categorias e verificação de capacidades específicas.
- **testes_prontos.py**: Biblioteca de casos de teste predefinidos usados pelos comandos de teste.
- **README.md**: Documentação sobre os comandos e suas opções.

## Categorias de Teste

Os testes são organizados nas seguintes categorias:

1. **Notas**: Consultas relacionadas a notas e desempenho acadêmico
2. **Horários**: Consultas sobre horários de aula, salas e cronograma
3. **Informações Gerais**: Consultas sobre curso, semestre e dados do aluno
4. **Complexas**: Consultas que exigem contexto adicional ou raciocínio
5. **Conversação**: Testes de capacidade de manter contexto em conversas

## Capacidades Específicas Testadas

Além das categorias acima, o sistema testa capacidades específicas do LLM:

1. **Formatação de Tabela**: Capacidade de apresentar dados tabulares de forma organizada
2. **Atualização Recente**: Conhecimento sobre atualização de dados no sistema
3. **Explicação Pedagógica**: Capacidade de fornecer explicações educativas
4. **Comparação de Notas**: Habilidade de comparar categorias diferentes
5. **Recomendação**: Capacidade de fazer recomendações personalizadas

## Relatórios Gerados

Quando executado com a opção `--gerar_relatorio`, o sistema gera:

1. **Arquivo CSV**: Contém detalhes de todos os testes executados, incluindo:
   - ID do teste
   - Categoria
   - Pergunta utilizada
   - Resultado (PASSOU/FALHOU)
   - Data e hora de execução

2. **Gráficos**:
   - **Gráfico de Categorias**: Mostra a taxa de sucesso por categoria de teste
   - **Gráfico de Resultados**: Gráfico de pizza mostrando a distribuição geral dos resultados

Todos os relatórios são salvos no diretório `relatorios_llm/` na raiz do projeto backend.

## Executando os Testes

### Teste Básico

```bash
python manage.py test_llm_responses
```

Opções disponíveis:
- `--aluno_id ID`: Especifica o ID do aluno para realizar os testes
- `--disciplina NOME`: Especifica uma disciplina para focar os testes
- `--verbose`: Exibe detalhes completos de cada teste

### Teste Avançado

```bash
python manage.py test_llm_avancado
```

Opções disponíveis:
- `--aluno_id ID`: Especifica o ID do aluno para realizar os testes
- `--categoria CATEGORIA`: Executa apenas testes de uma categoria específica (notas, horarios, info_geral, complexa, conversacao)
- `--verbose`: Exibe detalhes completos de cada teste
- `--gerar_relatorio`: Gera relatório em CSV e gráficos dos resultados
- `--testar_capacidades`: Executa testes específicos para capacidades avançadas do LLM

## Ambiente de Execução

Os testes devem ser executados dentro do contêiner Docker do backend:

```bash
docker exec -it unichat-backend python manage.py test_llm_responses
```

ou

```bash
docker exec -it unichat-backend python manage.py test_llm_avancado --gerar_relatorio
```

## Interpretação dos Resultados

Os testes verificam se as respostas do LLM contêm determinados termos esperados para cada consulta. Por exemplo:

- Para uma consulta sobre nota, o teste verifica se a resposta contém o valor correto da nota
- Para uma consulta sobre horário, o teste verifica se a resposta contém o dia, horário e sala corretos

## Extensibilidade

O sistema foi projetado para ser facilmente extensível:

1. Novos casos de teste podem ser adicionados ao arquivo `testes_prontos.py`
2. Novas capacidades podem ser definidas com suas próprias funções de verificação
3. Novos tipos de relatórios podem ser implementados no método `gerar_relatorio_testes`

## Considerações de Performance

- Os testes incluem um atraso de 0.5 segundos entre as chamadas para não sobrecarregar o serviço LLM
- Gráficos são gerados apenas quando solicitados com a flag `--gerar_relatorio`
- O sistema salva o histórico de chat durante os testes de conversação para simular um ambiente real

## Limitações Conhecidas

- Os testes atuais não verificam a qualidade linguística ou a fluência das respostas
- Não há verificação de tempo de resposta ou performance do serviço LLM
- Os testes não avaliam a capacidade de lidar com consultas ambíguas ou mal-formadas

## Próximos Passos

1. Implementar testes para verificar a qualidade linguística das respostas
2. Adicionar testes de robustez para consultas ambíguas ou mal-formadas
3. Implementar métricas de tempo de resposta e performance
4. Criar um dashboard de monitoramento para acompanhar a evolução da qualidade das respostas ao longo do tempo 

## Otimizações de Performance do LLM

A versão mais recente do serviço LLM inclui otimizações significativas que melhoram drasticamente o tempo de resposta. Esta seção descreve as principais otimizações implementadas e como testá-las.

### Principais Otimizações

1. **Sistema de Cache em Dois Níveis**:
   - Cache de dados do aluno: evita consultas repetidas ao backend
   - Cache de respostas: armazena respostas para perguntas idênticas
   - Resultado: redução de 99.99% no tempo para consultas repetidas

2. **Otimização de Parâmetros do Modelo**:
   - Redução do contexto: 4096 → 1024 tokens
   - Aumento de threads: 4 → 12
   - Processamento em lote: 512 → 1024
   - Temperatura reduzida: 0.7 → 0.1
   - Tokens máximos reduzidos: 500 → 150

3. **Redução do Tamanho dos Prompts**:
   - Prompts mais concisos para reduzir processamento
   - Sistema de templating otimizado para reduzir tokens

4. **Pré-aquecimento do Modelo**:
   - Execução de consulta simples na inicialização
   - Prepara o modelo para respostas mais rápidas

### Métricas de Performance

Na versão atual, foram observadas as seguintes métricas:

| Consulta | Antes da Otimização | Após a Otimização | Melhoria |
|----------|---------------------|-------------------|----------|
| Primeira consulta | 5m 34s | 2m 49s | 49% |
| Segunda consulta | 3m 16s | 21s | 89% |
| Terceira consulta | 2m 27s | 1m 38s | 33% |
| Consulta em cache | N/A | 28ms | 99.99% |

### Como Testar as Otimizações

Para testar o impacto das otimizações de performance, foram implementados scripts que medem o tempo de resposta sob diferentes condições:

#### 1. Teste de Primeira Resposta

```bash
time curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Quais são meus horários de aula?", "student_id": 1}'
```

Este teste mede o tempo da primeira consulta, que inclui o carregamento completo do pipeline de processamento.

#### 2. Teste de Segunda Resposta (Modelo Aquecido)

```bash
time curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Qual é minha nota em Física?", "student_id": 1}'
```

Este teste mede o tempo após o modelo estar "aquecido".

#### 3. Teste de Cache

Execute a mesma consulta do teste anterior novamente:

```bash
time curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Qual é minha nota em Física?", "student_id": 1}'
```

A resposta deve ser praticamente instantânea devido ao cache.

### Verificando o Uso do Cache

Para confirmar que o cache está sendo utilizado:

```bash
docker compose logs llm | grep "cache" -A 1 -B 1
```

Você deverá ver mensagens como:
- "Usando dados em cache para aluno ID: X"
- "Usando resposta em cache para pergunta: 'Y'"

### Testes Automatizados para Performance

Futuramente, serão implementados testes automatizados para monitorar a performance:

1. **Testes de Latência**: Medição automática do tempo de resposta
2. **Testes de Carga**: Desempenho sob múltiplas consultas simultâneas
3. **Testes de Regressão**: Garantir que novas versões mantenham ou melhorem a performance
4. **Testes de Warmup**: Comportamento de performance durante a inicialização do sistema

## Integrando e Testando Modelos GGUF

### Sobre Modelos GGUF

O formato GGUF (GPT-Generated Unified Format) é um formato de modelo otimizado para inferência eficiente em dispositivos com recursos limitados. Os modelos GGUF permitem executar LLMs localmente com melhor desempenho e menor consumo de memória comparado a outros formatos.

No UniChat, integramos suporte para o modelo Phi-3-mini-4k-instruct-q4 em formato GGUF através da biblioteca llama-cpp-python.

### Passos para Testes Manuais

1. **Verificar se o modelo foi carregado corretamente**
   ```bash
   docker compose logs llm | grep "Modelo GGUF carregado com sucesso"
   ```

2. **Testar diretamente via API**
   ```bash
   curl -X POST "http://localhost:8080/api/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "Qual é a minha nota em Física?", "student_id": 1}'
   ```

3. **Testar via interface web**
   Acesse http://localhost:3000 e faça perguntas ao chatbot para verificar se as respostas estão sendo geradas pelo modelo GGUF.

### Comparação entre Modo Simulado e Modelo GGUF

Para fins de desenvolvimento, o UniChat pode operar em dois modos:

1. **Modo Simulado**
   - Resposta prefixada com "[SIMULAÇÃO]"
   - Baseado em regras predefinidas
   - Rápido, sem necessidade de carregar modelo
   - Útil para testes de interface e fluxos

2. **Modo GGUF**
   - Utiliza o modelo GGUF para gerar respostas
   - Qualidade superior e contextualização mais precisa
   - Requer mais recursos de hardware
   - Dependências adicionais (llama-cpp-python)

O sistema usa automaticamente o modo GGUF se o modelo e a biblioteca estiverem disponíveis, caso contrário, faz fallback para o modo simulado.

### Métricas para Avaliar Qualidade do Modelo GGUF

Para avaliar objetivamente o desempenho do modelo GGUF comparado à simulação, recomendamos focar nas seguintes métricas:

1. **Relevância do Contexto**: Como o modelo incorpora os dados do aluno na resposta
2. **Precisão Factual**: Correção das informações apresentadas
3. **Riqueza de Resposta**: Nível de detalhe e completude
4. **Tempo de Resposta**: Latência de processamento
5. **Consistência**: Variação na qualidade entre diferentes tipos de consultas

### Parâmetros de Configuração do Modelo

O modelo GGUF pode ser ajustado através dos seguintes parâmetros na função `Llama()`:

```python
llm_gguf = llama_cpp.Llama(
    model_path=model_path,
    n_ctx=4096,        # Tamanho do contexto (ajustável entre 2048 - 8192)
    n_threads=4,       # Número de threads (ajuste conforme CPU disponível)
    n_batch=512,       # Tamanho do lote para processamento
    verbose=False      # Modo verboso para debugging
)
```

Para gerar respostas, você pode ajustar:

```python
output = llm_gguf(
    prompt,
    max_tokens=500,     # Número máximo de tokens na resposta
    stop=["<|end|>"],   # Sequências para interromper a geração
    temperature=0.7,    # Maior valor = mais criativo, menor = mais determinístico
    echo=False          # Se deve incluir o prompt na saída
)
```

### Próximos Passos para Melhorias

1. **Otimização de Prompts**: Refinar o sistema de prompts para melhor aproveitar as capacidades do modelo
2. **Quantização Otimizada**: Experimentar diferentes níveis de quantização (q8_0, q4_0, q4_K_M)
3. **Suporte a GPU**: Habilitar aceleração via CUDA para melhor desempenho
4. **Cache de KV**: Implementar cache de key-value para acelerar respostas em conversas longas
5. **Testes Comparativos**: Desenvolver testes automatizados para comparar desempenho com outros modelos 