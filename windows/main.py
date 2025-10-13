from installer import installAll
from gui import launchGUI
from components.runner import runner
from logger import logger

log = logger()
log.debug("Logger initialized.")

def main():
    installAll()
    launchGUI(runner)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.error(e)
