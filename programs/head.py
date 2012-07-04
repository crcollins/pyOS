from kernel.utils import Parser
import kernel.filesystem

desc = "Returns the first n lines of a file."
parser = Parser('head', name="Head", description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-n', action="store", type=int, dest="lineamount", default=5)

def run(shell, args):
    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        for x in args.paths:
            path = shell.sabs_path(x)
            if args.paths > 1 or shell.stdin:
                shell.stdout.write("==> %s <==" % (x, ))
            try:
                f = kernel.filesystem.open_file(path, 'r')
                for x in xrange(args.lineamount):
                    shell.stdout.write(f.readline().rstrip())
                f.close()
            except IOError:
                shell.stderr.write("%s does not exist" % (path))
        if shell.stdin:
            if args.paths:
                shell.stdout.write("==> %% stdin %% <==")
            for x in xrange(args.lineamount):
                shell.stdout.write(shell.stdin.readline())
            shell.stdout.write("")
        else:
            if not args.paths:
                shell.stderr.write("missing file operand")

def help():
    return parser.help_msg()
