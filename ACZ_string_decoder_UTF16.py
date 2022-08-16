## ACE COMBAT ZERO string decoder by death_the_d0g (death_the_d0g @ Twitter)
## =========================================================================
## Decodes and prints string data found in mission files found in ACZ
## TODO: doesnt work with MERLON K

import os

def padding_skip(current_position):
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
    return string_data_file.seek(string_data_file.tell(), 0)

def string_decoder():
    ## Initialize arrays
    str_character_set = [] ## store decoded characters
    str_string_length = [] ## store length of string
    str_string_offset = [] ## store offset of string in the string data
    str_string_data = [] ## store the string data
    str_decoded_string = [] ## store single decoded string
    str_decoded_string_list = [] ## store all decoded strings
    ## Get amount of lines in the data
    amount_of_lines = int.from_bytes(string_data_file.read(4), "little")
    ## Get the amount of characters that the string data has
    character_set_length = int.from_bytes(string_data_file.read(2), "little")
    ## Set a value limiter so we can replace the line breaks that exist in the string data with blank spaces
    character_set_item_list_limit = character_set_length
    ## Skip the rest of the header and go straitgh to where the character set data is located
    null = string_data_file.read(10)
    ##string_data_file.seek(16, 0)
    ## Get the ASCII characters and append them to a list then skip the rest
    for i in range(character_set_length):
        null = string_data_file.read(8)
        is_this_character_printable = (string_data_file.read(2)).decode("utf-16", errors = "ignore") ## Run a small check and replacement rountine for non printable characters found in the set
        if (is_this_character_printable.isprintable()):
            str_character_set.append(is_this_character_printable)
        else:
            str_character_set.append(" ")
        null = string_data_file.read(6)
    ## Get the length of individual strings
    for i in range(amount_of_lines):
        str_string_length.append(int.from_bytes(string_data_file.read(2), "little"))
    ## Skip padding but subtract 4 from the returned position since the last skipped 4 bytes is an offset value
    padding_skip(string_data_file.tell())
    string_data_file.seek(-4, 1)
    ## Get the string position on the string data
    for i in range(amount_of_lines):
        str_string_offset.append(int.from_bytes(string_data_file.read(4), "little"))
    ## And finally, get the string data.
    ## The amount of characters in the string data is obtained by adding all string lenghts that are stored in the "str_string_length" list.
    for i in range(sum(str_string_length)):
        str_string_data.append(int.from_bytes(string_data_file.read(2), "little"))
    ## Process retrieved data and form the string
    for i in range(amount_of_lines):
        string_offset = str_string_offset[i] ## get start position of the currenttly processed string within the "str_string_data" list
        string_length = str_string_length[i] ## get the length of the currenttly processed string within the "str_string_length" list
        for sub_i in range(string_length): ## loop for n amount of characters in the currenttly processed string
            character = str_string_data[string_offset + sub_i] ## get the string s character ID value by retrieveing its position from the "str_string_data" list. As soon the "sub_i" loop itinerates move the offset reading by 1 and repeat by the amount of letters in the curent string.
            if character > character_set_item_list_limit : ## check if the character ID value goes above the "character_set_item_list_limit". If true the replace it a blank space, else append the character.
                str_decoded_string.append(" ")
            else:
                str_decoded_string.append(str_character_set[character])
        str_decoded_string_list.append(str("".join(str_decoded_string))) ## Join the read characters and form the string then add it to the list.
        str_decoded_string.clear() ## clear this list to make up for the next string
    return [str_decoded_string_list, character_set_length]


## //Open needed files

string_parameter_file = open("0006.unk", "rb")
string_data_file = open("0007.unk", "rb")

## //Retrieve parameters from "string_parameter_file"

## Jump to where the amount of string parameters is located in the file then read and store it

string_parameter_file.seek(1792, 0)
amount_of_string_parameters = int.from_bytes(string_parameter_file.read(2), "little")

## Jump to where the string parameters starts

string_parameter_file.seek(1824, 0)

## Initialize array for storing values

speaker_id_list = []
string_id_list = []

## Retrieve needed/relevant data

