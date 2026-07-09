import pandas as pd
import src.database as base
import datetime

####

df_despesas = pd.DataFrame(base.import_tabela("tb_despesas").data)
df_despesas_fixas = pd.DataFrame(base.import_tabela("tb_despesas_fixas").data)
df_receita = pd.DataFrame(base.import_tabela("tb_receita").data)



def total_gasto_anual():
    print("")

def despesas_por_categoria_mes(balanco):
    print("")

def despesas_por_cartao_mes(balanco):
    print("")

def indicadores_total_mes(balanco):
    
    #total despesa variaveis
    df_depesa_variavel_atual = df_despesas[df_despesas["balanco"] == balanco]
    total_despesa_variavel = float(df_depesa_variavel_atual["valor"].sum())

    #total despesas fixas
    total_despesa_fixa = float(df_despesas_fixas["valor"].sum())

    #total ganho
    df_ganho_atual = df_receita[df_receita["balanco"] == balanco]
    total_ganho = float(df_ganho_atual["valor"].sum())

    #Sobra
    total_sobra = 3000 - (total_despesa_variavel + total_despesa_fixa)

    resultado = {
        "total_despesa_variavel": total_despesa_variavel,
        "total_despesa_fixa": total_despesa_fixa,
        "total_ganho": 3000,
        "total_sobra": total_sobra
    }

    return resultado


def import_despesas():

    df_despesas = pd.DataFrame(base.import_tabela("tb_despesas").data)
    return df_despesas

def import_balanco_atual():

    data_hoje = datetime.date.today()
    mes = data_hoje.strftime("%m")
    ano = data_hoje.strftime("%Y")
    balanco = f'{mes}/{ano}'
    return balanco



def import_despesas_por_categoria(balanco):

    df_despesas = import_despesas()

    df_despesas_atuais = df_despesas[df_despesas['balanco'] == balanco]

    df_despesas_por_categoria = df_despesas_atuais[['categoria', 'valor']].groupby('categoria').sum().reset_index()

    return df_despesas_por_categoria


def import_despesas_por_cartao(balanco):

    df_despesas = import_despesas()

    df_despesas_atuais = df_despesas[df_despesas['balanco'] == balanco]

    df_despesas_por_cartao = df_despesas_atuais[['cartao', 'valor']].groupby('cartao').sum().reset_index()

    return df_despesas_por_cartao
