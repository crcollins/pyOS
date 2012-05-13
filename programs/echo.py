import kernel.filesystem

def run(shell, args):
    shell.stdout.write(" ".join(args))

def help():
    a = """
    Echo

    Writes the arguments into the stdout.

    usage: echo [args]
    """
    return a
