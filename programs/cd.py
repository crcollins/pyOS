def run(shell, args):
    #hack to fix encapsulation
    shell = shell.parent
    if args:
        path = shell.sabs_path(args[0])
        if shell.syscall.is_dir(path):
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
