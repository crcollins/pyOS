from kernel.utils import Parser
import kernel.filesystem

desc = "Returns the command history."
parser = Parser('history', name="History", description=desc)
pa = parser.add_argument
pa('bla', type=str, nargs='*',)

def run(shell, args):
    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        mlen = len(str(len(shell.prevcommands))) + 1
        format = "{0:%dd}  {1}" % mlen
        for i, line in enumerate(shell.prevcommands):
            if not shell.stdout:
                msg = format.format(i, line)
            else:
                msg = line
            shell.stdout.write(msg)

def help():
    return parser.help_msg()
