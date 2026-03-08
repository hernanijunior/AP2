#!/bin/bash
# === setup.sh ===
echo "=== MVP Diploma Digital UFMT ==="
pip install django
python3 manage.py makemigrations core
python3 manage.py migrate
python3 manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ufmt.br', 'ufmt2026')
    print('Superusuário criado: admin / ufmt2026')
"
python3 manage.py shell -c "
from core.models import Programa, Orientador, Aluno, Defesa, Diploma
from datetime import date
import uuid

p, _ = Programa.objects.get_or_create(
    codigo_sucupira='40001016001P0',
    defaults={
        'nome': 'Programa de Pós-Graduação em Ciência da Computação',
        'sigla': 'PPGCC', 
        'nivel': 'MESTRADO_ACADEMICO',
        'area_capes': 'Ciência da Computação',
        'modalidade': 'PRESENCIAL'
    }
)
o, _ = Orientador.objects.get_or_create(
    cpf='123.456.789-00',
    defaults={
        'nome_completo': 'Prof. Dr. João Carlos da Silva',
        'email': 'joao.silva@ufmt.br'
    }
)
a, _ = Aluno.objects.get_or_create(
    cpf='987.654.321-00',
    defaults={
        'nome_civil': 'Maria Aparecida Souza',
        'data_nascimento': date(1995, 3, 15), 
        'sexo': 'F',
        'naturalidade_municipio': 'Cuiabá', 
        'naturalidade_uf': 'MT',
        'rg': '1234567', 
        'rg_orgao_emissor': 'SSP', 
        'rg_uf': 'MT',
        'email': 'maria.souza@ufmt.br', 
        'programa': p, 
        'orientador': o,
        'data_ingresso': date(2022, 3, 1), 
        'matricula': '2022001'
    }
)
d, _ = Defesa.objects.get_or_create(
    aluno=a,
    defaults={
        'titulo': 'Aplicação de Redes Neurais na Análise de Dados Agrícolas do Cerrado Mato-grossense',
        'data_defesa': date(2024, 11, 20), 
        'data_conclusao': date(2024, 11, 20),
        'carga_horaria_total': 24
    }
)
Diploma.objects.get_or_create(defesa=d, defaults={'status': 'Rascunho'})
print('Dados de exemplo verificados/criados com sucesso.')
"
echo ""
echo "=== Setup concluído ==="
echo "Execute: python3 manage.py runserver"
echo "Acesse:  http://localhost:8000"
echo "Login:   admin / ufmt2026"
