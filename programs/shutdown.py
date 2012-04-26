from kernel.system import System

def run(shell, args):
    System.state = -1

def help():
    a = """
    Shutdown

    Shuts down the OS.

    usage: shutdown
    """
    return a