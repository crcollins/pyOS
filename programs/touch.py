def run(shell, args):
    if args:
        path = shell.iabs_path(args[0])
        if not kernel.filesystem.exists(path):
            f = kernel.filesystem.open_file(path,'w')
            f.close()
        else:
            shell.stderr.write("%s already exists" %(path))
    else:
        shell.stderr.write("missing file operand")

def help():
    a = """
    Touch

    Creates an empty file at the given path.

    usage: touch [path]
    """
    return a