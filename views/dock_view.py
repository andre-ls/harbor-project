import pandas as pd
from utils import file_utils

def readFiles(dockedShipsFile,operationsFile):
    dockedShipsDf = file_utils.readData(dockedShipsFile)
    operationsDf = file_utils.readData(operationsFile)

    return dockedShipsDf, operationsDf

def filterOperations(operationsDf):
    operationsDf = operationsDf[['Navio','Status','Movimentacao_%']]
    operationsDf = operationsDf.groupby('Navio').first()

    return operationsDf

def mergeDatasets(dockedShipsDf,operationsDf):
    return dockedShipsDf.merge(operationsDf,how='inner',on='Navio')

def generateView(dockedShipsFile,operationsFile,outputPath):
    dockedShipsDf, operationsDf = readFiles(dockedShipsFile,operationsFile)
    operationsDf = filterOperations(operationsDf)
    dockViewDf = mergeDatasets(dockedShipsDf,operationsDf)
    file_utils.saveData(dockViewDf,outputPath,'parquet')
