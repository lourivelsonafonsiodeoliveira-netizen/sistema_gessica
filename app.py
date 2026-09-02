import streamlit as st
import pandas as pd
import io
from datetime import datetime, date

# Configuração da página
st.set_page_config(
    page_title="Gestão Processual | Escritório de Advocacia",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado - Dark Theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }

    header[data-testid="stHeader"] {
        background-color: #0F172A !important;
    }
    div[data-testid="stToolbar"] {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    label, .stMarkdown p {
        color: #E2E8F0 !important;
        font-weight: 500 !important;
    }

    .header-title {
        font-size: 28px;
        font-weight: 700;
        color: #F8FAFC;
    }
    .header-subtitle {
        font-size: 14px;
        color: #94A3B8;
        margin-bottom: 20px;
        border-bottom: 1px solid #334155;
        padding-bottom: 10px;
    }

    .filter-header {
        font-size: 16px;
        font-weight: 600;
        color: #38BDF8 !important;
        margin-bottom: 12px;
    }

    [data-testid="stMetric"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }

    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: visible;}
    </style>
""", unsafe_allow_html=True)

# Topo Neutro
st.markdown('<div class="header-title">⚖️ Gestão Processual</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Escritório de Advocacia — Painel de Controle</div>', unsafe_allow_html=True)

ADVOGADOS = ["Dra. Géssica", "Dr. Carlos Eduardo", "Dra. Mariana Prado", "Sem Responsável Definido"]
OPCOES_RESULTADO = ["Em Andamento", "Deferido (Ganho)", "Indeferido (Perda)", "Acordo"]

# --- DADOS MOCKADOS PARA HOMOLOGAÇÃO ---
dados_base = [
    {
        "Data Cadastro": "2026-08-10", "Cliente": "Maria Silva", "CPF": "000.111.222-33",
        "Benefício": "Salário Maternidade", "Frente": "Administrativo (INSS)", "Fase": "Em Instrução",
        "Resultado": "Em Andamento", "Advogado Responsável": "Dra. Géssica", "Parceiro/Origem": "Indicação Direct",
        "Honorários Previsto": 2500.00, "Situacao": "Ativo"
    },
    {
        "Data Cadastro": "2026-08-15", "Cliente": "João Santos", "CPF": "444.555.666-77",
        "Benefício": "Auxílio-Doença", "Frente": "Administrativo (INSS)", "Fase": "Exigência Pendente",
        "Resultado": "Em Andamento", "Advogado Responsável": "Dr. Carlos Eduardo",
        "Parceiro/Origem": "Parceiro Dr. Carlos",
        "Honorários Previsto": 2000.00, "Situacao": "Ativo"
    },
    {
        "Data Cadastro": "2026-08-20", "Cliente": "Ana Oliveira", "CPF": "888.999.000-11",
        "Benefício": "Aposentadoria", "Frente": "Judicial (TRF / Vara)", "Fase": "Cumprimento de Sentença",
        "Resultado": "Deferido (Ganho)", "Advogado Responsável": "Dra. Géssica", "Parceiro/Origem": "Google / Site",
        "Honorários Previsto": 6000.00, "Situacao": "Ativo"
    },
    {
        "Data Cadastro": "2026-07-05", "Cliente": "Roberto Lima", "CPF": "111.222.333-44",
        "Benefício": "Auxílio-Acidente", "Frente": "Administrativo (INSS)", "Fase": "Arquivado",
        "Resultado": "Indeferido (Perda)", "Advogado Responsável": "Dra. Mariana Prado",
        "Parceiro/Origem": "Indicação Direct",
        "Honorários Previsto": 0.00, "Situacao": "Arquivado"
    }
]

df_geral = pd.DataFrame(dados_base)
df_geral['Data Cadastro'] = pd.to_datetime(df_geral['Data Cadastro']).dt.date

# Sidebar Navigation (Menu simplificado)
with st.sidebar:
    st.image("https://img.icons8.com/color/96/scale.png", width=50)
    st.markdown("### **Navegação**")

    opcao = st.radio(
        "",
        ["📊 Dashboard / Indicadores", "➕ Novo Cadastro", "📋 Processos / Consulta Geral"],
        index=0
    )

    # Rodapé da Sidebar
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.divider()
    st.caption("💻 **Desenvolvido por:**")
    st.markdown(
        "<span style='font-size: 12px; color: #94A3B8;'>TechIndigenaSolutions</span><br><span style='font-size: 11px; color: #64748B;'>Dev Velson</span>",
        unsafe_allow_html=True)

# --- TELA 1: DASHBOARD ---
if opcao == "📊 Dashboard / Indicadores":
    st.markdown("### 📊 Painel Geral de Métricas")

    st.markdown('<div class="filter-header">🔍 Filtros Globais de Pesquisa</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filtro_adv = st.multiselect("Advogado Responsável", options=ADVOGADOS, default=[])
        filtro_situacao = st.selectbox("Situação dos Casos", ["Apenas Ativos (Padrão)", "Apenas Arquivados",
                                                              "Exibir Todos (Ativos + Arquivados)"])
    with col_f2:
        filtro_frente = st.multiselect("Frente Processual", options=["Administrativo (INSS)", "Judicial (TRF / Vara)"],
                                       default=[])
        filtro_resultado = st.multiselect("Resultado / Êxito", options=OPCOES_RESULTADO, default=[])
    with col_f3:
        data_inicio = st.date_input("Data Início", value=date(2026, 7, 1))
        data_fim = st.date_input("Data Fim", value=date(2026, 9, 30))

    df_filtrado = df_geral.copy()

    if filtro_situacao == "Apenas Ativos (Padrão)":
        df_filtrado = df_filtrado[df_filtrado["Situacao"] == "Ativo"]
    elif filtro_situacao == "Apenas Arquivados":
        df_filtrado = df_filtrado[df_filtrado["Situacao"] == "Arquivado"]

    if filtro_adv:
        df_filtrado = df_filtrado[df_filtrado["Advogado Responsável"].isin(filtro_adv)]
    if filtro_frente:
        df_filtrado = df_filtrado[df_filtrado["Frente"].isin(filtro_frente)]
    if filtro_resultado:
        df_filtrado = df_filtrado[df_filtrado["Resultado"].isin(filtro_resultado)]

    df_filtrado = df_filtrado[
        (df_filtrado["Data Cadastro"] >= data_inicio) & (df_filtrado["Data Cadastro"] <= data_fim)]

    st.divider()

    st.markdown("#### **Resumo do Período Selecionado**")
    c1, c2, c3, c4, c5 = st.columns(5)

    total_casos = len(df_filtrado)
    total_admin = len(df_filtrado[df_filtrado["Frente"] == "Administrativo (INSS)"])
    total_judicial = len(df_filtrado[df_filtrado["Frente"] == "Judicial (TRF / Vara)"])
    total_ganhos = len(df_filtrado[df_filtrado["Resultado"] == "Deferido (Ganho)"])
    soma_honorarios = df_filtrado["Honorários Previsto"].sum()

    c1.metric(label="Total Exibido", value=total_casos)
    c2.metric(label="Frente INSS", value=total_admin)
    c3.metric(label="Frente Judicial", value=total_judicial)
    c4.metric(label="Deferidos (Ganhos)", value=total_ganhos)
    c5.metric(label="Honorários Previstos",
              value=f"R$ {soma_honorarios:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.divider()
    st.markdown("#### **Detalhamento de Processos**")
    st.dataframe(df_filtrado, width='stretch')

# --- TELA 2: NOVO CADASTRO ---
elif opcao == "➕ Novo Cadastro":
    st.markdown("### Cadastro de Cliente e Processo Previdenciário")

    with st.form("form_cadastro", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            nome = st.text_input("Nome do Cliente*")
            cpf = st.text_input("CPF*")
            whatsapp = st.text_input("WhatsApp / Telefone")
            advogado_resp = st.selectbox("Advogado Responsável (Dono do Caso)*", ADVOGADOS)

        with col_b:
            tipo_beneficio = st.selectbox(
                "Tipo de Benefício Previdenciário*",
                ["Salário Maternidade", "Auxílio-Doença / Incapacidade", "Auxílio-Acidente", "Aposentadoria",
                 "BPC / LOAS", "Outro"]
            )
            frente = st.selectbox("Frente Processual*", ["Administrativo (INSS)", "Judicial (TRF / Vara)"])
            resultado_inicial = st.selectbox("Resultado Atual", OPCOES_RESULTADO)
            parceiro = st.text_input("Parceiro / Origem do Lead (Opcional)")
            honorario_estimado = st.number_input("Valor Estimado do Honorário (R$)", min_value=0.0, step=100.0)

        observacoes = st.text_area("Observações / Histórico Inicial")
        submitted = st.form_submit_button("Salvar Cadastro")

        if submitted:
            st.success(f"Cadastro de '{nome}' salvo com sucesso! (Modo de Homologação)")

# --- TELA 3: CONSULTA UNIFICADA DE PROCESSOS ---
elif opcao == "📋 Processos / Consulta Geral":
    st.markdown("### 📋 Consulta Geral de Processos")

    # Campo de Busca por Nome ou CPF
    busca_termo = st.text_input("🔎 Busca Rápida (Digite o Nome do Cliente ou CPF):", value="",
                                placeholder="Ex: Maria ou 000.111...")

    # Filtros de apoio
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        frente_select = st.selectbox("Frente Processual:", ["Todas", "Administrativo (INSS)", "Judicial (TRF / Vara)"])
    with col_l2:
        adv_select = st.selectbox("Filtrar por Advogado:", ["Todos"] + ADVOGADOS)
    with col_l3:
        sit_select = st.selectbox("Filtrar por Situação:", ["Apenas Ativos", "Apenas Arquivados", "Todos"])

    # Aplicação da filtragem em tempo real
    df_lista = df_geral.copy()

    # Busca por texto (Nome ou CPF)
    if busca_termo:
        termo = busca_termo.strip().lower()
        df_lista = df_lista[
            df_lista["Cliente"].str.lower().str.contains(termo, na=False) |
            df_lista["CPF"].str.contains(termo, na=False)
            ]

    if frente_select != "Todas":
        df_lista = df_lista[df_lista["Frente"] == frente_select]
    if adv_select != "Todos":
        df_lista = df_lista[df_lista["Advogado Responsável"] == adv_select]
    if sit_select == "Apenas Ativos":
        df_lista = df_lista[df_lista["Situacao"] == "Ativo"]
    elif sit_select == "Apenas Arquivados":
        df_lista = df_lista[df_lista["Situacao"] == "Arquivado"]

    st.markdown(f"**Registros encontrados:** `{len(df_lista)}`")
    st.dataframe(df_lista, width='stretch')