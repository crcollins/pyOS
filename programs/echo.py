import kernel.filesystem

def run(shell, args):
    shell.stdout.write(" ".join(args))

def help():
    a = """
    Echo

    Prints the arguments into the terminal.

    usage: echo [args]
    """
    return a
