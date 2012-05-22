import argparse

import kernel.filesystem

parser = argparse.ArgumentParser(add_help=False)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-a', action="store_true", dest="append", default=False)


def run(shell, args):
    args = parser.parse_args(args)
    if args.paths:
        if args.append:
            mode = 'a'
        else:
            mode = 'w'
        if args.paths:
            files = []
            for x in args.paths:
                try:
                    files.append(kernel.filesystem.open_file(x, mode))
                except:
                    pass
            for line in shell.stdin.read():
                for f in files:
                    f.write(line)
                shell.stdout.write(line)
            for f in files:
                f.close()
    else:
        for line in shell.stdin.read():
            print line
            shell.stdout.write(line)

def help():
    a = """
    Tee

    Allows tapping into the stdout to write to multiple files.

    usage: tee [path] [-a]
    """
    return a
