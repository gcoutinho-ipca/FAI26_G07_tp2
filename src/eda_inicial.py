import pandas as pd
import numpy as np
from pathlib import Path

def run_analysis(file_path):
    try:
        df = pd.read_csv(file_path, low_memory=False)
        interest_cols = ['Price', 'District', 'Type', 'EnergyCertificate', 'NumberOfBathrooms', 
                         'Parking', 'TotalArea', 'ConstructionYear', 'EnergyEfficiencyLevel', 
                         'NumberOfBedrooms', 'NumberOfWC', 'LivingArea', 'LotSize', 'BuiltArea']
        
        print("--- Detalhe de Colunas de Interesse ---")
        print(f"{'Coluna':25} | {'Tipo':15} | {'Missing':10} | {'Total':10}")
        print("-" * 65)
        
        for col in interest_cols:
            if col in df.columns:
                missing = df[col].isnull().sum()
                dtype = str(df[col].dtype)
                total = len(df)
                print(f"{col:25} | {dtype:15} | {missing:10} | {total:10}")
        
        print("\n--- Estatística Descritiva (Target: Price) ---")
        if 'Price' in df.columns:
            print(df['Price'].describe())

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    run_analysis(str(Path(__file__).resolve().parent.parent / 'data' / 'archive' / 'portugal_listinigs.csv'))
