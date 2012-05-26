import kernel.filesystem

desc = "Returns the last n lines of a file."
parser = kernel.filesystem.Parser('tail', name="Tail", description=desc)
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
                for line in f.readlines()[-args.lineamount:]:
                    shell.stdout.write(line.rstrip())
                f.close()
            except IOError:
                shell.stderr.write("%s does not exist" % (path, ))
        shell.stdout.write("")
        if shell.stdin:
            if args.paths:
                shell.stdout.write("==> %% stdin %% <==")
            for line in shell.stdin.readlines()[-args.lineamount:]:
                shell.stdout.write(line)
            shell.stdout.write("")
        else:
            if not args.paths:
                shell.stderr.write("missing file operand")

def help():
    return parser.help_msg()
