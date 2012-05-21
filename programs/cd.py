import kernel.filesystem

def run(shell, args):
    #hack to fix encapsulation
    shell = shell.parent
    if args:
        path = shell.iabs_path(args[0])
        if kernel.filesystem.is_directory(path):
            shell.set_path(path)
        else:
            shell.stderr.write("%s: no such directory" % (path, ))

def help():
    a = """
    Change Directory

    Changes the current directory.

    usage: cd [path]
    """
    return a
