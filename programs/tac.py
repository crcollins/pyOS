import kernel.filesystem

def run(shell, args):
    if args:
        path = shell.iabs_path(args[0])
        if kernel.filesystem.exists(path):
            f = kernel.filesystem.open_file(path, 'r')
            for line in reversed(f.readlines()):
                shell.stdout.write(line)
            f.close()
        else:
            shell.stderr.write("%s does not exist" % (path))
    else:
        shell.stderr.write("missing file operand")

def help():
    a = """
    Etanetacnoc (Reverse Concatenate)

    Reverse concatenate the files at the given paths.

    usage: tac [path]
    """
    return a
