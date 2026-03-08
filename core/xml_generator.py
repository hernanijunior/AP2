# === core/xml_generator.py ===
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def gerar_xml_diploma(diploma):
    defesa = diploma.defesa
    aluno = defesa.aluno
    programa = aluno.programa
    orientador = aluno.orientador

    root = ET.Element("diplomaDigital", xmlns="http://portal.mec.gov.br/diplomadigital/arquivos-em-xsd")
    
    # Dados da Instituição (Fixo para UFMT)
    dados_inst = ET.SubElement(root, "dadosInstituicaoEmissora")
    ET.SubElement(dados_inst, "nomeIES").text = "Universidade Federal de Mato Grosso"
    ET.SubElement(dados_inst, "siglaIES").text = "UFMT"
    ET.SubElement(dados_inst, "codigoMEC").text = "572"
    ET.SubElement(dados_inst, "cnpj").text = "33.555.921/0001-70"
    ET.SubElement(dados_inst, "tipoInstituicao").text = "Universidade"
    ET.SubElement(dados_inst, "categoriaAdministrativa").text = "Pública Federal"
    ET.SubElement(dados_inst, "municipio").text = "Cuiabá"
    ET.SubElement(dados_inst, "uf").text = "MT"

    # Dados do Diplomado
    dados_diplomado = ET.SubElement(root, "dadosDiplomado")
    ET.SubElement(dados_diplomado, "nomeDiplomado").text = aluno.nome_civil
    ET.SubElement(dados_diplomado, "cpf").text = aluno.cpf
    if aluno.data_nascimento:
        ET.SubElement(dados_diplomado, "dataNascimento").text = aluno.data_nascimento.strftime('%Y-%m-%d')
    ET.SubElement(dados_diplomado, "sexo").text = aluno.sexo
    ET.SubElement(dados_diplomado, "nacionalidade").text = aluno.nacionalidade
    ET.SubElement(dados_diplomado, "naturalidadeMunicipio").text = aluno.naturalidade_municipio
    ET.SubElement(dados_diplomado, "naturalidadeUF").text = aluno.naturalidade_uf
    
    doc_ident = ET.SubElement(dados_diplomado, "documentoIdentificacao", tipo="RG")
    ET.SubElement(doc_ident, "numero").text = aluno.rg
    ET.SubElement(doc_ident, "orgaoEmissor").text = aluno.rg_orgao_emissor
    ET.SubElement(doc_ident, "uf").text = aluno.rg_uf

    # Dados do Curso
    dados_curso = ET.SubElement(root, "dadosCurso")
    ET.SubElement(dados_curso, "nomeCurso").text = programa.nome
    ET.SubElement(dados_curso, "nivelCurso").text = dict(programa.NIVEL_CHOICES).get(programa.nivel, programa.nivel)
    ET.SubElement(dados_curso, "areaConhecimento").text = programa.area_capes
    ET.SubElement(dados_curso, "codigoProgramaCAPES").text = programa.codigo_sucupira
    ET.SubElement(dados_curso, "modalidadeCurso").text = dict(programa.MODALIDADE_CHOICES).get(programa.modalidade, programa.modalidade)
    ET.SubElement(dados_curso, "tituloDissertacaoTese").text = defesa.titulo
    ET.SubElement(dados_curso, "nomeOrientador").text = orientador.nome_completo
    if aluno.data_ingresso:
        ET.SubElement(dados_curso, "dataIngresso").text = aluno.data_ingresso.strftime('%Y-%m-%d')
    if defesa.data_conclusao:
        ET.SubElement(dados_curso, "dataConclusao").text = defesa.data_conclusao.strftime('%Y-%m-%d')
    ET.SubElement(dados_curso, "cargaHorariaTotal").text = str(defesa.carga_horaria_total)

    # Dados de Registro
    dados_registro = ET.SubElement(root, "dadosRegistro")
    ET.SubElement(dados_registro, "numeroDiploma").text = diploma.numero_diploma or ""
    ET.SubElement(dados_registro, "numeroLivro").text = diploma.numero_livro or ""
    ET.SubElement(dados_registro, "numeroFolha").text = diploma.numero_folha or ""
    ET.SubElement(dados_registro, "numeroRegistro").text = diploma.numero_registro or ""
    ET.SubElement(dados_registro, "urlDiploma").text = diploma.url_diploma or ""
    ET.SubElement(dados_registro, "codigoValidacao").text = diploma.codigo_validacao or ""

    if hasattr(ET, 'indent'):
        ET.indent(root)
    else:
        indent(root)
        
    xml_str = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
    return xml_str
