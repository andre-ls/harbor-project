import functions_framework
import settings
from extractions import docked_ships_extract, operations_extract
from transformations import docked_ships_transform, operations_transform
from views import dock_view, operations_view

def dockedShipsPipeline(rawPath,trustedPath):
    savedRawFile = docked_ships_extract.run(rawPath)
    savedTrustedFile = docked_ships_transform.run(savedRawFile,trustedPath)
    return savedTrustedFile

def operationsPipeline(rawPath,trustedPath):
    savedRawFile = operations_extract.run(rawPath)
    savedTrustedFile = operations_transform.run(savedRawFile,trustedPath)
    return savedTrustedFile

def runPipeline():
    settings.init()

    dockedShipsRawPath = 'gcs://cloud-7-test/harbor/data/raw/docked_ships'
    dockedShipsTrustedPath = 'gcs://cloud-7-test/harbor/data/trusted/docked_ships'
    operationsRawPath = 'gcs://cloud-7-test/harbor/data/raw/operations'
    operationsTrustedPath = 'gcs://cloud-7-test/harbor/data/trusted/operations'
    dockViewPath = 'gcs://cloud-7-test/harbor/data/views/dock'
    operationsViewPath = 'gcs://cloud-7-test/harbor/data/views/operations'

    dockedShipsTrustedFile = dockedShipsPipeline(dockedShipsRawPath,dockedShipsTrustedPath)
    operationsTrustedFile = operationsPipeline(operationsRawPath,operationsTrustedPath)
    dock_view.generateView(dockedShipsTrustedFile,operationsTrustedFile,dockViewPath)
    operations_view.generateView(dockedShipsTrustedFile,operationsTrustedFile,operationsViewPath)

@functions_framework.http
def cloudEntrypoint(request):
    runPipeline()
    return 'OK'

if __name__ == '__main__':
    runPipeline()
