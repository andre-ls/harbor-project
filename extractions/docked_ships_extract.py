import settings
import requests
import pandas as pd
from bs4 import BeautifulSoup
from utils import file_utils

URL = 'https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/atracados-porto-terminais/'

def extractTable(page):
    table = page.find('table',id='atracados')

    columnNames = extractColumnNames(table)
    rowValues = extractRows(table)

    df = pd.DataFrame(data=rowValues,columns=columnNames)
    df['extract_date'] = settings.EXTRACT_TIME_FORMATTED
    return df

def extractColumnNames(table):
    columnTags = table.find_all('th')[:9]
    return [columnTag.text for columnTag in columnTags]

def extractRows(table):
    rowTags = table.find_all('tr',class_='text-center')
    return list(map(extractRowValues,rowTags))

def extractRowValues(row):
    rowValues = row.find_all('td')[:9]
    return [value.text for value in rowValues]

def run(outputPath):
    html = requests.get(URL).content
    bs = BeautifulSoup(html,'html.parser')

    df = extractTable(bs)
    return file_utils.saveData(df,outputPath,'csv')


