import pandas as pd
import src.database as base
#

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
    tota_sobra = total_ganho - (total_despesa_variavel + total_despesa_fixa)

    resultado = {
        "total_despesa_variavel": total_despesa_variavel,
        "total_despesa_fixa": total_despesa_fixa,
        "total_ganho": total_ganho,
        "tota_sobra": tota_sobra
    }

    return resultado

