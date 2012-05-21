import re

import kernel.filesystem

def run(shell, args):
    if args or shell.stdin:
        try:
            expression = re.compile(args[0])
            for x in args[1:]:
                path = shell.iabs_path(x)
                try:
                    f = kernel.filesystem.open_file(path, 'r')
                    for line in f:
                        m = re.match(expression, line)
                        if m is not None:
                            shell.stdout.write(line.rstrip())
                    f.close()
                except IOError:
                    shell.stderr.write("%s does not exist" % (path, ))
            if shell.stdin:
                for line in shell.stdin.read():
                    shell.stdout.write(line)
        except:
            shell.stderr.write("invalid regular expression")
    else:
        shell.stderr.write("missing file operand")

def help():
    a = """
    Grep

    Search for lines in a file matching the pattern given.

    usage: grep [pattern] [path]
    """
    return a
