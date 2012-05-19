from kernel.system import System
from kernel.constants import SHUTDOWN

def run(shell, args):
    System.state = RESTART

def help():
    a = """
    Restart

    Restarts the OS.

    usage: restart
    """
    return a