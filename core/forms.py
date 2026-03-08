# === core/forms.py ===
from django import forms
from .models import Programa, Orientador, Aluno, Defesa

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = ['nome', 'sigla', 'nivel', 'codigo_sucupira', 'area_capes', 'modalidade', 'ativo']

class OrientadorForm(forms.ModelForm):
    class Meta:
        model = Orientador
        fields = ['nome_completo', 'cpf', 'email', 'lattes', 'ativo']

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            'nome_civil', 'cpf', 'data_nascimento', 'sexo', 'nacionalidade',
            'naturalidade_municipio', 'naturalidade_uf', 'rg', 'rg_orgao_emissor',
            'rg_uf', 'email', 'programa', 'orientador', 'data_ingresso', 'matricula'
        ]

class DefesaForm(forms.ModelForm):
    class Meta:
        model = Defesa
        fields = [
            'aluno', 'titulo', 'data_defesa', 'data_conclusao',
            'carga_horaria_total', 'coorientador_nome', 'resumo'
        ]
