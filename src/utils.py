import os

def getFromEnv(key: str) -> str:
    value = os.getenv(key)

    if value is None:
        raise Exception(f"Missing environment variable: {key}")
    
    return value