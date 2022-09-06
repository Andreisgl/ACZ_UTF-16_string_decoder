## ACE COMBAT ZERO line swapper by Andrei Segal (Andreisgl @ GitHub, SegalAndrei @ Twitter)
## Based on ACE COMBAT ZERO string decoder by death_the_d0g (deththed0g @ GitHub, death_the_d0g @ Twitter)
## =========================================================================
## Allows for changing of mission radio lines and names. Intended for translation.
## (Warranty void if used for memes)


from cgitb import text
import os
import re
import shutil
from sqlite3 import ProgrammingError
from sys import byteorder

basedir = os.getcwd()
folders_list = []
current_folder = ""

file_list = []
short_file_list = [] # Filenames without number prefix and extension
path_file_list = [] # Filenames with path in folder

sil = [] # Short fo "section_index_list" Index of each section in the previous lists

bmp_out_folder = "bmp_lib"
bmp_out_speaker = "speaker"
bmp_out_radio = "radio"

# List of file names needed for the job
speaker_nol = "speaker_nol"
speaker_csl = "speaker_csl"
speaker_unknown = "speaker_unknown"
speaker_cs = "speaker_cs"
speaker_sls = "speaker_sls"
speaker_padd1 = "speaker_padd1"
speaker_so = "speaker_so"
speaker_sd = "speaker_sd"
interstitial1_interstitial1 = "interstitial1_interstitial1"
#
radio_nol = "radio_nol"
radio_csl = "radio_csl"
radio_unknown = "radio_unknown"
radio_cs = "radio_cs"
radio_sls = "radio_sls"
radio_padd1 = "radio_padd1"
radio_so = "radio_so"
radio_sd = "radio_sd"
interstitial2_interstitial2 = "interstitial2_interstitial2"

# Prompts user to choose folder from folders_list.
# Returns index of folder to be worked on.
def choose_working_folder():
    global basedir
    global folders_list
    global bmp_out_folder
    global bmp_out_speaker
    global bmp_out_radio
    folder_blacklist = [".git", "storage", bmp_out_folder] # Remove these folders from folder list
                                # AKA ".git" is annoying
    bmp_out_folder = basedir + "/" + bmp_out_folder
    bmp_out_speaker = bmp_out_folder + "/" + bmp_out_speaker
    bmp_out_radio = bmp_out_folder + "/" + bmp_out_radio

    # Facilitate folder calling
    bmp_out_folder = [bmp_out_folder, bmp_out_speaker, bmp_out_radio]
    folders_list = os.listdir()
    try:
        for i in range(len(folders_list)):
            while ((not os.path.isdir(basedir + "/" + folders_list[i]))
                    or (folders_list[i] in folder_blacklist)):
                folders_list.pop(i)
    except IndexError:
        pass
    
    # Gets input from user
    choice = 0
    if len(folders_list) > 1:
        print("Choose folder to work on!: ")
        for i in range(len(folders_list)):
            print(str(i) + " - " + folders_list[i])
        choice = input("Choice: ")
        if choice in range(len(folders_list)):
            print(choice)
        else:
            err_msg = "No such folder!"
            input(err_msg + "\n Press ENTER to continue...")
            exit(err_msg)
    elif len(folders_list) == 1:
        choice = 0
    elif len(folders_list) == 0:
        err_msg = "No folders in current directory!"
        input(err_msg + "\n Press ENTER to continue...")
        exit(err_msg)
    print("Loading: " + folders_list[choice])
    return(choice)
    print()

def check_files_in_folder():
    global file_list
    file_list = os.listdir(current_folder)
    try:
        for i in range(len(file_list)):
            while (os.path.isdir(basedir + "/" + file_list[i])):
                file_list.pop(i)
    except IndexError:
        pass

    for i in range(len(file_list)):
        short_file_list.append(file_list[i][5:-4])
    for i in range(len(file_list)):
        path_file_list.append(current_folder + "/" + file_list[i])
    
    sil.append( short_file_list.index(speaker_nol))
    sil.append( short_file_list.index(speaker_csl))
    sil.append( short_file_list.index(speaker_unknown))
    sil.append( short_file_list.index(speaker_cs))
    sil.append( short_file_list.index(speaker_sls))
    sil.append( short_file_list.index(speaker_padd1))
    sil.append( short_file_list.index(speaker_so))
    sil.append( short_file_list.index(speaker_sd))
    sil.append( short_file_list.index(interstitial1_interstitial1))
    #
    sil.append( short_file_list.index(radio_nol))
    sil.append( short_file_list.index(radio_csl))
    sil.append( short_file_list.index(radio_unknown))
    sil.append( short_file_list.index(radio_cs))
    sil.append( short_file_list.index(radio_sls))
    sil.append( short_file_list.index(radio_padd1))
    sil.append( short_file_list.index(radio_so))
    sil.append( short_file_list.index(radio_sd))
    sil.append( short_file_list.index(interstitial2_interstitial2))
    print()
    
