import kernel.filesystem

def run(shell, args):
    #hack to fix encapsulation
    shell = shell.parent
    if args:
        if kernel.filesystem.is_directory(shell.iabs_path(args[0])):
            shell.set_curpath(args[0])
        else:
            shell.stderr.write("%s: no such directory" %args[0])

def help():
    a = """
    Change Directory

    Changes the current directory.

    usage: cd [path]
    """
    return a