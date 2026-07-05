import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

url = os.getenv("supabase_url") or st.secrets.get("supabase_url")
key = os.getenv("supabase_key") or st.secrets.get("supabase_key")

if not url or not key:
    st.error("Chaves de configuração do Supabase não encontradas!")
else:
    supabase: Client = create_client(url, key)



#=================Configuracoes do App=======================

st.set_page_config(
    page_title="Controle Financeiro",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.title("Finanças")

#==================Busca dos dados na base===================

dados = supabase.table("despesas").select("*").execute()



#==================Configuracao variaveis====================

data_hoje = datetime.date.today()
mes = data_hoje.strftime("%m")
ano = data_hoje.strftime("%Y")


#==================Botoes de cadastro========================


with st.container(horizontal=True, horizontal_alignment="center", border=True):
    cdt_despesa = st.button("Cadastro Despesa")
    cdt_ganho = st.button("Cadastro Ganho")

    #st.write(cdt_despesa)
    #st.write(cdt_ganho)


@st.dialog("Cadastrar Nova Despesa")
def popup_cadastro_despesa():
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
    categoria = st.selectbox("Categoria", ["Alimentação", "Parcelado", "Plano", "Carro", "Lazer", "Presente", "Outros"])
    data_despesa = st.date_input("Data")
    balanco = st.text_input("Balanço (MM/YYYY)", value=f'{mes}/{ano}')
    cartao = st.selectbox("Cartão", ["Nubank", "Mercado Pago", "Santander", "XP", "Debito"])
    parcela = st.text_input("Qtd. Parcelas", value="")

    if st.button("Salvar", type="primary"):
        if not descricao:
            st.error("Por favor, preencha a descrição!")
        else:
            try:
                nova_dp = {
                        "descricao": descricao, "valor": valor, "categoria": categoria,
                        "data_despesa": str(data_despesa), "balanco": balanco, 
                        "cartao": cartao, "parcela": parcela
                    }
                supabase.table("despesas").insert(nova_dp).execute()
                st.success("Cadastrado com sucesso!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")


if cdt_despesa:
        popup_cadastro_despesa()





#============================================================

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