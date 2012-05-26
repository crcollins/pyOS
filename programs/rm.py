import kernel.filesystem as fs

desc = "Removes the file/directory."
parser = fs.Parser('rm', name="Remove", description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-f', action="store_true", dest="force", default=False)
pa('-r', action="store_true", dest="recursive", default=False)
pa('-v', action="store_true", dest="verbose", default=False)

def run(shell, args):
    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        if len(args.paths) >= 1:
            for path in args.paths:
                remove(shell, args, path)
        else:
            shell.stderr.write("missing file operand")

def remove(shell, args, path):
    path = shell.sabs_path(path)
    if fs.is_file(path) or (fs.is_directory(path) and args.recursive):
        if args.verbose:
            shell.stdout.write("Removing %s" % (path, ))
        fs.remove(path, recursive=args.recursive)
    elif not args.recursive and fs.is_directory(path):
        shell.stderr.write("%s is a directory" % (path, ))
    elif not fs.is_file(path):
        shell.stderr.write("%s is not a file" % (path,))

def help():
    return parser.help_msg()
