import kernel.filesystem as fs

def run(shell, args):
    if args:
        path = shell.sabs_path(args[0])
    else:
        path = shell.get_path()
    tree = tree_gen(path)
    shell.stdout.write(tree_print(tree))

def sorter(x):
    return ("f" if fs.is_file(x) else "d") + x.lower()

def tree_gen(path):
    pathtree = [path]
    if fs.is_directory(path):
        listing = sorted([fs.join_path(path, x) for x in fs.list_dir(path)],
                 key=sorter)
        for x in listing:
            pathtree.append(tree_gen(fs.join_path(path, x)))
    return pathtree

def tree_print(tree, level=0, extra="", idx=None):
        string = ''
        for i, x in enumerate(tree):
            spacing = "   " if (level > 1) else ''
            bar = "|" if (level > 0) else ''
            added = extra + spacing + bar
            if type(x) is list:
                string += tree_print(x, level + 1, added, len(tree) - 1 == i)
            else:
                char = "-- " if fs.is_file(x) else "++ "
                if x != "/":
                    x = fs.base_name(x)
                end = "%s%s\n" % (char if (level > 0) else '', x)
                if not idx:
                    string += "%s%s" % (added, end)
                else:
                    string += "%s`%s" % (added[:-1], end)
        return string

def help():
    a = """
    Tree

    Returns the file/directory tree of the given directory.

    usage: tree [directory]
    """
    return a
