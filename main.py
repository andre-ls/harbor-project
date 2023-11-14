import functions_framework
import settings
from extractions import docked_ships_extract, operations_extract
from transformations import docked_ships_transform, operations_transform

DATALAKE_PATH = 'gcs://harbor-datalake'

def dockedShipsPipeline():
    rawPath = DATALAKE_PATH + '/raw/docked_ships'
    trustedPath = DATALAKE_PATH + '/trusted/docked_ships'

    savedRawFile = docked_ships_extract.run(rawPath)
    docked_ships_transform.run(savedRawFile,trustedPath)

def operationsPipeline():
    rawPath = DATALAKE_PATH + '/raw/operations'
    trustedPath = DATALAKE_PATH + '/trusted/operations'

    savedRawFile = operations_extract.run(rawPath)
    operations_transform.run(savedRawFile,trustedPath)

def runPipeline():
    settings.init()
    dockedShipsPipeline()
    operationsPipeline()

@functions_framework.http
def cloudEntrypoint(request):
    runPipeline()
    return 'OK'

if __name__ == '__main__':
    runPipeline()
