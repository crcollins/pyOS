import kernel.filesystem
import kernel.metadata
import kernel.userdata

def run(shell, args):
    print "STARTING"
    kernel.userdata.build_user_data_database(shell)
    kernel.metadata.build_meta_data_database(shell, shell.syscall.list_all())

