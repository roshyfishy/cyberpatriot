import os
import subprocess
from logger import logger

log = logger()
log.debug("Logger initialized.")
readme = os.path.abspath(os.path.join(os.path.dirname(__file__), "../components/readme.txt")) # will be changed later to actually retrieve readme from website
you = ""
admins = []
users = []
known_defaults = ["Administrator", "Guest", "DefaultAccount", "WDAGUtilityAccount", "WsiAccount", "INTERACTIVE", "Authenticated Users"]
defaults = []

try:
    with open(readme, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    if not lines:
        log.warning("readme file is empty.")
    try:
        admins = lines[lines.index("Authorized Administrators:")+1:lines.index("Authorized Users:")-1][::2]
        you = admins.pop(0).replace(" (you)", "").strip()
    except ValueError:
        raise Exception(ValueError("Missing Authorized Administrators section in readme file"))
    try:
        users = lines[lines.index("Authorized Users:")+1:lines.index("Competition Guidelines")-1]
    except ValueError:
        raise Exception(ValueError("Missing Authorized Users section in readme file"))
except Exception as e:
    log.critical(f"Could not read readme file: {e}")
    raise Exception(f"Could not read readme file: {e}")

defaults.extend([u for u in users if u in known_defaults])
users = [u for u in users if u not in known_defaults]

defaults.extend([a for a in admins if a in known_defaults])
admins = [a for a in admins if a not in known_defaults]




def safe_call(func, label):
    try:
        return func()
    except Exception as e:
        log.error(f"{label} - {e}")
        return f"Error in {label}: {e}\n"

def verifyUsers():
    command = [
        "powershell.exe",
        "-NoProfile",
        "-Command",
        "Get-LocalUser | Select-Object -ExpandProperty Name"
    ]
    result = subprocess.run(command, capture_output=True, text=True).stdout.splitlines()
    for account in result:
        if account in users or account in admins or account in defaults:
            continue
        log.warning(f"verifyUsers - Unauthorized account found: {account}")
        # todo: create pop up that asks for confirmation to delete account before deleting and creates missing accounts
    return ""

def verifyAccountType():
    command = [
        "powershell.exe",
        "-NoProfile",
        "-Command",
        "Get-LocalGroupMember -Group 'Administrators' | Select-Object -ExpandProperty Name"
    ]
    result = subprocess.run(command, capture_output=True, text=True).stdout.splitlines()
    result = [account.split("\\")[-1] for account in result]
    unique_admins = list(set(result) ^ set(admins))
    for admin in unique_admins:
        if admin in defaults or admin == you:   
            continue
        if admin in result:
            log.warning(f"verifyAccountType - Unauthorized administrator account found: {admin}")
            continue
        if admin in admins:
            log.warning(f"verifyAccountType - Administrator account missing or without admin rights: {admin}")
    # todo: create pop up that asks for confirmation before removing/adding admin rights or deleting the user
    command = [
        "powershell.exe",
        "-NoProfile",
        "-Command",
        "Get-LocalGroupMember -Group 'Users' | Select-Object -ExpandProperty Name"
    ]
    result = subprocess.run(command, capture_output=True, text=True).stdout.splitlines()
    result = [account.split("\\")[-1] for account in result]
    unique_users = list(set(result) ^ set(users))
    for user in unique_users:
        if user in defaults or user in admins or user == you:
            continue
        if user in result:
            log.warning(f"verifyAccountType - Unauthorized user account found: {user}")
            continue
        if user in users:
            log.warning(f"verifyAccountType - User account missing or with admin rights: {user}")
    # todo: create pop up that asks for confirmation before adding/removing admin rights or creating the user
    return ""

def makeAllSecurePasswords():
    flag = False
    for account in users + admins:
        command = [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            f"Set-LocalUser -Name '{account}' -Password (ConvertTo-SecureString -AsPlainText 'Cyb3rP@trIot' -Force)"
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            log.error(f"makeAllSecurePasswords - Failed to reset password for {account}: {e}")
            flag = True

    return "Failed to reset passwords for some accounts.\n" if flag else ""

def userPasswordsExpire():
    flag = False
    for account in users + admins:
        command = [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            f"Set-LocalUser -Name '{account}' -PasswordNeverExpires $false"
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            log.error (f"userPasswordsExpire - Failed to set password expiration for {account}: {e}")
            flag = True
    return "Failed to set password expiration for some accounts.\n" if flag else ""

def makeUsersChangePasswordNextLogon():
    flag = False
    for account in users + admins:
        command = [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            f"net user '{account}' /logonpasswordchg:yes"
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            log.error (f"makeUsersChangePasswordNextLogon - Failed to set password change for {account}: {e}")
            flag = True
    return "Failed to set password change for some accounts.\n" if flag else ""

def disableDefaultAccounts():
    flag = False
    for account in defaults:
        command = [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            f"Disable-LocalUser -Name '{account}'"
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            log.error (f"disableDefaultAccounts - Failed to disable account {account}: {e}")
            flag = True
    return "Failed to disable some default accounts.\n" if flag else ""

def runAll():
    checks = [
        (verifyUsers, "verifyUsers"),
        (verifyAccountType, "verifyAccountType"),
        (makeAllSecurePasswords, "makeAllSecurePasswords"),
        (userPasswordsExpire, "userPasswordsExpire"),
        (makeUsersChangePasswordNextLogon, "makeUsersChangePasswordNextLogon"),
        (disableDefaultAccounts, "disableDefaultAccounts"),
    ]
    return "".join(safe_call(func, label) for func, label in checks)