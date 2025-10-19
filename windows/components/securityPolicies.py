import os
import subprocess
from logger import logger

log = logger()
log.debug("Logger initialized.")

def safe_call(func, label):
    try:
        return func()
    except Exception as e:
        log.error(f"{label} - {e}")
        return f"Error in {label}: {e}\n"

def accountPolicy():
    return ""

def accountLockoutPolicy():
    return ""

def remoteDesktop():
    return ""

def autoplay():
    return ""

def runAll():
    checks = [
        (accountPolicy, "accountPolicy"),
        (accountLockoutPolicy, "accountLockoutPolicy"),
        (remoteDesktop, "remoteDesktop"),
        (autoplay, "autoplay"),
    ]
    return "".join(safe_call(func, label) for func, label in checks)