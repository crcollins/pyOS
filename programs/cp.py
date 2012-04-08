import kernel.filesystem

def run(shell, args):
    if len(args) >= 2:
        src = shell.iabs_path(args[0])
        dest = shell.iabs_path(args[1])
        if kernel.filesystem.is_file(src):
            kernel.filesystem.copy(src, dest)
        else:
            print "ERRRRRRR"
    else:
        print "EEERRRR"