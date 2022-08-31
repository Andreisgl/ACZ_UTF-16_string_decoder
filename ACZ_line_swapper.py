## ACE COMBAT ZERO line swapper by Andrei Segal (Andreisgl @ GitHub, SegalAndrei @ Twitter)
## Based on ACE COMBAT ZERO string decoder by death_the_d0g (deththed0g @ GitHub, death_the_d0g @ Twitter)
## =========================================================================
## Allows for changing of mission radio lines and names. Intended for translation.
## (Warranty void if used for memes)

import os
import shutil
from sys import byteorder

basedir = os.getcwd()
lines_file = "0007.unk"


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

def file_divider():
    
    with open(lines_file, 'rb') as lf:
        # Divide file into important data and sections
        
        spkr_nol = lf.read(4) # nol = "number of lines"
        spkr_csl = lf.read(2) # csl = "character set lenght"
        spkr_unk1 = lf.read(10) # Unknown part
        
        spker_cs = lf.read(16 * int.from_bytes(spkr_csl, "little")) # Read whole cs section

        spker_sls = lf.read(int.from_bytes(spkr_nol, "little") * 2)# sls = "string lengths"

        aux = lf.tell() # Save position from before padding
        aux2 = padding_skip(lf.tell(), lf) -4 # Save end of padding position
        lf.seek(452) # Go back to before padding

        spker_padding1 = lf.read(aux2 - aux) # Read padding

        spkr_so = lf.read(int.from_bytes(spkr_nol, "little") * 4) # so = "sring offset"

        spker_sd_size = 0
        for i in range(0, int(len(spker_sls)), 2): # Iterate bytes to sum them, 2 by 2
            b = spker_sls[i].to_bytes(1, "little") + spker_sls[i+1].to_bytes(1, "little")
            spker_sd_size += int.from_bytes(b, byteorder = "little")  

        spkr_sd = lf.read(spker_sd_size *2) # sd = "string data"
        
        padding_length = line_fill(lf.tell(), 16) # How many bytes to add as end-of-line padding
        spkr_sd += lf.read(padding_length)
        print()

check_files()
file_divider()


##################



print("end")