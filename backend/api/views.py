from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Aluno, Nota, HorarioAula, Frequencia, DadoFinanceiro, 
    Matricula, DisciplinaMatriculada, ChatHistorico
)
from .serializers import (
    AlunoSerializer, NotaSerializer, HorarioAulaSerializer, 
    FrequenciaSerializer, DadoFinanceiroSerializer, MatriculaSerializer, 
    DisciplinaMatriculadaSerializer, ChatHistoricoSerializer, AlunoDetalhadoSerializer
)


class AlunoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar alunos
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['curso', 'semestre']
    search_fields = ['nome', 'matricula', 'email']
    ordering_fields = ['nome', 'matricula', 'semestre']
    
    @action(detail=True, methods=['get'])
    def detalhes(self, request, pk=None):
        """
        Endpoint para retornar detalhes completos de um aluno, incluindo todos os dados relacionados
        """
        aluno = self.get_object()
        serializer = AlunoDetalhadoSerializer(aluno)
        return Response(serializer.data)


class NotaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar notas
    """
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aluno', 'disciplina', 'semestre']
    search_fields = ['disciplina', 'aluno__nome']
    ordering_fields = ['data_avaliacao', 'nota_final']
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """
        Endpoint para filtrar notas por aluno usando query parameter
        """
        aluno_id = request.query_params.get('aluno_id', None)
        if aluno_id:
            notas = Nota.objects.filter(aluno__id=aluno_id)
            serializer = self.get_serializer(notas, many=True)
            return Response(serializer.data)
        return Response({"error": "Parâmetro aluno_id é necessário"}, status=400)


class HorarioAulaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar horários de aula
    """
    queryset = HorarioAula.objects.all()
    serializer_class = HorarioAulaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aluno', 'dia_semana', 'semestre']
    search_fields = ['disciplina', 'professor', 'sala']
    ordering_fields = ['dia_semana', 'horario_inicio']
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """
        Endpoint para filtrar horários por aluno usando query parameter
        """
        aluno_id = request.query_params.get('aluno_id', None)
        if aluno_id:
            horarios = HorarioAula.objects.filter(aluno__id=aluno_id)
            serializer = self.get_serializer(horarios, many=True)
            return Response(serializer.data)
        return Response({"error": "Parâmetro aluno_id é necessário"}, status=400)


class FrequenciaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar frequências
    """
    queryset = Frequencia.objects.all()
    serializer_class = FrequenciaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aluno', 'disciplina', 'status']
    search_fields = ['disciplina', 'aluno__nome']
    ordering_fields = ['data']
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """
        Endpoint para filtrar frequências por aluno usando query parameter
        """
        aluno_id = request.query_params.get('aluno_id', None)
        if aluno_id:
            frequencias = Frequencia.objects.filter(aluno__id=aluno_id)
            serializer = self.get_serializer(frequencias, many=True)
            return Response(serializer.data)
        return Response({"error": "Parâmetro aluno_id é necessário"}, status=400)


class DadoFinanceiroViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar dados financeiros
    """
    queryset = DadoFinanceiro.objects.all()
    serializer_class = DadoFinanceiroSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aluno', 'status_pagamento']
    search_fields = ['descricao', 'aluno__nome']
    ordering_fields = ['data_vencimento', 'mensalidade']
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """
        Endpoint para filtrar dados financeiros por aluno usando query parameter
        """
        aluno_id = request.query_params.get('aluno_id', None)
        if aluno_id:
            dados = DadoFinanceiro.objects.filter(aluno__id=aluno_id)
            serializer = self.get_serializer(dados, many=True)
            return Response(serializer.data)
        return Response({"error": "Parâmetro aluno_id é necessário"}, status=400)


class MatriculaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar matrículas
    """
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aluno', 'semestre']
    search_fields = ['aluno__nome', 'semestre']
    ordering_fields = ['data_matricula', 'semestre']
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """
        Endpoint para filtrar matrículas por aluno usando query parameter
        """
        aluno_id = request.query_params.get('aluno_id', None)
        if aluno_id:
            matriculas = Matricula.objects.filter(aluno__id=aluno_id)
            serializer = self.get_serializer(matriculas, many=True)
            return Response(serializer.data)
        return Response({"error": "Parâmetro aluno_id é necessário"}, status=400)


class DisciplinaMatriculadaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar disciplinas matriculadas
    """
    queryset = DisciplinaMatriculada.objects.all()
    serializer_class = DisciplinaMatriculadaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['matricula', 'status']
    search_fields = ['nome', 'codigo', 'professor']
    ordering_fields = ['nome', 'codigo']
    
    @action(detail=False, methods=['get'])
    def por_matricula(self, request):
        """
        Endpoint para filtrar disciplinas por matrícula usando query parameter
        """
        matricula_id = request.query_params.get('matricula_id', None)
        if matricula_id:
            disciplinas = DisciplinaMatriculada.objects.filter(matricula__id=matricula_id)
            serializer = self.get_serializer(disciplinas, many=True)
            return Response(serializer.data)
        return Response({"error": "Parâmetro matricula_id é necessário"}, status=400)


class ChatHistoricoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar histórico do chat
    """
    queryset = ChatHistorico.objects.all()
    serializer_class = ChatHistoricoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['aluno']
    search_fields = ['pergunta', 'resposta', 'aluno__nome']
    ordering_fields = ['-timestamp']
    
    @action(detail=False, methods=['get'])
    def por_aluno(self, request):
        """
        Endpoint para filtrar histórico de chat por aluno usando query parameter
        """
        aluno_id = request.query_params.get('aluno_id', None)
        if aluno_id:
            historico = ChatHistorico.objects.filter(aluno__id=aluno_id).order_by('-timestamp')
            serializer = self.get_serializer(historico, many=True)
            return Response(serializer.data)
        return Response({"error": "Parâmetro aluno_id é necessário"}, status=400)
