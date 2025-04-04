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