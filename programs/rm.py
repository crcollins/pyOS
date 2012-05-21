import argparse

import kernel.filesystem as fs

parser = argparse.ArgumentParser(add_help=False)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-f', action="store_true", dest="force", default=False)
pa('-r', action="store_true", dest="recursive", default=False)
pa('-v', action="store_true", dest="verbose", default=False)

def run(shell, args):
    args = parser.parse_args(args)
    if len(args.paths) >= 1:
        for path in args.paths:
            path = shell.iabs_path(path)
            if fs.is_file(path) or (fs.is_directory(path) and args.recursive):
                if args.verbose:
                    shell.stdout.write("Removing %s" % (path, ))
                fs.remove(path, recursive=args.recursive)
            else:
                if not args.recursive and fs.is_directory(path):
                    shell.stderr.write("%s is a directory" % (path, ))
                elif not fs.is_file(path):
                    shell.stderr.write("%s is not a file" % (path,))
    else:
        shell.stderr.write("missing file operand")

def help():
    a = """
    Remove

    Removes the file/directory.

    usage: rm [path]
    """
    return a
