import os
import subprocess
from logger import logger

log = logger()
log.debug("Logger initialized.")
readme = os.path.abspath(os.path.join(os.path.dirname(__file__), "../components/readme.txt")) # will be changed later to actually retrieve readme from website
admins = []
users = []
defaults = ["Administrator", "Guest", "DefaultAccount", "WDAGUtilityAccount", "WsiAccount"]
try:
    with open(readme, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    if not lines:
        log.warning("readme file is empty.")
    admins = lines[lines.index("Authorized Administrators:")+1:lines.index("Authorized Users:")-1][::2]
    users = lines[lines.index("Authorized Users:")+1:lines.index("Competition Guidelines")-1]
except Exception as e:
    log.error(f"Could not read readme file: {e}")

def safe_call(func, label):
    try:
        return func()
    except Exception as e:
        log.error(f"{label} - {e}")
        return f"Error in {label}: {e}\n"

def verifyUsers():
    command = [
        "powershell",
        "-Command",
        "Get-LocalUser | Select-Object -ExpandProperty Name"
    ]
    result = subprocess.run(command, capture_output=True, text=True).stdout.splitlines()
    for account in result:
        if account in users or account in admins or account in defaults:
            continue
        log.warning(f"Unauthorized account found: {account}")
        # todo: create pop up that asks for confirmation to delete account before deleting
    return ""

def verifyAccountType():
    command = [
        "powershell",
        "-Command",
        "Get-LocalGroupMember -Group 'Administrators' | Select-Object -ExpandProperty Name"
    ]
    result = subprocess.run(command, capture_output=True, text=True).stdout.splitlines()
    result = [account.split("\\")[-1] for account in result]
    unique_admins = list(set(result) ^ set(admins))
    for admin in unique_admins:
        if admin in defaults:
            continue
        if admin in result:
            log.warning(f"Unauthorized administrator account found: {admin}")
            continue
        if admin in admins:
            log.warning(f"Administrator account missing or without admin rights: {admin}")
    # todo: create pop up that asks for confirmation before removing admin rights
    return ""

def makeAllSecurePasswords():
    return ""

def userPasswordsExpire():
    return ""

def makeUsersChangePasswordNextLogon():
    return ""

def disableDefaultAccounts():
    return ""

def runAll():
    checks = [
        (verifyUsers, "verifyUsers"),
        (verifyAccountType, "verifyAccountType"),
        (makeAllSecurePasswords, "makeAllSecurePasswords"),
        (userPasswordsExpire, "userPasswordsExpire"),
        (makeUsersChangePasswordNextLogon, "makeUsersChangePasswordNextLogon"),
    ]
    return "".join(safe_call(func, label) for func, label in checks)