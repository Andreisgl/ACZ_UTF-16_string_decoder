# ACZ_UTF-16_string_decoder
My work improving death_the_d0g's ACZ_UTF-16_string_decoder

This set of tools aid the manipulation of radio text data.

## ACZ_mission_text_file_splitter.py:
  Splits the mission's text file into a folder. It is hard-coded to unpack the English text, "0007.unk"
  Output folder is <filename>_out, containing each section of the file separated for easier manipulation.
  Must be the first program to be run.

## ACZ_line_swapper.py:
  Reads/modifies the previous folder text sections. Choose whether to work with the speaker names or radio lines.
  MODES:
    
    0 - Read: Reads the unpacked folder and export contained text (names or lines) to a .txt file
    (either "line_speaker_export.txt" or "line_radio_export.txt"). The files can then be modified.
    
    1 - Write: Reads the previously exported and modified .txt file and rewrites the file sections.
  After each run, independent of the mode, the script will repack the contents of the folder back to a single file,
  "end.unk". It shall be renamed to match the original file ("0007.unk")

## ACZ_text_bitmap_utility.py:
  Retrieves bitmap data from each letter from the unpacked folder and store it in the "bmp_lib" folder.
  It is a rough code, meant to be only used to assemble the bitmap library. I'm including it here, anyways.
  
## ACZ_string_decoder_UTF16.py:
  The original extraction program by death_the_d0g, with a few changes I made.
  It is not part of the workflow anymore, since I adapted it into "ACZ_line_swapper.py". I'm including it here, anyways.
