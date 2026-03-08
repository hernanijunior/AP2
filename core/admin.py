# === core/admin.py ===
from django.contrib import admin
from .models import Programa, Orientador, Aluno, Defesa, Diploma, LogAssinatura

admin.site.register(Programa)
admin.site.register(Orientador)
admin.site.register(Aluno)
admin.site.register(Defesa)
admin.site.register(Diploma)
admin.site.register(LogAssinatura)
