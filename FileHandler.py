from Config import save_location
import os
from shutil import copyfile

saves = os.listdir(save_location)
latest_save = max([f"{save_location}\\{save}" for save in saves], key=os.path.getctime)

# Get and create a working copy of the latest save
def get_save():
    temp_save_location = f"{os.getcwd()}\\latest_save_copy.save"
    copyfile(latest_save, temp_save_location)
    return temp_save_location

# Create a patched save game name and export to the save location
def insert_save(zipped_buffer):
    save_name_loc = latest_save.index("""songsofsyx\\saves\\saves\\""") + len("""songsofsyx\\saves\\saves\\""")
    patched_save_loc = save_location + """\\patched_""" + latest_save[save_name_loc:]
    with open(patched_save_loc, "wb") as file:
        file.write(zipped_buffer)

    # Clear up temp file
    os.remove(f"{os.getcwd()}\\latest_save_copy.save")


