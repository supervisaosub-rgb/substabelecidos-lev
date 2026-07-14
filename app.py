import streamlit as st

from streamlit_cookies_controller import CookieController

import pandas as pd

from datetime import datetime, timedelta, date

from io import BytesIO

import json

import ast

import os

from PIL import Image # <-- Importamos para ler a imagem da logo



# Carrega a logo para a aba (usando o caminho completo da rede Z:)

try:

    favicon = Image.open(r"Z:\SUBSTABELECIDO\Sistema_Sub\Fotos\LOGO LEV ROXO.png")

except Exception:

    favicon = "🔮" # Reserva se a rede Z: oscilar



# Configuração da página deve ser o primeiro comando Streamlit executado

st.set_page_config(

    page_title="Login | Gestão de Substabelecidos", 

    page_icon=favicon, 

    layout="wide"

)



# =========================================================

# CONFIG GERAL (Sincronizado com a sua rede Z:)

# =========================================================


BASE_DIR = r"Z:\SUBSTABELECIDO\Sistema_Sub"

ARQUIVO_BASE = os.path.join(BASE_DIR, "base_sub.xlsx")

ARQUIVO_HIST = os.path.join(BASE_DIR, "historico_sub.xlsx")


# =========================================================

# LOGIN COM CONTROLE DE PERFIS E COOKIES (TRAVA F5 CORRIGIDA)

# =========================================================


# Inicializa o controlador de cookies

controller = CookieController()



USUARIOS = {

    "ana.costa@levnegocios.com.br": "Lev@SUB28",

    "mariana.santos@levnegocios.com.br": "Lev@SUB28",

    "gustavo.cintra@levnegocios.com.br": "Lev@SUB28"

}



USUARIO_NOME = {

    "ana.costa@levnegocios.com.br": "Ana Laura",

    "mariana.santos@levnegocios.com.br": "Mariana Santos",

    "gustavo.cintra@levnegocios.com.br": "Gustavo Cintra"

}



EMAILS_SUPERVISAO = [

    "ana.costa@levnegocios.com.br"

]



# Inicialização padrão do Session State

if "logado" not in st.session_state:

    st.session_state.logado = False

if "usuario" not in st.session_state:

    st.session_state.usuario = ""

if "nome_usuario" not in st.session_state:

    st.session_state.nome_usuario = ""

if "perfil_usuario" not in st.session_state:

    st.session_state.perfil_usuario = ""

if "go_to_base" not in st.session_state:

    st.session_state.go_to_base = False

if "base_filters" not in st.session_state:

    st.session_state.base_filters = {}



# --- LEITURA SEGURA DE COOKIE (TRAVA F5) ---

if not st.session_state.logado:

    try:

        # Puxa o e-mail armazenado no cookie do navegador

        cookie_usuario = controller.get("user_session_email")

        

        if cookie_usuario and cookie_usuario in USUARIOS:

            st.session_state.logado = True

            st.session_state.usuario = cookie_usuario

            st.session_state.nome_usuario = USUARIO_NOME.get(cookie_usuario, cookie_usuario)

            if cookie_usuario in EMAILS_SUPERVISAO:

                st.session_state.perfil_usuario = "Supervisão"

            else:

                st.session_state.perfil_usuario = "Colaborador"

            st.rerun()

    except Exception:

        # Evita falhas caso o componente do cookie ainda esteja renderizando

        pass





def logout():

    """Função responsável por deslogar o utilizador e limpar a sessão/cookies"""

    st.session_state.logado = False

    st.session_state.usuario = ""

    st.session_state.nome_usuario = ""

    st.session_state.perfil_usuario = ""

    

    # Remove o e-mail guardado nos cookies do navegador

    try:

        controller.remove("user_session_email")

    except Exception:

        pass

    st.rerun()





def login():

    # Injeta a técnica de fixação absoluta com a paleta de cores oficial da LEV

    st.markdown(

        """

        <style>

            /* Esconde absolutamente tudo o que é nativo do Streamlit */

            [data-testid="stHeader"], #MainMenu, footer, [data-testid="stMainHeader"] {

                visibility: hidden !important; 

                display: none !important;

            }

            [data-testid="stSidebar"] {display: none !important;}

            

            /* Tira a rolagem do navegador para fixar o ecrã */

            body, .stApp {

                overflow: hidden !important;

                height: 100vh !important;

            }



            /* Força o bloco de colunas a colar no teto e no chão do ecrã */

            [data-testid="stHorizontalBlock"] {

                position: fixed !important;

                top: 0px !important;

                left: 0px !important;

                width: 100vw !important;

                height: 100vh !important;

                gap: 0px !important;

                margin: 0px !important;

                padding: 0px !important;

                z-index: 999999 !important;

                align-items: stretch !important;

                background-color: #ffffff !important;

            }

            

            /* Garante que as colunas internas herdem a altura inteira */

            [data-testid="column"] {

                height: 100vh !important;

                padding: 0px !important;

                margin: 0px !important;

            }

            

            /* COLUNA DA ESQUERDA (FORMULÁRIO): Centralização vertical absoluta */

            [data-testid="stHorizontalBlock"] > div:first-child {

                background-color: #ffffff !important;

                padding: 0% 8% !important;

                display: flex !important;

                flex-direction: column !important;

                justify-content: center !important;

                height: 100vh !important;

                box-sizing: border-box !important;

            }

            

            /* COLUNA DA DIREITA (IMAGEM) */

            [data-testid="stHorizontalBlock"] > div:last-child {

                height: 100vh !important;

                overflow: hidden !important;

                padding: 0px !important;

                margin: 0px !important;

            }

            

            /* Força a foto a preencher tudo perfeitamente */

            [data-testid="stHorizontalBlock"] > div:last-child img {

                object-fit: cover !important;

                height: 100vh !important;

                width: 100% !important;

                margin: 0px !important;

                padding: 0px !important;

            }

            

            /* BOTÃO PREVIEW: Corrigido para o roxo oficial da identidade LEV */

            div.stButton > button {

                background-color: #6134b2 !important; /* Roxo oficial LEV */

                color: white !important;

                border-radius: 8px !important;

                padding: 12px 24px !important;

                font-weight: 600 !important;

                border: none !important;

                width: 100% !important;

                margin-top: 20px;

                box-shadow: 0 4px 12px rgba(97, 52, 178, 0.2);

                transition: all 0.2s ease-in-out;

            }

            div.stButton > button:hover {

                background-color: #4c2692 !important; /* Roxo ligeiramente mais escuro no hover */

                box-shadow: 0 6px 15px rgba(97, 52, 178, 0.3);

            }



            /* INPUTS REFINADOS: Caixa de texto limpa */

            div[data-testid="stTextInput"] input {

                border-radius: 8px !important;

                border: 1.5px solid #e2e8f0 !important;

                padding: 10px 14px !important;

                background-color: #f8fafc !important;

                transition: all 0.2s ease-in-out;

            }

            

            /* FOCO DOS INPUTS: Acende em roxo ao clicar para digitar igual a sistemas modernos */

            div[data-testid="stTextInput"] input:focus {

                border-color: #6134b2 !important;

                box-shadow: 0 0 0 3px rgba(97, 52, 178, 0.15) !important;

                background-color: #ffffff !important;

            }

        </style>

        """,

        unsafe_allow_html=True

    )



    # Divide o ecrã (45% para o formulário, 55% para a imagem)

    col_form, col_imagem = st.columns([45, 55])



    # --- COLUNA DA ESQUERDA: FORMULÁRIO CENTRALIZADO ---

    with col_form:

        # Logo Oficial Roxo da LEV

        st.image(r"Z:\SUBSTABELECIDO\Sistema_Sub\Fotos\LOGO LEV ROXO.png", width=120)

        

        # Título atualizado com a cor roxa oficial da LEV (#6134b2)

        st.markdown("<h2 style='color:#6134b2; margin-top:20px; margin-bottom:5px; font-weight:700; font-family: sans-serif; font-size: 28px;'>Gestão de Substabelecidos</h2>", unsafe_allow_html=True)

        st.markdown("<p style='color:#64748b; font-size:14px; margin-bottom:25px; font-family: sans-serif;'>Seja bem-vindo! Insira seus dados para acessar o painel.</p>", unsafe_allow_html=True)

        

        # Inputs oficiais de login

        usuario = st.text_input("E-mail corporativo", placeholder="nome@empresa.com.br").strip().lower()

        senha = st.text_input("Sua senha", type="password", placeholder="••••••••")



        # Clique do botão oficial

        if st.button("Entrar no Sistema"):

            if usuario in USUARIOS and USUARIOS[usuario] == senha:

                st.session_state.logado = True

                st.session_state.usuario = usuario

                st.session_state.nome_usuario = USUARIO_NOME.get(usuario, usuario)

                

                if usuario in EMAILS_SUPERVISAO:

                    st.session_state.perfil_usuario = "Supervisão"

                else:

                    st.session_state.perfil_usuario = "Colaborador"

                

                controller.set("user_session_email", usuario)

                st.rerun()

            else:

                st.error("⚠️ Login ou senha inválidos.")

                

        # Rodapé corporativo

        st.markdown("<p style='text-align:center; color:#94a3b8; font-size:11px; margin-top:40px; font-family: sans-serif;'>&copy; 2026 LEV. Todos os direitos reservados.</p>", unsafe_allow_html=True)



    # --- COLUNA DA DIREITA: IMAGEM FIXA NO TOPO ---

    with col_imagem:

        st.image(

            r"Z:\SUBSTABELECIDO\Sistema_Sub\Fotos\FOTO SIMPLICIDADE.jpg", 

            use_container_width=True

        ) 

# =========================================================
# LISTAS / REGRAS
# =========================================================

STATUS_LISTA = ["Em andamento", "Concluído", "Cancelado"]
TIPOS_CREDENCIAMENTO = ["Credenciamento Novo", "Migração", "Reativação"]
RESPONSAVEIS = ["Mariana Santos", "Ana Laura", "Gustavo Cintra"]

FASES = [
    "Aguardando Banco: Cadastro iniciado",
    "Aguardando Banco: Verificação de assinaturas",
    "Aguardando Banco: Verificação de Documentos",
    "Aguardando Banco: Liberação de acessos",
    "Aguardando Banco: Envio de contrato para assinatura",
    "Aguardando Banco: Gerar Token/Acesso Documentação",
    "Aguardando Parceiro: Criação de conta Daycoval",
    "Aguardando Documentação: Parceiro",
    "Aguardando De acordo Superintendentente",
    "Aguardando De acordo Regional",
    "Aguardando De acordo Comercial",
    "Aguardando De acordo Diretoria",
    "Aguardando comercial: Negociação débitos",
    "Aguardando comercial: Modalidade/rateio",
    "Aguardando alinhamento GC Lev e GC Banco",
    "Cancelado: CNPJ ativo por outro corban",
    "Cancelado: Parceiro optou por não prosseguir com o credenciamento",
    "Cancelado: Motivos internos do banco",
    "Cancelado: Produto suspenso",
    "Cancelado: Falta de Retorno",
    "Fase de Assinaturas: Sub",
    "Fase de Assinaturas: Lev",
    "Aguardando Jurídico: Validação Contrato",
    "Finalizado: Código criado"
]

STATUS_CONTRATUAL = [
    "Não enviado",
    "A ser enviado",
    "Pendente assinatura",
    "Assinado",
    "Arquivado",
    "Cancelado - Contrato Expirado"
]

COPIA_CONTRATO_OPCOES = ["", "Não", "A ser enviado", "Enviado", "Arquivado"]

BANCOS_PRAZO = {
    "TOTALCASH": 1, "V8 DIGITAL": 2, "NYC BANK": 2, "NOVO SAQUE": 2, "VCTEX": 2, "VILEVE": 2,
    "GRANDINO": 5, "MEU CASH CARD": 5, "ÂNCORA CONSÓRCIO": 5, "AMIGOZ": 5, "BTW BANK": 5, "QUALIBANK": 5,
    "HOPE": 7, "AKI CAPITAL": 7, "CAPITAL CONSIG": 7, "EMPRESTEI CARD": 7, "ICRED": 10,
    "SAFRA": 15, "BMG": 15, "OLÉ": 15, "MERCANTIL": 15, "C6 PAY": 15, "C6 BANK": 20,
    "PAN": 30, "DAYCOVAL": 30, "FACTA": 30, "QUERO MAIS CRÉDITO": 30, "ITAU": 15, "EVOL": 6
}

