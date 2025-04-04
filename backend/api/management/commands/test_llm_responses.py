from django.core.management.base import BaseCommand
import requests
import json
from django.conf import settings
import re
import time
from api.models import Aluno, Nota, HorarioAula, ChatHistorico

class Command(BaseCommand):
    help = 'Testa a qualidade das respostas do serviço LLM para diferentes tipos de consultas'
    
    def add_arguments(self, parser):
        parser.add_argument('--aluno_id', type=int, help='ID específico do aluno para testar')
        parser.add_argument('--disciplina', type=str, help='Nome específico da disciplina para testar')
        parser.add_argument('--verbose', action='store_true', help='Exibir detalhes dos testes')
    
    def handle(self, *args, **options):
        self.verbose = options.get('verbose', False)
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
        
        # Testes para diferentes cenários
        self.test_nota_queries()
        self.test_horario_queries()
        self.test_informacao_geral_queries()
        self.test_complex_queries()
        
        self.stdout.write(self.style.SUCCESS('Testes de qualidade das respostas do LLM concluídos'))
    
    def test_nota_queries(self):
        """Testa consultas relacionadas a notas"""
        self.stdout.write(self.style.WARNING('Testando consultas sobre notas'))
        
        # Obter disciplinas do aluno
        disciplinas = Nota.objects.filter(aluno=self.aluno).values_list('disciplina', flat=True).distinct()
        
        if not disciplinas:
            self.stdout.write(self.style.WARNING('Nenhuma nota encontrada para o aluno'))
            return
        
        # Teste 1: Consulta de nota específica
        disciplina = disciplinas[0]
        nota = Nota.objects.filter(aluno=self.aluno, disciplina=disciplina).first()
        
        query = f"Qual é a minha nota em {disciplina}?"
        response = self.send_query_to_llm(query)
        
        # Verificar se a resposta contém a nota correta
        expected_value = str(nota.nota_final)
        if self.verbose:
            self.stdout.write(f"Pergunta: {query}")
            self.stdout.write(f"Resposta: {response}")
            self.stdout.write(f"Valor esperado: {expected_value}")
        
        result = self.verify_response(response, [expected_value, disciplina, "nota"])
        self.report_result("Consulta de nota específica", result)
        
        # Teste 2: Consulta de todas as notas
        query = "Quais são todas as minhas notas?"
        response = self.send_query_to_llm(query)
        
        # Verificar se a resposta contém todas as disciplinas
        success = True
        for disciplina in disciplinas:
            if disciplina not in response:
                success = False
                if self.verbose:
                    self.stdout.write(self.style.ERROR(f"Disciplina não encontrada na resposta: {disciplina}"))
        
        if self.verbose:
            self.stdout.write(f"Pergunta: {query}")
            self.stdout.write(f"Resposta: {response}")
        
        self.report_result("Consulta de todas as notas", success)
    
    def test_horario_queries(self):
        """Testa consultas relacionadas a horários"""
        self.stdout.write(self.style.WARNING('Testando consultas sobre horários'))
        
        # Obter horários do aluno
        horarios = HorarioAula.objects.filter(aluno=self.aluno)
        
        if not horarios:
            self.stdout.write(self.style.WARNING('Nenhum horário encontrado para o aluno'))
            return
        
        # Teste 1: Consulta de horário específico
        horario = horarios.first()
        
        query = f"Qual é o horário da disciplina {horario.disciplina}?"
        response = self.send_query_to_llm(query)
        
        # Verificar se a resposta contém os dados corretos
        dia_semana = horario.get_dia_semana_display()
        hora_inicio = horario.horario_inicio
        sala = horario.sala
        
        if self.verbose:
            self.stdout.write(f"Pergunta: {query}")
            self.stdout.write(f"Resposta: {response}")
            self.stdout.write(f"Valores esperados: {dia_semana}, {hora_inicio}, {sala}")
        
        result = self.verify_response(response, [horario.disciplina, dia_semana, str(hora_inicio)[:5], sala])
        self.report_result("Consulta de horário específico", result)
        
        # Teste 2: Consulta por dia da semana
        query = f"Quais disciplinas eu tenho na {horario.get_dia_semana_display()}?"
        response = self.send_query_to_llm(query)
        
        if self.verbose:
            self.stdout.write(f"Pergunta: {query}")
            self.stdout.write(f"Resposta: {response}")
        
        result = self.verify_response(response, [horario.disciplina, dia_semana])
        self.report_result("Consulta de disciplinas por dia", result)
    
    def test_informacao_geral_queries(self):
        """Testa consultas de informações gerais sobre o aluno"""
        self.stdout.write(self.style.WARNING('Testando consultas sobre informações gerais'))
        
        # Teste 1: Consulta sobre o curso
        query = "Qual curso eu estou fazendo?"
        response = self.send_query_to_llm(query)
        
        if self.verbose:
            self.stdout.write(f"Pergunta: {query}")
            self.stdout.write(f"Resposta: {response}")
        
        result = self.verify_response(response, [self.aluno.curso])
        self.report_result("Consulta sobre curso", result)
        
        # Teste 2: Consulta sobre o semestre
        query = "Em qual semestre estou?"
        response = self.send_query_to_llm(query)
        
        if self.verbose:
            self.stdout.write(f"Pergunta: {query}")
            self.stdout.write(f"Resposta: {response}")
        
        result = self.verify_response(response, [str(self.aluno.semestre)])
        self.report_result("Consulta sobre semestre", result)
    
    def test_complex_queries(self):
        """Testa consultas mais complexas que requerem contexto ou raciocínio"""
        self.stdout.write(self.style.WARNING('Testando consultas complexas'))
        
        # Verificar se o aluno tem notas e horários para testar
        has_notas = Nota.objects.filter(aluno=self.aluno).exists()
        has_horarios = HorarioAula.objects.filter(aluno=self.aluno).exists()
        
        if not has_notas or not has_horarios:
            self.stdout.write(self.style.WARNING('Dados insuficientes para testes complexos'))
            return
        
        # Teste 1: Consulta que requer relacionar informações
        query = "Qual a minha nota na disciplina que tenho aula na segunda-feira?"
        response = self.send_query_to_llm(query)
        
        if self.verbose:
            self.stdout.write(f"Pergunta: {query}")
            self.stdout.write(f"Resposta: {response}")
        
        # Não podemos verificar valor específico, mas verificamos se parece razoável
        segunda_disciplinas = HorarioAula.objects.filter(
            aluno=self.aluno, 
            dia_semana="SEG"
        ).values_list('disciplina', flat=True)
        
        if segunda_disciplinas:
            disciplina = segunda_disciplinas[0]
            result = disciplina in response and "nota" in response.lower()
            self.report_result("Consulta relacionando disciplina e dia da semana", result)
        else:
            self.stdout.write(self.style.WARNING('Nenhuma disciplina na segunda-feira para testar'))
        
        # Teste 2: Consulta que requer memória/contexto
        context_query = "Quais são meus horários de aula?"
        context_response = self.send_query_to_llm(context_query)
        
        if self.verbose:
            self.stdout.write(f"Pergunta de contexto: {context_query}")
            self.stdout.write(f"Resposta de contexto: {context_response}")
        
        # Salvar para criar contexto
        ChatHistorico.objects.create(
            aluno=self.aluno,
            pergunta=context_query,
            resposta=context_response
        )
        
        # Consulta de follow-up que depende da anterior
        followup_query = "E qual é a minha nota na disciplina que tenho na quarta-feira?"
        response = self.send_query_to_llm(followup_query)
        
        if self.verbose:
            self.stdout.write(f"Pergunta de follow-up: {followup_query}")
            self.stdout.write(f"Resposta: {response}")
        
        quarta_disciplinas = HorarioAula.objects.filter(
            aluno=self.aluno, 
            dia_semana="QUA"
        ).values_list('disciplina', flat=True)
        
        if quarta_disciplinas:
            disciplina = quarta_disciplinas[0]
            result = disciplina in response and "nota" in response.lower()
            self.report_result("Consulta com contexto de conversa anterior", result)
        else:
            self.stdout.write(self.style.WARNING('Nenhuma disciplina na quarta-feira para testar'))
    
    def send_query_to_llm(self, question):
        """Envia uma consulta para o serviço LLM e retorna a resposta"""
        try:
            payload = {
                "question": question,
                "student_id": self.aluno.id
            }
            
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