def run(shell, args):
    shell.stdout.write(shell.path)

def help():
    a = """
    Print Working Directory

    Prints the path of the current directory.

    usage: pwd
    """
    return a