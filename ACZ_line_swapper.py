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

choose_working_folder()