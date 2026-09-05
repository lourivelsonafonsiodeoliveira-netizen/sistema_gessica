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
        import os
import pandas as pd
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Credenciais do Supabase não encontradas nas variáveis de ambiente.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# --- PROCESSOS ---
def buscar_processos():
    try:
        supabase = get_supabase_client()
        response = supabase.table("processos").select("*").order("created_at", desc=True).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            mapeamento = {
                "id": "id",
                "data_cadastro": "Data Cadastro",
                "cliente": "Cliente",
                "cpf": "CPF",
                "whatsapp": "WhatsApp",
                "beneficio": "Benefício",
                "frente": "Frente",
                "fase": "Fase",
                "resultado": "Resultado",
                "advogado_responsavel": "Advogado Responsável",
                "parceiro_origem": "Parceiro / Origem",
                "honorarios_previsto": "Honorários Previsto",
                "situacao": "Situacao",
                "observacoes": "Observações"
            }
            df = df.rename(columns=mapeamento)
            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"Erro ao buscar processos: {e}")
        return pd.DataFrame()

def salvar_processo(dados):
    try:
        supabase = get_supabase_client()
        supabase.table("processos").insert(dados).execute()
        return True, "Processo cadastrado com sucesso!"
    except Exception as e:
        return False, f"Erro ao cadastrar processo: {str(e)}"

def atualizar_processo(id_processo, dados):
    try:
        supabase = get_supabase_client()
        supabase.table("processos").update(dados).eq("id", id_processo).execute()
        return True, "Processo atualizado com sucesso!"
    except Exception as e:
        return False, f"Erro ao atualizar processo: {str(e)}"

def deletar_processo(id_processo):
    try:
        supabase = get_supabase_client()
        supabase.table("processos").delete().eq("id", id_processo).execute()
        return True, "Processo excluído com sucesso!"
    except Exception as e:
        return False, f"Erro ao excluir processo: {str(e)}"

# --- ADVOGADOS ---
def buscar_advogados():
    try:
        supabase = get_supabase_client()
        response = supabase.table("advogados").select("*").order("nome", desc=False).execute()
        if response.data:
            return [row["nome"] for row in response.data if "nome" in row]
        return ["Dra. Géssica", "Dr. Carlos Eduardo", "Dra. Mariana Prado"]
    except Exception as e:
        # Caso a tabela ainda não exista no Supabase, usa os nomes padrão
        return ["Dra. Géssica", "Dr. Carlos Eduardo", "Dra. Mariana Prado"]

def salvar_advogado(nome):
    try:
        supabase = get_supabase_client()
        supabase.table("advogados").insert({"nome": nome}).execute()
        return True, f"Advogado(a) '{nome}' cadastrado(a) com sucesso!"
    except Exception as e:
        return False, f"Erro ao salvar advogado: {str(e)}"

def deletar_advogado(nome):
    try:
        supabase = get_supabase_client()
        supabase.table("advogados").delete().eq("nome", nome).execute()
        return True, f"Advogado(a) '{nome}' removido(a) com sucesso!"
    except Exception as e:
        return False, f"Erro ao remover advogado: {str(e)}"
        return False, f"Erro ao excluir: {str(e)}"
