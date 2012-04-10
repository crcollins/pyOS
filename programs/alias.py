def run(shell, args):
    if not args:
        for x in shell.aliases:
            print x, shell.aliases[x]
    else:
        for item in args:
            if "=" in item:
                x = item.index("=")
                key = item[:x]
                value = item[x+1:]
                shell.aliases[key] = value
            else:
                print "error", item
