# === core/views.py ===
import uuid
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Programa, Orientador, Aluno, Defesa, Diploma, LogAssinatura
from .forms import ProgramaForm, OrientadorForm, AlunoForm, DefesaForm
from .xml_generator import gerar_xml_diploma

def get_papel(request):
    return request.session.get('papel_ativo', 'Secretaria do Programa')

@login_required
def dashboard(request):
    context = {
        'total_alunos': Aluno.objects.count(),
        'total_programas': Programa.objects.count(),
        'diplomas_por_status': [
            {'status': s[0], 'count': Diploma.objects.filter(status=s[0]).count()}
            for s in Diploma.STATUS_CHOICES
        ],
        'ultimas_atividades': LogAssinatura.objects.order_by('-timestamp')[:5],
        'papel_ativo': get_papel(request)
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def trocar_papel(request):
    if request.method == 'POST':
        novo_papel = request.POST.get('papel')
        if novo_papel:
            request.session['papel_ativo'] = novo_papel
            messages.success(request, f'Papel alterado para: {novo_papel}')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def aluno_list(request):
    alunos = Aluno.objects.all().order_by('-id')
    return render(request, 'core/aluno_list.html', {'alunos': alunos})

@login_required
def aluno_form(request, id=None):
    if id:
        aluno = get_object_or_404(Aluno, id=id)
    else:
        aluno = None

    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno salvo com sucesso.')
            return redirect('aluno_list')
        else:
            messages.error(request, 'Erro ao salvar aluno. Verifique os dados.')
    else:
        form = AlunoForm(instance=aluno)
    
    return render(request, 'core/aluno_form.html', {'form': form, 'aluno': aluno, 'programas': Programa.objects.filter(ativo=True), 'orientadores': Orientador.objects.filter(ativo=True)})

@login_required
def programa_list(request):
    programas = Programa.objects.all().order_by('nome')
    return render(request, 'core/programa_list.html', {'programas': programas})

@login_required
def programa_form(request, id=None):
    if id:
        programa = get_object_or_404(Programa, id=id)
    else:
        programa = None

    if request.method == 'POST':
        form = ProgramaForm(request.POST, instance=programa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Programa salvo com sucesso.')
            return redirect('programa_list')
        else:
            messages.error(request, 'Erro ao salvar programa. Verifique os dados.')
    else:
        form = ProgramaForm(instance=programa)
    
    return render(request, 'core/programa_form.html', {'form': form, 'programa': programa})

@login_required
def orientador_list(request):
    orientadores = Orientador.objects.all().order_by('nome_completo')
    return render(request, 'core/orientador_list.html', {'orientadores': orientadores})

@login_required
def orientador_form(request, id=None):
    if request.method == 'POST':
        form = OrientadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Orientador salvo com sucesso.')
            return redirect('orientador_list')
    else:
        form = OrientadorForm()
    return render(request, 'core/orientador_form.html', {'form': form})

@login_required
def defesa_list(request):
    defesas = Defesa.objects.select_related('diploma', 'aluno').order_by('-data_defesa')
    return render(request, 'core/defesa_list.html', {'defesas': defesas})

@login_required
def defesa_form(request):
    if request.method == 'POST':
        form = DefesaForm(request.POST)
        if form.is_valid():
            defesa = form.save()
            # Cria o diploma em rascunho
            Diploma.objects.create(defesa=defesa, status='Rascunho')
            messages.success(request, 'Defesa lançada e Diploma em Rascunho criado.')
            return redirect('defesa_list')
        else:
            messages.error(request, 'Erro ao salvar defesa.')
    else:
        form = DefesaForm()
    return render(request, 'core/defesa_form.html', {'form': form, 'alunos': Aluno.objects.filter(defesa__isnull=True)})

@login_required
def diploma_detail(request, id):
    defesa = get_object_or_404(Defesa, id=id)
    diploma = defesa.diploma
    
    papel = get_papel(request)
    acao_disponivel = None
    
    # Lógica de botões / papéis
    if diploma.status == 'Rascunho' and papel == 'Secretaria do Programa':
        acao_disponivel = ('confirmar_dados', 'Confirmar Dados (Enviar ao Coordenador)', 'primary')
    elif diploma.status == 'Aguardando Coordenador' and papel == 'Coordenador de Programa':
        acao_disponivel = ('aprovar_coordenador', 'Aprovar Dados (Enviar à PROPG)', 'success')
    elif diploma.status == 'Aguardando PROPG' and papel == 'PROPG':
        acao_disponivel = ('autorizar_propg', 'Autorizar e Gerar XML', 'warning')
    elif diploma.status == 'XML Gerado' and (papel == 'Administrador/STI' or papel == 'Reitor' or papel == 'Administrador'):
        acao_disponivel = ('assinar', 'Assinar Digitalmente (Simulado)', 'danger')
    elif diploma.status == 'Assinado (Simulado)' and papel == 'PROPG':
        acao_disponivel = ('registrar', 'Registrar em Livro Eletrônico', 'info')
    elif diploma.status == 'Registrado' and (papel == 'Administrador/STI' or papel == 'Reitor' or papel == 'Administrador'):
        acao_disponivel = ('emitir', 'Emitir Diploma Digital', 'success')
        
    context = {
        'defesa': defesa,
        'diploma': diploma,
        'logs': diploma.logs.order_by('-timestamp'),
        'acao_disponivel': acao_disponivel,
        'papel_ativo': papel
    }
    return render(request, 'core/diploma_detail.html', context)

def _registrar_log(diploma, papel, request, observacao=""):
    LogAssinatura.objects.create(
        diploma=diploma,
        papel=papel,
        nome_assinante=request.user.username,
        ip=request.META.get('REMOTE_ADDR', '127.0.0.1'),
        observacao=observacao
    )

@login_required
def diploma_acao(request, id):
    if request.method != 'POST':
        return redirect('diploma_detail', id=id)
        
    acao = request.POST.get('acao')
    diploma = get_object_or_404(Diploma, id=id)
    papel = get_papel(request)
    
    if acao == 'confirmar_dados':
        if diploma.status == 'Rascunho' and papel == 'Secretaria do Programa':
            diploma.status = 'Aguardando Coordenador'
            diploma.save()
            _registrar_log(diploma, papel, request, "Dados confirmados pela Secretaria")
            messages.success(request, 'Dados confirmados. Enviado ao Coordenador.')
    
    elif acao == 'aprovar_coordenador':
        if diploma.status == 'Aguardando Coordenador' and papel == 'Coordenador de Programa':
            diploma.status = 'Aguardando PROPG'
            diploma.save()
            _registrar_log(diploma, papel, request, "Dados aprovados pelo Coordenador")
            messages.success(request, 'Dados aprovados pelo Coordenador. Enviado à PROPG.')
            
    elif acao == 'autorizar_propg':
        if diploma.status == 'Aguardando PROPG' and papel == 'PROPG':
            diploma.status = 'Aprovado PROPG'
            # Gera XML
            xml_str = gerar_xml_diploma(diploma)
            diploma.xml_gerado = xml_str
            diploma.status = 'XML Gerado'
            diploma.save()
            _registrar_log(diploma, papel, request, "Autorizado pela PROPG e XML gerado")
            messages.success(request, 'Autorizado e XML gerado com sucesso.')

    elif acao == 'assinar':
        if diploma.status == 'XML Gerado' and 'Administrador' in papel or 'STI' in papel or 'Reitor' in papel:
            diploma.status = 'Assinado (Simulado)'
            diploma.save()
            _registrar_log(diploma, papel, request, "Assinatura Digital aplicada (Simulado)")
            messages.success(request, 'Diploma assinado com sucesso.')
            
    elif acao == 'registrar':
        if diploma.status == 'Assinado (Simulado)' and papel == 'PROPG':
            diploma.status = 'Registrado'
            diploma.numero_livro = "E-001"
            # Conta quantos diplomas têm livro E-001 para ser o num folha
            qtd_registrados = Diploma.objects.filter(numero_livro="E-001").count()
            diploma.numero_folha = str(qtd_registrados + 1)
            diploma.numero_registro = f"REG-{diploma.id:06d}"
            
            # Atualiza o XML com os dados de registro
            xml_str = gerar_xml_diploma(diploma)
            diploma.xml_gerado = xml_str
            
            diploma.save()
            _registrar_log(diploma, papel, request, f"Registrado em Livro {diploma.numero_livro}, Folha {diploma.numero_folha}")
            messages.success(request, 'Diploma registrado em livro eletrônico.')
            
    elif acao == 'emitir':
        if diploma.status == 'Registrado' and ('Administrador' in papel or 'STI' in papel or 'Reitor' in papel):
            diploma.status = 'Emitido'
            ano = datetime.now().year
            diploma.numero_diploma = f"UFMT-PG-{ano}-{diploma.id:06d}"
            diploma.codigo_validacao = uuid.uuid4().hex[:16].upper()
            diploma.url_diploma = f"https://diplomas.ufmt.br/validar/{diploma.codigo_validacao}"
            
            # Atualiza XML final
            xml_str = gerar_xml_diploma(diploma)
            diploma.xml_gerado = xml_str
            
            diploma.save()
            _registrar_log(diploma, papel, request, f"Diploma Emitido: {diploma.numero_diploma}")
            messages.success(request, f'Diploma {diploma.numero_diploma} emitido com sucesso e URL gerada.')

    else:
        messages.error(request, 'Ação inválida ou você não tem permissão para esta etapa.')

    return redirect('diploma_detail', id=diploma.defesa.id)

@login_required
def diploma_xml(request, id):
    diploma = get_object_or_404(Diploma, id=id)
    return render(request, 'core/diploma_xml.html', {'diploma': diploma})

@login_required
def diploma_log(request, id):
    diploma = get_object_or_404(Diploma, id=id)
    return render(request, 'core/diploma_log.html', {'diploma': diploma, 'logs': diploma.logs.order_by('-timestamp')})
