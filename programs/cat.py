import kernel.filesystem

def run(shell, args):
    if args:
        path = shell.iabs_path(args[0])
        if kernel.filesystem.exists(path):
            f = kernel.filesystem.open_file(path,'w')
            for line in f:
                shell.stdout.write(line)
            f.close()
        else:
            shell.stderr.write("%s does not exist" %(path))
    else:
        shell.stderr.write("missing file operand")

def help():
    a = """
    Concatenate

    Concatenate the files at the given paths.

    usage: cat [path]
    """
    return a