def run(shell, args):
    if args:
        path = shell.sabs_path(args[0])
        if shell.syscall.exists(path):
            f = shell.syscall.open_file(path, 'r')
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
