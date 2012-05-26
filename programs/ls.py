import kernel.filesystem

def run(shell, args):
    if args:
        path = shell.sabs_path(args[0])
    else:
        path = shell.path
    a = sorted(kernel.filesystem.list_dir(path))
    if shell.stdout:
        shell.stdout.write('\n'.join(a))
    else:
        maxlen = max([len(x) for x in a])
        # arbitrary line length
        columns = (80 / maxlen) - 1
        shell.stdout.write('')  # skip <out> line
        b = []
        for i, x in enumerate(a):
            newline = "\n" if not ((i + 1) % columns) else ""
            if not ((i + 1) % columns):
                newline = "\n"
                spacing = ""
            else:
                newline = ""
                spacing = " " * (maxlen - len(x) + 1)
            b.append(x + spacing + newline)
        shell.stdout.write(''.join(b).rstrip())
        shell.stdout.write('')  # end with newline

def help():
    a = """
    List Directory

    Returns the contents of the directory.

    usage: ls [path]
    """
    return a
