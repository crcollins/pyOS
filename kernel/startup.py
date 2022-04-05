import kernel.filesystem
import kernel.metadata
import kernel.userdata

def run():
    print("STARTING")
    kernel.userdata.build_user_data_database()
    kernel.metadata.build_meta_data_database(kernel.filesystem.list_all('/'))

