from components import securityPolicies
from components import userAccounts
from logger import logger

log = logger()
log.debug("Logger initialized.")

def runComponents():
    components = [
        securityPolicies,
        userAccounts,
    ]
    results = [component.runAll() for component in components]
    result = "".join(results)
    return result if result else "success"

def runner(x: int = 0):
    actions = {
        0: runComponents,
        1: securityPolicies.runAll,
        2: userAccounts.runAll,
    }

    action = actions.get(x)
    if action:
        try:
            result = action()
            return result if result else "success"
        except Exception as e:
            log.error(f"Error in runner({x}): {e}")
            return f"Error in runner({x}): {e}"
    else:
        log.error(f"Invalid runner argument: {x}")
        return f"Invalid runner option: {x}"