from django.core.management.base import BaseCommand
import requests
import json
from django.conf import settings
import re
import time
import datetime
from django.utils import timezone
from api.models import Aluno, Nota, HorarioAula, ChatHistorico
from .testes_prontos import TESTES_CONSULTAS, CAPACIDADES_LLMS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import os

class Command(BaseCommand):
    help = 'Executa testes avançados nas respostas do serviço LLM usando casos de teste predefinidos'
    
    def add_arguments(self, parser):
        parser.add_argument('--aluno_id', type=int, help='ID específico do aluno para testar')
        parser.add_argument('--categoria', type=str, help='Categoria específica de testes para executar (notas, horarios, info_geral, complexa, conversacao)')
        parser.add_argument('--verbose', action='store_true', help='Exibir detalhes dos testes')
        parser.add_argument('--gerar_relatorio', action='store_true', help='Gerar relatório em formato CSV e gráficos')
        parser.add_argument('--testar_capacidades', action='store_true', help='Testar capacidades específicas do LLM')
    
    def handle(self, *args, **options):
        self.verbose = options.get('verbose', False)
        self.gerar_relatorio = options.get('gerar_relatorio', False)
        self.resultados = []
        self.llm_url = "http://llm:8080/api/query"
        
        # Define ou obtém o aluno para teste
        aluno_id = options.get('aluno_id')
        if aluno_id:
            try:
                self.aluno = Aluno.objects.get(id=aluno_id)
            except Aluno.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Aluno com ID {aluno_id} não encontrado'))
                return
        else:
            # Usa o primeiro aluno disponível
            self.aluno = Aluno.objects.first()
            if not self.aluno:
                self.stdout.write(self.style.ERROR('Nenhum aluno encontrado no banco de dados'))
                return
        
        self.stdout.write(self.style.WARNING(f'Testando respostas do LLM para o aluno: {self.aluno.nome}'))
        
        # Filtra por categoria se especificado
        categoria = options.get('categoria')
        if categoria:
            testes_filtrados = [t for t in TESTES_CONSULTAS if t.get('categoria') == categoria]
            if not testes_filtrados:
                self.stdout.write(self.style.ERROR(f'Categoria {categoria} não encontrada'))
                return
            self.realizar_testes(testes_filtrados)
        else:
            # Realiza todos os testes
            self.realizar_testes(TESTES_CONSULTAS)
        
        # Teste de capacidades específicas do LLM
        if options.get('testar_capacidades'):
            self.stdout.write(self.style.WARNING('Testando capacidades específicas do LLM'))
            self.testar_capacidades()
        
        # Gerar relatório se solicitado
        if self.gerar_relatorio:
            self.gerar_relatorio_testes()
        
        self.stdout.write(self.style.SUCCESS('Testes de qualidade das respostas do LLM concluídos'))
    
    def realizar_testes(self, testes):
        """Executa todos os testes especificados"""
        total_testes = len(testes)
        testes_passados = 0
        
        for i, teste in enumerate(testes, 1):
            categoria = teste.get('categoria')
            self.stdout.write(self.style.WARNING(f'Executando teste {i}/{total_testes} - Categoria: {categoria}'))
            
            # Executa teste conforme sua categoria
            if categoria == 'conversacao':
                resultado = self.testar_conversacao(teste)
            else:
                resultado = self.testar_consulta_simples(teste)
            
            # Atualiza contadores
            if resultado:
                testes_passados += 1
            
            # Adiciona aos resultados
            self.resultados.append({
                'teste_id': i,
                'categoria': categoria,
                'pergunta': teste.get('pergunta', teste.get('pergunta_inicial', 'N/A')),
                'resultado': 'PASSOU' if resultado else 'FALHOU',
                'data': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        taxa_sucesso = (testes_passados / total_testes) * 100 if total_testes > 0 else 0
        self.stdout.write(self.style.SUCCESS(f'Taxa de sucesso: {taxa_sucesso:.2f}% ({testes_passados}/{total_testes})'))
    
    def testar_consulta_simples(self, teste):
        """Testa uma consulta simples"""
        pergunta = teste.get('pergunta')
        termos_esperados = teste.get('termos_esperados', [])
        contexto_necessario = teste.get('contexto_necessario', False)
        
        # Se precisar de contexto, verificar o tipo
        if contexto_necessario:
            tipo_contexto = teste.get('contexto')
            if tipo_contexto == 'data_atual':
                # Adicionar contexto de data na pergunta
                hoje = datetime.datetime.now()
                dia_semana = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo'][hoje.weekday()]
                pergunta = f"Hoje é {dia_semana}, {hoje.day}/{hoje.month}. {pergunta}"
        
        # Enviar consulta ao LLM
        resposta = self.send_query_to_llm(pergunta)
        
        if self.verbose:
            self.stdout.write(f"Pergunta: {pergunta}")
            self.stdout.write(f"Resposta: {resposta}")
            self.stdout.write(f"Termos esperados: {termos_esperados}")
        
        # Verificar se a resposta contém os termos esperados
        resultado = self.verify_response(resposta, termos_esperados)
        self.report_result(f"Consulta: '{pergunta}'", resultado)
        
        return resultado
    
    def testar_conversacao(self, teste):
        """Testa uma sequência de conversação"""
        pergunta_inicial = teste.get('pergunta_inicial')
        pergunta_sequencia = teste.get('pergunta_sequencia')
        termos_esperados = teste.get('termos_esperados', [])
        
        # Passo 1: Enviar primeira pergunta para criar contexto
        resposta_inicial = self.send_query_to_llm(pergunta_inicial)
        
        if self.verbose:
            self.stdout.write(f"Pergunta inicial: {pergunta_inicial}")
            self.stdout.write(f"Resposta inicial: {resposta_inicial}")
        
        # Salvar o histórico para criar contexto
        ChatHistorico.objects.create(
            aluno=self.aluno,
            pergunta=pergunta_inicial,
            resposta=resposta_inicial
        )
        
        # Passo 2: Enviar pergunta de sequência
        resposta_sequencia = self.send_query_to_llm(pergunta_sequencia)
        
        if self.verbose:
            self.stdout.write(f"Pergunta sequência: {pergunta_sequencia}")
            self.stdout.write(f"Resposta sequência: {resposta_sequencia}")
            self.stdout.write(f"Termos esperados: {termos_esperados}")
        
        # Verificar se a resposta contém os termos esperados
        resultado = self.verify_response(resposta_sequencia, termos_esperados)
        self.report_result(f"Conversação: '{pergunta_inicial}' seguido de '{pergunta_sequencia}'", resultado)
        
        return resultado
    
    def testar_capacidades(self):
        """Testa capacidades específicas do LLM"""
        capacidades_passadas = 0
        
        for i, capacidade in enumerate(CAPACIDADES_LLMS, 1):
            nome_capacidade = capacidade.get('capacidade')
            descricao = capacidade.get('descricao')
            pergunta = capacidade.get('pergunta')
            verificacao = capacidade.get('verificacao')
            
            self.stdout.write(self.style.WARNING(f'Testando capacidade {i}/{len(CAPACIDADES_LLMS)}: {nome_capacidade}'))
            self.stdout.write(f'Descrição: {descricao}')
            
            # Enviar consulta ao LLM
            resposta = self.send_query_to_llm(pergunta)
            
            if self.verbose:
                self.stdout.write(f"Pergunta: {pergunta}")
                self.stdout.write(f"Resposta: {resposta}")
            
            # Verificar a resposta usando a função de verificação específica
            resultado = verificacao(resposta) if resposta else False
            
            if resultado:
                capacidades_passadas += 1
            
            self.report_result(f"Capacidade: {nome_capacidade}", resultado)
            
            # Adiciona aos resultados
            self.resultados.append({
                'teste_id': f'C{i}',
                'categoria': 'capacidade',
                'pergunta': pergunta,
                'resultado': 'PASSOU' if resultado else 'FALHOU',
                'data': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
        taxa_sucesso = (capacidades_passadas / len(CAPACIDADES_LLMS)) * 100 if CAPACIDADES_LLMS else 0
        self.stdout.write(self.style.SUCCESS(f'Taxa de sucesso em capacidades: {taxa_sucesso:.2f}% ({capacidades_passadas}/{len(CAPACIDADES_LLMS)})'))
    
    def send_query_to_llm(self, question):
        """Envia uma consulta para o serviço LLM e retorna a resposta"""
        try:
            payload = {
                "question": question,
                "student_id": self.aluno.id
            }
            
            # Adicionar tempo de espera entre as consultas para não sobrecarregar o serviço
            time.sleep(0.5)
            
            response = requests.post(self.llm_url, json=payload)
            
            if response.status_code == 200:
                return response.json().get("answer", "")
            else:
                self.stdout.write(self.style.ERROR(f"Erro ao consultar LLM: {response.status_code}"))
                return ""
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Exceção ao consultar LLM: {str(e)}"))
            return ""
    
    def verify_response(self, response, expected_terms):
        """Verifica se a resposta contém os termos esperados"""
        result = True
        for term in expected_terms:
            if term.lower() not in response.lower():
                if self.verbose:
                    self.stdout.write(self.style.ERROR(f"Termo não encontrado na resposta: {term}"))
                result = False
        return result
    
    def report_result(self, test_name, success):
        """Reporta o resultado de um teste"""
        if success:
            self.stdout.write(self.style.SUCCESS(f"✅ PASSOU: {test_name}"))
        else:
            self.stdout.write(self.style.ERROR(f"❌ FALHOU: {test_name}"))
    
    def gerar_relatorio_testes(self):
        """Gera relatório dos testes realizados"""
        if not self.resultados:
            self.stdout.write(self.style.WARNING('Nenhum resultado de teste para gerar relatório'))
            return
        
        # Criar diretório para relatórios se não existir
        relatorio_dir = os.path.join(settings.BASE_DIR, 'relatorios_llm')
        os.makedirs(relatorio_dir, exist_ok=True)
        
        # Nome do arquivo com timestamp
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = os.path.join(relatorio_dir, f'relatorio_testes_llm_{timestamp}.csv')
        
        # Criar DataFrame e salvar CSV
        df = pd.DataFrame(self.resultados)
        df.to_csv(csv_filename, index=False)
        self.stdout.write(self.style.SUCCESS(f'Relatório CSV salvo em: {csv_filename}'))
        
        # Gerar gráficos
        self.gerar_graficos(df, relatorio_dir, timestamp)
    
    def gerar_graficos(self, df, relatorio_dir, timestamp):
        """Gera gráficos com base nos resultados dos testes"""
        try:
            # Configuração inicial
            plt.figure(figsize=(10, 6))
            
            # Gráfico 1: Taxa de sucesso por categoria
            categoria_stats = df.groupby('categoria')['resultado'].apply(
                lambda x: (x == 'PASSOU').mean() * 100
            ).reset_index()
            
            plt.figure(figsize=(10, 6))
            bars = plt.bar(categoria_stats['categoria'], categoria_stats['resultado'], color='skyblue')
            
            # Adicionar valores percentuais acima das barras
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{height:.1f}%',
                        ha='center', va='bottom')
            
            plt.title('Taxa de Sucesso por Categoria')
            plt.xlabel('Categoria')
            plt.ylabel('Taxa de Sucesso (%)')
            plt.ylim(0, 105)  # Limite y para deixar espaço para os rótulos
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Salvar gráfico
            grafico_path = os.path.join(relatorio_dir, f'grafico_categorias_{timestamp}.png')
            plt.savefig(grafico_path)
            self.stdout.write(self.style.SUCCESS(f'Gráfico de categorias salvo em: {grafico_path}'))
            
            # Gráfico 2: Resumo geral
            plt.figure(figsize=(8, 8))
            resultados_count = df['resultado'].value_counts()
            colors = ['#4CAF50', '#F44336'] if 'PASSOU' in resultados_count.index else ['#F44336']
            
            plt.pie(resultados_count, labels=resultados_count.index, autopct='%1.1f%%',
                   colors=colors, startangle=90)
            plt.title('Distribuição dos Resultados dos Testes')
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            
            # Salvar gráfico
            grafico_pie_path = os.path.join(relatorio_dir, f'grafico_resultados_{timestamp}.png')
            plt.savefig(grafico_pie_path)
            self.stdout.write(self.style.SUCCESS(f'Gráfico de resultados salvo em: {grafico_pie_path}'))
            
            plt.close('all')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao gerar gráficos: {str(e)}')) 