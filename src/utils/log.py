import os
import time

def lastLog() -> str:
    i = 0

    while True:
        if os.path.exists(f'logs/run_{i}.log'):
            i += 1
        else:
            break

    return i - 1

def initLog() -> str:
    logFilePath = f'logs/run_{lastLog() + 1}.log'

    with open(logFilePath, 'w') as _:
        pass

    addLog('Log file created')

def addLog(message: str) -> None:
    logFilePath = f'logs/run {lastLog()}.log'
    with open(logFilePath, 'a') as file:
        file.write(f'{time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())} : {message}\n')

    return