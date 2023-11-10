import pandas as pd
from utils import file_utils

def readFiles(dockedShipsFile,operationsFile):
    dockedShipsDf = file_utils.readData(dockedShipsFile)
    operationsDf = file_utils.readData(operationsFile)

    return dockedShipsDf, operationsDf

def filterDockedShips(dockedShipsDf):
    return dockedShipsDf[['Navio','Carga','Desembarque','Embarque']]

def mergeDatasets(dockedShipsDf,operationsDf):
    return operationsDf.merge(dockedShipsDf,how='inner',on='Navio')

def generateView(dockedShipsFile,operationsFile,outputPath):
    dockedShipsDf,operationsDf = readFiles(dockedShipsFile,operationsFile)
    dockedShipsDf = filterDockedShips(dockedShipsDf)
    operationsViewDf = mergeDatasets(dockedShipsDf,operationsDf)
    file_utils.saveData(operationsViewDf,outputPath,'parquet')
