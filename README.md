# MVP Diploma Digital UFMT

Protótipo de sistema para simular o fluxo de emissão de Diplomas Digitais dos programas de Pós-Graduação da Universidade Federal de Mato Grosso (UFMT), adequado minimamente à Portaria MEC nº 70/2025.

Este sistema foi desenvolvido utilizando o framework **Django** com **Python 3**, utilizando MVT (Model-View-Template) com um design responsivo baseado no bootstrap e inspirado na identidade visual (SUAP) e regras institucionais.

## Funcionalidades Principais
*   **Gestão Acadêmica:** Cadastros completos de Alunos, Orientadores e Programas de Pós-Graduação (com níveis Mestrado Acadêmico, Profissional e Doutorado).
*   **Controle de Acessos Simulados:** Alteração rápida de "Papel Ativo" (ex: Secretaria, Coordenador, PROPG, Reitor) no cabeçalho da aplicação para testar as permissões de cada etapa.
*   **Fluxo de Defesa e Emissão:** Um workflow passo-a-passo acompanhando o diploma desde a aprovação da Defesa (Rascunho) até a Emissão e Assinatura Digital simulada.
*   **Geração de XML:** Geração do diploma eletrônico no formato padrão XML para conformidade com o MEC, contendo assinatura digital fictícia, identificador unívoco de diploma e dados acadêmicos do egresso.
*   **Dashboard e Auditoria:** Relatórios de progresso na tela inicial e listagem completa dos Logs e Histórico de transições/assinaturas por usuário.

## Passo a Passo do Fluxo de Emissão

Para testar o fluxo completo de emissão de um diploma, siga estas etapas trocando o **"Acesso como:"** (localizado no canto superior direito da tela):

1. **Rascunho:** (Qualquer papel) Cadastre uma nova *Defesa*. O diploma será gerado automaticamente com o status inicial sugerido.
2. **Aguardando Coordenador:** Mude para `Secretaria do Programa`, acesse o diploma na lista e clique em *Confirmar Dados*.
3. **Aguardando PROPG:** Mude para `Coordenador de Programa`, acesse o diploma e clique em *Aprovar Dados*.
4. **XML Gerado:** Mude para `PROPG` e clique em *Autorizar e Gerar XML* (isso gera a primeira via do arquivo XML seguindo o padrão MEC).
5. **Assinatura (Simulada):** Mude para `Reitor` (ou `Administrador/STI`) e clique em *Assinar Digitalmente*.
6. **Registrado:** Mude para `PROPG` e clique em *Registrar em Livro Eletrônico*.
7. **Emitido:** Mude para `Reitor` (ou `Administrador/STI`), clique em *Emitir Diploma Digital* para gerar a URL pública final e o código de validação.

## Tecnologias Utilizadas
*   Python 3.10+
*   Django 4.2+
*   Banco de Dados: SQLite3 (Ambiente de Desenvolvimento)
*   Interface: HTML5, CSS3, e Bootstrap 5 (Estilização baseada em SCSS com componentes UI padrão SUAP)
*   Deploy Local: Compatível nativamente com WSL (Windows Subsystem for Linux) / Ubuntu.

## Como Executar na Máquina Local

O repositório já conta com o banco de dados (SQLite3) configurado localmente. Você pode rodar a aplicação nas seguintes plataformas:

### Opção A: Linux / WSL (Recomendado)

O projeto possui um script automatizado (`setup.sh`) que prepara o ambiente, roda as migrações e popula os dados iniciais.

1. **Abra o terminal e acesse a pasta do projeto.**
2. **Execute o script de Autoconfiguração:**
```bash
bash setup.sh
```
3. **Inicie o Servidor de Desenvolvimento:**
```bash
python3 manage.py runserver
```

### Opção B: Windows (PowerShell / CMD)

Caso prefira rodar usando a instalação Python nativa do Windows:

1. **Abra o terminal na pasta do projeto.**
2. **Crie e ative um ambiente virtual (Recomendado):**
```powershell
python -m venv venv
venv\Scripts\activate
```
3. **Instale as dependências:**
```powershell
pip install -r requirements.txt
```
4. **Aplique as Migrações do Banco de Dados:**
```powershell
python manage.py migrate
```
5. **Inicie o Servidor de Desenvolvimento:**
```powershell
python manage.py runserver
```

### Acessando a Aplicação
Após iniciar o servidor (em qualquer um dos SOs), abra o navegador no endereço:
`http://127.0.0.1:8000/`

**Usuário:** `admin`  
**Senha:** `ufmt2026`

---
*Projeto desenvolvido para fins de Demonstração / MVP.*
"# AP2" 