def padding_skip(current_position, string_data_file):
    ## Set zero padding skipping function:
    ## What this will do is to go where the position before the fuction was called then 
    ## read two bytes and convert them to a integer. If the integer is equal to zero
    ## then continue reading moving through the file two places at time and skipping any padding there might be.
    ## When the condition is not longer met move two places back to make up for the read bytes,
    ## break the WHILE loop then update the current position in the file to where the padding area ends.
    string_data_file.seek(current_position, 0)
    while True:
        zero_check = int.from_bytes(string_data_file.read(2), "little")
        if zero_check != 0:
            string_data_file.seek(-2, 1)
            break
        else:
            pass
    skip_to = string_data_file.seek(string_data_file.tell(), 0)
    return skip_to

# Splits lines from raw data
def split_lines(number_of_lines, string_lengths, string_data):
    # Split "string_data" based on "string_lengths"
    encoded_lines = [] 
    progress = 0
    for i in range(number_of_lines):
        data = []
        for j in range(string_lengths[i]):
            data.append(string_data[j + progress])
        progress += j + 1
        encoded_lines.append(data)
    return encoded_lines

# Decodes lines previously split into lists by "split_lines"
def line_decoder(encoded_lines, character_set):
    # Decode encoded lines based on character set
    decoded_lines = []
    for i in range(len(encoded_lines)):
        current_line = []
        for j in range(len(encoded_lines[i])):
            try:
                current_line.append(character_set[encoded_lines[i][j]])
            except IndexError:
                if encoded_lines[i][j] == 65535: # Space
                    current_line.append(" ")
                else:
                    input("Unknown character! \n Press enter to continue")
        decoded_lines.append(current_line)
    return decoded_lines

# Gets list of lines, returns a new character set and encodes the list
def line_re_encoder(recovered_lines):
    # Create character set
    new_character_set = []
    for i in range(len(recovered_lines)):
        for j in range(len(recovered_lines[i])):
            new_character_set.append(recovered_lines[i][j])
            new_character_set = [*set(new_character_set)]
            new_character_set.sort()
    
    # Encode list
    encoded_list = []
    for i in range(len(recovered_lines)):
        current_line = []
        for j in range(len(recovered_lines[i])):
            current_line.append(new_character_set.index(recovered_lines[i][j]))
        encoded_list.append(current_line)


    return encoded_list, new_character_set

# Returns lines into a single simple list, string offsets and string lengths
def line_cs_re_uniter(line_list):
    raw_lines = []
    string_offsets = []
    string_lenghts = []
    for i in range(len(line_list)):
        for j in range(len(line_list[i])):
            raw_lines.append(line_list[i][j])
        string_lenghts.append(j + 1)
    
    string_offsets.append(0)
    current_offset = 0
    for i in range(len(string_lenghts)):
        current_offset += string_lenghts[i]
        string_offsets.append(current_offset)
    return raw_lines, string_offsets, string_lenghts

def line_fill(curr_offset, line_size):
    if curr_offset % line_size != 0:
        return ((int(curr_offset/16) + 1) * 16) - curr_offset
    else:
        return 0

