import kernel.filesystem as fs

def run(shell, args):
    path = shell.path
    expression = '*'
    if len(args) >= 2:
        expression = args[1]
    if len(args) >= 1:
        path = args[0]
    a = find(path, expression)
    shell.stdout.write('\n'.join(a))

def find(path, expression):
    listing = []

    for x in fs.list_glob(fs.join_path(path, expression)):
        new = fs.join_path(path, x)
        if fs.is_directory(x):
            listing.extend(find(new, expression))
        else:
            #remove this filter later
            if ".git" not in x and x[-4:] != ".pyc":
                listing.append(new)
    return listing

def help():
    a = """
    Find

    Finds files matching the expression given.

    usage: find [path] [expression]
    """
    return a
