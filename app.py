# Atualizacao do sistema gessica
import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import buscar_processos, salvar_processo, atualizar_processo, deletar_processo

# Configuração da página
st.set_page_config(
    page_title="Gestão Processual | Escritório de Advocacia",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado - Dark Theme com Alto Contraste
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

# Busca dados reais do Supabase
df_geral = buscar_processos()

if not df_geral.empty and 'Data Cadastro' in df_geral.columns:
    df_geral['Data Cadastro'] = pd.to_datetime(df_geral['Data Cadastro']).dt.date

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/scale.png", width=50)
    st.markdown("### **Navegação**")

    opcao = st.radio(
        "",
        [
            "📊 Dashboard / Indicadores", 
            "➕ Novo Cadastro", 
            "📋 Processos / Consulta Geral",
            "✏️ Editar / Excluir Processo"
        ],
        index=0
    )

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.divider()
    st.caption("💻 **Desenvolvido por:**")
    st.markdown(
        "<span style='font-size: 12px; color: #94A3B8;'>TechIndigenaSolutions</span><br><span style='font-size: 11px; color: #64748B;'>Dev Velson</span>",
        unsafe_allow_html=True)

# --- TELA 1: DASHBOARD ---
if opcao == "📊 Dashboard / Indicadores":
    st.markdown("### 📊 Painel Geral de Métricas")

    if df_geral.empty:
        st.info(
            "Nenhum processo cadastrado no banco de dados até o momento. Acesse a aba '➕ Novo Cadastro' para adicionar o primeiro!")
    else:
        st.markdown('<div class="filter-header">🔍 Filtros Globais de Pesquisa</div>', unsafe_allow_html=True)

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filtro_adv = st.multiselect("Advogado Responsável", options=ADVOGADOS, default=[])
            filtro_situacao = st.selectbox("Situação dos Casos", ["Apenas Ativos (Padrão)", "Apenas Arquivados",
                                                                  "Exibir Todos (Ativos + Arquivados)"])
        with col_f2:
            filtro_frente = st.multiselect("Frente Processual",
                                           options=["Administrativo (INSS)", "Judicial (TRF / Vara)"], default=[])
            filtro_resultado = st.multiselect("Resultado / Êxito", options=OPCOES_RESULTADO, default=[])
        with col_f3:
            data_inicio = st.date_input("Data Início", value=date(2026, 1, 1))
            data_fim = st.date_input("Data Fim", value=date(2026, 12, 31))

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
        total_admin = len(df_filtrado[df_filtrado["Frente"] == "Administrativo (INSS)"]) if not df_filtrado.empty else 0
        total_judicial = len(
            df_filtrado[df_filtrado["Frente"] == "Judicial (TRF / Vara)"]) if not df_filtrado.empty else 0
        total_ganhos = len(df_filtrado[df_filtrado["Resultado"] == "Deferido (Ganho)"]) if not df_filtrado.empty else 0
        soma_honorarios = df_filtrado["Honorários Previsto"].sum() if not df_filtrado.empty else 0.0

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
            fase_inicial = st.text_input("Fase Inicial (Ex: Em Instrução, Protocolado, Cumprimento)",
                                         value="Em Instrução")

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
        submitted = st.form_submit_button("Salvar Cadastro no Banco")

        if submitted:
            if not nome or not cpf:
                st.error("Por favor, preencha os campos obrigatórios: Nome e CPF.")
            else:
                novo_registro = {
                    "data_cadastro": str(date.today()),
                    "cliente": nome,
                    "cpf": cpf,
                    "whatsapp": whatsapp,
                    "beneficio": tipo_beneficio,
                    "frente": frente,
                    "fase": fase_inicial,
                    "resultado": resultado_inicial,
                    "advogado_responsavel": advogado_resp,
                    "parceiro_origem": parceiro,
                    "honorarios_previsto": honorario_estimado,
                    "situacao": "Ativo",
                    "observacoes": observacoes
                }

                sucesso, msg = salvar_processo(novo_registro)
                if sucesso:
                    st.success(f"✅ Processo de '{nome}' gravado com sucesso no Supabase!")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

# --- TELA 3: CONSULTA UNIFICADA DE PROCESSOS ---
elif opcao == "📋 Processos / Consulta Geral":
    st.markdown("### 📋 Consulta Geral de Processos")

    if df_geral.empty:
        st.info("Nenhum registro encontrado no banco de dados.")
    else:
        busca_termo = st.text_input("🔎 Busca Rápida (Digite o Nome do Cliente ou CPF):", value="",
                                    placeholder="Ex: Maria ou 000.111...")

        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1:
            frente_select = st.selectbox("Frente Processual:",
                                         ["Todas", "Administrativo (INSS)", "Judicial (TRF / Vara)"])
        with col_l2:
            adv_select = st.selectbox("Filtrar por Advogado:", ["Todos"] + ADVOGADOS)
        with col_l3:
            sit_select = st.selectbox("Filtrar por Situação:", ["Apenas Ativos", "Apenas Arquivados", "Todos"])

        df_lista = df_geral.copy()

        if busca_termo:
            termo = busca_termo.strip().lower()
            df_lista = df_lista[
                df_lista["Cliente"].astype(str).str.lower().str.contains(termo, na=False) |
                df_lista["CPF"].astype(str).str.contains(termo, na=False)
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

# --- TELA 4: EDITAR / EXCLUIR PROCESSO ---
elif opcao == "✏️ Editar / Excluir Processo":
    st.markdown("### ✏️ Edição e Exclusão de Processos")

    if df_geral.empty:
        st.info("Nenhum processo cadastrado no banco de dados para editar ou excluir.")
    else:
        # Seletor do processo pelo ID/Nome do Cliente
        lista_opcoes = [f"ID {row['id']} - {row['Cliente']} (CPF: {row['CPF']})" for _, row in df_geral.iterrows()]
        processo_selecionado = st.selectbox("Selecione o Processo que deseja editar ou excluir:", lista_opcoes)

        if processo_selecionado:
            id_selecionado = int(processo_selecionado.split(" - ")[0].replace("ID ", ""))
            dados_proc = df_geral[df_geral['id'] == id_selecionado].iloc[0]

            # Função auxiliar segura para pegar valor de coluna
            def get_val(df_row, keys, default=""):
                for k in keys:
                    if k in df_row and pd.notna(df_row[k]):
                        return df_row[k]
                return default

            tab_editar, tab_excluir = st.tabs(["✏️ Editar Registro", "🗑️ Excluir Registro"])

            with tab_editar:
                with st.form("form_edicao"):
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        val_cliente = get_val(dados_proc, ['Cliente', 'cliente'])
                        val_cpf = get_val(dados_proc, ['CPF', 'cpf'])
                        val_whats = get_val(dados_proc, ['WhatsApp', 'whatsapp'])
                        val_adv = get_val(dados_proc, ['Advogado Responsável', 'advogado_responsavel'])
                        val_fase = get_val(dados_proc, ['Fase', 'fase'])

                        e_cliente = st.text_input("Nome do Cliente", value=str(val_cliente))
                        e_cpf = st.text_input("CPF", value=str(val_cpf))
                        e_whatsapp = st.text_input("WhatsApp", value=str(val_whats))
                        
                        idx_adv = ADVOGADOS.index(val_adv) if val_adv in ADVOGADOS else 0
                        e_adv = st.selectbox("Advogado Responsável", ADVOGADOS, index=idx_adv)
                        e_fase = st.text_input("Fase do Processo", value=str(val_fase))

                    with col_e2:
                        val_ben = get_val(dados_proc, ['Benefício', 'beneficio'])
                        val_frente = get_val(dados_proc, ['Frente', 'frente'])
                        val_res = get_val(dados_proc, ['Resultado', 'resultado'])
                        val_parceiro = get_val(dados_proc, ['Parceiro / Origem', 'Parceiro', 'parceiro_origem'])
                        val_hon = get_val(dados_proc, ['Honorários Previsto', 'honorarios_previsto'], default=0.0)

                        beneficios_lista = ["Salário Maternidade", "Auxílio-Doença / Incapacidade", "Auxílio-Acidente", "Aposentadoria", "BPC / LOAS", "Outro"]
                        idx_ben = beneficios_lista.index(val_ben) if val_ben in beneficios_lista else 0
                        e_beneficio = st.selectbox("Benefício", beneficios_lista, index=idx_ben)

                        frentes_lista = ["Administrativo (INSS)", "Judicial (TRF / Vara)"]
                        idx_frente = frentes_lista.index(val_frente) if val_frente in frentes_lista else 0
                        e_frente = st.selectbox("Frente Processual", frentes_lista, index=idx_frente)

                        idx_res = OPCOES_RESULTADO.index(val_res) if val_res in OPCOES_RESULTADO else 0
                        e_resultado = st.selectbox("Resultado", OPCOES_RESULTADO, index=idx_res)

                        e_parceiro = st.text_input("Parceiro / Origem", value=str(val_parceiro))
                        
                        try:
                            val_hon_float = float(val_hon)
                        except (ValueError, TypeError):
                            val_hon_float = 0.0
                        e_honorarios = st.number_input("Honorários Previstos (R$)", value=val_hon_float, min_value=0.0, step=100.0)

                    val_sit = get_val(dados_proc, ['Situacao', 'situacao'], default='Ativo')
                    val_obs = get_val(dados_proc, ['Observações', 'observacoes'])

                    situacoes_lista = ["Ativo", "Arquivado"]
                    idx_sit = situacoes_lista.index(val_sit) if val_sit in situacoes_lista else 0
                    e_situacao = st.selectbox("Situação do Registro", situacoes_lista, index=idx_sit)
                    
                    e_obs = st.text_area("Observações / Histórico", value=str(val_obs))

                    btn_salvar = st.form_submit_button("💾 Salvar Alterações")

                    if btn_salvar:
                        dados_atualizados = {
                            "cliente": e_cliente,
                            "cpf": e_cpf,
                            "whatsapp": e_whatsapp,
                            "beneficio": e_beneficio,
                            "frente": e_frente,
                            "fase": e_fase,
                            "resultado": e_resultado,
                            "advogado_responsavel": e_adv,
                            "parceiro_origem": e_parceiro,
                            "honorarios_previsto": e_honorarios,
                            "situacao": e_situacao,
                            "observacoes": e_obs
                        }
                        ok, msg = atualizar_processo(id_selecionado, dados_atualizados)
                        if ok:
                            st.success(f"✅ Processo ID {id_selecionado} atualizado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

            with tab_excluir:
                val_nome_del = get_val(dados_proc, ['Cliente', 'cliente'])
                st.warning(f"⚠️ **Atenção:** Deseja realmente excluir permanentemente o registro de **{val_nome_del}** (ID: {id_selecionado})?")
                btn_deletar = st.button("🔴 Confirmar Exclusão Definitiva")
                if btn_deletar:
                    ok, msg = deletar_processo(id_selecionado)
                    if ok:
                        st.success(f"🗑️ Processo ID {id_selecionado} excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
