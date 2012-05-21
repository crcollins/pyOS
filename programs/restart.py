from kernel.system import System
from kernel.constants import REBOOT

def run(shell, args):
    System.state = REBOOT

def help():
    a = """
    Restart

    Restarts the OS.

    usage: restart
    """
    return a
