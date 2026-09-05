import os
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None

if URL and KEY:
    try:
        supabase = create_client(URL, KEY)
    except Exception as e:
        print(f"Erro ao inicializar cliente Supabase: {e}")


def buscar_processos():
    """Busca todos os processos cadastrados no Supabase com proteção contra erros de conexão"""
    if not supabase:
        return pd.DataFrame()

    try:
        response = supabase.table("processos").select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df.rename(columns={
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
                "situacao": "Situacao"
            }, inplace=True)
            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"Erro de conexão ao buscar processos: {e}")
        return pd.DataFrame()


def salvar_processo(dados_processo: dict):
    """Insere um novo processo na tabela do Supabase"""
    if not supabase:
        return False, "Credenciais do banco não foram carregadas."

    try:
        response = supabase.table("processos").insert(dados_processo).execute()
        return True, "Processo salvo com sucesso!"
    except Exception as e:
        return False, f"Erro na conexão com o banco: {str(e)}"