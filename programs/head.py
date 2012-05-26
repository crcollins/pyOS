import kernel.filesystem

desc = "Returns the first n lines of a file."
parser = kernel.filesystem.Parser('head', description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-n', action="store", type=int, dest="lineamount", default=5)

def run(shell, args):
    print 
    if args or shell.stdin:
        args = parser.parse_args(args)
        for x in args.paths:
            path = shell.iabs_path(x)
            if args > 1:
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
        shell.stderr.write("missing file operand")

def help():
    return parser.format_help()
