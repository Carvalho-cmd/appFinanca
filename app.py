import streamlit as st
import datetime
import pandas as pd

import src.utils as utils
import src.database as base



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

df_despesas = pd.DataFrame(base.import_tabela_despesas().data)


balanco_disponiveis = df_despesas['balanco'].unique()
balanco_selecionados = st.sidebar.multiselect(
    "Selecione as Categorias:",
    options=balanco_disponiveis,
    default="08/2026" # Começa com todas selecionadas
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
                #nova_dp = {
                #        "descricao": descricao, "valor": valor, "categoria": categoria,
                #        "data_despesa": str(data_despesa), "balanco": balanco, 
                #        "cartao": cartao, "parcela": parcela
                #    }
                #supabase.table("despesas").insert(nova_dp).execute()
                #st.success("Cadastrado com sucesso!")
                #st.rerun()
                utils.cadastro_despesa(descricao, valor, categoria, data_despesa, cartao, parcela, responsavel, local)
                st.success("Cadastrado com sucesso!")

            except Exception as e:
                st.error(f"Erro ao salvar: {e}")


with st.container(horizontal=True, horizontal_alignment="center", border=True):
    cdt_despesa = st.button("Cadastro Despesa")
    cdt_ganho = st.button("Cadastro Ganho")

    #st.write(cdt_despesa)
    #st.write(cdt_ganho)


if cdt_despesa:
        popup_cadastro_despesa()





#============================================================

st.markdown("### Indicadores do mês")

with st.container(horizontal=True, horizontal_alignment="center"):

    total_deslpesa_variavel, total_deslpesa_fixa, total_ganho, total_sobra = st.columns(4)

    with total_deslpesa_variavel:
        st.metric(label="Despesas variáveis", value="R$ 1.000,00")
        st.caption("Cartão de Crédito")
    
    with total_deslpesa_fixa:
        st.metric(label="Despesas fixas", value="R$ 1.250,00")
        st.caption("Dívidas fixas")

    with total_ganho:
        st.metric(label="Total Ganho", value="R$ 2.000,00")
        st.caption("PIX / Débito")

    with total_sobra:
        st.metric(label="Sobra", value="R$ 300,00")
        st.caption("Meta de Poupança")



#=============================================================


df_despesas_filtradas = df_despesas[ 
    df_despesas['balanco'].isin(balanco_selecionados)
 ]

st.write(df_despesas_filtradas)

