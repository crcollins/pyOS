import argparse

import kernel.filesystem

parser = argparse.ArgumentParser(add_help=False)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-f', action="store_true", dest="force", default=False)
pa('-r', action="store_true", dest="recursive", default=False)
pa('-v', action="store_true", dest="verbose", default=False)

def run(shell, args):
    args = parser.parse_args(args)
    if len(args.paths) >= 2:
        src = shell.iabs_path(args[0])
        dest = shell.iabs_path(args[1])
        if kernel.filesystem.is_file(src):
            if kernel.filesystem.is_dir(dest):
                if args.verbose:
                    print "Copying %s to %s" %(src, dest)
                kernel.filesystem.copy(src, dest)
            else:
                print dest, "is not a directory"
        else:
            print src, "is not a file"
    else:
        print "missing file operand"

def help(shell):
    print "HELP"