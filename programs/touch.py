import kernel.filesystem

def run(shell, args):
    if args:
        for x in args:
            path = shell.sabs_path(x)
            if not kernel.filesystem.exists(path):
                kernel.filesystem.open_file(path, 'w').close()
            else:
                shell.stderr.write("%s already exists" % (path, ))
    else:
        shell.stderr.write("missing file operand")

def help():
    a = """
    Touch

    Creates an empty file at the given path.

    usage: touch [path]
    """
    return a
