import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("supabase_url") or st.secrets.get("supabase_url")
key = os.getenv("supabase_key") or st.secrets.get("supabase_key")

if not url or not key:
    st.error("Chaves de configuração do Supabase não encontradas!")
else:
    supabase: Client = create_client(url, key)



#============================================================

st.set_page_config(
    page_title="Controle Financeiro",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.title("Controle de Despesas")

#============================================================

dados = supabase.table("despesas").select("*").execute()



#============================================================


with st.container(horizontal=True, horizontal_alignment="distribute"):
    st.button("Cadastro Despesa")
    st.button("Cadastro Ganho")




# Aba de Consulta e Aba de Cadastro
aba_consultar, aba_cadastrar = st.tabs(["📊 Consultar", "➕ Cadastrar"])

with aba_consultar:
    st.subheader("Suas Despesas")
    st.dataframe(dados.data)

with aba_cadastrar:
    st.subheader("Nova Despesa")
    with st.form("form_despesa"):
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")
        categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Outros"])
        data_despesa = st.date_input("Data")
        balanco = st.text_input("Balanço (MM/YYYY)", value="07/2026")
        cartao = st.text_input("Cartão")
        parcela = st.text_input("Parcela", value="1/1")
        
        enviado = st.form_submit_button("Salvar no Supabase")
        
        if enviado:
            nova_dp = {
                "descricao": descricao, "valor": valor, "categoria": categoria,
                "data_despesa": str(data_despesa), "balanco": balanco, 
                "cartao": cartao, "parcela": parcela
            }
            supabase.table("despesas").insert(nova_dp).execute()
            st.success("Cadastrado com sucesso!")