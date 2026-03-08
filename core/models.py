# === core/models.py ===
from django.db import models

class Programa(models.Model):
    NIVEL_CHOICES = (
        ('MESTRADO_ACADEMICO', 'Mestrado Acadêmico'),
        ('MESTRADO_PROFISSIONAL', 'Mestrado Profissional'),
        ('DOUTORADO', 'Doutorado'),
    )
    MODALIDADE_CHOICES = (
        ('PRESENCIAL', 'Presencial'),
        ('EAD', 'EaD'),
        ('HIBRIDO', 'Híbrido'),
    )

    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20)
    nivel = models.CharField(max_length=30, choices=NIVEL_CHOICES)
    codigo_sucupira = models.CharField(max_length=20)
    area_capes = models.CharField(max_length=100)
    modalidade = models.CharField(max_length=20, choices=MODALIDADE_CHOICES)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sigla} - {self.nome}"


class Orientador(models.Model):
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    lattes = models.URLField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_completo


class Aluno(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    )

    nome_civil = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    nacionalidade = models.CharField(max_length=100, default='Brasileira')
    naturalidade_municipio = models.CharField(max_length=100)
    naturalidade_uf = models.CharField(max_length=2)
    rg = models.CharField(max_length=30)
    rg_orgao_emissor = models.CharField(max_length=20)
    rg_uf = models.CharField(max_length=2)
    email = models.EmailField()
    programa = models.ForeignKey(Programa, on_delete=models.deletion.PROTECT)
    orientador = models.ForeignKey(Orientador, on_delete=models.deletion.PROTECT)
    data_ingresso = models.DateField()
    matricula = models.CharField(max_length=20, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.matricula} - {self.nome_civil}"


class Defesa(models.Model):
    aluno = models.OneToOneField(Aluno, on_delete=models.deletion.CASCADE)
    titulo = models.CharField(max_length=300)
    data_defesa = models.DateField()
    data_conclusao = models.DateField()
    carga_horaria_total = models.IntegerField()
    coorientador_nome = models.CharField(max_length=200, blank=True)
    resumo = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Defesa: {self.aluno.nome_civil}"


class Diploma(models.Model):
    STATUS_CHOICES = (
        ('Rascunho', 'Rascunho'),
        ('Aguardando Coordenador', 'Aguardando Coordenador'),
        ('Aguardando PROPG', 'Aguardando PROPG'),
        ('Aprovado PROPG', 'Aprovado PROPG'),
        ('XML Gerado', 'XML Gerado'),
        ('Assinado (Simulado)', 'Assinado (Simulado)'),
        ('Registrado', 'Registrado'),
        ('Emitido', 'Emitido'),
    )

    defesa = models.OneToOneField(Defesa, on_delete=models.deletion.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Rascunho')
    numero_diploma = models.CharField(max_length=30, unique=True, null=True, blank=True)
    numero_livro = models.CharField(max_length=10, blank=True)
    numero_folha = models.CharField(max_length=10, blank=True)
    numero_registro = models.CharField(max_length=20, blank=True)
    url_diploma = models.CharField(max_length=255, blank=True)
    codigo_validacao = models.CharField(max_length=50, unique=True, null=True, blank=True)
    xml_gerado = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diploma {self.numero_diploma or 'Rascunho'} - {self.defesa.aluno.nome_civil}"


class LogAssinatura(models.Model):
    diploma = models.ForeignKey(Diploma, on_delete=models.deletion.CASCADE, related_name='logs')
    papel = models.CharField(max_length=50)
    nome_assinante = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=45)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.papel} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