MODALIDADES_POR_BANCO = {
    "C6 BANK": ["SUB BANCO", "SUB ZERO", "INDICADO BANCO"],
    "BMG": ["SUB BANCO", "SUB ZERO", "INDICADO BANCO"],
    "PAN": ["SUB BANCO", "SUB ZERO", "INDICADO BANCO"],
    "DAYCOVAL": ["SUB BANCO", "SUB ZERO", "INDICADO BANCO"],
    "FACTA": ["SUB BANCO", "SUB ZERO"],
    "SAFRA": ["SUB BANCO", "SUB ZERO", "INDICADO BANCO"],
    "OLÉ": ["SUB BANCO", "SUB ZERO", "INDICADO BANCO"],
    "MERCANTIL": ["SUB BANCO", "SUB ZERO", "INDICADO BANCO"],
    "ICRED": ["SUB BANCO", "SUB ZERO"],
    "VCTEX": ["SUB BANCO", "SUB ZERO"],
    "HOPE": ["SUB BANCO", "SUB ZERO"],
    "QUALIBANK": ["SUB BANCO", "SUB ZERO"],
    "MEU CASH CARD": ["SUB BANCO", "SUB ZERO"],
    "TOTALCASH": ["SUB BANCO", "SUB ZERO"],
    "EVOL": ["SUB BANCO", "SUB ZERO"],
    "AMIGOZ": ["SUB BANCO", "SUB ZERO"],
    "AKI CAPITAL": ["SUB BANCO"],
    "V8 DIGITAL": ["SUB BANCO"],
    "GRANDINO": ["SUB BANCO"],
    "VILEVE": ["SUB BANCO"],
    "EMPRESTEI CARD": ["SUB BANCO"],
    "BTW BANK": ["SUB BANCO"],
    "NYC BANK": ["SUB BANCO"],
    "NOVO SAQUE": ["SUB BANCO", "SUB ZERO"],
    "ITAU": ["SUB BANCO"],
    "QUERO MAIS CRÉDITO": ["SUB BANCO", "SUB ZERO"],
    "ÂNCORA CONSÓRCIO": ["SUB BANCO", "SUB ZERO"],
    "CAPITAL CONSIG": ["SUB BANCO", "SUB ZERO"],
    "C6 PAY": ["SUB ZERO"]
}

HIERARQUIA_COMERCIAL = {
    "GC - LEV NEGOCIOS LTDA": ("GR - LEV", "SUP. BERGSON ARRAIS"),
    "GC - CONSIGA": ("GR - LEV", "SUP. BERGSON ARRAIS"),
    "GC - SP INTERIOR NEY 2": ("GR - JOSE DOMINGOS ROSA ZAGUI", "SUP. JOSE DOMINGOS ROSA ZAGUI"),
    "GC - SP INTERIOR DOUGLAS": ("GR - DOUGLAS CLAUDIO PINHEIRO DE CAMPOS", "SUP. JOSE DOMINGOS ROSA ZAGUI"),
    "GC - DOUGLAS CLAUDIO PINHEIRO DE CAMPOS": ("GR - DOUGLAS CLAUDIO PINHEIRO DE CAMPOS", "SUP. JOSE DOMINGOS ROSA ZAGUI"),
    "GC - MATHEUS MARCAL DE CARVALHO": ("GR - DOUGLAS CLAUDIO PINHEIRO DE CAMPOS", "SUP. JOSE DOMINGOS ROSA ZAGUI"),
    "GC - LUCIANA VANESSA RUSSAFA MOSQUIM": ("GR - LUCIANA VANESSA RUSSAFA MOSQUIM", "SUP. JOSE DOMINGOS ROSA ZAGUI"),
    "GC - THAIS CUNHA TERENCIO": ("GR - THAIS CUNHA ZAGUI", "SUP. JOSE DOMINGOS ROSA ZAGUI"),
    "GC - JOAO APARECIDO SANDOR": ("GR - THAIS CUNHA ZAGUI", "SUP. JOSE DOMINGOS ROSA ZAGUI"),
    "GC - LORENA CUNHA MARTINELLI": ("GR - GLADSTON PERICLES GONÇALVES BARBOSA", "SUP. JOSE DOMINGOS ROSA ZAGUI"),
    "GC - GLADSTON PERICLES GONÇALVES": ("GR - GLADSTON PERICLES GONÇALVES BARBOSA", "SUP. JOSE DOMINGOS ROSA ZAGUI"),
    "GC - JOSE DOMINGOS ROSA ZAGUI": ("GR - JOSE DOMINGOS ROSA ZAGUI", "SUP. JOSE DOMINGOS ROSA ZAGUI"),
    "GC - ANA BARBARA CARDOSO GUIMARAES": ("GR - ANA BARBARA CARDOSO GUIMARAES", "SUP. EUDES MARTINS DE ARAUJO"),
    "GC - PARANA": ("GR - AMANDA APARECIDA DIMARTINI OLIVEIRA", "SUP. CASSIANO JOSE DE SOUZA"),
    "GC - AMANDA APARECIDA DIMARTINI": ("GR - AMANDA APARECIDA DIMARTINI OLIVEIRA", "SUP. CASSIANO JOSE DE SOUZA"),
    "GC - SUL": ("GR - DENIO DA SILVEIRA VIÇOSA", "SUP. CASSIANO JOSE DE SOUZA")
}
COMERCIAIS = sorted(HIERARQUIA_COMERCIAL.keys())

# =========================================================
# FICHAS / CHECKLISTS
# =========================================================

DADOS_EMPRESA_GERAL = [
    "RAZAO SOCIAL", "CNPJ", "QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO",
    "GERENTE COMERCIAL LEV", "GERENTE REGIONAL LEV", "HEAD LEV", "ENDEREÇO COMERCIAL - RUA",
    "ENDEREÇO COMERCIAL - Nº", "ENDEREÇO COMERCIAL - COMPLEMENTO", "ENDEREÇO COMERCIAL - BAIRRO",
    "ENDEREÇO COMERCIAL - CIDADE", "ENDEREÇO COMERCIAL - UF", "ENDEREÇO COMERCIAL - CEP",
    "NOME SÓCIO 1", "CPF SÓCIO 1", "RG SÓCIO 1", "ORGÃO EXPEDIDOR SÓCIO 1", "DATA NASCIMENTO SÓCIO 1",
    "ESTADO CIVIL SÓCIO 1", "TELEFONE PARA CONTATO SÓCIO 1", "ENDEREÇO RESIDENCIAL - RUA",
    "ENDEREÇO RESIDENCIAL - Nº", "ENDEREÇO RESIDENCIAL - COMPLEMENTO", "ENDEREÇO RESIDENCIAL - BAIRRO",
    "ENDEREÇO RESIDENCIAL - CIDADE", "ENDEREÇO RESIDENCIAL - UF", "ENDEREÇO RESIDENCIAL - CEP",
    "E-mail do responsável para assinatura/sócio", "E-mail jurídico", "E-mail comercial",
    "DADOS BANCÁRIOS EMPRESA - BANCO", "DADOS BANCÁRIOS EMPRESA - AGENCIA", "DADOS BANCÁRIOS EMPRESA - CONTA",
    "TITULARIDADE DA CONTA - TIPO", "TITULARIDADE DA CONTA - NOME OU RAZÃO SOCIAL",
    "TITULARIDADE DA CONTA - CPF OU CNPJ", "TIPO DE CONTA"
]

ANALISE_INTERNA_FIELDS = [
    "CADASTRO DE CONTA CORRENTE CASH FLOW", "DOCUMENTO DE IDENTIFICAÇÃO E VALIDAÇÃO ANTIFRAUDE - ACERTPIX",
    "CARTÃO CNPJ / CERTIFICADO MEI / CONTRATO SOCIAL - RECEITA FEDERAL", "COMPROVANTE DE ENDEREÇO RESIDENCIAL",
    "COMPROVANTE DE ENDEREÇO COMERCIAL", "COMPROVANTE DE DADOS BANCÁRIOS", "PESQUISA NO CONTROL CENTER",
    "PRA POSITIVO EM DÍVIDA ANEC - SOLICITAR DE ACORDO", "CONSULTA DE VÍNCULO POR NOME/CPF A OUTROS CÓDIGOS",
    "POSSUI DÍVIDA ACERTPIX?", "CONTRATO ENVIADO?", "DECLARAÇÃO DE ENDEREÇO ENVIADA?",
    "TERMO DE INDICAÇÃO ENVIADO?", "AUTORIZAÇÃO PARA CONTA DE TERCEIROS?"
]

CHECKLIST_BANCOS = {
    "FACTA": ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "HOME OFFICE?", "POSSUI FILIAIS? SE SIM, QUANTAS?", "QUANTIDADE DE FUNCIONÁRIOS CLT?", "ESTIMATIVA DE PRODUÇÃO PARA O BANCO", "LOJA OU CALLCENTER?", "ATUA WITH PRODUÇÃO DE TERCEIROS NÃO FUNCIONÁRIOS?", "SALÁRIO (RENDA MENSAL)", "TIPO FISCAL (SIMPLES, REAL OU PRESUMIDO)", "ESTADO CIVIL"],
    "AKI CAPITAL": ["RAZAO SOCIAL", "CNPJ", "QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "GERENTE COMERCIAL LEV", "GERENTE REGIONAL LEV", "HEAD LEV"],
    "NOVO SAQUE": ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "QUAL O @ DO INSTAGRAM DA EMPRESA?", "PREFERE RECEBER CMS VIA PIX OU DADOS BANCARIOS?", "CHAVE PIX", "COMO CONHECEU A NOVO SAQUE?", "QUAL SEU MODELO DE NEGOCIO?", "QUAL CANAL DE CAPTAÇÃO?", "PRODUTOS QUE DESEJA OPERAR?", "POSSUI VENDEDORES? QUANTOS?"],
    "HOPE": ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "QUANTIDADE DE COLABORADORES", "QUAL A CHAVE PIX?", "3 PRINCIPAIS BANCOS QUE OPERA", "PRODUÇÃO MÉDIA AO MÊS"],
    "QUALIBANK": ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "QUAL A CHAVE PIX?", "E-MAIL COMISSÃO", "E-MAIL CONTESTAÇÃO", "E-MAIL COMUNICADOS"],
    "C6 BANK": ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "E-MAIL ASSUNTOS ADMINISTRATIVOS E OPERACIONAIS", "E-MAIL PARA ENVIO DE FÍSICO (ACCESS - PROTOCOLAR)", "E-MAIL CONTESTAÇÃO", "E-MAIL COMISSÃO (SUB BANCO)", "E-MAIL NOTA FISCAL (SUB BANCO)", "PRODUÇÃO ESTIMADA", "QUANTOS ATENDENTES?", "IRÁ TRABALHAR WITH O CAR EQUITY?"],
    "SAFRA": ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "POSSUI ATENDENTE? SE SIM, QUANTOS?", "POSSUI FILIAIS? SE SIM, QUANTAS?", "QUAL ESTIMATIVA DE PRODUÇÃO PRÓPRIA?", "QUAL ESTIMATIVA DE PRODUÇÃO PARA O BANCO?", "QUAIS INSTITUIÇÕES FINANCEIRAS (BANCOS) QUE TRABALHAM?", "QUAIS OS PRINCIPAIS CONVÊNIOS QUE ATUAM?", "PROCESSO SERÁ FÍSICO OU DIGITAL?", "POSSUI ASSINATURA DIGITAL?"],
    "BMG": ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "QUAL A RENDA MENSAL?", "QUAIS INSTITUIÇÕES FINANCEIRAS (BANCOS) QUE TRABALHAM?", "QUANTIDADE DE FUNCIONÁRIOS?", "QUAL ESTIMATIVA DE PRODUÇÃO PARA O BANCO?", "HAVERÁ VENDA DE CONSÓRCIO?", "HAVERÁ VENDA DE SEGUROS?", "TRATA-SE DE CALL CENTER?"],
    "ICRED": ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "QUAIS INSTITUIÇÕES FINANCEIRAS (BANCOS) QUE TRABALHAM?", "PRODUÇÃO MÉDIA AO MÊS", "QUAIS OS PRINCIPAIS CONVÊNIOS QUE ATUAM?", "QUANTOS ATENDENTES?"],
    "DAYCOVAL": ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "QUAL A PRODUÇÃO MÉDIA MENSAL COM O BANCO?", "QUAIS OS PRINCIPAIS CONVÊNIOS QUE ATUAM?", "QUANTIDADE DE FUNCIONÁRIOS CLT?", "FAÇA UM BREVE HISTÓRICO SOBRE A EMPRESA", "NECESSIDADES DO CORRESPONDENTE", "QUAIS INSTITUIÇÕES FINANCEIRAS (BANCOS) QUE TRABALHAM?", "PROCESSO SERÁ FÍSICO OU DIGITAL?", "POSSUI CERTIFICADO DIGITAL?"],
    "PAN": ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "POTENCIAL DE VENDAS EM MÉDIA AO MÊS?", "QUAIS INSTITUIÇÕES FINANCEIRAS (BANCOS) QUE TRABALHAM?", "QUANTIDADE DE FUNCIONÁRIOS?", "QUAIS OS PRINCIPAIS CONVÊNIOS QUE OPERA?", "POSSUI ASSINATURA DIGITAL?", "OBRIGATÓRIO E-MAIL DE DOMÍNIO PRIVADO"]
}

