import time
from . import helpers

def run():
    for x in range(10):
        for y in range(50):
            time.sleep(0.01)
            helpers.setProgress(x/10, y/50)