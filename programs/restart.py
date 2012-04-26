from kernel.system import System

def run(shell, args):
    System.state = -2

def help():
    a = """
    Restart

    Restarts the OS.

    usage: restart
    """
    return a