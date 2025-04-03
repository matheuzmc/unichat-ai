from rest_framework import serializers
from .models import (
    Aluno, Nota, HorarioAula, Frequencia, DadoFinanceiro, 
    Matricula, DisciplinaMatriculada, ChatHistorico
)

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class NotaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    
    class Meta:
        model = Nota
        fields = '__all__'
        
class HorarioAulaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    dia_semana_display = serializers.CharField(source='get_dia_semana_display', read_only=True)
    
    class Meta:
        model = HorarioAula
        fields = '__all__'
        
class FrequenciaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Frequencia
        fields = '__all__'
        
class DadoFinanceiroSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    status_pagamento_display = serializers.CharField(source='get_status_pagamento_display', read_only=True)
    
    class Meta:
        model = DadoFinanceiro
        fields = '__all__'
        
class DisciplinaMatriculadaSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = DisciplinaMatriculada
        fields = '__all__'
        
class MatriculaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    disciplinas = DisciplinaMatriculadaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Matricula
        fields = '__all__'
        
class ChatHistoricoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    
    class Meta:
        model = ChatHistorico
        fields = '__all__'
        
class AlunoDetalhadoSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir detalhes completos de um aluno, incluindo dados relacionados
    """
    notas = NotaSerializer(many=True, read_only=True)
    horarios = HorarioAulaSerializer(many=True, read_only=True)
    frequencias = FrequenciaSerializer(many=True, read_only=True)
    dados_financeiros = DadoFinanceiroSerializer(many=True, read_only=True)
    matriculas = MatriculaSerializer(many=True, read_only=True)
    historico_chat = ChatHistoricoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Aluno
        fields = '__all__' 