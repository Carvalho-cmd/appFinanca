
from supabase import create_client, Client
from dotenv import load_dotenv
import os

import streamlit as st

load_dotenv()



#=================Conectando com o banco=======================

url = os.getenv("supabase_url") or st.secrets.get("supabase_url")
key = os.getenv("supabase_key") or st.secrets.get("supabase_key")

if not url or not key:
    st.error("Chaves de configuração do Supabase não encontradas!")
else:
    supabase: Client = create_client(url, key)

#===============================================================


#======Select
def import_tabela(tabela):
    return (supabase.table(tabela).select("*").execute())

#======Insert
def inserir_tabela(tabela, df):
    supabase.table(tabela).insert(df).execute()