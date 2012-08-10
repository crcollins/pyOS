from kernel.utils import Parser

desc = "Creates a directory at the given path."
parser = Parser('mkdir', name="Make Directory", description=desc)
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
                make_dir(shell, args, path)
        else:
            shell.stderr.write("missing directory operand")

def make_dir(shell, args, path):
    path = shell.sabs_path(path)
    if not shell.syscall.exists(path):
        paths = []
        if args.parent:
            while True:
                paths.append(path)
                path = shell.syscall.dir_name(path)
                if shell.syscall.is_dir(path):
                    break
        else:
            paths.append(path)
        for x in reversed(paths):
            if args.verbose:
                shell.stdout.write("Making directory: %s" %(path, ))
            try:
                shell.syscall.make_dir(x)
            except IOError:
                shell.stderr.write("could not make directory %s" % (path, ))
                break
                # TODO # delete on fail?
    else:
        shell.stderr.write("%s already exists" % (path, ))

def help():
    return parser.help_msg()