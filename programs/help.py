import kernel.filesystem

def run(shell, args):
    if len(args) >= 1:
        x = kernel.filesystem.open_program(args[0])
        if x:
            x.help()
        else:
            print "%s: command not found" %name
    else:
        help()

def help(shell):
    print "HELP"