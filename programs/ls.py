import kernel.filesystem

def run(shell, args):
    if args:
        path = shell.iabs_path(args[0])
    else:
        path = shell.path
    a = '\n'.join(kernel.filesystem.list_dir(path))
    shell.stdout.write(a)

def help():
    a = """
    List Directory

    Returns the contents of the directory.

    usage: ls [path]
    """
    return a