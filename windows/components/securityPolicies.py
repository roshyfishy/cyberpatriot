import os
import subprocess
from logger import logger

log = logger()
log.debug("Logger initialized.")

def accountPolicy():
    pass
def accountLockoutPolicy():
    pass

def runAll():
    accountPolicy()
    accountLockoutPolicy()