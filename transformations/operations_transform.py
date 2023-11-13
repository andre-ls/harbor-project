import pandas as pd
from utils import file_utils
from datetime import datetime

def processData(df):
    df = df.drop(df.columns[[4,8]],axis=1)
    df.columns = ['Local','Viagem','Navio','Agente','Atracamento','Inicio_Operacao','Operador','Movimentacao_%','Status','Estimativa_Fim_Operacao','Data_Extracao']
    df['Atracamento'] = df['Atracamento'].apply(lambda x:formatDate(x))
    df['Inicio_Operacao'] = df['Inicio_Operacao'].apply(lambda x:formatDate(x))
    df['Movimentacao_%'] = pd.to_numeric(df['Movimentacao_%'].apply(lambda x:cleanMovementRows(x)))

    return df

def cleanMovementRows(row):
    row = row.replace('%','').replace(',','.')
    row = row[:len(row)//2]

    if row == '':
        row = '0'

    return row

def formatDate(row):
    if row == row: #Filter NaN Values
        row = datetime.strptime(row,'%d/%m/%y %H:%M:%S')
        return row.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return row

def run(inputPath,outputPath):
    df = file_utils.readData(inputPath)
    df = processData(df)

    return file_utils.saveData(df,outputPath,'parquet')





