import kernel.filesystem

def run(shell, args):
    if args:
        path = shell.sabs_path(args[0])
        if not kernel.filesystem.exists(path):
            kernel.filesystem.make_dir(path)
        else:
            shell.stderr.write("%s already exists" % (path, ))
    else:
        shell.stderr.write("missing directory operand")

def help():
    a = """
    Make Directory

    Creates a directory at the given path.

    usage: mkdir [path]
    """
    return a
