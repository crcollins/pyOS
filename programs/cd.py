def run(shell, args):
    #hack to fix encapsulation
    shell = shell.parent
    if args:
        shell.set_curpath(args[0])

def help():
    a = """
    Change Directory

    Changes the current directory.

    usage: cd [path]
    """
    return a