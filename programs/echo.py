def run(shell, args):
    shell.stdout.write(" ".join(args))
    if not shell.stdout:
        shell.stdout.write('')

def help():
    a = """
    Echo

    Writes the arguments into the stdout.

    usage: echo [args]
    """
    return a
