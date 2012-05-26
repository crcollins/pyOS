import argparse

import kernel.filesystem

desc = "Copies the given file/directory to the given location."
parser = kernel.filesystem.Parser('cp', description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-f', action="store_true", dest="force", default=False)
pa('-r', action="store_true", dest="recursive", default=False)
pa('-v', action="store_true", dest="verbose", default=False)

def run(shell, args):
    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        if len(args.paths) >= 2:
            dest = shell.iabs_path(args.paths[-1])
            if kernel.filesystem.is_directory(dest) or len(args.paths) == 2:
                for src in args.paths[:-1]:
                    src = shell.iabs_path(src)
                    if args.verbose:
                        shell.stdout.write("Copying %s to %s" %(src, dest))
                    try:
                        kernel.filesystem.copy(src, dest, recursive=args.recursive)
                    except IOError:
                        shell.stderr.write("file error" %dest)
            else:
                shell.stderr.write("%s is not a directory" %dest)
        else:
            shell.stderr.write("missing file operand")

def help():
    return parser.format_help()