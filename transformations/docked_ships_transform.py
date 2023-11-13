import pandas as pd
from utils import file_utils

def processData(df):
    df = df.drop(df.columns[[2,3,4,5]],axis=1)
    df.columns = ['Local','Navio','Carga','Desembarque','Embarque','Data_Extracao']
    df['Desembarque'] = pd.to_numeric(df['Desembarque'])
    df['Embarque'] = pd.to_numeric(df['Embarque'])
    df['Data_Extracao'] = pd.to_datetime(df['Data_Extracao'])

    return df

def run(inputPath,outputPath):
    df = file_utils.readData(inputPath)
    df = processData(df)

    return file_utils.saveData(df,outputPath,'parquet')


