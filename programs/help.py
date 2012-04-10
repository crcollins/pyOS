import kernel.filesystem

def run(shell, args):
    if len(args) >= 1:
        name = args[0]
        if name[0:2] == "./":
            a = [shell.iabs_path(name)]
        else:
            paths = shell.get_var('PATH').split(':')
            a = [kernel.filesystem.join_path(x, name) for x in paths]
        program = False
        for x in a:
            program = kernel.filesystem.open_program(x)
            if program:
                shell.stdout.put(program.help())
                break
        else:
            shell.stderr.put("%s: command not found" %name)
    else:
        shell.stdout.put(help())

def help():
    return "HELP"