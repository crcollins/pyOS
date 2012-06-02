import kernel.filesystem


desc = "Creates a directory at the given path."
parser = kernel.filesystem.Parser('mkdir', name="Make Directory", description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-p', action="store_true", dest="parent", default=False)
pa('-v', action="store_true", dest="verbose", default=False)

def run(shell, args):
    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        if args.paths:
            for path in args.paths:
                path = shell.sabs_path(path)
                if not kernel.filesystem.exists(path):
                    if args.verbose:
                        shell.stdout.write("Making directory: %s" %(path, ))
                    kernel.filesystem.make_dir(path, args.parent)
                else:
                    shell.stderr.write("%s already exists" % (path, ))
        else:
            shell.stderr.write("missing directory operand")

def help():
    return parser.help_msg()