from datetime import datetime

def init():
    global EXTRACT_TIME
    global FILE_PATH
    global FILE_NAME
    EXTRACT_TIME = datetime.now()
    FILE_PATH = EXTRACT_TIME.strftime('%Y-%m-%d')
    FILE_NAME = EXTRACT_TIME.strftime('%H:%M:%S')
