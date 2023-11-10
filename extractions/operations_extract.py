import settings
import requests
import pandas as pd
from bs4 import BeautifulSoup
from utils import file_utils

URL = 'https://www.portodesantos.com.br/painel-de-monitoramento-das-operacoes-portuarias/'

def extractTable(page):
    table = page.find('table',id='monitoramento')

    columnNames = extractColumnNames(table)
    rowValues = extractRows(table)

    df = pd.DataFrame(data=rowValues,columns=columnNames)
    df['extract_date'] = settings.EXTRACT_TIME
    return df

def extractColumnNames(table):
    columnTags = table.find_all('th',style='font-size: 0.8rem !important;',string=True)
    return [columnTag.text for columnTag in columnTags]

def extractRows(table):
    rowTags = table.find_all('tr',class_='text-center')[1:] #First Row is always empty
    return list(map(extractRowValues,rowTags))

def extractRowValues(row):
    rowValues = row.find_all('td')
    return [value.text for value in rowValues]

def run(outputPath):
    html = requests.get(URL).content
    bs = BeautifulSoup(html,'html.parser')

    df = extractTable(bs)
    return file_utils.saveData(df,outputPath,'csv')


