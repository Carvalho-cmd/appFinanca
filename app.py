import streamlit as st
import datetime
import pandas as pd

import src.utils as utils
import src.database as base
import src.metricas as metricas



#=================Configuracoes do App=======================

st.set_page_config(
    page_title="Controle Financeiro",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

with st.sidebar:
    st.title("Finanças")
    st.write("Versão 1.0")

st.title("Cadastro ganhos e despesas")

#==================Busca dos dados na base===================

df_despesas = pd.DataFrame(base.import_tabela("tb_despesas").data)


balanco_disponiveis = df_despesas['balanco'].unique()
balanco_selecionados = st.sidebar.multiselect(
    "Selecione o mês:",
    options=balanco_disponiveis,
    default="07/2026" # Começa com todas selecionadas
)


#==================Configuracao variaveis====================

data_hoje = datetime.date.today()
mes = data_hoje.strftime("%m")
ano = data_hoje.strftime("%Y")


#==================Botoes de cadastro========================


@st.dialog("Cadastrar Nova Despesa")
def popup_cadastro_despesa():
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
    categoria = st.selectbox("Categoria", ["Alimentação", "Parcelado", "Plano", "Carro", "Lazer", "Presente", "Outros"])
    data_despesa = st.date_input("Data")
    cartao = st.selectbox("Cartão", ["Nubank", "Mercado Pago", "Santander", "XP", "Debito"])
    parcela = st.text_input("Qtd. Parcelas", value=1)
    responsavel = st.text_input("Responsável", value="")
    local = st.text_input("Local", value="")

    if st.button("Salvar", type="primary"):
        if not descricao:
            st.error("Por favor, preencha a descrição!")
        else:
            try:
                utils.cadastro_despesa(descricao, valor, categoria, data_despesa, cartao, parcela, responsavel, local)
                st.success("Cadastrado com sucesso!")

            except Exception as e:
                st.error(f"Erro ao salvar: {e}")




@st.dialog("Cadastrar Nova Receita")
def popup_cadastro_receita():
    descricao = st.text_input("Descrição")
    balanco = st.text_input("balanco", value = f"{mes}/{ano}")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
    data_receita = st.date_input("Data Receita")
    categoria = st.selectbox("Categoria", ["Salario", "PIX", "PPR", "Decimo", "Ferias"]) 


    if st.button("Salvar", type="primary"):
        if not descricao:
            st.error("Por favor, preencha a descrição!")
        else:
            try:
                utils.cadastro_receita(descricao, balanco, categoria, data_receita, valor)
                st.success("Cadastrado com sucesso!")

            except Exception as e:
                st.error(f"Erro ao salvar: {e}")



with st.container(horizontal=True, horizontal_alignment="center", border=True):
    cdt_despesa = st.button("Cadastro Despesa")
    cdt_receita = st.button("Cadastro Ganho")

    #st.write(cdt_despesa)
    #st.write(cdt_ganho)


if cdt_despesa:
    popup_cadastro_despesa()

if cdt_receita:
    popup_cadastro_receita()





#============================================================

st.markdown("### Indicadores do mês")

indicadores = metricas.indicadores_total_mes(f"{mes}/{ano}")

var_despesa_variavel = indicadores["total_despesa_variavel"]
var_despesa_fixa = indicadores["total_despesa_fixa"]
var_ganho = indicadores["total_ganho"]
var_sobra = indicadores["tota_sobra"]

with st.container(horizontal=True, horizontal_alignment="center"):

    total_deslpesa_variavel, total_deslpesa_fixa, total_ganho, total_sobra = st.columns(4)

    with total_deslpesa_variavel:
        st.metric(label="Despesas variáveis", value=f"{var_despesa_variavel} R$")
        st.caption("Cartão de Crédito")
    
    with total_deslpesa_fixa:
        st.metric(label="Despesas fixas", value=f"{var_despesa_fixa} R$")
        st.caption("Dívidas fixas")

    with total_ganho:
        st.metric(label="Total Ganho", value=f"{var_ganho} R$")
        st.caption("PIX / Débito")

    with total_sobra:
        st.metric(label="Sobra", value=f"{var_sobra} R$")
        st.caption("Meta de Poupança")



#=============================================================


df_despesas_filtradas = df_despesas[ 
    df_despesas['balanco'].isin(balanco_selecionados)
 ]

st.write(df_despesas_filtradas)

