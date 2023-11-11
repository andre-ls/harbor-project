import functions_framework
import settings
from extractions import docked_ships_extract, operations_extract
from transformations import docked_ships_transform, operations_transform
from views import dock_view, operations_view

DATALAKE_PATH = 'gcs://harbor-datalake'

def dockedShipsPipeline():
    rawPath = DATALAKE_PATH + '/raw/docked_ships'
    trustedPath = DATALAKE_PATH + '/trusted/docked_ships'

    savedRawFile = docked_ships_extract.run(rawPath)
    savedTrustedFile = docked_ships_transform.run(savedRawFile,trustedPath)
    return savedTrustedFile

def operationsPipeline():
    rawPath = DATALAKE_PATH + '/raw/operations'
    trustedPath = DATALAKE_PATH + '/trusted/operations'

    savedRawFile = operations_extract.run(rawPath)
    savedTrustedFile = operations_transform.run(savedRawFile,trustedPath)
    return savedTrustedFile

def viewsPipeline(dockedShipsTrustedFile, operationsTrustedFile):

    dockViewPath = DATALAKE_PATH + '/views/dock'
    operationsViewPath = DATALAKE_PATH + '/views/operations'

    dock_view.generateView(dockedShipsTrustedFile,operationsTrustedFile,dockViewPath)
    operations_view.generateView(dockedShipsTrustedFile,operationsTrustedFile,operationsViewPath)

def runPipeline():
    settings.init()

    dockedShipsTrustedFile = dockedShipsPipeline()
    operationsTrustedFile = operationsPipeline()
    viewsPipeline(dockedShipsTrustedFile,operationsTrustedFile)

@functions_framework.http
def cloudEntrypoint(request):
    runPipeline()
    return 'OK'

if __name__ == '__main__':
    runPipeline()
