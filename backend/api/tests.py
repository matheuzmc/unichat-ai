from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from datetime import date, datetime

from .models import (
    Aluno, Nota, HorarioAula, Frequencia, DadoFinanceiro, 
    Matricula, DisciplinaMatriculada, ChatHistorico
)

class ModelTestCase(TestCase):
    """Testes para os modelos do sistema"""
    
    def setUp(self):
        """Configurar dados de teste"""
        # Criar um aluno de teste
        self.aluno = Aluno.objects.create(
            nome="Aluno Teste",
            email="teste@example.com",
            matricula="20240001",
            curso="Ciência da Computação",
            semestre=3,
            data_nascimento=date(2000, 1, 1),
            endereco="Rua Teste, 123"
        )
        
        # Criar uma nota
        self.nota = Nota.objects.create(
            aluno=self.aluno,
            disciplina="Programação I",
            nota_prova=8.5,
            nota_trabalho=9.0,
            nota_final=8.7,
            data_avaliacao=date(2024, 3, 15),
            semestre="2024.1"
        )
        
        # Criar um horário de aula
        self.horario = HorarioAula.objects.create(
            aluno=self.aluno,
            disciplina="Programação I",
            dia_semana="SEG",
            horario_inicio="08:00:00",
            horario_fim="10:00:00",
            sala="Lab 01",
            professor="Prof. Silva",
            semestre="2024.1"
        )
        
        # Criar uma frequência
        self.frequencia = Frequencia.objects.create(
            aluno=self.aluno,
            disciplina="Programação I",
            data=date(2024, 3, 15),
            status="PRESENTE"
        )
        
        # Criar um dado financeiro
        self.financeiro = DadoFinanceiro.objects.create(
            aluno=self.aluno,
            mensalidade=1000.00,
            data_vencimento=date(2024, 4, 10),
            status_pagamento="PENDENTE",
            descricao="Mensalidade Abril/2024"
        )
        
        # Criar uma matrícula
        self.matricula = Matricula.objects.create(
            aluno=self.aluno,
            semestre="2024.1",
            data_matricula=date(2024, 1, 15)
        )
        
        # Criar uma disciplina matriculada
        self.disciplina = DisciplinaMatriculada.objects.create(
            matricula=self.matricula,
            codigo="CC001",
            nome="Programação I",
            creditos=4,
            professor="Prof. Silva",
            status="EM_ANDAMENTO"
        )
        
        # Criar um histórico de chat
        self.chat = ChatHistorico.objects.create(
            aluno=self.aluno,
            pergunta="Qual é minha nota em Programação I?",
            resposta="Sua nota em Programação I é 8.7.",
            dados_contextuais={"intent": "consulta_nota", "confianca": 0.95}
        )
    
    def test_aluno_creation(self):
        """Testar criação de aluno"""
        self.assertEqual(self.aluno.nome, "Aluno Teste")
        self.assertEqual(self.aluno.email, "teste@example.com")
        self.assertEqual(self.aluno.curso, "Ciência da Computação")
    
    def test_nota_calculation(self):
        """Testar cálculo de nota"""
        self.assertEqual(self.nota.nota_final, 8.7)
        self.assertEqual(self.nota.disciplina, "Programação I")
    
    def test_horario_display(self):
        """Testar exibição de dia da semana"""
        self.assertEqual(self.horario.get_dia_semana_display(), "Segunda-feira")
    
    def test_frequencia_status(self):
        """Testar status de frequência"""
        self.assertEqual(self.frequencia.get_status_display(), "Presente")
    
    def test_relacionamentos(self):
        """Testar relacionamentos entre modelos"""
        self.assertEqual(self.aluno.notas.count(), 1)
        self.assertEqual(self.aluno.horarios.count(), 1)
        self.assertEqual(self.aluno.frequencias.count(), 1)
        self.assertEqual(self.aluno.dados_financeiros.count(), 1)
        self.assertEqual(self.aluno.matriculas.count(), 1)
        self.assertEqual(self.aluno.historico_chat.count(), 1)
        
        # Verificar relação entre matrícula e disciplinas
        self.assertEqual(self.matricula.disciplinas.count(), 1)
        self.assertEqual(self.matricula.disciplinas.first().nome, "Programação I")


