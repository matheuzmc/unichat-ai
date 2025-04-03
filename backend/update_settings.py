import os
import re

# Caminho para o arquivo settings.py
settings_path = 'config/settings.py'

# Ler o conteúdo atual do arquivo
with open(settings_path, 'r') as file:
    content = file.read()

# Substituir a configuração de DATABASE
db_config = '''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'unichat'),
        'USER': os.environ.get('POSTGRES_USER', 'unichat_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'unichat_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}
'''

# Substituir a configuração de SECRET_KEY
secret_key_config = '''
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'insecure-dev-key-do-not-use-in-production')
'''

# Substituir a configuração de DEBUG
debug_config = '''
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
'''

# Substituir a configuração de ALLOWED_HOSTS
allowed_hosts_config = '''
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
'''

# Adicionar import os no topo do arquivo se não existir
if "import os" not in content:
    content = "import os\n" + content

# Substituir configurações
content = re.sub(r"SECRET_KEY = .*", secret_key_config, content)
content = re.sub(r"DEBUG = .*", debug_config, content)
content = re.sub(r"ALLOWED_HOSTS = .*", allowed_hosts_config, content)
content = re.sub(r"DATABASES = .*?\}", db_config, content, flags=re.DOTALL)

# Escrever o conteúdo modificado de volta ao arquivo
with open(settings_path, 'w') as file:
    file.write(content)

print("Arquivo settings.py atualizado com sucesso!")