# === core/apps.py ===
from django.apps import AppConfig
import sys
import threading

def create_initial_data():
    try:
        from django.contrib.auth.models import User
        from core.models import Programa, Orientador, Aluno, Defesa, Diploma
        from datetime import date
        from django.db.utils import OperationalError, ProgrammingError
        
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@ufmt.br', 'ufmt2026')
                print('\n[MVP Diploma] Superusuário criado automaticamente: admin / ufmt2026')

            p, created_p = Programa.objects.get_or_create(
                codigo_sucupira='40001016001P0',
                defaults={
                    'nome': 'Programa de Pós-Graduação em Ciência da Computação',
                    'sigla': 'PPGCC', 
                    'nivel': 'MESTRADO_ACADEMICO',
                    'area_capes': 'Ciência da Computação',
                    'modalidade': 'PRESENCIAL'
                }
            )
            o, created_o = Orientador.objects.get_or_create(
                cpf='123.456.789-00',
                defaults={
                    'nome_completo': 'Prof. Dr. João Carlos da Silva',
                    'email': 'joao.silva@ufmt.br'
                }
            )
            a, created_a = Aluno.objects.get_or_create(
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
            d, created_d = Defesa.objects.get_or_create(
                aluno=a,
                defaults={
                    'titulo': 'Aplicação de Redes Neurais na Análise de Dados Agrícolas do Cerrado Mato-grossense',
                    'data_defesa': date(2024, 11, 20), 
                    'data_conclusao': date(2024, 11, 20),
                    'carga_horaria_total': 24
                }
            )
            _, created_dip = Diploma.objects.get_or_create(defesa=d, defaults={'status': 'Rascunho'})
            
            if created_p or created_o or created_a or created_d or created_dip:
                print('[MVP Diploma] Dados de exemplo carregados no banco de dados com sucesso!\n')
                
        except (OperationalError, ProgrammingError):
            pass
    except Exception as e:
        print(f"Erro ao criar dados iniciais: {e}")

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        if 'runserver' in sys.argv:
            timer = threading.Timer(1.5, create_initial_data)
            timer.start()
