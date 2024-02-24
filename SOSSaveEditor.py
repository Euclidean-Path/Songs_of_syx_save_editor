import zlib
from Config import select_options_here
from FileHandler import get_save, insert_save

def patch_game():
    matches = { # int8 representation of binary for the string
        "civic_maintenance": [67, 0, 73, 0, 86, 0, 73, 0, 67, 0, 95,
                              0, 77, 0, 65, 0, 73, 0, 78, 0, 84, 0,
                              69, 0, 78, 0, 65, 0, 78, 0, 67, 0, 69],

        "civic_spoilage": [67, 0, 73, 0, 86, 0, 73, 0, 67, 0, 95, 0,
                           83, 0, 80, 0, 79, 0, 73, 0, 76, 0, 65, 0,
                           71, 0, 69],

        "civic_raiding": [67, 0, 73, 0, 86, 0, 73, 0, 67, 0, 95, 0, 82,
                          0, 65, 0, 73, 0, 68, 0, 73, 0, 78, 0, 71]}


    selected_matches = {}
    processed_bytes = []
    patch_locations = []

    # Get the selected options from config and add it to a dict if selected
    for option in select_options_here:
        if select_options_here[option] > 0:
            selected_matches[option] = matches[option]

    selected_matches_keys_list = list(selected_matches.keys())
    # Check the len of patch locations (0 here) and then get the corresponding key for that patch,
    # using the key to get the patch values which will then be searched for.
    match = selected_matches[selected_matches_keys_list[len(patch_locations)]]
    # Get and create a working copy of the latest save
    latest_save_copy = get_save()

    with open(latest_save_copy, "rb") as file:
        zipped_buffer = file.read()
        # Expand the game content
        inflated_buffer = zlib.decompress(zipped_buffer)

    for i, byte in enumerate(inflated_buffer):
        processed_bytes.append(byte)
        # if it is over the length of the match we are searching for
        if len(processed_bytes) > len(match):
            # If the search slice matches the patch we are looking for
            if processed_bytes[-len(match):] == match:
                # Add to patch locations to be modified later
                patch_locations.append(i + 1)
                # If all patches are found
                if len(patch_locations) == len(selected_matches): break
                # As the patch locations will contain 1+ items it will search for the next patch
                match = selected_matches[selected_matches_keys_list[len(patch_locations)]]

    # Makes data mutable
    inflated_buffer = bytearray(inflated_buffer)
    for patch in patch_locations:
        # insert each patch
        inflated_buffer[patch] = 64

    zipped_buffer = zlib.compress(inflated_buffer)

    # Create a patched save game name and export to the save location
    insert_save(zipped_buffer)

    print(f"Inserted: {len(patch_locations)} patches")

if __name__ == "__main__":
    patch_game()