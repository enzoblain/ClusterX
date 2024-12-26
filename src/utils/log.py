import os
import time
import inspect

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

    addLog(f'Log file created')
    print(f'Log file created at {logFilePath}')

def addLog(message: str) -> None:
    logFilePath = f'logs/run_{lastLog()}.log'
    with open(logFilePath, 'a') as file:
        file.write(f'{time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())} : {message}\n')

    return

def displayError(error_message: str) -> None:
    caller_function  = caller = inspect.stack()[1].function
    caller_file = inspect.stack()[1].filename

    addLog(f"ERROR in '{caller_function}' (file: {caller_file}): {error_message}")

    exit()