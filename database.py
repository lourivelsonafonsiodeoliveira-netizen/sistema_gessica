import os
import pandas as pd
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = None
SUPABASE_KEY = None

try:
    if "SUPABASE_URL" in st.secrets:
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
    else:
        SUPABASE_URL = os.getenv("SUPABASE_URL")

    if "SUPABASE_KEY" in st.secrets:
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    else:
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")
except Exception:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Erro ao conectar com Supabase: {e}")

def buscar_processos():
    if not supabase:
        return pd.DataFrame()
    try:
        response = supabase.table("processos").select("*").execute()
        dados = response.data
        if not dados:
            return pd.DataFrame()
        df = pd.DataFrame(dados)
        colunas_map = {
            "id": "id",
            "data_cadastro": "Data Cadastro",
            "cliente": "Cliente",
            "cpf": "CPF",
            "beneficio": "Benefício",
            "frente": "Frente",
            "fase": "Fase",
            "resultado": "Resultado",
            "advogado_responsavel": "Advogado Responsável",
            "parceiro_origem": "Parceiro/Origem",
            "honorarios_previsto": "Honorários Previsto",
            "situacao": "Situacao",
            "observacoes": "observacoes",
            "whatsapp": "whatsapp"
        }
        return df.rename(columns={k: v for k, v in colunas_map.items() if k in df.columns})
    except Exception as e:
        st.error(f"Erro ao buscar processos: {e}")
        return pd.DataFrame()

def salvar_processo(dados_processo: dict):
    if not supabase:
        return False, "Credenciais do banco não foram carregadas."
    try:
        supabase.table("processos").insert(dados_processo).execute()
        return True, "Processo salvo com sucesso!"
    except Exception as e:
        return False, f"Erro ao salvar: {str(e)}"

def atualizar_processo(id_processo: int, dados_atualizados: dict):
    if not supabase:
        return False, "Credenciais do banco não foram carregadas."
    try:
        supabase.table("processos").update(dados_atualizados).eq("id", id_processo).execute()
        return True, "Processo atualizado com sucesso!"
    except Exception as e:
        return False, f"Erro ao atualizar: {str(e)}"

def deletar_processo(id_processo: int):
    if not supabase:
        return False, "Credenciais do banco não foram carregadas."
    try:
        supabase.table("processos").delete().eq("id", id_processo).execute()
        return True, "Processo excluído com sucesso!"
    except Exception as e:
        return False, f"Erro ao excluir: {str(e)}"