import pandas as pd
import numpy as np
import matplotlib as plt



def infos(df:pd.DataFrame):
    print("Bairros:")
    print(df['location'].unique())

def preencherBairro(df: pd.DataFrame, coluna):
    df[coluna]= df.groupby('location')[coluna].transform(
        lambda x :x.fillna( x.median())
    )
    return df

def tratar_dados(df: pd.DataFrame):
    df['time']= pd.to_datetime(df['time'])


    df_zeros = df.fillna(0)
    print("Percentual NAN por coluna: \n"+ str(df.isnull().mean()*100))
    colunas_faltantes = ['sewer_and_water', 'medical', 'buildings', 'shake_intensity']
    for c in colunas_faltantes:
        df = preencherBairro(df, c)

    print("Percentual NAN por coluna: \n"+ str(df.isnull().mean()*100))

    print("Media dfZero: "+str(df_zeros.mean()))
    print("Media dfmedias: "+str(df.mean()))
    
    'Aqui é melhor colocar a melhor colocar a media do bairro pq fica mais realista do que usar o 0,'
    'pq se remover vai ter coluna que vamos ter que apagar metade dos dados'
    
df = pd.read_csv("MC1/mc1-reports-data.csv")
infos(df)
tratar_dados(df)