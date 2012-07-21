from kernel.utils import Parser

desc = "Allows tapping into the stdout to write to multiple files."
parser = Parser('tee', name="Tee",  description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-a', action="store_true", dest="append", default=False)

def run(shell, args):
    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        if args.paths:
            if args.append:
                mode = 'a'
            else:
                mode = 'w'
            if args.paths:
                files = []
                for x in args.paths:
                    try:
                        files.append(shell.syscall.open_file(x, mode))
                    except:
                        pass
                for line in shell.stdin.read():
                    for f in files:
                        f.write(line)
                    shell.stdout.write(line)
                for f in files:
                    f.close()
        else:
            for line in shell.stdin.read():
                print line
                shell.stdout.write(line)

def help():
    return parser.help_msg()