# =========================================================
# ESTRUTURA DE BASE E COLUNAS
# =========================================================

BASE_COLUMNS = [
    "Ticket#", "Prazo Banco", "Razão Social", "CNPJ Sub", "Tipo Credenciamento",
    "Modalidade", "Banco", "Responsável", "Recepção E-mail", "1º Envio Banco",
    "Ultima atuação", "Finalização Estimada", "Data de Conclusão", "Cumprimento do Prazo Geral",
    "Verificador", "Fase", "Status", "Cumprimento do Prazo Banco", "Telefone Sub",
    "Cópia de contrato Banco", "CPS - LEV", "Termo Usuario Master", "Comercial",
    "Regional", "Head", "Cód WB"
]

FICHAS_COLUMNS = ["Ticket#", "Ficha Banco JSON", "Dados Empresa JSON", "Análise Interna JSON"]
COLUNAS_GRADE_PRINCIPAL = BASE_COLUMNS.copy()

ALIASES_COLUNAS = {
    "Última atuação": "Ultima atuação",
    "CNPJ": "CNPJ Sub",
    "Ticket": "Ticket#",
    "PrazoBanco": "Prazo Banco"
}

def normalizar_status(val):
    return str(val).strip().lower()

# --- NOVA FUNÇÃO DE CÁLCULO DE PRAZOS AUTOMÁTICOS ---
def atualizar_prazos_da_base(df):
    df['Recepção E-mail'] = pd.to_datetime(df['Recepção E-mail'], errors='coerce')
    df['1º Envio Banco'] = pd.to_datetime(df['1º Envio Banco'], errors='coerce')
    df['Data de Conclusão'] = pd.to_datetime(df['Data de Conclusão'], errors='coerce')
    
    SLA_GERAL_PADRAO = 5
    hoje = pd.to_datetime(datetime.now().date())

    def avaliar_linha(row):
        data_final_geral = row['Data de Conclusão'] if pd.notna(row['Data de Conclusão']) else hoje
        
        if pd.notna(row['Recepção E-mail']):
            dias_geral = (data_final_geral - row['Recepção E-mail']).days
            if pd.notna(row['Data de Conclusão']):
                status_geral = 'No Prazo' if dias_geral <= SLA_GERAL_PADRAO else 'Atrasado'
            else:
                status_geral = 'Em andamento' if dias_geral <= SLA_GERAL_PADRAO else 'Atrasado'
        else:
            status_geral = 'Sem Recepção E-mail'

        if pd.notna(row['1º Envio Banco']):
            data_final_banco = row['Data de Conclusão'] if pd.notna(row['Data de Conclusão']) else hoje
            dias_banco = (data_final_banco - row['1º Envio Banco']).days
            banco_nome = str(row['Banco']).strip().upper() if pd.notna(row['Banco']) else ""
            prazo_banco = BANCOS_PRAZO.get(banco_nome, 5)
            
            if pd.notna(row['Data de Conclusão']):
                status_banco = 'No Prazo' if dias_banco <= prazo_banco else 'Atrasado'
            else:
                status_banco = 'Em andamento' if dias_banco <= prazo_banco else 'Atrasado'
        else:
            status_banco = 'Não enviado ao banco'
            
        return pd.Series([status_geral, status_banco])

    df[['Cumprimento do Prazo Geral', 'Cumprimento do Prazo Banco']] = df.apply(avaliar_linha, axis=1)
    return df

# =========================================================
# UTILITÁRIOS / REGRAS AUTOMÁTICAS
# =========================================================

def parse_date(value):
    if value is None or pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime().date()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    
    txt = str(value).strip().split(" ")[0]
    if not txt or txt.lower() == "nan" or txt.lower() == "nat":
        return None
        
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(txt, fmt).date()
        except:
            pass
    return None


def fmt_date(value):
    d = parse_date(value)
    return d.strftime("%d-%m-%Y") if d else ""


def normalize_id(value):
    if pd.isna(value):
        return ""
    s = str(value).strip()
    if s.lower() == "nan":
        return ""
    if s.endswith(".0"):
        s = s[:-2]
    return s


def normalize_bank(bank):
    if bank is None:
        return ""
    bank = normalize_id(bank).upper()
    aliases = {
        "QUALIBANKING": "QUALIBANK",
        "MEU CASHCARD": "MEU CASH CARD",
        "ANCORA": "ÂNCORA CONSÓRCIO",
        "ANCORA CONSÓRCIO": "ÂNCORA CONSÓRCIO",
        "OLE": "OLÉ"
    }
    return aliases.get(bank, bank)


def get_prazo_banco(bank):
    bank = normalize_bank(bank)
    return BANCOS_PRAZO.get(bank, 0)


def get_modalidades_banco(bank):
    bank = normalize_bank(bank)
    return MODALIDADES_POR_BANCO.get(bank, ["SUB BANCO", "SUB ZERO", "INDICADO BANCO", "LEV - MASTER", "NÃO INFORMADO"])


def get_checklist_banco(bank):
    bank = normalize_bank(bank)
    return CHECKLIST_BANCOS.get(bank, ["QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO"])


def get_hierarquia(comercial):
    if comercial in HIERARQUIA_COMERCIAL:
        return HIERARQUIA_COMERCIAL[comercial]
    return "", ""


def to_excel_bytes(df_dict):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        if isinstance(df_dict, dict):
            for nome, dfx in df_dict.items():
                dfx.to_excel(writer, index=False, sheet_name=nome[:31])
        else:
            df_dict.to_excel(writer, index=False, sheet_name="Dados")
    output.seek(0)
    return output.getvalue()


def ensure_base_columns(df):
    if df is None or df.empty:
        df = pd.DataFrame(columns=BASE_COLUMNS)
    for col in BASE_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[BASE_COLUMNS]


def ensure_fichas_columns(df):
    if df is None or df.empty:
        df = pd.DataFrame(columns=FICHAS_COLUMNS)
    for col in FICHAS_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df[FICHAS_COLUMNS]


def aplicar_aliases_colunas(df):
    if df is None or df.empty:
        return pd.DataFrame(columns=BASE_COLUMNS)
    rename_map = {}
    for col in df.columns:
        if col in ALIASES_COLUNAS:
            rename_map[col] = ALIASES_COLUNAS[col]
    if rename_map:
        df = df.rename(columns=rename_map)
    return df


def limpar_base(df):
    if df is None or df.empty:
        return ensure_base_columns(pd.DataFrame(columns=BASE_COLUMNS))

    df = aplicar_aliases_colunas(df)
    df = ensure_base_columns(df).copy()
    df = df.fillna("")

    texto_cols = [
        "Ticket#", "Razão Social", "CNPJ Sub", "Banco", "Modalidade", "Status",
        "Fase", "Comercial", "Cód WB", "Recepção E-mail", "1º Envio Banco",
        "Ultima atuação", "Data de Conclusão", "Telefone Sub",
        "Cópia de contrato Banco", "CPS - LEV", "Termo Usuario Master"
    ]
    for col in texto_cols:
        if col in df.columns:
            df[col] = df[col].apply(normalize_id)

    if "Prazo Banco" in df.columns:
        df["Prazo Banco"] = df["Prazo Banco"].apply(lambda x: int(x) if str(x).strip().isdigit() else x)

    df = df[df["Ticket#"].astype(str).str.strip() != ""]
    df = df[df["Ticket#"].astype(str).str.lower() != "nan"]

    return df.reset_index(drop=True)


def calcular_finalizacao_estimada(row):
    banco = normalize_bank(row.get("Banco", ""))
    prazo = get_prazo_banco(banco)
    base_data = (
        parse_date(row.get("1º Envio Banco")) or
        parse_date(row.get("Recepção E-mail")) or
        parse_date(row.get("Ultima atuação"))
    )
    if base_data and prazo:
        return fmt_date(base_data + timedelta(days=prazo))
    return ""


def calcular_verificador(status, ultima_atuacao):
    status_txt = str(status).strip().lower()
    if status_txt != "em andamento":
        return "EM DIA"
        
    let_ult = parse_date(ultima_atuacao)
    if let_ult == date.today() or str(ultima_atuacao).strip() == date.today().strftime("%d-%m-%Y"):
        return "EM DIA"
        
    if let_ult is None:
        return "A COBRAR"
        
    dias = (date.today() - let_ult).days
    if dias > 2:
        return "A COBRAR"
    return "EM DIA"


def calcular_prazo_geral(row):
    data_recepcao = parse_date(row.get("Recepção E-mail"))
    data_conclusao = parse_date(row.get("Data de Conclusão"))
    status = normalize_id(row.get("Status", ""))
    
    if data_recepcao is None:
        return ""
        
    SLA_GERAL_PADRAO = 5
    prazo_limite = data_recepcao + timedelta(days=SLA_GERAL_PADRAO)
    
    if status in ["Concluído", "Cancelado"] and data_conclusao is not None:
        return "ATRASADO" if data_conclusao > prazo_limite else "EM DIA"
    return "ATRASADO" if date.today() > prazo_limite else "EM ANDAMENTO"


def calcular_prazo_banco(row):
    data_envio = parse_date(row.get("1º Envio Banco"))
    data_conclusao = parse_date(row.get("Data de Conclusão"))
    status = normalize_id(row.get("Status", ""))
    
    if data_envio is None:
        return "Não enviado ao banco"
        
    banco = normalize_bank(row.get("Banco", ""))
    prazo_limite_banco = get_prazo_banco(banco)
    prazo_limite = data_envio + timedelta(days=prazo_limite_banco)
    
    if status in ["Concluído", "Cancelado"] and data_conclusao is not None:
        return "ATRASADO" if data_conclusao > prazo_limite else "EM DIA"
    return "ATRASADO" if date.today() > prazo_limite else "EM ANDAMENTO"


def apply_auto_rules(df):
    df = df.copy()

    for col in BASE_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df["Banco"] = df["Banco"].apply(normalize_bank)
    df["Prazo Banco"] = df["Banco"].apply(get_prazo_banco)

    regionais = []
    heads = []
    for _, row in df.iterrows():
        reg, hd = get_hierarquia(row.get("Comercial", ""))
        regionais.append(reg)
        heads.append(hd)
    df["Regional"] = regionais
    df["Head"] = heads

    hoje_str = fmt_date(date.today())
    for idx, row in df.iterrows():
        fase_atual = str(row["Fase"]).strip()
        
        if fase_atual == "Finalizado: Código criado":
            df.at[idx, "Status"] = "Concluído"
            if not str(row["Data de Conclusão"]).strip():
                df.at[idx, "Data de Conclusão"] = hoje_str
        elif fase_atual.startswith("Cancelado:"):
            df.at[idx, "Status"] = "Cancelado"
            if not str(row["Data de Conclusão"]).strip():
                df.at[idx, "Data de Conclusão"] = hoje_str
        else:
            df.at[idx, "Status"] = "Em andamento"
            df.at[idx, "Data de Conclusão"] = ""

    df["Finalização Estimada"] = df.apply(calcular_finalizacao_estimada, axis=1)
    df["Verificador"] = df.apply(lambda x: calcular_verificador(x.get("Status", ""), x.get("Ultima atuação", "")), axis=1)
    df["Cumprimento do Prazo Banco"] = df.apply(calcular_prazo_banco, axis=1)
    df["Cumprimento do Prazo Geral"] = df.apply(calcular_prazo_geral, axis=1)

    return df


