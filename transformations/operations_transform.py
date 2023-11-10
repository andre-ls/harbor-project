import pandas as pd
from utils import file_utils

def processData(df):
    df = df.drop(df.columns[[4,8]],axis=1)
    df.columns = ['Local','Viagem','Navio','Agente','Atracamento','Inicio_Operacao','Operador','Movimentacao_%','Status','Estimativa_Fim_Operacao','Data_Extracao']
    df['Atracamento'] = pd.to_datetime(df['Atracamento'],format='%d/%m/%y %H:%M:%S')
    df['Inicio_Operacao'] = pd.to_datetime(df['Inicio_Operacao'],format='%d/%m/%y %H:%M:%S')
    df['Estimativa_Fim_Operacao'] = pd.to_datetime(df['Estimativa_Fim_Operacao'],format='%Y-%m-%d %H:%M:%S')
    df['Movimentacao_%'] = df['Movimentacao_%'].apply(lambda x:cleanMovementRows(x))
    df['Movimentacao_%'] = pd.to_numeric(df['Movimentacao_%'])

    return df

def cleanMovementRows(row):
    row = row.replace('%','').replace(',','.')
    row = row[:len(row)//2]

    if row == '':
        row = '0'

    return row

def run(inputPath,outputPath):
    df = file_utils.readData(inputPath)
    df = processData(df)

    return file_utils.saveData(df,outputPath,'parquet')





