import kernel.filesystem
import kernel.metadata

def run():
    print "STARTING"
    kernel.metadata.build_meta_data_database(kernel.filesystem.list_all())

