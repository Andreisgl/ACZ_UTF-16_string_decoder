## ACE COMBAT ZERO line swapper by Andrei Segal (Andreisgl @ GitHub, SegalAndrei @ Twitter)
## Based on ACE COMBAT ZERO string decoder by death_the_d0g (deththed0g @ GitHub, death_the_d0g @ Twitter)
## =========================================================================
## Allows for changing of mission radio lines and names. Intended for translation.
## (Warranty void if used for memes)


from cgitb import text
import os
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
    folder_blacklist = [".git"] # Remove these folders from folder list
                                # AKA ".git" is annoying
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
            print(i + " - " + folders_list[i])
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
            current_line.append(character_set[encoded_lines[i][j]])
        decoded_lines.append(current_line)
    return decoded_lines

def manipulate_text(nol, csl, unk, cs, sls, padd1, so, sd):
    nol = current_folder + "/" + file_list[nol]
    csl = current_folder + "/" + file_list[csl]
    unk = current_folder + "/" + file_list[unk]
    cs = current_folder + "/" + file_list[cs]
    sls = current_folder + "/" + file_list[sls]
    padd1 = current_folder + "/" + file_list[padd1]
    so = current_folder + "/" + file_list[so]
    sd = current_folder + "/" + file_list[sd]

    number_of_lines = 0
    character_set_length = 0
    character_set = []
    string_lengths = []
    string_offset = []
    string_data = []

    with open(nol, "rb") as nol:
        number_of_lines = int.from_bytes(nol.read(4), "little")
    with open(csl, "rb") as csl:
        character_set_length = int.from_bytes(csl.read(2), "little")
    with open(cs, "rb") as cs:
        ## Get the ASCII characters and append them to a list then skip the rest
        for i in range(character_set_length):
            null = cs.read(8)
            is_this_character_printable = (cs.read(2)).decode("utf-16", errors = "ignore") ## Run a small check and replacement rountine for non printable characters found in the set
            if (is_this_character_printable.isprintable()):
                character_set.append(is_this_character_printable)
            else:
                character_set.append(" ")
            null = cs.read(6)
    with open(sls, "rb") as sls:
        ## Get the length of individual strings
        for i in range(number_of_lines):
            string_lengths.append(int.from_bytes(sls.read(2), "little"))
    with open(so, "rb") as so:
        ## Skip padding but subtract 4 from the returned position since the last skipped 4 bytes is an offset value
        padding_skip(so.tell(), so)
        so.seek(-4, 1)
        ## Get the string position on the string data
        for i in range(number_of_lines):
            string_offset.append(int.from_bytes(so.read(4), "little"))
    with open(sd, "rb") as sd:
        ## And finally, get the string data.
        ## The amount of characters in the string data is obtained by adding all string lenghts that are stored in the "str_string_length" list.
        for i in range(sum(string_lengths)):
            string_data.append(int.from_bytes(sd.read(2), "little"))

    # Separate string data into lists
    encoded_lines = split_lines(number_of_lines, string_lengths, string_data)
    # Decode lists from to readable text
    decoded_lines = line_decoder(encoded_lines, character_set)

    # Re-encode line lists based on character set
    re_encoded_lines = []
    # Re-unite encoded lists into raw string data
    re_united_lines = []
    

    print()



current_folder = choose_working_folder()
current_folder = "./" + folders_list[current_folder]
check_files_in_folder()

manipulate_text(sil[0], sil[1], sil[2], sil[3], sil[4], sil[5], sil[6], sil[7]) # Test for speaker stuff

print("end")