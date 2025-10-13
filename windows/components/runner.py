from components import gpeditPolicies
from components import securityPolicies
from logger import logger

log = logger()
log.debug("Logger initialized.")

def runComponents():
    securityPolicies.runAll()
    gpeditPolicies.runAll()

def runner(x: int=0):
    if x == 0:
        runComponents()
    else:
        print("idot")