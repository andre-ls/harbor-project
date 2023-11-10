import os
import settings
import pandas as pd
from google.cloud import storage

def readData(filePath):
    if '.csv' in filePath:
        return pd.read_csv(filePath)
    elif '.parquet' in filePath:
        return pd.read_parquet(filePath)
    else:
        raise Exception('Could not read file ' + filePath)

def checkDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path,exist_ok=True)

def saveData(df,layerPath,fileFormat):
    if fileFormat not in ['csv','parquet']:
        raise Exception('Unrecognized file format. Only csv or parquet are accepted.')

    outerPath = layerPath + '/' + settings.FILE_PATH
    fullPath = outerPath + '/' + settings.FILE_NAME + '.' + fileFormat

    if 'gs://' not in outerPath: #If directory not on Cloud, check Locally
        checkDirectory(outerPath)

    if fileFormat == 'csv':
        df.to_csv(fullPath,index=False)
    elif fileFormat == 'parquet':
        df.to_parquet(fullPath,index=False)

    return fullPath
