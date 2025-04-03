# Melhorias Futuras para o Backend do UniChat

Este documento detalha as melhorias sugeridas para o backend do UniChat que podem ser implementadas após o MVP para tornar a API mais robusta, eficiente e fácil de manter.

## 1. Serializadores

### 1.1. Validação Personalizada de Campos
```python
class NotaSerializer(serializers.ModelSerializer):
    # Exemplo de validação personalizada
    def validate_nota_final(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("A nota deve estar entre 0 e 10.")
        return value
    
    def validate(self, data):
        # Validação envolvendo múltiplos campos
        if data['nota_prova'] > data['nota_final'] or data['nota_trabalho'] > data['nota_final']:
            raise serializers.ValidationError("A nota final não pode ser menor que as notas parciais.")
        return data
    
    class Meta:
        model = Nota
        fields = '__all__'
```

### 1.2. Serializadores Específicos para Criação e Atualização
```python
class AlunoCreateSerializer(serializers.ModelSerializer):
    # Campos específicos para criação
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Aluno
        exclude = ['created_at', 'updated_at']
        
class AlunoUpdateSerializer(serializers.ModelSerializer):
    # Campos específicos para atualização
    class Meta:
        model = Aluno
        exclude = ['created_at', 'updated_at', 'matricula']  # Impedir alteração da matrícula
```

### 1.3. Serializadores para Consultas Específicas
```python
class AlunoListSerializer(serializers.ModelSerializer):
    # Versão simplificada para listagem
    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'matricula', 'curso', 'semestre']
        
# Use no ViewSet:
def get_serializer_class(self):
    if self.action == 'list':
        return AlunoListSerializer
    return AlunoSerializer
```

### 1.4. Otimização de Serializadores Aninhados
```python
class AlunoDetalhadoSerializer(serializers.ModelSerializer):
    # Limitando o número de itens retornados para relações aninhadas
    notas = serializers.SerializerMethodField()
    historico_chat = serializers.SerializerMethodField()
    
    def get_notas(self, obj):
        # Retornar apenas as 10 notas mais recentes
        notas = obj.notas.order_by('-data_avaliacao')[:10]
        return NotaSerializer(notas, many=True).data
        
    def get_historico_chat(self, obj):
        # Retornar apenas as 20 mensagens mais recentes
        historico = obj.historico_chat.order_by('-timestamp')[:20]
        return ChatHistoricoSerializer(historico, many=True).data
    
    class Meta:
        model = Aluno
        fields = '__all__'
```

### 1.5. Métodos de Representação Personalizada
```python
class NotaSerializer(serializers.ModelSerializer):
    situacao = serializers.SerializerMethodField()
    
    def get_situacao(self, obj):
        if obj.nota_final >= 7.0:
            return "Aprovado"
        elif obj.nota_final >= 5.0:
            return "Em recuperação"
        else:
            return "Reprovado"
            
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Adicionando campos calculados
        representation['media_turma'] = calculate_media_turma(instance.disciplina, instance.semestre)
        return representation
```

### 1.6. Controle de Permissões por Campo
```python
class DadoFinanceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadoFinanceiro
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context['request'].user
        
        # Remover campos sensíveis para usuários não administrativos
        if not user.is_staff:
            representation.pop('valor_pago', None)
            representation.pop('data_pagamento', None)
        
        return representation
```

### 1.7. Hyperlinked Relations
```python
class HorarioAulaSerializer(serializers.HyperlinkedModelSerializer):
    aluno = serializers.HyperlinkedRelatedField(
        view_name='aluno-detail',
        read_only=True
    )
    
    class Meta:
        model = HorarioAula
        fields = '__all__'
```

## 2. ViewSets e Performance

### 2.1. Cache para Desempenho
```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class AlunoViewSet(viewsets.ModelViewSet):
    # Cache para métodos de leitura
    @method_decorator(cache_page(60 * 15))  # Cache por 15 minutos
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
```

### 2.2. Otimização de Consultas com Select Related e Prefetch Related
```python
class NotaViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Nota.objects.select_related('aluno').all()
        
class MatriculaViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Matricula.objects.select_related('aluno').prefetch_related('disciplinas').all()
```

### 2.3. Paginação Customizada
```python
from rest_framework.pagination import PageNumberPagination

class LargePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500

class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

# Aplicar no ViewSet:
class ChatHistoricoViewSet(viewsets.ModelViewSet):
    pagination_class = SmallPagination
```

## 3. Autenticação e Segurança

### 3.1. Implementação de JWT (JSON Web Tokens)
```python
# settings.py
INSTALLED_APPS = [
    # ... apps existentes
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ... URLs existentes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### 3.2. Permissões Personalizadas
```python
from rest_framework.permissions import BasePermission

class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permitir acesso se o usuário é o dono do objeto ou é um administrador
        return obj.aluno.user == request.user or request.user.is_staff

# Aplicar no ViewSet:
class DadoFinanceiroViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrStaff]
```

### 3.3. Rate Limiting
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

## 4. Manutenção e Qualidade de Código

### 4.1. Testes Automatizados
```python
from rest_framework.test import APITestCase

class AlunoAPITests(APITestCase):
    def setUp(self):
        # Configuração de dados de teste
        self.aluno = Aluno.objects.create(
            nome="Aluno Teste",
            email="teste@example.com",
            # ... outros campos
        )
        
    def test_get_aluno_list(self):
        url = '/api/alunos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
```

### 4.2. Documentação com Swagger/OpenAPI
```python
# settings.py
INSTALLED_APPS = [
    # ... apps existentes
    'drf_yasg',
]

# urls.py
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="UniChat API",
      default_version='v1',
      description="API para o sistema UniChat",
   ),
   public=True,
)

urlpatterns = [
    # ... URLs existentes
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

### 4.3. Logging Estruturado
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'api_access.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 5. Escalabilidade

### 5.1. Implementação de Celery para Tarefas Assíncronas
```python
# tasks.py
from celery import shared_task

@shared_task
def gerar_relatorio_aluno(aluno_id):
    # Lógica para gerar relatório em background
    aluno = Aluno.objects.get(id=aluno_id)
    # ... processamento pesado
    return "Relatório gerado com sucesso"

# views.py
from .tasks import gerar_relatorio_aluno

class AlunoViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def gerar_relatorio(self, request, pk=None):
        task = gerar_relatorio_aluno.delay(pk)
        return Response({"task_id": task.id, "status": "Em processamento"})
```

### 5.2. Implementação de GraphQL
```python
# Adicionar graphene-django e configurar
import graphene
from graphene_django import DjangoObjectType

class AlunoType(DjangoObjectType):
    class Meta:
        model = Aluno

class Query(graphene.ObjectType):
    alunos = graphene.List(AlunoType)
    aluno = graphene.Field(AlunoType, id=graphene.Int())
    
    def resolve_alunos(self, info, **kwargs):
        return Aluno.objects.all()
        
    def resolve_aluno(self, info, id):
        return Aluno.objects.get(pk=id)

schema = graphene.Schema(query=Query)
```

Estas melhorias podem ser implementadas gradualmente conforme o projeto evolui além do MVP, priorizando aquelas que trarão maior benefício para os usuários e para a manutenção do sistema. 