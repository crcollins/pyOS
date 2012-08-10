from kernel.utils import Parser

desc = "Copies the given file/directory to the given location."
parser = Parser('cp', name="Copy", description=desc)
pa = parser.add_argument
pa('paths', type=str, nargs='*',)
pa('-f', action="store_true", dest="force", default=False)
pa('-r', action="store_true", dest="recursive", default=False)
pa('-v', action="store_true", dest="verbose", default=False)

def run(shell, args):
    parser.add_shell(shell)
    args = parser.parse_args(args)
    if not parser.help:
        if len(args.paths) >= 2:
            dest = shell.sabs_path(args.paths[-1])
            if shell.syscall.is_dir(dest) or len(args.paths) == 2 \
                    or not shell.syscall.exists(dest):
                for src in args.paths[:-1]:
                    copy(shell, args, src, dest)
            else:
                shell.stderr.write("%s is not a directory" % dest)
        else:
            shell.stderr.write("missing file operand")

def copy(shell, args, src, dest):
    src = shell.sabs_path(src)

    if args.recursive and shell.syscall.is_dir(src):
        srcpaths = shell.syscall.list_all(src)
    else:
        srcpaths = [src]

    if shell.syscall.is_dir(dest):
        join = [dest, shell.syscall.base_name(src)]
        destbase = shell.syscall.join_path(*join)
    else:
        destbase = dest

    for path in srcpaths:
        relpath = shell.srel_path(path, src)
        if relpath != '.':
            destpath = shell.syscall.join_path(destbase, relpath)
        else:
            destpath = destbase

        if args.verbose:
            shell.stdout.write("Copying %s to %s" % (path, destpath))

        try:
            if shell.syscall.is_dir(path):
                if args.recursive:
                    copy_dir(shell, path, destpath)
                else:
                    shell.stdout.write("omitting directory: %s" % path)
            else:
                shell.syscall.copy(path, destpath)
        except OSError:
            shell.stderr.write("file error " + destpath)

def copy_dir(shell, src, dest):
    shell.syscall.make_dir(dest)
    # TODO # add copy metedata to syscalls?
    meta = shell.syscall.get_meta_data(src)
    shell.syscall.set_owner(dest, meta[1])
    shell.syscall.set_permission(dest, meta[2])
    shell.syscall.set_time(dest, meta[3:6])

def help():
    return parser.help_msg()
