#%%
import pandas as pd
import re
import numpy as np

dict_number = {0:1, 1:2, 2:3, 3:4, 4:5,5:6,6:7,7:8,8:9,9:0}

df = pd.read_csv('doacoes.csv', sep=';', encoding='iso8859_1')


def transform_number(x):
    x = str(x)
    x = re.sub(r'[^\w\s]', "", x)
    x = re.sub(r' ', "", x)

    return x

def departure_number(x):
    x = str(x)
    dict_number = {'0':'1', '1':'2', '2':'3', '3':'4', '4':'5','5':'6','6':'7','7':'8','8':'9','9':'0'}
    x = "".join([dict_number[l] if l in dict_number else l for l in x])
    return x

#%%
df.columns
#%%
# Seleção de colunas
df_selected = df[['Nome do comprador', 'CPF / CNPJ', 'Telefone', 'E-mail', 'Cidade',
                'Estado']]
# Rename columns
dict_column = {'Nome do comprador':'NOME', 'CPF / CNPJ':'CPF',
             'Telefone':'TELEFONE','E-mail':'EMAIL', 'Cidade':'CIDADE', 'Estado':'ESTADO'}
df_selected.columns = df_selected.columns.map(dict_column)

# Transform number cpf
df_selected = df_selected.dropna(subset=['CPF', 'TELEFONE'])
df_selected['ID'] = df_selected['CPF'].apply(transform_number)
df_selected['TELEFONE'] = df_selected['TELEFONE'].apply(transform_number)

df_selected['ID'] = df_selected['ID'].apply(departure_number)
df_selected['ID'] = df_selected['ID'].astype('int64')
df_selected['TELEFONE'] = df_selected['TELEFONE'].astype('int64')

df_selected = df_selected[['CPF', 'ID','NOME', 'TELEFONE', 'EMAIL','CIDADE', 'ESTADO']]
df_selected = df_selected.drop_duplicates(subset=['TELEFONE','CPF'], keep='last')
#%%
df_selected = df_selected.drop('CPF', axis=1)
df_selected.to_csv('BEMDAMADRUGADA_DATA.csv', index=False, encoding='utf-8')
# %%
df_selected.info()
# %%
# https://github.com/StephenFilippone