def carregar_abas_historico(caminho):
    historico_padrao = pd.DataFrame(columns=["Ticket#", "Campo", "Valor Antigo", "Valor Novo", "Usuário", "Data/Hora"])
    fichas_padrao = pd.DataFrame(columns=FICHAS_COLUMNS)
    try:
        if not os.path.exists(caminho):
            return historico_padrao, fichas_padrao

        xls = pd.ExcelFile(caminho, engine="openpyxl")
        hist = pd.read_excel(caminho, sheet_name="Historico", engine="openpyxl") if "Historico" in xls.sheet_names else historico_padrao
        fichas = pd.read_excel(caminho, sheet_name="Fichas", engine="openpyxl") if "Fichas" in xls.sheet_names else fichas_padrao
        return hist, fichas
    except:
        return historico_padrao, fichas_padrao


def salvar_historico_e_fichas(df_hist, df_fichas):
    df_fichas = ensure_fichas_columns(df_fichas)
    try:
        with pd.ExcelWriter(ARQUIVO_HIST, engine="openpyxl") as writer:
            df_hist.to_excel(writer, index=False, sheet_name="Historico")
            df_fichas.to_excel(writer, index=False, sheet_name="Fichas")
    except PermissionError:
        st.error("⚠️ Não foi possível salvar! O arquivo **historico_sub.xlsx** está aberto no Excel. Feche a planilha e tente novamente.")
        st.stop()


def salvar_base(df):
    df = limpar_base(df)
    df = ensure_base_columns(df)
    df = apply_auto_rules(df)
    try:
        df.to_excel(ARQUIVO_BASE, index=False)
    except PermissionError:
        st.error("⚠️ Não foi possível salvar! O arquivo **base_sub.xlsx** está aberto no Excel. Feche a planilha e tente novamente.")
        st.stop()


def registrar_historico(df_hist, df_fichas, ticket, campo, valor_antigo, valor_novo):
    novo_hist = pd.DataFrame([{
        "Ticket#": normalize_id(ticket),
        "Campo": campo,
        "Valor Antigo": valor_antigo,
        "Valor Novo": valor_novo,
        "Usuário": st.session_state.usuario,
        "Data/Hora": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }])
    df_hist = pd.concat([df_hist, novo_hist], ignore_index=True)
    salvar_historico_e_fichas(df_hist, df_fichas)
    return df_hist


def salvar_ficha_ticket(df_fichas, ticket, ficha_banco, dados_empresa, analise):
    tk = normalize_id(ticket)
    novo = pd.DataFrame([{
        "Ticket#": tk,
        "Ficha Banco JSON": json.dumps(ficha_banco, ensure_ascii=False),
        "Dados Empresa JSON": json.dumps(dados_empresa, ensure_ascii=False),
        "Análise Interna JSON": json.dumps(analise, ensure_ascii=False)
    }])
    df_fichas = df_fichas[df_fichas["Ticket#"].apply(normalize_id) != tk]
    df_fichas = pd.concat([df_fichas, novo], ignore_index=True)
    return ensure_fichas_columns(df_fichas)


def resetar_base_vazia():
    df_vazio = pd.DataFrame(columns=BASE_COLUMNS)
    salvar_base(df_vazio)
    return df_vazio

# =========================================================
# CARREGAMENTO INICIAL DOS DADOS
# =========================================================

df = None
try:
    if os.path.exists(ARQUIVO_BASE):
        df = pd.read_excel(ARQUIVO_BASE, engine="openpyxl")
except:
    df = None

df = limpar_base(df)
df = ensure_base_columns(df)
df = apply_auto_rules(df)

df_hist, df_fichas = carregar_abas_historico(ARQUIVO_HIST)
df_fichas = ensure_fichas_columns(df_fichas)

# --- FLUXO PRINCIPAL DE CONTROLE DE TELA (A TRAVA QUE FALTAVA) ---
if not st.session_state.logado:
    login()
    st.stop()  # Força o Streamlit a parar aqui se não estiver logado!

# =========================================================
# MENU DA SIDEBAR PREMIUM (SÓ EXECUTA SE ESTIVER LOGADO)
# =========================================================
from streamlit_option_menu import option_menu

