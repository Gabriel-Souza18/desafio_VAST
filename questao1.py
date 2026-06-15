import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def infos(df:pd.DataFrame):
    print("Bairros:")
    print(df['location'].unique())



def contar_NaN(df :pd.DataFrame):
    colunas = ['sewer_and_water', 'medical', 'buildings', 'shake_intensity']
    # Contar NaN por bairro em cada coluna
    nan_por_bairro = df.groupby('location')[colunas].apply(lambda x: x.isna().sum())
    print("NaN por bairro:\n"+str(nan_por_bairro))


    print("Percentual NAN por coluna: \n"+ str(df.isnull().mean()*100))


def tratar_dados(df: pd.DataFrame):
    df['time']= pd.to_datetime(df['time'])
    contar_NaN(df)

    df_zeros = df.fillna(0) #preenhida em 0 nos NaN

    print("Percentual NAN por coluna(ANTES): \n"+ str(df.isnull().mean()*100))
    colunas_faltantes = ['sewer_and_water', 'medical', 'buildings', 'shake_intensity']
    for c in colunas_faltantes:
        nan_pct_por_bairro = df.groupby('location')[c].transform(lambda x: x.isna().mean())
        
        mediana_por_bairro = df.groupby('location')[c].transform('median')
        
    
        # Se o percentual de NaNs no bairro for maior que 80% (0.80), preenche com 0.
        # Caso contrário, preenche com a mediana daquele bairro.
        df[c] = np.where(
            nan_pct_por_bairro > 0.80,
            df[c].fillna(0),
            df[c].fillna(mediana_por_bairro)
        )
        
        # Caso algum bairro inteiro seja NaN (a mediana retorna NaN), garantimos o preenchimento com 0
        df[c] = df[c].fillna(0)

        
    print("Percentual NaN por coluna(DEPOIS): \n"+ str(df.isnull().mean()*100))
    print("Media dfmedias: "+str(df.mean()))
    print("Media dfZero: "+str(df_zeros.mean()))
    'Aqui é melhor colocar a melhor colocar a media do bairro pq fica mais realista do que usar o 0,'
    'pq se remover vai ter coluna que vamos ter que apagar metade dos dados'
    
    return df

def prioridades(df: pd.DataFrame):
    bairros_map = {
        1: '1 - Palace Hills', 2: '2 - Northwest', 3: '3 - Old Town', 4: '4 - Safe Town',
        5: '5 - Southwest', 6: '6 - Downtown', 7: '7 - Wilson Forest', 8: '8 - Scenic Vista',
        9: '9 - Broadview', 10: '10 - Chapparal', 11: '11 - Terrapin Springs', 12: '12 - Pepper Mill',
        13: '13 - Cheddarford', 14: '14 - Easton', 15: '15 - Weston', 16: '16 - Southton',
        17: '17 - Oak Willow', 18: '18 - East Parton', 19: '19 - West Parton'
    }
    
    # Criando a nova coluna de nomes
    df['location_name'] = df['location'].map(bairros_map)
    #Talvez variar esses valores de prioridade

    df['priority_score'] = (
        df['buildings'] * 0.25 +         
        df['power'] * 0.20 +             
        df['medical'] * 0.15 +           
        df['roads_and_bridges'] * 0.15 + 
        df['sewer_and_water'] * 0.15 +   
        df['shake_intensity'] * 0.10     
    )
    # Agregar por bairro (média do score)
    priority_by_neigh = df.groupby('location_name')['priority_score'].mean().sort_values(ascending=False)

    print("Ranking de prioridade por bairro (score médio):")
    print(priority_by_neigh)
    return priority_by_neigh

def gerar_graficos(df:pd.DataFrame, priority_by_neigh):
    os.makedirs('graficos', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # exemplo: 20260614_162826

    sns.set_style("whitegrid")
    
    # Gráfico 1: Top 10 bairros (barras horizontais)
    top10 = priority_by_neigh.head(10)
    plt.figure(figsize=(10, 6))
    top10.sort_values().plot(kind='barh', color='crimson')
    plt.xlabel('Score de prioridade')
    plt.title('Top 10 bairros com maior necessidade de resposta emergencial')
    plt.tight_layout()

    plt.savefig("graficos/grafico1"+timestamp)
    
    # Gráfico 2: Heatmap de danos por bairro (todos os 19 bairros)
    damage_cols = ['buildings', 'roads_and_bridges', 'power', 'sewer_and_water', 'medical', 'shake_intensity']
    avg_by_neigh = df.groupby('location_name')[damage_cols].mean()
    
    avg_by_neigh = avg_by_neigh.sort_index(key=lambda x: x.str.split(' - ').str[0].astype(int))
    plt.figure(figsize=(14, 10))
    sns.heatmap(avg_by_neigh, annot=True, cmap='Reds', fmt='.1f', 
                cbar_kws={'label': 'Intensidade média (0-10)'})
    plt.title('Intensidade média de danos por bairro (valores preenchidos com mediana)')
    plt.tight_layout()
    plt.savefig("graficos/grafico2"+timestamp)

df = pd.read_csv("MC1/mc1-reports-data.csv")
infos(df)
df = tratar_dados(df)
pr = prioridades(df=df)
gerar_graficos(df,pr)