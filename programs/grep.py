import re

from kernel.utils import Parser
import kernel.filesystem

desc = "Search for lines in a file matching the pattern given."
parser = Parser('grep', name="Grep", description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-e', action="store", type=str, dest="pattern", default='')
pa('-a', action="store_true", dest="all", default=False)
pa('-i', action="store_true", dest="ignorecase", default=False)
pa('-v', action="store_true", dest="invert", default=False)

def run(shell, args):
    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        if args.paths:
            skip = 0
            # re.IGNORECASE is a number
            case = args.ignorecase * re.IGNORECASE
            if not args.pattern:
                pattern = re.compile(args.paths[0], case)
                skip = 1
            else:
                pattern = re.compile(args.pattern, case)

            for path in sorted(args.paths[skip:]):
                grep(shell, args, pattern, path)

            if shell.stdin:
                for line in shell.stdin.read():
                    # use xor to invert the selection
                    if bool(re.findall(pattern, line)) ^ args.invert:
                        shell.stdout.write(line.strip())
            if not shell.stdout:
                shell.stdout.write('')
        else:
            shell.stderr.write("missing file operand")

def grep(shell, args, pattern, path):
    newpath = shell.sabs_path(path)
    if kernel.filesystem.is_file(path):
        f = kernel.filesystem.open_file(newpath, 'r')
        for line in f:
            # use xor to invert the selection
            if bool(re.findall(pattern, line)) ^ args.invert:
                if shell.stdout:
                    shell.stdout.write(line.rstrip())
                else:
                    shell.stdout.write("%s:%s" % (path, line.rstrip()))
        f.close()
    else:
        shell.stderr.write("%s does not exist" % (newpath, ))

def help():
    return parser.help_msg()
