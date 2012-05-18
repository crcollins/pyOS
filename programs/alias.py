def run(shell, args):
    #hack to fix encapsulation
    shell = shell.parent
    if not args:
        for x in shell.aliases:
            shell.stdout.write("%s %s" %(x, shell.aliases[x]))
    else:
        for item in args:
            if "=" in item:
                x = item.index("=")
                key = item[:x]
                value = item[x+1:]
                shell.aliases[key] = value
            else:
                shell.stderr.write("")

def help():
    a = """
    Alias

    Aliases a key with a command.

    usage: alias [key=command]
    """
    return a