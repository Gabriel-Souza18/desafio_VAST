import pandas as pd
import numpy as np
import matplotlib as plt

def main():
    df = pd.read_csv("MC1/mc1-reports-data.csv")
    print(df.head)
    print(df.info)
    print(df['location'].unique())


main()