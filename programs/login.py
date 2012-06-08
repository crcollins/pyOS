import hashlib
import getpass

from kernel.system import System

def run(shell, args):
    user = raw_input("user: ")
    passwd = hashlib.sha256(getpass.getpass("password: ")).hexdigest()

    if passwd: # == db(user).password
        stuff = {
                'USER': user,
                'SHELL': 'interpreter',
                'USERNAME': user,
                'HOME': '/', # db(user).homedir
                }

        path = "/" # db(user).homedir
        newshell = System.new_shell(parent=shell, path=path)
        add_vars(newshell, stuff)
        newshell.run()

def add_vars(shell, stuff):
    for key in stuff:
        shell.set_var(key, stuff[key])


def help():
    a = """
    """
    return a
