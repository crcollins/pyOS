from kernel.system import System
from kernel.constants import SHUTDOWN

def run(shell, args):
    System.state = SHUTDOWN

def help():
    a = """
    Shutdown

    Shuts down the OS.

    usage: shutdown
    """
    return a