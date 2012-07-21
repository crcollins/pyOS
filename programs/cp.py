from kernel.utils import Parser

desc = "Copies the given file/directory to the given location."
parser = Parser('cp', name="Copy", description=desc)
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
            dest = shell.sabs_path(args.paths[-1])
            if shell.syscall.is_dir(dest) or len(args.paths) == 2:
                for src in args.paths[:-1]:
                    copy(shell, args, src, dest)
            else:
                shell.stderr.write("%s is not a directory" %dest)
        else:
            shell.stderr.write("missing file operand")

def copy(shell, args, src, dest):
    src = shell.sabs_path(src)
    if args.verbose:
        shell.stdout.write("Copying %s to %s" %(src, dest))
    try:
        shell.syscall.copy(src, dest, recursive=args.recursive)
    except IOError:
        shell.stderr.write("file error" %dest)

def help():
    return parser.help_msg()
