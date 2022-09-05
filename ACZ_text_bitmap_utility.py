## ACE COMBAT ZERO text_bitmap_utility by Andrei Segal (Andreisgl @ GitHub, SegalAndrei @ Twitter)
## =========================================================================
## Manipulates letter bitmaps for assembly of character sets

from email.mime import base
import os
from os import listdir
from os.path import isfile, join

import sys

import pathlib
import shutil
import textwrap

import subprocess

basedir = os.getcwd()
current_folder = "0007_out"
bmp_out_folder = basedir + "/" + "bmp_lib"
bmp_out_speaker = "speaker"
bmp_out_radio = "radio"

bmp_out_speaker = bmp_out_folder + "/" + bmp_out_speaker
bmp_out_radio = bmp_out_folder + "/" + bmp_out_radio
bmp_out_folder = [bmp_out_folder, bmp_out_speaker, bmp_out_radio]



def file_chooser(output_folder):
    # Chooses which files to get: Speaker or Radio.
    # If invalid choice, defaults to speaker.
    global character_set_file
    global character_set_length_file
    global bmp_file
    if output_folder == 2:
        character_set_file = current_folder + "/" + "0012_radio_cs.spl"
        character_set_length_file = current_folder + "/" + "0010_radio_csl.spl"
        bmp_file = current_folder + "/" + "0017_interstitial2_interstitial2.spl"
    else:
        output_folder = 1
        character_set_file = current_folder + "/" + "0003_speaker_cs.spl"
        character_set_length_file = current_folder + "/" + "0001_speaker_csl.spl"
        bmp_file = current_folder + "/" + "0008_interstitial1_interstitial1.spl"
    splice_bitmap(character_set_file, character_set_length_file, bmp_file, output_folder)
# Gets a character set file and it's corresponding bitmap section file.
# Splices bitmaps for each letter, organizes them into folder in UTF-16 order
# output_folder: 
    # 0 for base folder
    # 1 for Speaker
    # 2 for Radio
def splice_bitmap(cs, csl, bitmap_data_file, output_folder):
    character_set = []

    header = 64
    letter_heigth = 32
    letter_length = 16
    letter_size = letter_heigth * letter_length
    character_set_length = 0
    number_of_letters = 0
    
    file_contents = []

    # Get character set
    with open(csl, "rb") as of:
            character_set_length = int.from_bytes(of.read(2), "little")
    with open(cs, "rb") as of:
        ## Get the ASCII characters and append them to a list then skip the rest
        of.seek(0)
        for i in range(character_set_length):
            null = of.read(8)
            char = of.read(2) ## Run a small check and replacement rountine for non printable characters found in the set
            character_set.append(char)
            null = of.read(6)
    
    # Manipulate bitmap file
    with open(bitmap_data_file, "rb") as bmp:
        file_size = bmp.seek(0, 2)
        bmp.seek(0)

        bmp.seek(header) # Skip header
        number_of_letters_bmp = int((file_size - 64) / letter_size)
        for c in range(number_of_letters_bmp):
            file_contents.append(bmp.read(letter_size))
        print()

    # Export single letter bmp files
    global bmp_out_folder
    bmp_out_folder = bmp_out_folder[output_folder]
    if not os.path.exists(bmp_out_folder):
        os.mkdir(bmp_out_folder)
    for i in range(number_of_letters_bmp):
        file_name = bmp_out_folder + "/"
        file_name += (str(int.from_bytes(character_set[i], "little")) + "_").zfill(6)
        file_name += hex(int.from_bytes(character_set[i], "little"))
        file_name += ".bmp"
        with open(file_name, "wb") as of:
            of.write(file_contents[i])

    print()


file_chooser(1)