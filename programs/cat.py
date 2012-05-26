import kernel.filesystem

def run(shell, args):
    if args or shell.stdin:
        for x in args:
            path = shell.iabs_path(x)
            try:
                f = kernel.filesystem.open_file(path, 'r')
                for line in f:
                    shell.stdout.write(line.rstrip())
                f.close()
            except IOError:
                shell.stderr.write("%s does not exist" % (path))
        if shell.stdin:
            for line in shell.stdin.read():
                shell.stdout.write(line.rstrip())
    else:
        shell.stderr.write("missing file operand")

def help():
    a = """
    Concatenate

    Concatenate the files at the given paths.

    usage: cat [path]
    """
    return a