# Receives each relevant section as parameter.
# First parameter = mode:
#   0 = Read
#   1 = Write
# Second parameter: datamode. Choose between manipulating Speaker data or Radio data
#   0 = Speaker
#   1 = Radio
def manipulate_text(mode, datamode, nol, csl, unk, cs, sls, padd1, so, sd, intrs):
    nol = current_folder + "/" + file_list[nol]
    csl = current_folder + "/" + file_list[csl]
    unk = current_folder + "/" + file_list[unk]
    cs = current_folder + "/" + file_list[cs]
    sls = current_folder + "/" + file_list[sls]
    padd1 = current_folder + "/" + file_list[padd1]
    so = current_folder + "/" + file_list[so]
    sd = current_folder + "/" + file_list[sd]
    intrs = current_folder + "/" + file_list[intrs]

    number_of_lines = 0
    character_set_length = 0
    character_set = []
    string_lengths = []
    string_offset = []
    string_data = []
    bmp_data = ""

    test_file = ["line_speaker_export.txt", "line_radio_export.txt"]
    test_file = test_file[datamode]
    if mode == 0: # Read mode
        with open(nol, "rb") as of:
            number_of_lines = int.from_bytes(of.read(4), "little")
        with open(csl, "rb") as of:
            character_set_length = int.from_bytes(of.read(2), "little")
        with open(cs, "rb") as of:
            ## Get the ASCII characters and append them to a list then skip the rest
            for i in range(character_set_length):
                null = of.read(8)
                is_this_character_printable = (of.read(2)).decode("utf-16", errors = "ignore") ## Run a small check and replacement rountine for non printable characters found in the set
                if (is_this_character_printable.isprintable()):
                    character_set.append(is_this_character_printable)
                else:
                    character_set.append(" ")
                null = of.read(6)
        with open(sls, "rb") as of:
            ## Get the length of individual strings
            for i in range(number_of_lines):
                string_lengths.append(int.from_bytes(of.read(2), "little"))
        with open(so, "rb") as of:
            ## Skip padding but subtract 4 from the returned position since the last skipped 4 bytes is an offset value
            padding_skip(of.tell(), of)
            of.seek(-4, 1)
            ## Get the string position on the string data
            for i in range(number_of_lines):
                string_offset.append(int.from_bytes(of.read(4), "little"))
        with open(sd, "rb") as of:
            ## And finally, get the string data.
            ## The amount of characters in the string data is obtained by adding all string lenghts that are stored in the "str_string_length" list.
            for i in range(sum(string_lengths)):
                string_data.append(int.from_bytes(of.read(2), "little"))
                
        # Separate string data into lists
        encoded_lines = split_lines(number_of_lines, string_lengths, string_data)
        # Decode lists from to readable text
        decoded_lines = line_decoder(encoded_lines, character_set)

        
        
        # Export lines to .txt
        with open(test_file, "w") as tf:
            for i in range(len(decoded_lines)):
                line_data = ""
                for j in range(len(decoded_lines[i])):
                    line_data += decoded_lines[i][j]        
                tf.write(line_data)
                if i < len(decoded_lines) - 1:
                    tf.write("\n")
    else: # Write mode

        # Recover lines from .txt
        recovered_lines = []
        with open(test_file, "r") as tf:
            data = tf.read()
            recovered_lines = data.split("\n")
        
        # Re-encode line lists based on character set
        re_encoded_lines, new_character_set = line_re_encoder(recovered_lines)
        # Re-unite encoded lists into raw string data
        re_united_lines, new_string_offsets, new_string_lengths = line_cs_re_uniter(re_encoded_lines)
        
        # Set new values for file sections:
        current_nol = len(recovered_lines) # Check if number of lines changed.
        #if number_of_lines != current_nol:
        #    print("HEY! The number of lines changed! Check file again!\n")
        #    print("The number of lines should be: " + str(number_of_lines))
        #    print("\nThe current number of is: " + str(current_nol))
        #    input("\nI'll let that pass because I'm lazy. Press ENTER to continue")

        character_set_length = len(new_character_set) + 1
        character_set = new_character_set
        string_lengths = new_string_lengths
        string_offset = new_string_offsets
        string_data = re_united_lines

        # Rewrite new data into their files.
        with open(csl, "wb") as of:
            of.write(int.to_bytes(character_set_length-1, 2, byteorder="little"))
        with open(cs, "wb") as of:
            ## Get the ASCII characters and append them to a list then skip the rest
            for i in range(character_set_length - 1):
                padding1 = b'\x0A\00\x18\00\00\00\00\00'
                padding2 = b'\x00\x00\xCD\xCD\xCD\xCD'
                
                of.write(padding1)
                of.write(character_set[i].encode("utf-8", "little"))
                of.write(b'\00')
                of.write(padding2)
        with open(sls, "wb") as of:
            for i in range(current_nol):
                of.write(string_lengths[i].to_bytes(2, "little"))
        with open(so, "wb") as of:
            for i in range(current_nol):
                of.write(string_offset[i].to_bytes(4, "little"))
        with open(sd, "wb") as of:
            buffer = b''
            for i in range(len(string_data)):
                buffer += string_data[i].to_bytes(2, "little")
                paddsize = line_fill(len(buffer), 16) # Measure needed padding at end of file
            for j in range(paddsize):
                buffer += b'\00'
            of.write(buffer)
        
        with open(intrs, "rb") as of: # Recover header
            bmp_header = of.read(64)
        with open(intrs, "wb") as of:
            of.write(bmp_header) # Write header
            for i in range(len(character_set)):
                path = bmp_out_folder[datamode + 1] + "/"
                path += str(int.from_bytes(character_set[i].encode("utf-8", "little"), "little")).zfill(5)
                path += "_"
                path += str(hex(int.from_bytes(character_set[i].encode("utf-8", "little"), "little")))
                path += ".bmp"

                with open(path, "rb") as bmpf:
                    of.write(bmpf.read())

def repack_files():
    finished_file = basedir + "/" + "end.unk"

    with open(finished_file, "wb") as of:
        for path in path_file_list:
            with open(path, "rb") as section:
                data = section.read()
                of.write(data)

def open_file(mode, datamode):
    if datamode == 0:
        manipulate_text(mode, datamode, sil[0], sil[1], sil[2], sil[3], sil[4], sil[5], sil[6], sil[7], sil[8])
    elif datamode == 1:
        manipulate_text(mode, datamode, sil[9], sil[10], sil[11], sil[12], sil[13], sil[14], sil[15], sil[16], sil[17])

current_folder = choose_working_folder()
current_folder = "./" + folders_list[current_folder]
check_files_in_folder()

open_file(1, 0)


# Repack whole file
repack_files()





print("end")