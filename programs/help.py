import kernel.filesystem

def run(shell, args):
    if len(args) >= 1:
        x = kernel.filesystem.open_program(args[0])
        if x:
            shell.stdout.put(x.help())
        else:
            shell.stderr.put("%s: command not found" %name)
    else:
        shell.stdout.put(help())

def help(shell):
    return "HELP"