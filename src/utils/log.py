import time
import inspect

def initLog() -> str:
    logFilePath = f'logs/run.log'

    with open(logFilePath, 'w') as _:
        pass

    addLog(f'Log file created')
    print(f'Log file created at {logFilePath}')

def addLog(message: str) -> None:
    logFilePath = f'logs/run.log'
    with open(logFilePath, 'a') as file:
        file.write(f'{time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())} : {message}\n')

    return

def displayError(error_message: str) -> None:
    caller_function  = inspect.stack()[1].function
    caller_file = inspect.stack()[1].filename

    addLog(f"ERROR in '{caller_function}' (file: {caller_file}): {error_message}")

    exit()