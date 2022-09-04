## ACE COMBAT ZERO line swapper by Andrei Segal (Andreisgl @ GitHub, SegalAndrei @ Twitter)
## Based on ACE COMBAT ZERO string decoder by death_the_d0g (deththed0g @ GitHub, death_the_d0g @ Twitter)
## =========================================================================
## Allows for stripping text files for easier further manipulation
## (Warranty void if used for memes)

from cgitb import text
import os
import shutil
from sys import byteorder

basedir = os.getcwd()
lines_file = "0007.unk"
output_folder = basedir + "/" + "0007_out"

# FILE STRIPPING METHODS
def check_files():
    global lines_file
    lines_file = basedir + "/" + lines_file
    print()

def padding_skip(current_position, l_file):
    ## Set zero padding skipping function:
    ## What this will do is to go where the position before the fuction was called then 
    ## read two bytes and convert them to a integer. If the integer is equal to zero
    ## then continue reading moving through the file two places at time and skipping any padding there might be.
    ## When the condition is not longer met move two places back to make up for the read bytes,
    ## break the WHILE loop then update the current position in the file to where the padding area ends.
    l_file.seek(current_position, 0)
    while True:
        zero_check = int.from_bytes(l_file.read(2), "little")
        if zero_check != 0:
            l_file.seek(-2, 1)
            break
        else:
            pass
    skip_to = l_file.seek(l_file.tell(), 0)
    return skip_to

# Returns number of bytes to fill up the rest of the current line.
def line_fill(curr_offset, line_size):
    if curr_offset % line_size != 0:
        return ((int(curr_offset/16) + 1) * 16) - curr_offset
    else:
        return 0

# Splits the text parts into blocks.
# Receives the beginning position of the block as parameter,
# Returns list 9 positions long.
# Positions 0-7 are the actual data,
# Position 8 is the end offset of list.

# nol = "number of lines"
# csl = "character set lenght"
# Unknown part
# cs = whole "character set"
# sls = "string lengths"
# padding 1
# so = "sring offset"
# sd = "string data"

def text_splitter(initial_position):
    with open(lines_file, 'rb') as lf:
        # Divide file into important data and sections
        
        #SPEAKER ID
        lf.seek(initial_position)
        spkr_nol = lf.read(4) # nol = "number of lines"
        spkr_csl = lf.read(2) # csl = "character set lenght"
        spkr_unk1 = lf.read(10) # Unknown part
        
        spkr_cs = lf.read(16 * int.from_bytes(spkr_csl, "little")) # cs = whole "character set"

        spkr_sls = lf.read(int.from_bytes(spkr_nol, "little") * 2) # sls = "string lengths"

        aux = lf.tell() # Save position from before padding
        aux2 = padding_skip(lf.tell(), lf) -4 # Save end of padding position
        lf.seek(aux) # Go back to before padding

        spkr_padding1 = lf.read(aux2 - aux) # padding 1

        spkr_so = lf.read(int.from_bytes(spkr_nol, "little") * 4) # so = "sring offset"

        spkr_sd_size = 0
        for i in range(0, int(len(spkr_sls)), 2): # Iterate bytes to sum them, 2 by 2
            b = spkr_sls[i].to_bytes(1, "little") + spkr_sls[i+1].to_bytes(1, "little")
            spkr_sd_size += int.from_bytes(b, byteorder = "little")  

        spkr_sd = lf.read(spkr_sd_size *2) # sd = "string data"
        
        padding_length = line_fill(lf.tell(), 16) # How many bytes to add as end-of-line padding
        spkr_sd += lf.read(padding_length)
        end_position = lf.tell()
    return [spkr_nol, spkr_csl, spkr_unk1, spkr_cs, spkr_sls, spkr_padding1, spkr_so, spkr_sd, end_position]

# Splits whole file, returns list with all relevant parts.
# Positions:
    # 0: Speaker data list (removes position 8, end file offset)
    # 1: interstitial1 (Contains bitmap and pallete stuff for Speaker text)
    # 2: Voice data list (removes position 8, end file offset)
    # 3: interstitial 2 (Runs until the end of file.
    #                   Maybe the same as first interstitial)
def file_splitter():
    speaker_data_list = [] # List containing speaker text sections separated, in order.
    interstitial1 = "" # Section between speaker and radio lines
    voice_data_list = [] # List containing radio text sections separated, in order.
    interstitial2 = "" # Section between radio lines and end of file

    speaker_data_list = text_splitter(0)
    # Skip the bitmap sheet and palette data for SPEAKER_ID strings and jump to where the mission-relevant string data is located
    voice_lines_position = (int.from_bytes(speaker_data_list[1], "little") * 512) + 64 + speaker_data_list[8]
    voice_data_list = text_splitter(voice_lines_position)

    # Obtain interstitials:
    with open(lines_file, "rb") as lf:
        # interstitial1:
        begin_pos = speaker_data_list[8]
        lf.seek(begin_pos)
        interstitial1 = lf.read(voice_lines_position - begin_pos)
        # interstitial2:
        begin_pos = voice_data_list[8]
        end_pos = lf.seek(0, 2)
        lf.seek(begin_pos)
        interstitial2 = lf.read(end_pos - begin_pos)
    
    speaker_data_list.pop() # Remove position 7
    voice_data_list.pop() # Remove position 7

    return speaker_data_list, interstitial1, voice_data_list, interstitial2

# Exports a file for every section in a folder
def export_split_file(split_file_list, output_folder):
    # Speaker and Voice lines text names:
        # nol = "number of lines"
        # csl = "character set lenght"
        # Unknown part
        # cs = whole "character set"
        # sls = "string lengths"
        # padding 1
        # so = "sring offset"
        # sd = "string data"
    
    text_filenames = ["nol", "csl", "unknown", "cs", "sls", "padd1", "so", "sd"]
    all_filenames = [text_filenames, "interstitial1", text_filenames, "interstitial2"]
    speaker_tag = "_speaker_"
    radio_tag = "_radio_"
    interstitial1_tag = "_interstitial1_"
    interstitial2_tag = "_interstitial2_"
    file_ext = ".spl"

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder) # Empty folder if it already exists
    os.mkdir(output_folder)

    file_counter = 0
    # Speaker
    for i in range(len(all_filenames[0])):
        file_prefix = output_folder + "/" + str(file_counter).zfill(4) + speaker_tag
        with open(file_prefix + all_filenames[0][i] + file_ext, "wb") as of:
            of.write(split_file[0][i])
        file_counter += 1
    # Interstitial 1
    file_prefix = output_folder + "/" + str(file_counter).zfill(4) + interstitial1_tag
    with open(file_prefix + all_filenames[1]+ file_ext, "wb") as of:
        of.write(split_file[1])
    file_counter += 1

    # Speaker
    for i in range(len(all_filenames[2])):
        file_prefix = output_folder + "/" + str(file_counter).zfill(4) + radio_tag
        with open(file_prefix + all_filenames[0][i] + file_ext, "wb") as of:
            of.write(split_file[2][i])
        file_counter += 1

    # Interstitial 2
    file_prefix = output_folder + "/" + str(file_counter).zfill(4) + interstitial2_tag
    with open(file_prefix + all_filenames[3]+ file_ext, "wb") as of:
        of.write(split_file[3])
    file_counter += 1




    
split_file = [] # Will contain whole file split into sections

check_files()
split_file = file_splitter() #Obtain whole split file

export_split_file(split_file, output_folder)



print("end")