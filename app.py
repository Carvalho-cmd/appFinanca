import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("supabase_url")
key = os.getenv("supabase_key")

supabase: Client = create_client(url,key)


st.title("📱 Controle de Despesas")

# Aba de Consulta e Aba de Cadastro
aba_consultar, aba_cadastrar = st.tabs(["📊 Consultar", "➕ Cadastrar"])

with aba_consultar:
    st.subheader("Suas Despesas")
    dados = supabase.table("despesas").select("*").execute()
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