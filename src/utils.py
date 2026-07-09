
import pandas as pd
import streamlit as st
import src.database as base
import src.metricas as metricas

try:
    despesas = base.import_tabela('tb_despesas') #supabase.table("despesas").select("*").execute()
except Exception as e:
    print(e)




despesa = {
    'descricao': [],
    'balanco': [],
    'categoria': [],
    'data_despesa': [],
    'cartao': [],
    'local': [],
    'responsavel': [],
    'valor': [],
    'parcela': []
}


def cadastro_despesa(descricao, valor, categoria, data, cartao, parcela, responsavel, local):
    data_atual = str(data)
    mes = int(data_atual[5:7])
    ano = int(data_atual[0:4])

    valor_despesa = valor

    parcela = int(parcela)

    if parcela > 0:
        int_qtd_parcelas = int(parcela)
    else:
        int_qtd_parcelas = 1

    valor_parcelado = valor_despesa/int_qtd_parcelas

    for i in range(int_qtd_parcelas):

        parcela_contador = i + 1

        if mes == 13:
            mes = 1 
            ano += 1

        despesa['descricao'].append(descricao)

        if mes < 10:
            despesa['balanco'].append(f'0{mes}/{ano}')
        else:
            despesa['balanco'].append(f'{mes}/{ano}')

        despesa['categoria'].append(categoria)
        despesa['data_despesa'].append(str(data))
        despesa['cartao'].append(cartao)
        despesa['local'].append(local)
        despesa['responsavel'].append(responsavel)
        despesa['valor'].append(f'{valor_parcelado: .2f}')

        despesa['parcela'].append(f'{parcela_contador}/{int_qtd_parcelas}')

        df_despesa = pd.DataFrame(despesa)

        mes += 1

    #print(df_despesa)
    lista_para_envio = df_despesa.to_dict('records')

    base.inserir_tabela('tb_despesas', lista_para_envio)




def cadastro_despesa_fixa(descricao, valor, categoria, cartao):

    novo_registro_despesa_fixa = [{
    'descricao': descricao,
    'valor': valor,
    'categoria': categoria,
    'cartao': cartao, # Garante que a data vire string se necessário
    }]

    base.inserir_tabela('tb_despesas_fixa', novo_registro_despesa_fixa)





def cadastro_receita(descricao, balanco, categoria, data_receita, valor):

    novo_registro_receita = [{
        'descricao': descricao,
        'balanco': balanco,
        'categoria': categoria,
        'data_receita': str(data_receita), # Garante que a data vire string se necessário
        'valor': valor
    }]

    base.inserir_tabela('tb_receita', novo_registro_receita)




def format_brl(valor):
    try:
        # Garante que o valor é um número float
        valor = float(valor)
        # Formata inicialmente no padrão americano com duas casas decimais: 1250000.32 -> "1,250,000.32"
        fmt = f"{valor:,.2f}"
        # Inverte os separadores para o padrão BR: "1.250.000,32"
        fmt_br = fmt.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {fmt_br}"
    except (ValueError, TypeError):
        return "R$ 0,00"
    
