import subprocess
import sys
import os
from logger import logger

log = logger()
log.debug("Logger initialized.")

dir = os.path.dirname(os.path.abspath(__file__))

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def path(*paths):
    return os.path.abspath(os.path.join(dir, *paths))
def installAll():
    with open(path("dependencies.txt")) as f:
        for line in f:
            install(line.strip())
    log.info("All dependencies installed.")