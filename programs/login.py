import hashlib
import getpass

def run(shell, args):
    user = raw_input("user: ")
    passwd = hashlib.sha256(getpass.getpass("password: ")).hexdigest()
    shell.stdout.write(user)
    shell.stdout.write(passwd)

def help():
    a = """
    """
    return a