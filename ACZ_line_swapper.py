## ACE COMBAT ZERO line swapper by Andrei Segal (Andreisgl @ GitHub, SegalAndrei @ Twitter)
## Based on ACE COMBAT ZERO string decoder by death_the_d0g (deththed0g @ GitHub, death_the_d0g @ Twitter)
## =========================================================================
## Allows for changing of mission radio lines and names. Intended for translation.
## (Warranty void if used for memes)


from cgitb import text
import os
import shutil
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
    
    
def manipulate_text(nol, csl, unk, cs, sls, padd1, so, sd):
    
    print()

current_folder = choose_working_folder()
current_folder = "./" + folders_list[current_folder]
check_files_in_folder()

manipulate_text(sil[0], sil[1], sil[2], sil[3], sil[4], sil[5], sil[6], sil[7]) # Test for speaker stuff

print("end")