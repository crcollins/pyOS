import kernel.filesystem as fs
import pprint

def run(shell, args):
    if args:
        path = args[0]
    else:
        path = shell.curpath
    tree = tree_gen(path)
    shell.stdout.write(tree_print(tree))

def sorter(x):
    return ("f" if fs.is_file(x) else "d") + x.lower()


def tree_gen(path):
    l = [path]
    if fs.is_directory(path):
        listing = sorted([fs.join_path(path,x) for x in fs.list_dir(path)], key=sorter)
        for x in listing:
                if ".git" not in x and x[-4:] != ".pyc":
                    l.append(tree_gen(fs.join_path(path,x)))
    return l

def tree_print(tree, level=0, extra="", idx=None):
        string = ''
        for i, x in enumerate(tree):
            added =  extra + "   " * (level > 1) + "|" * (level > 0)
            if type(x) is list:
                string += tree_print(x, level + 1, added, len(tree)-1==i)
            else:
                char = "-- " if fs.is_file(x) else "++ "
                if x != "/":
                    x = fs.base_name(x)
                if not idx:
                    string += added + char * (level > 0) + x +  "\n"
                else:
                    string += added[:-1] + "'" + char * (level > 0) + x + "\n"
        return string


def help():
    a = """
    Tree

    Returns the file/direactory tree of the given directory.

    usage: tree [directory]
    """
    return a