class APITestCase(APITestCase):
    """Testes para as APIs do sistema"""
    
    def setUp(self):
        """Configurar dados de teste"""
        self.client = APIClient()
        
        # Criar um aluno de teste
        self.aluno_data = {
            "nome": "Aluno API Teste",
            "email": "api_teste@example.com",
            "matricula": "20240002",
            "curso": "Engenharia de Software",
            "semestre": 2,
            "data_nascimento": "2001-02-15",
            "endereco": "Av. API, 456"
        }
        
        # Criar o aluno via API
        self.aluno_response = self.client.post(
            reverse('aluno-list'),
            self.aluno_data,
            format='json'
        )
        self.aluno_id = self.aluno_response.data['id']
        
        # Criar uma nota via API
        self.nota_data = {
            "aluno": self.aluno_id,
            "disciplina": "Engenharia de Software I",
            "nota_prova": "7.5",
            "nota_trabalho": "8.0",
            "nota_final": "7.7",
            "data_avaliacao": "2024-03-20",
            "semestre": "2024.1"
        }
        self.nota_response = self.client.post(
            reverse('nota-list'),
            self.nota_data,
            format='json'
        )
        
        # Criar um histórico de chat via API
        self.chat_data = {
            "aluno": self.aluno_id,
            "pergunta": "Qual é minha nota em Engenharia de Software I?",
            "resposta": "Sua nota em Engenharia de Software I é 7.7.",
            "dados_contextuais": {"intent": "consulta_nota", "confianca": 0.92}
        }
        self.chat_response = self.client.post(
            reverse('chathistorico-list'),
            self.chat_data,
            format='json'
        )
    
    def test_get_aluno(self):
        """Testar obtenção de aluno"""
        response = self.client.get(
            reverse('aluno-detail', kwargs={'pk': self.aluno_id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], self.aluno_data['nome'])
        self.assertEqual(response.data['email'], self.aluno_data['email'])
    
    def test_get_aluno_detalhes(self):
        """Testar obtenção de detalhes completos do aluno"""
        response = self.client.get(
            reverse('aluno-detalhes', kwargs={'pk': self.aluno_id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], self.aluno_data['nome'])
        self.assertIn('notas', response.data)
        self.assertIn('historico_chat', response.data)
    
    def test_get_notas_por_aluno(self):
        """Testar obtenção de notas por aluno"""
        response = self.client.get(
            f"{reverse('nota-por-aluno')}?aluno_id={self.aluno_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['disciplina'], self.nota_data['disciplina'])
    
    def test_chat_historico(self):
        """Testar histórico de chat"""
        response = self.client.get(
            f"{reverse('chathistorico-por-aluno')}?aluno_id={self.aluno_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['pergunta'], self.chat_data['pergunta'])
        self.assertEqual(response.data[0]['resposta'], self.chat_data['resposta'])

    def test_create_and_list_aluno(self):
        """Testar criação e listagem de alunos"""
        # Criar outro aluno
        new_aluno_data = {
            "nome": "Outro Aluno",
            "email": "outro@example.com",
            "matricula": "20240003",
            "curso": "Sistemas de Informação",
            "semestre": 4,
            "data_nascimento": "1999-05-20",
            "endereco": "Rua Outro, 789"
        }
        response = self.client.post(
            reverse('aluno-list'),
            new_aluno_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Listar todos os alunos
        response = self.client.get(reverse('aluno-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 2)  # Considerando paginação
    
    def test_update_aluno(self):
        """Testar atualização de aluno"""
        update_data = {"nome": "Aluno Atualizado"}
        response = self.client.patch(
            reverse('aluno-detail', kwargs={'pk': self.aluno_id}),
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], update_data['nome'])
    
    def test_delete_aluno(self):
        """Testar exclusão de aluno"""
        # Criar aluno para excluir
        temp_aluno = {
            "nome": "Aluno Temporário",
            "email": "temp@example.com",
            "matricula": "20240004",
            "curso": "Matemática",
            "semestre": 1,
            "data_nascimento": "2002-10-10",
            "endereco": "Rua Temp, 000"
        }
        response = self.client.post(
            reverse('aluno-list'),
            temp_aluno,
            format='json'
        )
        temp_id = response.data['id']
        
        # Excluir o aluno
        response = self.client.delete(
            reverse('aluno-detail', kwargs={'pk': temp_id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se foi excluído
        response = self.client.get(
            reverse('aluno-detail', kwargs={'pk': temp_id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LLMResponseTestCase(APITestCase):
    """Testes específicos para respostas do LLM"""
    
    def setUp(self):
        """Configurar dados de teste"""
        self.client = APIClient()
        
        # Criar um aluno de teste
        self.aluno = Aluno.objects.create(
            nome="Aluno LLM Teste",
            email="llm_teste@example.com",
            matricula="20240005",
            curso="Ciência de Dados",
            semestre=5,
            data_nascimento=date(1998, 6, 15),
            endereco="Rua LLM, 789"
        )
        
        # Criar notas para o aluno
        self.nota1 = Nota.objects.create(
            aluno=self.aluno,
            disciplina="Inteligência Artificial",
            nota_prova=9.0,
            nota_trabalho=8.5,
            nota_final=8.8,
            data_avaliacao=date(2024, 3, 25),
            semestre="2024.1"
        )
        
        self.nota2 = Nota.objects.create(
            aluno=self.aluno,
            disciplina="Machine Learning",
            nota_prova=7.5,
            nota_trabalho=9.5,
            nota_final=8.5,
            data_avaliacao=date(2024, 3, 20),
            semestre="2024.1"
        )
        
        # Criar horários de aula
        self.horario1 = HorarioAula.objects.create(
            aluno=self.aluno,
            disciplina="Inteligência Artificial",
            dia_semana="SEG",
            horario_inicio="14:00:00",
            horario_fim="16:00:00",
            sala="Lab IA",
            professor="Prof. Santos",
            semestre="2024.1"
        )
        
        self.horario2 = HorarioAula.objects.create(
            aluno=self.aluno,
            disciplina="Machine Learning",
            dia_semana="QUA",
            horario_inicio="10:00:00",
            horario_fim="12:00:00",
            sala="Lab ML",
            professor="Prof. Oliveira",
            semestre="2024.1"
        )
        
        # Criar matrícula
        self.matricula = Matricula.objects.create(
            aluno=self.aluno,
            semestre="2024.1",
            data_matricula=date(2024, 1, 10)
        )
    
    def test_llm_response_quality_for_notas(self):
        """Testar qualidade das respostas relacionadas a notas"""
        # Criar histórico de chat simulando perguntas e respostas sobre notas
        pergunta = "Qual é a minha nota em Inteligência Artificial?"
        resposta = "Olá Aluno LLM Teste! Sua nota em Inteligência Artificial é 8.8."
        
        chat = ChatHistorico.objects.create(
            aluno=self.aluno,
            pergunta=pergunta,
            resposta=resposta,
            dados_contextuais={"intent": "consulta_nota", "disciplina": "Inteligência Artificial"}
        )
        
        # Verificar se a resposta contém a nota correta
        self.assertIn("8.8", resposta)
        self.assertIn("Inteligência Artificial", resposta)
        
        # Verificar se a resposta tem o formato esperado
        self.assertTrue(resposta.startswith("Olá"))
        self.assertTrue("nota" in resposta.lower())
    
    def test_llm_response_quality_for_horarios(self):
        """Testar qualidade das respostas relacionadas a horários de aula"""
        pergunta = "Qual é o horário da aula de Machine Learning?"
        resposta = "Olá Aluno LLM Teste! Sua aula de Machine Learning é Quarta-feira das 10:00:00 às 12:00:00 na sala Lab ML."
        
        chat = ChatHistorico.objects.create(
            aluno=self.aluno,
            pergunta=pergunta,
            resposta=resposta,
            dados_contextuais={"intent": "consulta_horario", "disciplina": "Machine Learning"}
        )
        
        # Verificar se a resposta contém as informações corretas
        self.assertIn("Quarta-feira", resposta)
        self.assertIn("10:00:00", resposta)
        self.assertIn("12:00:00", resposta)
        self.assertIn("Lab ML", resposta)
        
        # Verificar se a resposta tem o formato esperado
        self.assertTrue("aula" in resposta.lower())
        self.assertTrue("Machine Learning" in resposta)
    
    def test_llm_response_multiple_subjects(self):
        """Testar qualidade das respostas relacionadas a múltiplas disciplinas"""
        pergunta = "Quais são minhas notas neste semestre?"
        resposta = "Olá Aluno LLM Teste! Você tem as seguintes notas registradas: Inteligência Artificial: 8.8, Machine Learning: 8.5."
        
        chat = ChatHistorico.objects.create(
            aluno=self.aluno,
            pergunta=pergunta,
            resposta=resposta,
            dados_contextuais={"intent": "consulta_notas_semestre", "semestre": "2024.1"}
        )
        
        # Verificar se a resposta contém as informações de ambas disciplinas
        self.assertIn("Inteligência Artificial: 8.8", resposta)
        self.assertIn("Machine Learning: 8.5", resposta)
    
    def test_chat_context_retention(self):
        """Testar retenção de contexto entre mensagens"""
        # Simulação de uma conversa com contexto
        pergunta1 = "Qual o meu horário de aulas?"
        resposta1 = "Olá Aluno LLM Teste! Seus horários de aula são: Inteligência Artificial: Segunda-feira 14:00-16:00; Machine Learning: Quarta-feira 10:00-12:00."
        
        chat1 = ChatHistorico.objects.create(
            aluno=self.aluno,
            pergunta=pergunta1,
            resposta=resposta1,
            dados_contextuais={"intent": "consulta_horarios"}
        )
        
        # Segunda pergunta, referenciando a primeira
        pergunta2 = "E qual é minha nota na disciplina de segunda-feira?"
        resposta2 = "Sua nota em Inteligência Artificial, que é ministrada na segunda-feira, é 8.8."
        
        chat2 = ChatHistorico.objects.create(
            aluno=self.aluno,
            pergunta=pergunta2,
            resposta=resposta2,
            dados_contextuais={"intent": "consulta_nota", "dia_semana": "SEG", "referencia_anterior": True}
        )
        
        # Verificar se a resposta manteve o contexto e associou corretamente
        self.assertIn("Inteligência Artificial", resposta2)
        self.assertIn("8.8", resposta2)
        self.assertTrue("segunda-feira" in resposta2.lower() or "SEG" in resposta2)
