import argparse

import kernel.filesystem

parser = argparse.ArgumentParser(add_help=False)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-n', action="store", type=str, dest="lineamount", default=5)

def run(shell, args):
    if args or shell.stdin:
        args = parser.parse_args(args)
        for x in args.paths:
            path = shell.iabs_path(x)
            if args > 1:
                shell.stdout.write("==> %s <==" %x)
            try:
                f = kernel.filesystem.open_file(path,'r')
                for x in xrange(args.lineamount):
                    shell.stdout.write(f.readline().rstrip())
                f.close()
            except IOError:
                shell.stderr.write("%s does not exist" %(path))
        if shell.stdin:
            if args.paths:
                shell.stdout.write("==> %% stdin %% <==")
            for x in xrange(args.lineamount):
                shell.stdout.write(shell.stdin.readline())
        shell.stdout.write("")
    else:
        shell.stderr.write("missing file operand")

def help():
    a = """
    Head

    Returns the first n lines of a file.

    usage: head [path] [-n 5]
    """
    return a