# Aplica o estilo visual na barra lateral e esconde elementos nativos do topo do Streamlit (Deploy, Menu, etc)
st.markdown(
    """
    <style>
        /* Estilização Premium da Sidebar */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 2px solid #6134b2 !important;
        }
        [data-testid="stSidebarHeader"] {
            display: none !important;
        }
        
        /* ESCONDE O TOPO NATIVO (Botão Deploy, Três Pontinhos e Header Cinza) */
        [data-testid="stHeader"], #MainMenu, footer, [data-testid="stMainHeader"] {
            visibility: hidden !important;
            display: none !important;
        }
        
        /* Ajusta o espaçamento do topo do app para não colar na tela */
        .block-container {
            padding-top: 1.5rem !important;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

# Define as opções de texto puras (sem emojis) e mapeia os respectivos ícones profissionais de linha
opcoes_texto = ["Dashboard", "Cadastro", "Base (Editar)", "Fichas e Checklists"]
icones_menu = ["grid-1x2", "plus-circle", "table", "file-earmark-text"]

# Se for Supervisão, adiciona os menus e ícones correspondentes de forma dinâmica
if st.session_state.get("perfil_usuario") == "Supervisão":
    opcoes_texto.append("Histórico")
    icones_menu.append("clock-history")
    
    opcoes_texto.append("Reset / Testes")
    icones_menu.append("trash")

with st.sidebar:
    # Centraliza e ajusta o tamanho da logo no topo do menu lateral
    st.markdown("<div style='text-align: center; padding-top: 10px;'>", unsafe_allow_html=True)
    st.image(r"Z:\SUBSTABELECIDO\Sistema_Sub\Fotos\LOGO LEV ROXO.png", width=110)
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("") # Espaçador estético
    
    # Renderiza o menu profissional com a paleta oficial da LEV e ícones limpos
    menu_selecionado = option_menu(
        menu_title=None, 
        options=opcoes_texto,
        icons=icones_menu,
        default_index=0,
        styles={
            "icon": {"color": "#6134b2", "font-size": "16px"},
            "nav-link": {
                "font-size": "14px", 
                "text-align": "left", 
                "margin": "4px 0px", 
                "padding": "10px 15px",
                "font-family": "sans-serif", 
                "--hover-color": "#f3e8ff",
                "border-radius": "8px"
            },
            "nav-link-selected": {
                "background-color": "#6134b2", 
                "color": "white", 
                "font-weight": "500",
                "border-radius": "8px"
            },
        }
    )

# ---------------------------------------------------------
# BARRA DE TOPO DINÂMICA (HEADER NAVBAR CORPORATIVO)
# ---------------------------------------------------------
# Monta uma barra estilizada idêntica aos exemplos enviados
st.markdown(
    f"""
    <div style="
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 12px 20px; 
        background-color: #f8fafc; 
        border-radius: 10px; 
        margin-bottom: 25px; 
        border-left: 5px solid #6134b2;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        font-family: sans-serif;
    ">
        <div style="font-size: 18px; font-weight: 700; color: #1e293b;">
            {menu_selecionado}
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 13px; color: #64748b; font-weight: 500;">
                {st.session_state.nome_usuario} 
                <span style="color: #6134b2; font-weight: 600; margin-left: 4px;">({st.session_state.perfil_usuario})</span>
            </span>
            <div style="
                width: 32px; 
                height: 32px; 
                background-color: #e2e8f0; 
                border-radius: 50%; 
                display: flex; 
                align-items: center; 
                justify-content: center;
                color: #475569;
                font-size: 14px;
                font-weight: bold;
            ">
                {st.session_state.nome_usuario[0].upper() if st.session_state.nome_usuario else "U"}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Compatibilidade garantida de texto puro para o restante do seu código
# (Se as suas telas usavam o formato antigo com emoji, este mapeamento converte sem quebrar o código abaixo)
mapeamento_retorno = {
    "Dashboard": "📊 Dashboard",
    "Cadastro": "➕ Cadastro",
    "Base (Editar)": "📋 Base (Editar)",
    "Fichas e Checklists": "🧾 Fichas e Checklists",
    "Histórico": "📜 Histórico",
    "Reset / Testes": "🧹 Reset / Testes"
}
menu = mapeamento_retorno.get(menu_selecionado)

# Mantém a sua lógica original de aviso de redirecionamento de filtros intacta
if st.session_state.get("go_to_base") and menu_selecionado != "Base (Editar)":
    st.sidebar.info("Vá para 'Base (Editar)' para ver os tickets filtrados.")

# Botão de logout limpo e corporativo no final da barra lateral
with st.sidebar:
    st.markdown("---")
    if st.button("Sair do Sistema"):
        logout()
# =========================================================
# TELA: DASHBOARD COLABORADOR (REGRAS AVANÇADAS DE SLA E CANCELAMENTO)
# =========================================================

if menu == "📊 Dashboard":
    # 1. Injeta CSS para ajustar títulos, abas e o botão roxo premium
    st.markdown(
        """
        <style>
            h1, .main h1 { font-size: 22px !important; font-weight: 700 !important; color: #1e293b !important; margin-bottom: 5px !important; margin-top: 0px !important; }
            h2, .main h2 { font-size: 15px !important; font-weight: 600 !important; color: #334155 !important; margin-top: 15px !important; margin-bottom: 5px !important; }
            p { font-size: 13px !important; color: #64748b !important; }

            /* Ajuste estético das Abas Principais */
            button[data-baseweb="tab"] {
                font-size: 14px !important;
                font-weight: 600 !important;
                color: #64748b !important;
                padding: 10px 16px !important;
            }
            button[aria-selected="true"] {
                color: #6134b2 !important;
                border-bottom-color: #6134b2 !important;
            }

            /* ⚡ BOTÃO ROXO DE ATUAÇÃO UNIFICADO (PRIMARY) ⚡ */
            button[data-testid="stBaseButton-primary"] {
                background-color: #6134b2 !important;
                border: 1px solid #6134b2 !important;
                color: #ffffff !important;
                padding: 8px 20px !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
                margin-top: 15px !important;
            }
            button[data-testid="stBaseButton-primary"]:hover {
                background-color: #4d2496 !important;
                border-color: #4d2496 !important;
                color: #ffffff !important;
            }
            button[data-testid="stBaseButton-primary"] p,
            button[data-testid="stBaseButton-primary"] span {
                color: #ffffff !important;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    nome_usuario = st.session_state.nome_usuario
    hoje = date.today()
    hoje_str = fmt_date(hoje)

    if df.empty:
        st.info("Base vazia. Vá em Cadastro ou utilize a ferramenta de teste para gerar dados de exemplo.")
        st.stop()

    # --- MAPEAMENTO DE CATEGORIAS FORNECIDO POR VOCÊ ---
    MAPA_CATEGORIAS = {
        "Aguardando Banco: Verificação de assinaturas": "Banco - Processo politica banco",
        "Aguardando Banco: Verificação de Documentos": "Banco - Processo politica banco",
        "Aguardando Banco: Liberação de acessos": "Banco - Processo politica banco",
        "Aguardando Banco: Envio de contrato para assinatura": "Banco - Processo politica banco",
        "Aguardando Banco: Gerar Token/Acesso Documentação": "Banco - Processo politica banco",
        "Aguardando Parceiro: Criação de conta Daycoval": "Banco - Processo politica banco",
        "Aguardando Documentação Triagem: Parceiro": "Triagem",
        "Aguardando Documentação Banco: Parceiro": "Banco - Processo politica banco",
        "Aguardando De acordo Superintendente": "Triagem",
        "Aguardando De acordo Regional": "Triagem",
        "Aguardando De acordo Comercial": "Triagem",
        "Aguardando De acordo Diretoria": "Triagem",
        "Aguardando comercial: Negociação débitos": "Triagem",
        "Aguardando comercial: Modalidade/rateio": "Triagem",
        "Aguardando alinhamento GC Lev e GC Banco": "Banco - Processo politica banco",
        "Fase de Assinaturas: Sub": "Banco - Processo politica banco",
        "Fase de Assinaturas: Lev": "Banco - Processo politica banco",
        "Aguardando Jurídico: Validação Contrato": "Banco - Processo politica banco",
        "Finalizado: Código criado": "Banco - Processo politica banco",
        "Aguardando Banco: Cadastro iniciado": "Banco - Processo politica banco"
    }

    # Preparação da Base com Parsing de Datas Seguro
    df_dash = df.copy()
    df_dash["Ultima atuação DT"] = df_dash["Ultima atuação"].apply(parse_date)
    df_dash["Recepção E-mail DT"] = df_dash["Recepção E-mail"].apply(parse_date)
    df_dash["Categoria Fase"] = df_dash["Fase"].map(MAPA_CATEGORIAS).fillna("Sem categoria")
    
    # Filtra os tickets EXCLUSIVOS do usuário logado
    meus = df_dash[df_dash["Responsável"] == nome_usuario].copy()

    # --- TÍTULO E SUBTÍTULO ---
    st.markdown("<h1>Dashboard de Atividades</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin-bottom: 15px;'>Seja bem-vindo, <b>{nome_usuario}</b>. Gerencie suas demandas abaixo.</p>", unsafe_allow_html=True)

    # --- CÁLCULO DOS CARDS INICIAIS ---
    card_a_cobrar = len(meus[meus["Verificador"] == "A COBRAR"])
    
    ontem = hoje - timedelta(days=1)
    card_vencendo_amanha = len(meus[
        (meus["Status"].apply(normalizar_status) == normalizar_status("Em andamento")) &
        (meus["Ultima atuação DT"] == ontem)
    ])
    
    card_em_andamento = len(meus[meus["Status"].apply(normalizar_status) == normalizar_status("Em andamento")])

    # --- GRID DE CARDS PREMIUM ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div style="background-color: #fff5f5; padding: 12px; border-radius: 8px; border-left: 4px solid #ef4444; min-height: 65px;"><span style="font-size: 11px; font-weight: 600; color: #991b1b; display: block; margin-bottom: 2px;">SUAS A COBRAR</span><span style="font-size: 24px; font-weight: 700; color: #1e293b; line-height: 1;">{card_a_cobrar}</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div style="background-color: #fffbeb; padding: 12px; border-radius: 8px; border-left: 4px solid #f59e0b; min-height: 65px;"><span style="font-size: 11px; font-weight: 600; color: #92400e; display: block; margin-bottom: 2px;">VENCENDO AMANHÃ</span><span style="font-size: 24px; font-weight: 700; color: #1e293b; line-height: 1;">{card_vencendo_amanha}</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div style="background-color: #faf5ff; padding: 12px; border-radius: 8px; border-left: 4px solid #a855f7; min-height: 65px;"><span style="font-size: 11px; font-weight: 600; color: #6b21a8; display: block; margin-bottom: 2px;">TOTAL EM ANDAMENTO</span><span style="font-size: 24px; font-weight: 700; color: #1e293b; line-height: 1;">{card_em_andamento}</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ABAS PRINCIPAIS ---
    aba_cobrancas, aba_atrasos, aba_metricas = st.tabs([
        "🎯 Cobranças", 
        "⚠️ Alerta de Atrasos e Riscos", 
        "📈 Meu Desempenho"
    ])

    df_flegados_hoje = pd.DataFrame()
    df_flegados_radar = pd.DataFrame()
    df_flegados_triagem = pd.DataFrame()
    df_flegados_cancelamento = pd.DataFrame()

    # =========================================================
    # TAB 1: COBRANÇAS
    # =========================================================
    with aba_cobrancas:
        qtd_feita_hoje = 0
        if not df_hist.empty:
            try: qtd_feita_hoje = len(df_hist[(df_hist["Operador"] == nome_usuario) & (df_hist["Data Movimento"] == hoje_str)])
            except: pass

        col_sub, col_meta = st.columns([2, 1])
        with col_sub: st.markdown("<p style='font-style: italic; margin-top:5px;'>Filtre por Banco para focar as cobranças em portais específicos.</p>", unsafe_allow_html=True)
        with col_meta: st.markdown(f"<div style='text-align:right; font-size:12px; color:#166534; background-color:#f0fdf4; padding:4px 10px; border-radius:6px; display:inline-block; float:right;'><b>Hoje:</b> {qtd_feita_hoje} atualizações realizadas 🎉</div>", unsafe_allow_html=True)

        bancos_disponiveis = sorted(list(meus["Banco"].dropna().unique()))
        banco_selecionado = st.selectbox("Filtrar por Banco:", ["Todos os Bancos"] + bancos_disponiveis, key="sb_banco_cobrancas")

        meus_cobrancas = meus.copy()
        if banco_selecionado != "Todos os Bancos":
            meus_cobrancas = meus_cobrancas[meus_cobrancas["Banco"] == banco_selecionado].copy()

        minhas_cobrancas_ativas = meus_cobrancas[meus_cobrancas["Verificador"] == "A COBRAR"].copy()
        meus_vencendo_amanha = meus_cobrancas[(meus_cobrancas["Status"].apply(normalizar_status) == normalizar_status("Em andamento")) & (meus_cobrancas["Ultima atuação DT"] == ontem)].copy()

        # Seção Urgências
        st.markdown(f"<h2>🚨 Urgências de Hoje ({len(minhas_cobrancas_ativas)})</h2>", unsafe_allow_html=True)
        if not minhas_cobrancas_ativas.empty:
            df_edit_hoje = minhas_cobrancas_ativas[["Ticket#", "Razão Social", "Banco", "Fase", "Status", "Ultima atuação"]].copy()
            df_edit_hoje.insert(0, "Cobrar?", False)
            edited_hoje = st.data_editor(df_edit_hoje, column_config={"Cobrar?": st.column_config.CheckboxColumn("Cobrar?", default=False), "Ticket#": st.column_config.TextColumn("Ticket#", disabled=True), "Razão Social": st.column_config.TextColumn("Razão Social", disabled=True), "Banco": st.column_config.TextColumn("Banco", disabled=True), "Ultima atuação": st.column_config.TextColumn("Última atuação", disabled=True), "Fase": st.column_config.SelectboxColumn("Fase", options=FASES, required=True), "Status": st.column_config.TextColumn("Status", disabled=True)}, hide_index=True, width="stretch", key="editor_cobrancas_hoje")
            df_flegados_hoje = edited_hoje[edited_hoje["Cobrar?"] == True]
        else:
            st.success("Tudo limpo por aqui hoje!")

        # Seção Radar
        st.markdown(f"<h2>🔮 Antecipar Amanhã ({len(meus_vencendo_amanha)})</h2>", unsafe_allow_html=True)
        if not meus_vencendo_amanha.empty:
            df_edit_radar = meus_vencendo_amanha[["Ticket#", "Razão Social", "Banco", "Fase", "Status", "Ultima atuação"]].copy()
            df_edit_radar.insert(0, "Cobrar?", False)
            edited_radar = st.data_editor(df_edit_radar, column_config={"Cobrar?": st.column_config.CheckboxColumn("Cobrar?", default=False), "Ticket#": st.column_config.TextColumn("Ticket#", disabled=True), "Razão Social": st.column_config.TextColumn("Razão Social", disabled=True), "Banco": st.column_config.TextColumn("Banco", disabled=True), "Ultima atuação": st.column_config.TextColumn("Última atuação", disabled=True), "Fase": st.column_config.SelectboxColumn("Fase", options=FASES, required=True), "Status": st.column_config.TextColumn("Status", disabled=True)}, hide_index=True, width="stretch", key="editor_cobrancas_radar")
            df_flegados_radar = edited_radar[edited_radar["Cobrar?"] == True]
        else:
            st.info("Nenhum processo no radar para amanhã.")

    # =========================================================
    # TAB 2: ALERTA DE ATRASOS E RISCOS (SLA & REGRAS DO PRODUTOR)
    # =========================================================
    with aba_atrasos:
        # --- REGRA 1: RETIDOS NA TRIAGEM (Categoria "Triagem" e Sem 1º Envio Banco) ---
        st.markdown("<h2>🛑 Retidos na Triagem (Risco de Início de Prazo)</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom:10px;'>Processos travados internamente que <b>nunca foram enviados ao banco</b> enquanto o tempo está correndo.</p>", unsafe_allow_html=True)
        
        retidos_triagem = meus[
            (meus["Categoria Fase"] == "Triagem") & 
            ((meus["1º Envio Banco"].isna()) | (meus["1º Envio Banco"].astype(str).str.strip() == "")) &
            (meus["Status"].apply(normalizar_status) == normalizar_status("Em andamento"))
        ].copy()
        
        if not retidos_triagem.empty:
            # Calcula Dias na Triagem baseado na Recepção do E-mail
            retidos_triagem["Dias na Triagem"] = retidos_triagem["Recepção E-mail DT"].apply(lambda d: (hoje - d).days if pd.notna(d) else 0)
            
            df_edit_triagem = retidos_triagem[["Ticket#", "Razão Social", "Banco", "Fase", "Dias na Triagem", "Recepção E-mail"]].copy()
            df_edit_triagem.insert(0, "Atuar?", False)
            
            edited_triagem = st.data_editor(
                df_edit_triagem,
                column_config={
                    "Atuar?": st.column_config.CheckboxColumn("Atuar?", default=False),
                    "Ticket#": st.column_config.TextColumn("Ticket#", disabled=True),
                    "Razão Social": st.column_config.TextColumn("Razão Social", disabled=True),
                    "Banco": st.column_config.TextColumn("Banco", disabled=True),
                    "Dias na Triagem": st.column_config.NumberColumn("Dias Corridos", format="%d dias", disabled=True),
                    "Recepção E-mail": st.column_config.TextColumn("Data Recepção", disabled=True),
                    "Fase": st.column_config.SelectboxColumn("Fase", options=FASES, required=True),
                },
                hide_index=True, width="stretch", key="editor_risco_triagem"
            )
            df_flegados_triagem = edited_triagem[edited_triagem["Atuar?"] == True]
        else:
            st.success("Excelente! Nenhum processo retido na Triagem.")

        st.markdown("---")

        # --- REGRA 2: RÉGUA DE CANCELAMENTO POR INÉRCIA DO PARCEIRO (15 DIAS) ---
        st.markdown("<h2>💀 Régua de Cancelamento por Falta de Retorno</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom:10px;'>Processos travados aguardando o parceiro. Com 12 a 14 dias entra em aviso prévio; com <b>15 dias ou mais sem retorno, são listados para Cancelamento</b>.</p>", unsafe_allow_html=True)
        
        fases_inercia = ["Aguardando Documentação Triagem: Parceiro", "Aguardando Documentação Banco: Parceiro"]
        processos_inercia = meus[
            (meus["Fase"].isin(fases_inercia)) & 
            (meus["Status"].apply(normalizar_status) == normalizar_status("Em andamento"))
        ].copy()
        
        if not processos_inercia.empty:
            # Calcula dias sem alteração baseado na última atuação de cobrança realizada
            processos_inercia["Dias sem Retorno"] = processos_inercia["Ultima atuação DT"].apply(lambda d: (hoje - d).days if pd.notna(d) else 0)
            
            # Filtra somente quem entrou no gatilho crítico da régua (A partir de 12 dias)
            regua_critica = processos_inercia[processos_inercia["Dias sem Retorno"] >= 12].copy()
            
            if not regua_critica.empty:
                def definir_alerta_cancelamento(dias):
                    if dias >= 15: return "🔴 CANCELAR HOJE"
                    return f"⚠️ Aviso Prévio ({15 - dias}d restantes)"
                    
                regua_critica["Prazo/Ação"] = regua_critica["Dias sem Retorno"].apply(definir_alerta_cancelamento)
                
                df_edit_cancelamento = regua_critica[["Ticket#", "Razão Social", "Fase", "Dias sem Retorno", "Prazo/Ação"]].copy()
                df_edit_cancelamento.insert(0, "Confirmar?", False)
                
                edited_cancelamento = st.data_editor(
                    df_edit_cancelamento,
                    column_config={
                        "Confirmar?": st.column_config.CheckboxColumn("Confirmar?", default=False),
                        "Ticket#": st.column_config.TextColumn("Ticket#", disabled=True),
                        "Razão Social": st.column_config.TextColumn("Razão Social", disabled=True),
                        "Dias sem Retorno": st.column_config.NumberColumn("Dias em Cobrança", format="%d dias", disabled=True),
                        "Prazo/Ação": st.column_config.TextColumn("Status da Régua", disabled=True),
                        "Fase": st.column_config.SelectboxColumn("Alterar Fase", options=FASES, required=True),
                    },
                    hide_index=True, width="stretch", key="editor_regua_cancelamento"
                )
                df_flegados_cancelamento = edited_cancelamento[edited_cancelamento["Confirmar?"] == True]
            else:
                st.info("Nenhum processo em estágio crítico de cancelamento no momento.")
        else:
            st.success("Tudo perfeito! Nenhum parceiro em inércia de documentos.")

    # =========================================================
    # TAB 3: MEU DESEMPENHO
    # =========================================================
    with aba_metricas:
        st.markdown("<h2>📈 Seus Indicadores Gerais</h2>", unsafe_allow_html=True)
        total_meus = len(meus)
        ativos_meus = card_em_andamento
        concluidos_meus = len(meus[meus["Status"].apply(normalizar_status) == normalizar_status("Concluído")])
        
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Seus Processos Ativos", ativos_meus)
        with m2: st.metric("Seus Processos Concluídos (Total)", concluidos_meus)
        with m3: st.metric("Total sob sua Responsabilidade", total_meus)

    # =========================================================
    # PROCESSAMENTO CENTRALIZADO DE SALVAMENTO (BOTÃO ROXO)
    # =========================================================
    lista_atualizacoes = []
    if not df_flegados_hoje.empty: lista_atualizacoes.append(df_flegados_hoje[["Ticket#", "Fase"]])
    if not df_flegados_radar.empty: lista_atualizacoes.append(df_flegados_radar[["Ticket#", "Fase"]])
    if not df_flegados_triagem.empty: lista_atualizacoes.append(df_flegados_triagem[["Ticket#", "Fase"]])
    if not df_flegados_cancelamento.empty: lista_atualizacoes.append(df_flegados_cancelamento[["Ticket#", "Fase"]])

    if lista_atualizacoes:
        df_total_flegados = pd.concat(lista_atualizacoes, ignore_index=True)
        qtd_total = len(df_total_flegados)
        
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        if st.button(f"⚡ Salvar e Atualizar os {qtd_total} Processos Selecionados", type="primary"):
            alteracoes = 0
            for idx, row in df_total_flegados.iterrows():
                tk = str(row["Ticket#"])
                nova_fase = row["Fase"]
                
                # Regras automáticas de Status baseados na Fase selecionada
                if nova_fase == "Finalizado: Código criado":
                    novo_status = "Concluído"
                elif nova_fase.startswith("Cancelado:"):
                    novo_status = "Cancelado"
                else:
                    novo_status = "Em andamento"
                
                match_idx = df[df["Ticket#"].astype(str) == tk].index
                if len(match_idx) > 0:
                    orig_idx = match_idx[0]
                    orig_row = df.loc[orig_idx]
                    
                    if str(orig_row["Fase"]) != str(nova_fase):
                        df_hist = registrar_historico(df_hist, df_fichas, tk, "Fase (Via Dashboard)", str(orig_row["Fase"]), str(nova_fase))
                    if str(orig_row["Status"]) != str(novo_status):
                        df_hist = registrar_historico(df_hist, df_fichas, tk, "Status (Via Dashboard)", str(orig_row["Status"]), str(novo_status))
                    
                    if (nova_fase == "Finalizado: Código criado" or nova_fase.startswith("Cancelado:")) and not str(orig_row["Data de Conclusão"]).strip():
                        df.at[orig_idx, "Data de Conclusão"] = hoje_str
                    elif not nova_fase == "Finalizado: Código criado" and not nova_fase.startswith("Cancelado:"):
                        df.at[orig_idx, "Data de Conclusão"] = ""

                    df_hist = registrar_historico(df_hist, df_fichas, tk, "Última atuação (Cobrança)", str(orig_row["Ultima atuação"]), hoje_str)
                    
                    df.at[orig_idx, "Fase"] = nova_fase
                    df.at[orig_idx, "Status"] = novo_status
                    df.at[orig_idx, "Ultima atuação"] = hoje_str
                    alteracoes += 1
            
            if alteracoes > 0:
                salvar_base(df)
                st.success(f"Sucesso! {alteracoes} processos foram processados e salvos!")
                st.rerun()


# =========================================================
# ➕ TELA: CADASTRO NOVO (DESIGN MINIMALISTA & PREMIUM)
# =========================================================

elif menu == "➕ Cadastro":
    # Injeta CSS para acalmar o tamanho das fontes e estilizar o formulário de forma corporativa
    st.markdown(
        """
        <style>
            /* Reduz títulos e textos principais da área de conteúdo */
            h1, .main h1 { font-size: 22px !important; font-weight: 700 !important; color: #1e293b !important; margin-bottom: 5px !important; margin-top: 0px !important; }
            h2, .main h2 { font-size: 16px !important; font-weight: 600 !important; color: #334155 !important; }
            h4, .main h4 { font-size: 14px !important; font-weight: 600 !important; color: #475569 !important; margin-top: 10px !important; margin-bottom: 10px !important; }
            
            /* Mantém os parágrafos gerais limpos, exceto o texto de dentro do botão */
            p { font-size: 13px !important; color: #64748b !important; }
            
            /* Estilização moderna e compacta para os botões de envio do formulário */
            div.stFormSubmitButton > button {
                padding: 8px 16px !important;
                font-size: 13px !important;
                border-radius: 6px !important;
                background-color: #6134b2 !important;
                color: #ffffff !important; /* Força o texto a ficar branco */
                border: 1px solid #6134b2 !important;
                font-weight: 500 !important;
                width: 100% !important;
                transition: background-color 0.2s ease;
            }
            div.stFormSubmitButton > button:hover {
                background-color: #4d2496 !important;
                border-color: #4d2496 !important;
                color: #ffffff !important; /* Mantém o texto branco no hover */
            }
            
            /* Garante que a tag de parágrafo gerada internamente pelo Streamlit no botão fique branca */
            div.stFormSubmitButton > button p {
                color: #ffffff !important;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Título totalmente limpo
    st.markdown("<h1>Novo Cadastro</h1>", unsafe_allow_html=True)

    bancos_disponiveis = sorted(list(BANCOS_PRAZO.keys()))
    banco_selecionado = st.selectbox("Banco", bancos_disponiveis, key="cad_banco")

    modalidades_banco = get_modalidades_banco(banco_selecionado)
    ficha_banco_campos = get_checklist_banco(banco_selecionado)
    prazo_banco = get_prazo_banco(banco_selecionado)

    # Painel informativo customizado
    st.markdown(
        f"""
        <div style="padding: 10px 15px; background-color: #f8fafc; border-left: 4px solid #6134b2; border-radius: 6px; margin-bottom: 20px;">
            <span style="font-size: 13px; color: #475569; font-weight: 500;">
                Banco selecionado: <b style="color: #1e293b;">{banco_selecionado}</b> | Prazo: <b style="color: #6134b2;">{prazo_banco} dias</b>
            </span>
        </div>
        """, 
        unsafe_allow_html=True
    )

    with st.form("form_cadastro_completo", clear_on_submit=False):
        tab1, tab2, tab3, tab4 = st.tabs([
            "Dados do Ticket", 
            "Ficha do Banco", 
            "Dados da Empresa",
            "Validação Antifraude/Interna"
        ])

        with tab1:
            c1, c2, c3 = st.columns(3)
            ticket = c1.text_input("Ticket#")
            razao = c2.text_input("Razão Social")
            
            cnpj_input = c3.text_input("CNPJ Sub", max_chars=18, help="Digite os 14 caracteres (números ou letras)")
            
            cnpj_bruto = "".join(c for c in cnpj_input if c.isalnum()).upper()
            if len(cnpj_bruto) == 14:
                cnpj = f"{cnpj_bruto[0:2]}.{cnpj_bruto[2:5]}.{cnpj_bruto[5:8]}/{cnpj_bruto[8:12]}-{cnpj_bruto[12:14]}"
                cnpj_valido = True
                c3.caption(f"Formatado: {cnpj}")
            elif len(cnpj_bruto) == 0:
                cnpj = ""
                cnpj_valido = True
            else:
                cnpj = cnpj_input
                cnpj_valido = False
                c3.caption("O CNPJ deve ter 14 caracteres.")

            c4, c5, c6 = st.columns(3)
            tipo_cred = c4.selectbox("Tipo Credenciamento", TIPOS_CREDENCIAMENTO)
            modalidade = c5.selectbox("Modalidade", modalidades_banco)
            responsavel = c6.selectbox("Responsável", RESPONSAVEIS)

            c7, c8, c9 = st.columns(3)
            recepcao_email = c7.date_input("Recepção E-mail", value=date.today())
            c8.text_input("1º Envio Banco", value="", disabled=True)
            ultima_atuacao = c9.date_input("Última atuação", value=date.today())

            c10, c11, c12 = st.columns(3)
            telefone_sub = c10.text_input("Telefone Sub")
            fase = c12.selectbox("Fase", FASES, index=0)
            
            if fase == "Finalizado: Código criado":
                status_calculado = "Concluído"
            elif fase.startswith("Cancelado:"):
                status_calculado = "Cancelado"
            else:
                status_calculado = "Em andamento"
                
            c11.text_input("Status (Definido por Travas de Fase)", value=status_calculado, disabled=True)

            c13, c14, c15 = st.columns(3)
            comercial = c13.selectbox("Comercial", [""] + COMERCIAIS)
            regional, head = get_hierarquia(comercial)
            c14.text_input("Regional", value=regional, disabled=True)
            c15.text_input("Head", value=head, disabled=True)

        with tab2:
            st.markdown("<h4>Preencha os dados solicitados pelo banco operacional:</h4>", unsafe_allow_html=True)
            ficha_dados = {}
            for campo in ficha_banco_campos:
                ficha_dados[campo] = st.text_input(campo, key=f"ficha_{campo}")

        with tab3:
            st.markdown("<h4>Informações Cadastrais da Empresa:</h4>", unsafe_allow_html=True)
            empresa_dados = {}
            for campo in DADOS_EMPRESA_GERAL:
                if campo not in ["RAZAO SOCIAL", "CNPJ", "QUAL A MODALIDADE A SER CADASTRADA?", "PERCENTUAL COMISSIONAMENTO", "GERENTE COMERCIAL LEV", "GERENTE REGIONAL LEV", "HEAD LEV"]:
                    empresa_dados[campo] = st.text_input(campo, key=f"emp_{campo}")

        with tab4:
            st.markdown("<h4>Checklist Operacional de Segurança / Validação Interna:</h4>", unsafe_allow_html=True)
            analise_dados = {}
            for campo in ANALISE_INTERNA_FIELDS:
                analise_dados[campo] = st.selectbox(campo, ["", "OK", "Pendente", "Não se aplica"], key=f"cad_ana_{campo}")

        btn_salvar = st.form_submit_button("Salvar Cadastro Completo")

    if btn_salvar:
        tk_s = normalize_id(ticket)
        if not tk_s:
            st.error("O campo Ticket# é obrigatório!")
        elif tk_s in df["Ticket#"].astype(str).values:
            st.error(f"O Ticket# {tk_s} já existe no sistema!")
        elif not cnpj_valido or (cnpj != "" and len(cnpj_bruto) != 14):
            st.error("Não foi possível salvar! O CNPJ informado é inválido. Digite exatamente os 14 caracteres.")
        else:
            ficha_dados["QUAL A MODALIDADE A SER CADASTRADA?"] = modalidade
            ficha_dados["PERCENTUAL COMISSIONAMENTO"] = ""

            empresa_dados["RAZAO SOCIAL"] = razao
            empresa_dados["CNPJ"] = cnpj
            empresa_dados["QUAL A MODALIDADE A SER CADASTRADA?"] = modalidade
            empresa_dados["PERCENTUAL COMISSIONAMENTO"] = ""
            empresa_dados["GERENTE COMERCIAL LEV"] = comercial
            empresa_dados["GERENTE REGIONAL LEV"] = regional
            empresa_dados["HEAD LEV"] = head

            novo_row = {
                "Ticket#": tk_s, "Prazo Banco": prazo_banco, "Razão Social": razao, "CNPJ Sub": cnpj,
                "Tipo Credenciamento": tipo_cred, "Modalidade": modalidade, "Banco": banco_selecionado,
                "Responsável": responsavel, "Recepção E-mail": fmt_date(recepcao_email), "1º Envio Banco": "",
                "Ultima atuação": fmt_date(ultima_atuacao), "Status": status_calculado, "Fase": fase, "Comercial": comercial,
                "Regional": regional, "Head": head, "Telefone Sub": telefone_sub, "Data de Conclusão": "",
                "Cópia de contrato Banco": "", "CPS - LEV": "", "Termo Usuario Master": "", "Cód WB": ""
            }

            df = pd.concat([df, pd.DataFrame([novo_row])], ignore_index=True)
            salvar_base(df)

            df_fichas = salvar_ficha_ticket(df_fichas, tk_s, ficha_dados, empresa_dados, analise_dados)
            df_hist = registrar_historico(df_hist, df_fichas, tk_s, "Criar Ticket", "", f"Criado por {st.session_state.usuario}")
            
            st.success(f"Ticket #{tk_s} cadastrado com sucesso!")
            st.rerun()

# =========================================================
# 📋 TELA: BASE (EDITAR) - DESIGN CORPORATIVO & CLEAN
# =========================================================

elif menu == "📋 Base (Editar)":
    # Injeta CSS para acalmar as fontes e estilizar botões nativos/formulários
    st.markdown(
        """
        <style>
            /* Reduz títulos e textos principais da área de conteúdo */
            h1, .main h1 { font-size: 22px !important; font-weight: 700 !important; color: #1e293b !important; margin-bottom: 5px !important; margin-top: 0px !important; }
            h2, .main h2 { font-size: 16px !important; font-weight: 600 !important; color: #334155 !important; }
            h3, .main h3 { font-size: 15px !important; font-weight: 600 !important; color: #1e293b !important; margin-top: 20px !important; margin-bottom: 10px !important; }
            h4, .main h4 { font-size: 14px !important; font-weight: 600 !important; color: #475569 !important; margin-top: 15px !important; margin-bottom: 10px !important; }
            p, span { font-size: 13px !important; }
            
            /* Estilização para o botão de download e botões de formulário */
            div.stDownloadButton > button, div.stFormSubmitButton > button {
                padding: 8px 16px !important;
                font-size: 13px !important;
                border-radius: 6px !important;
                background-color: #6134b2 !important;
                color: #ffffff !important; /* Texto perfeitamente branco */
                border: 1px solid #6134b2 !important;
                font-weight: 500 !important;
                width: 100% !important;
                transition: background-color 0.2s ease;
            }
            div.stDownloadButton > button:hover, div.stFormSubmitButton > button:hover {
                background-color: #4d2496 !important;
                border-color: #4d2496 !important;
                color: #ffffff !important;
            }
            
            /* Garante que textos internos das tags de parágrafo nos botões fiquem brancos */
            div.stDownloadButton > button p, div.stFormSubmitButton > button p {
                color: #ffffff !important;
            }
            
            /* Estilo secundário para o botão de limpar filtros */
            div.element-container button:has(div[data-testid="stMarkdownContainer"] p:contains("Limpar Filtros Cruzados")) {
                background-color: #f1f5f9 !important;
                color: #475569 !important;
                border: 1px solid #cbd5e1 !important;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Título limpo e profissional
    st.markdown("<h1>Base Operacional de Substabelecidos</h1>", unsafe_allow_html=True)

    if st.session_state.get("go_to_base"):
        filters = st.session_state.get("base_filters", {})
        
        # Painel de filtro ativo no padrão premium
        st.markdown(
            f"""
            <div style="padding: 10px 15px; background-color: #f8fafc; border-left: 4px solid #6134b2; border-radius: 6px; margin-bottom: 15px;">
                <span style="font-size: 13px; color: #475569; font-weight: 500;">
                    Filtro ativo do Dashboard: <b style="color: #1e293b;">{filters}</b>
                </span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Limpar Filtros Cruzados"):
            st.session_state.go_to_base = False
            st.session_state.base_filters = {}
            st.rerun()
        
        df_filtrado = df.copy()
        if "responsavel" in filters:
            df_filtrado = df_filtrado[df_filtrado["Responsável"] == filters["responsavel"]]
        if "verificador" in filters:
            df_filtrado = df_filtrado[df_filtrado["Verificador"] == filters["verificador"]]
        if "status" in filters:
            df_filtrado = df_filtrado[df_filtrado["Status"] == filters["status"]]
    else:
        c1, c2, c3, c4 = st.columns(4)
        f_resp = c1.multiselect("Filtrar Responsável", ["Todos"] + RESPONSAVEIS, default="Todos")
        f_status = c2.multiselect("Filtrar Status", ["Todos"] + STATUS_LISTA, default="Todos")
        f_verif = c3.multiselect("Filtrar Verificador", ["Todos", "EM DIA", "A COBRAR"], default="Todos")
        f_banco = c4.multiselect("Filtrar Banco", ["Todos"] + sorted(list(df["Banco"].unique())), default="Todos")

        df_filtrado = df.copy()
        if "Todos" not in f_resp and f_resp:
            df_filtrado = df_filtrado[df_filtrado["Responsável"].isin(f_resp)]
        if "Todos" not in f_status and f_status:
            df_filtrado = df_filtrado[df_filtrado["Status"].isin(f_status)]
        if "Todos" not in f_verif and f_verif:
            df_filtrado = df_filtrado[df_filtrado["Verificador"].isin(f_verif)]
        if "Todos" not in f_banco and f_banco:
            df_filtrado = df_filtrado[df_filtrado["Banco"].isin(f_banco)]

    # Contador discreto
    st.markdown(f"<p style='color: #64748b; margin-bottom: 15px;'>Total de registros exibidos: <b>{len(df_filtrado)}</b></p>", unsafe_allow_html=True)
    
    st.markdown("<h3>Visualização da Base</h3>", unsafe_allow_html=True)
    st.dataframe(df_filtrado[COLUNAS_GRADE_PRINCIPAL], width="stretch", hide_index=True)

    xlsx_data = to_excel_bytes(df_filtrado)
    st.download_button("📥 Exportar Grade Atual (Excel)", data=xlsx_data, file_name="base_filtrada.xlsx", mime="application/vnd.ms-excel")

    st.markdown("<hr style='margin: 25px 0; border: 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    
    st.markdown("<h3>Selecione um Ticket para Editar</h3>", unsafe_allow_html=True)

    if df_filtrado.empty:
        st.warning("Nenhum ticket encontrado com os parâmetros informados.")
    else:
        lista_opcoes = []
        for _, r in df_filtrado.iterrows():
            lista_opcoes.append(f"{r['Ticket#']} - {r['Razão Social']} ({r['Banco']})")

        selected_option = st.selectbox("Ticket para Edição", lista_opcoes)
        ticket_id = selected_option.split(" - ")[0]

        row_index = df[df["Ticket#"].astype(str) == str(ticket_id)].index[0]
        row_data = df.loc[row_index].to_dict()

        st.markdown(f"<h4>📝 Editando Registro: Ticket# <b>{ticket_id}</b> — {row_data.get('Razão Social', '')} ({row_data.get('Banco', '')})</h4>", unsafe_allow_html=True)

        with st.form(f"form_edit_{ticket_id}"):
            e1, e2 = st.columns(2)
            edit_fase = e1.selectbox("Fase", FASES, index=FASES.index(row_data["Fase"]) if row_data["Fase"] in FASES else 0)
            edit_wb = e2.text_input("Cód WB", value=str(row_data.get("Cód WB", "")))

            e3, e4 = st.columns(2)
            edit_telefone = e3.text_input("Telefone Sub", value=str(row_data.get("Telefone Sub", "")))
            edit_responsavel = e4.selectbox("Responsável", RESPONSAVEIS, index=RESPONSAVEIS.index(row_data["Responsável"]) if row_data["Responsável"] in RESPONSAVEIS else 0)

            edit_comercial = st.selectbox("Gerente Comercial", [""] + COMERCIAIS, index=([""] + COMERCIAIS).index(row_data["Comercial"]) if row_data["Comercial"] in COMERCIAIS else 0)

            btn_salvar_edit = st.form_submit_button("Salvar Alterações do Ticket")

        if btn_salvar_edit:
            if edit_fase == "Finalizado: Código criado":
                status_atualizado = "Concluído"
                data_conclusao_atualizada = fmt_date(date.today()) if not str(row_data.get("Data de Conclusão", "")).strip() else fmt_date(parse_date(row_data.get("Data de Conclusão")))
            elif edit_fase.startswith("Cancelado:"):
                status_atualizado = "Cancelado"
                data_conclusao_atualizada = fmt_date(date.today()) if not str(row_data.get("Data de Conclusão", "")).strip() else fmt_date(parse_date(row_data.get("Data de Conclusão")))
            else:
                status_atualizado = "Em andamento"
                data_conclusao_atualizada = ""

            hoje_atualizacao = fmt_date(date.today())

            novos_valores = {
                "Fase": edit_fase,
                "Status": status_atualizado,
                "Cód WB": edit_wb,
                "Telefone Sub": edit_telefone,
                "Responsável": edit_responsavel,
                "Comercial": edit_comercial,
                "Ultima atuação": hoje_atualizacao,
                "Data de Conclusão": data_conclusao_atualizada
            }

            reg_h, head_h = get_hierarquia(edit_comercial)
            novos_valores["Regional"] = reg_h
            novos_valores["Head"] = head_h

            for campo, n_val in novos_valores.items():
                v_antigo = str(row_data.get(campo, ""))
                if str(n_val) != v_antigo:
                    df_hist = registrar_historico(df_hist, df_fichas, ticket_id, campo, v_antigo, str(n_val))

            for campo, n_val in novos_valores.items():
                df.at[row_index, campo] = n_val

            salvar_base(df)
            st.success("Ticket atualizado com sucesso!")
            st.rerun()

# =========================================================
# 🧾 TELA: FICHAS E CHECKLISTS (DESIGN PREMIUM COESIVO)
# =========================================================

elif menu == "🧾 Fichas e Checklists":
    # Injeta CSS para acalmar o tamanho das fontes e padronizar os botões do formulário
    st.markdown(
        """
        <style>
            /* Reduz títulos e textos principais da área de conteúdo */
            h1, .main h1 { font-size: 22px !important; font-weight: 700 !important; color: #1e293b !important; margin-bottom: 5px !important; margin-top: 0px !important; }
            h2, .main h2 { font-size: 16px !important; font-weight: 600 !important; color: #334155 !important; }
            h3, .main h3 { font-size: 15px !important; font-weight: 600 !important; color: #1e293b !important; margin-top: 20px !important; margin-bottom: 10px !important; }
            h4, .main h4 { font-size: 14px !important; font-weight: 600 !important; color: #475569 !important; margin-top: 10px !important; margin-bottom: 10px !important; }
            p { font-size: 13px !important; color: #64748b !important; }
            
            /* Estilização moderna para o botão de envio das fichas */
            div.stFormSubmitButton > button {
                padding: 8px 16px !important;
                font-size: 13px !important;
                border-radius: 6px !important;
                background-color: #6134b2 !important;
                color: #ffffff !important; /* Força o texto em branco */
                border: 1px solid #6134b2 !important;
                font-weight: 500 !important;
                width: 100% !important;
                transition: background-color 0.2s ease;
            }
            div.stFormSubmitButton > button:hover {
                background-color: #4d2496 !important;
                border-color: #4d2496 !important;
                color: #ffffff !important; /* Mantém branco no hover */
            }
            
            /* Garante que tags de parágrafo geradas internamente no botão fiquem brancas */
            div.stFormSubmitButton > button p {
                color: #ffffff !important;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Título principal limpo
    st.markdown("<h1>Fichas e Checklists Customizados por Ticket</h1>", unsafe_allow_html=True)

    if df.empty:
        st.info("Base operacional vazia.")
    else:
        opcoes_tickets = [f"{r['Ticket#']} - {r['Razão Social']} ({r['Banco']})" for _, r in df.iterrows()]
        selecionado = st.selectbox("Selecione o Ticket para abrir as fichas completas", opcoes_tickets)
        tk_id = selecionado.split(" - ")[0]

        row_data = df[df["Ticket#"].astype(str) == str(tk_id)].iloc[0].to_dict()
        st.markdown(f"<h3>Gerenciando Ficha Cadastral Avançada — Ticket# <b>{tk_id}</b> ({row_data['Banco']})</h3>", unsafe_allow_html=True)

        match_ficha = df_fichas[df_fichas["Ticket#"].astype(str) == str(tk_id)]
        
        ficha_banco_salva = {}
        dados_empresa_salva = {}
        analise_salva = {}

        if not match_ficha.empty:
            f_b_js = match_ficha.iloc[0]["Ficha Banco JSON"]
            d_e_js = match_ficha.iloc[0]["Dados Empresa JSON"]
            a_i_js = match_ficha.iloc[0]["Análise Interna JSON"]
            try:
                if f_b_js: ficha_banco_salva = json.loads(f_b_js)
                if d_e_js: dados_empresa_salva = json.loads(d_e_js)
                if a_i_js: analise_salva = json.loads(a_i_js)
            except:
                pass

        campos_especificos_banco = get_checklist_banco(row_data["Banco"])

        with st.form("form_fichas_avancadas"):
            t1, t2, t3 = st.tabs(["Checklist do Banco", "Informações Corporativas", "Validação Antifraude/Interna"])

            with t1:
                st.markdown(f"<h4>Campos exigidos pelo parceiro <b>{row_data['Banco']}</b></h4>", unsafe_allow_html=True)
                novos_campos_banco = {}
                for c in campos_especificos_banco:
                    val_antigo = ficha_banco_salva.get(c, "")
                    if c == "QUAL A MODALIDADE A SER CADASTRADA?" and not val_antigo: val_antigo = row_data["Modalidade"]
                    novos_campos_banco[c] = st.text_input(c, value=str(val_antigo), key=f"f_b_v_{c}")

            with t2:
                st.markdown("<h4>Ficha Cadastral Unificada</h4>", unsafe_allow_html=True)
                novos_dados_empresa = {}
                for c in DADOS_EMPRESA_GERAL:
                    val_antigo = dados_empresa_salva.get(c, "")
                    if c == "RAZAO SOCIAL" and not val_antigo: val_antigo = row_data["Razão Social"]
                    if c == "CNPJ" and not val_antigo: val_antigo = row_data["CNPJ Sub"]
                    if c == "QUAL A MODALIDADE A SER CADASTRADA?" and not val_antigo: val_antigo = row_data["Modalidade"]
                    if c == "GERENTE COMERCIAL LEV" and not val_antigo: val_antigo = row_data["Comercial"]
                    if c == "GERENTE REGIONAL LEV" and not val_antigo: val_antigo = row_data["Regional"]
                    if c == "HEAD LEV" and not val_antigo: val_antigo = row_data["Head"]
                    novos_dados_empresa[c] = st.text_input(c, value=str(val_antigo), key=f"d_e_v_{c}")

            with t3:
                st.markdown("<h4>Checklist Operacional de Segurança</h4>", unsafe_allow_html=True)
                novas_analises = {}
                opcoes_combobox = ["", "OK", "Pendente", "Não se aplica"]
                for c in ANALISE_INTERNA_FIELDS:
                    val_antigo = analise_salva.get(c, "")
                    idx = opcoes_combobox.index(val_antigo) if val_antigo in opcoes_combobox else 0
                    novas_analises[c] = st.selectbox(c, opcoes_combobox, index=idx, key=f"a_i_v_{c}")

            btn_salvar_fichas = st.form_submit_button("Gravar Alterações nas Fichas Coletadas")

        if btn_salvar_fichas:
            df_fichas = salvar_ficha_ticket(df_fichas, tk_id, novos_campos_banco, novos_dados_empresa, novas_analises)
            salvar_historico_e_fichas(df_hist, df_fichas)
            df_hist = registrar_historico(df_hist, df_fichas, tk_id, "Atualização Fichas JSON", "Várias Fichas", f"Alterado por {st.session_state.usuario}")
            st.success("Fichas e checklists salvos com sucesso!")
            st.rerun()

# =========================================================
# 📜 TELA: HISTÓRICO (DESIGN AUDITORIA PREMIUM)
# =========================================================

elif menu == "📜 Histórico":
    # Injeta CSS para acalmar o tamanho das fontes e manter a coesão visual do painel
    st.markdown(
        """
        <style>
            /* Reduz títulos e textos principais da área de conteúdo */
            h1, .main h1 { font-size: 22px !important; font-weight: 700 !important; color: #1e293b !important; margin-bottom: 15px !important; margin-top: 0px !important; }
            p { font-size: 13px !important; color: #64748b !important; }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Título principal limpo e sem emojis repetidos
    st.markdown("<h1>Logs de Auditoria e Alterações do Sistema</h1>", unsafe_allow_html=True)
    
    if df_hist.empty:
        st.info("Nenhuma modificação registrada até o momento.")
    else:
        todos_tickets_hist = ["Todos"] + sorted(list(df_hist["Ticket#"].astype(str).unique()))
        filtro_tk = st.selectbox("Auditar Ticket# específico", todos_tickets_hist)

        df_hist_exibir = df_hist.copy()
        if filtro_tk != "Todos":
            df_hist_exibir = df_hist_exibir[df_hist_exibir["Ticket#"].astype(str) == filtro_tk]

        # Contador discreto no padrão do sistema
        st.markdown(f"<p style='margin-bottom: 15px;'>Total de logs localizados: <b>{len(df_hist_exibir)}</b></p>", unsafe_allow_html=True)
        
        # Exibe a grade de logs com a ordenação mais recente primeiro
        st.dataframe(df_hist_exibir.sort_index(ascending=False), width="stretch", hide_index=True)

# =========================================================
# 🧹 TELA: RESET / TESTES (DESIGN SEGURO & PREMIUM)
# =========================================================

elif menu == "🧹 Reset / Testes":
    # Injeta CSS para acalmar as fontes e diferenciar botões normais de ações críticas
    st.markdown(
        """
        <style>
            /* Reduz títulos e textos principais da área de conteúdo */
            h1, .main h1 { font-size: 22px !important; font-weight: 700 !important; color: #1e293b !important; margin-bottom: 5px !important; margin-top: 0px !important; }
            h3, .main h3 { font-size: 15px !important; font-weight: 600 !important; color: #1e293b !important; margin-top: 15px !important; margin-bottom: 15px !important; }
            p { font-size: 13px !important; }
            
            /* Botão padrão do sistema (Roxo com texto branco) - Usado para Massa de Testes */
            div.element-container button {
                padding: 8px 16px !important;
                font-size: 13px !important;
                border-radius: 6px !important;
                background-color: #6134b2 !important;
                color: #ffffff !important; /* Texto branco */
                border: 1px solid #6134b2 !important;
                font-weight: 500 !important;
                width: 100% !important;
                transition: background-color 0.2s ease;
            }
            div.element-container button:hover {
                background-color: #4d2496 !important;
                border-color: #4d2496 !important;
                color: #ffffff !important;
            }
            div.element-container button p {
                color: #ffffff !important;
            }
            
            /* Botões de Reset (Cinza discreto para segurança visual contra cliques acidentais) */
            div.element-container button:has(div[data-testid="stMarkdownContainer"] p:contains("Limpar")) {
                background-color: #f1f5f9 !important;
                color: #ef4444 !important; /* Texto em vermelho para indicar perigo */
                border: 1px solid #cbd5e1 !important;
            }
            div.element-container button:has(div[data-testid="stMarkdownContainer"] p:contains("Limpar")):hover {
                background-color: #fee2e2 !important;
                border-color: #fca5a5 !important;
                color: #b91c1c !important;
            }
            div.element-container button:has(div[data-testid="stMarkdownContainer"] p:contains("Limpar")) p {
                color: inherit !important;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Título limpo e profissional
    st.markdown("<h1>Ferramentas de Manutenção e Testes</h1>", unsafe_allow_html=True)

    st.warning("Atenção: As ações abaixo modificam ou deletam arquivos físicos da base de dados.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<h3>Reset do Sistema</h3>", unsafe_allow_html=True)
        if st.button("Limpar Toda a Base Operacional (Zerar Excel)"):
            df = resetar_base_vazia()
            st.success("Arquivo base_sub.xlsx resetado e esvaziado!")
            st.rerun()

        if st.button("Limpar Todo Histórico e Fichas JSON"):
            df_hist = pd.DataFrame(columns=["Ticket#", "Campo", "Valor Antigo", "Valor Novo", "Usuário", "Data/Hora"])
            df_fichas = pd.DataFrame(columns=FICHAS_COLUMNS)
            salvar_historico_e_fichas(df_hist, df_fichas)
            st.success("Arquivo historico_sub.xlsx esvaziado!")
            st.rerun()

    with c2:
        st.markdown("<h3>Massa de Testes (Gerar Carga Fake)</h3>", unsafe_allow_html=True)
        if st.button("Inserir Amostras de Teste para Equipe"):
            dados_teste = [
                {
                    "Ticket#": "1001", "Prazo Banco": 20, "Razão Social": "Parceiro Teste C6", "CNPJ Sub": "11.222.333/0001-44",
                    "Tipo Credenciamento": "Credenciamento Novo", "Modalidade": "SUB BANCO", "Banco": "C6 BANK",
                    "Responsável": "Mariana Santos", "Recepção E-mail": fmt_date(date.today() - timedelta(days=5)), "1º Envio Banco": "",
                    "Ultima atuação": fmt_date(date.today() - timedelta(days=3)), "Status": "Em andamento", "Fase": "Aguardando Banco: Cadastro iniciado",
                    "Comercial": "GC - LEV NEGOCIOS LTDA", "Regional": "GR - LEV", "Head": "SUP. BERGSON ARRAIS"
                },
                {
                    "Ticket#": "1002", "Prazo Banco": 30, "Razão Social": "Correspondente Facta Cobrar", "CNPJ Sub": "55.666.777/0001-88",
                    "Tipo Credenciamento": "Migração", "Modalidade": "SUB ZERO", "Banco": "FACTA",
                    "Responsável": "Ana Laura", "Recepção E-mail": fmt_date(date.today() - timedelta(days=10)), "1º Envio Banco": "",
                    "Ultima atuação": fmt_date(date.today() - timedelta(days=4)), "Status": "Em andamento", "Fase": "Aguardando Parceiro: Criação de conta Daycoval",
                    "Comercial": "GC - SP INTERIOR NEY 2", "Regional": "GR - JOSE DOMINGOS ROSA ZAGUI", "Head": "SUP. JOSE DOMINGOS ROSA ZAGUI"
                },
                {
                    "Ticket#": "1003", "Prazo Banco": 15, "Razão Social": "Parceiro Safra Em Dia", "CNPJ Sub": "99.888.777/0001-11",
                    "Tipo Credenciamento": "Reativação", "Modalidade": "INDICADO BANCO", "Banco": "SAFRA",
                    "Responsável": "Gustavo Cintra", "Recepção E-mail": fmt_date(date.today()), "1º Envio Banco": "",
                    "Ultima atuação": fmt_date(date.today()), "Status": "Em andamento", "Fase": "Fase de Assinaturas: Sub",
                    "Comercial": "GC - PARANA", "Regional": "GR - AMANDA APARECIDA DIMARTINI OLIVEIRA", "Head": "SUP. CASSIANO JOSE DE SOUZA"
                },
                {
                    "Ticket#": "1004", "Prazo Banco": 30, "Razão Social": "Antigo Finalizado Concluido", "CNPJ Sub": "44.333.222/0001-99",
                    "Tipo Credenciamento": "Credenciamento Novo", "Modalidade": "SUB BANCO", "Banco": "DAYCOVAL",
                    "Responsável": st.session_state.nome_usuario, "Recepção E-mail": fmt_date(date.today() - timedelta(days=40)), "1º Envio Banco": "",
                    "Ultima atuação": fmt_date(date.today() - timedelta(days=15)), "Status": "Concluído", "Fase": "Finalizado: Código criado",
                    "Comercial": "GC - SUL", "Regional": "GR - DENIO DA SILVEIRA VIÇOSA", "Head": "SUP. CASSIANO JOSE DE SOUZA",
                    "Data de Conclusão": fmt_date(date.today() - timedelta(days=15))
                }
            ]
            
            df_amostra = pd.DataFrame(dados_teste)
            df = pd.concat([df, df_amostra], ignore_index=True).drop_duplicates(subset=["Ticket#"], keep="last")
            salvar_base(df)
            st.success("Massa de testes injetada com sucesso!")
            st.rerun()
