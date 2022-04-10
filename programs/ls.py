from kernel.utils import Parser, calc_permission_string

desc = "Returns the contents of a directory."
parser = Parser('ls', name="List Directory", description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-l', action="store_true", dest="long", default=False)
pa('-a', action="store_true", dest="all", default=False)

def run(shell, args):
    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        if args.paths:
            paths = args.paths
        else:
            paths = [shell.get_path()]
        for relpath in sorted(paths):
            ls(shell, relpath, args)

def ls(shell, relpath, args):
    fscp = calc_permission_string
    fsgm = shell.syscall.get_meta_data
    fsbn = shell.syscall.base_name
    format = "%s %s %s %s"
    path = shell.sabs_path(relpath)
    try:
        a = shell.syscall.list_dir(path)
        if args.long:
            b = [fsgm(shell.sabs_path(shell.syscall.join_path(path, x))) for x in a]
            a = [format % (fscp(perm), owner, "1", fsbn(name)) for name, owner, perm in b]

        if len(args.paths) > 1:
            shell.stdout.write("%s:" % (relpath, ))
        if shell.stdout or args.long:
            shell.stdout.write('\n'.join(a))
        else:
            if a:
                maxlen = max(max([len(x) for x in a]), 1)
                # arbitrary line length
                columns_max = 80
                columns = (columns_max / maxlen) - 1
                b = []
                pos = 0
                line = "\n"
                to_add = ""
                for i, x in enumerate(a):
                    if not ((i + 1) % columns):
                        newline = "\n"
                        spacing = ""
                    else:
                        newline = ""
                        spacing = " " * (maxlen - len(x) + 1)
                    to_add = "%s%s%s" % (x, spacing, newline)
                    if pos < columns_max:
                        pos += len(to_add)
                        line += to_add
                    else:
                        b.append(line)
                        pos = 0
                        line = ""
                shell.stdout.write("%s\n" % '\n'.join(b))
        if len(args.paths) > 1:
            shell.stdout.write("")
    except OSError:
        shell.stderr.write('ls: cannot access %s: no such file or directory\n' % (relpath, ))

def help():
    return parser.help_msg()
