import os

def fromEnv(var_name):
    return os.getenv(var_name)


TK = fromEnv("TK_SCENE")