for i in range(amount_of_string_parameters):
    ## Note: "string_null" variables are buffer areas that the game writes when reading the entire string data, so they are ignored.
    ## TODO: figure what the unknown values do
    string_parameter_unknown_flag1 = int.from_bytes(string_parameter_file.read(1), "little")
    string_parameter_unknown_flag2 = int.from_bytes(string_parameter_file.read(1), "little")
    string_parameter_play_voiceclip_as_background_chatter = int.from_bytes(string_parameter_file.read(1), "little")
    string_parameter_unknown_flag3 = int.from_bytes(string_parameter_file.read(1), "little")
    length_check = int.from_bytes(string_parameter_file.read(4), "little") ## count as a NULL variable if the value is 0
    if length_check != 0:
        string_parameter_unknown_flag4 = int.from_bytes(string_parameter_file.read(4), "little")
        string_parameter_unknown_flag5 = int.from_bytes(string_parameter_file.read(4), "little")
        string_parameter_unknown_flag6 = int.from_bytes(string_parameter_file.read(4), "little")
        string_null = int.from_bytes(string_parameter_file.read(4), "little")
        string_null = int.from_bytes(string_parameter_file.read(4), "little")
    else:
        string_null = int.from_bytes(string_parameter_file.read(4), "little")
    string_parameter_rgba_value = int.from_bytes(string_parameter_file.read(4), "little")
    string_parameter_play_associated_voiceclip_id_value = int.from_bytes(string_parameter_file.read(2), "little")
    string_parameter_play_next_voiceclip_id_value = int.from_bytes(string_parameter_file.read(2), "little")
    string_parameter_speaker_id_value = int.from_bytes(string_parameter_file.read(2), "little")
    string_parameter_string_id_value = int.from_bytes(string_parameter_file.read(2), "little")
    string_parameter_play_sfx_with_voiceline_id_value = int.from_bytes(string_parameter_file.read(2), "little")
    string_parameter_voiceline_playback_start_delay_value = int.from_bytes(string_parameter_file.read(2), "little")
    string_parameter_voiceline_playback_end_delay_value = int.from_bytes(string_parameter_file.read(2), "little")
    string_parameter_voiceline_playback_unknown_delay_value = int.from_bytes(string_parameter_file.read(2), "little")
    string_null = int.from_bytes(string_parameter_file.read(4), "little")
    string_parameter_unknown = int.from_bytes(string_parameter_file.read(4), "little")
    string_parameter_unknown = int.from_bytes(string_parameter_file.read(4), "little")
    string_parameter_unknown = int.from_bytes(string_parameter_file.read(4), "little")
    speaker_id_list.append(string_parameter_speaker_id_value)
    string_id_list.append(string_parameter_string_id_value)


## Get the string data and decode it into readable lines then return them in a list
## SPEAKER_ID

string_decoder_retuned_data = string_decoder()
decoded_speaker_id_string_list = string_decoder_retuned_data[0]

## Skip the remaning padding by checking the current offset in the file ends with 0

current_position = string_data_file.tell()
while True:
    zero_check = format(current_position, "x")
    if zero_check[-1] != "0":
        current_position += 2
    else:
        string_data_file.seek(current_position, 0)
        break

## Skip the bitmap sheet and palette data for SPEAKER_ID strings and jump to where the mission-relevant string data is located
    
string_data_file.seek((string_decoder_retuned_data[1] * 512) + 64 + current_position, 0)

## Get the string data and decode it into readable lines then return them in a list
## STRING_DATA

string_decoder_retuned_data = string_decoder()
decoded_string_list = string_decoder_retuned_data[0]

## With all strings decoded, merge the mission-relevant string and its speaker then write them to a text file

output_file = open("acz_output_mission_strings.txt", "w", encoding="utf-16")

for i in range(amount_of_string_parameters):
    full_string = str(string_id_list[i]) + " - " + decoded_speaker_id_string_list[speaker_id_list[i]] + ": " + decoded_string_list[string_id_list[i]]
    output_file.write(full_string + "\n")

output_file.close()
exit()
