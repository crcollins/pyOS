import argparse

import kernel.filesystem

parser = argparse.ArgumentParser(add_help=False)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-n', action="store", type=int, dest="lineamount", default=5)

def run(shell, args):
    if args or shell.stdin:
        args = parser.parse_args(args)
        for x in args.paths:
            path = shell.iabs_path(x)
            if args > 1:
                shell.stdout.write("==> %s <==" %x)
            try:
                f = kernel.filesystem.open_file(path,'r')
                for line in f.readlines()[-args.lineamount:]:
                    shell.stdout.write(line.rstrip())
                f.close()
            except IOError:
                shell.stderr.write("%s does not exist" %(path))
        if shell.stdin:
            if args.paths:
                shell.stdout.write("==> %% stdin %% <==")
            for line in shell.stdin.readlines()[-args.lineamount:]:
                shell.stdout.write(line)
        shell.stdout.write("")
    else:
        shell.stderr.write("missing file operand")

def help():
    a = """
    Tail

    Returns the last n lines of a file.

    usage: tail [path] [-n 5]
    """
    return a
