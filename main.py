#!/usr/bin/env python3
import os
from os.path import isfile, join
from pprint import pprint
from sty import fg, rs
from pyfzf.pyfzf import FzfPrompt
import re

fzf = FzfPrompt()

playlist_folder = '/home/adam/.local/share/mpd/playlists/'
music_folder = '/home/adam/music/'
debug = True

def process_entry(entry):
    basename = entry.split('/')[-1]
    basename_no_ext = basename.rsplit( ".", 1 )[0]
    if basename_no_ext[0].isnumeric():
        song_title = re.sub(r'\d+ - ', '' , basename_no_ext)
    else:
        song_title = basename_no_ext
    if re.search(r'\(.*?\)', song_title):
        for m in re.finditer(r'\(.*?\)', song_title):
            matched_str = song_title[m.start():m.end()]
            if "remaster" in matched_str.lower():
                song_title = song_title.replace(matched_str, '').strip()
    return song_title

# TODO check if artist is the same, and if not, pause and ask user if it's correct
def search_music(str):
    result = os.popen(f'fd -c never -iF "{str}" {music_folder}').read().strip()
    if result:
        if result.count('\n') != 0:
            result = select_from_array(result.split('\n'))
        print(fg.green + f'Song found at "{result}"')
    else:
        print(fg.red + f'"{str}" not found.')
        search = input(fg.rs + 'Manual search: ')
        search_music(search)

# TODO save all user selections, so you don't have to keep selecting the song for different playlists
def select_from_array(arr):
    if debug:
        return arr[0]
    for id, i in enumerate(arr):
        print(fg.rs + f'{id} - {i}')
    inputIndex = input('Select: ').strip()
    if inputIndex.isnumeric():
        index = int(inputIndex)
        if index < len(arr):
            return arr[index]
        else:
            print(fg.red + f'"{inputIndex}" not in range')
    else:
        print(fg.red + f'"{inputIndex}" is not a number')
    select_from_array(arr)

for playlist in os.listdir(playlist_folder):
    playlist_path = join(playlist_folder, playlist)
    if isfile(playlist_path):
        with open(playlist_path,'r',encoding = 'utf-8') as f:
                playlist_entries = f.read().splitlines()
                print(fg.rs + f'Current playlist: {playlist}')
                for entry in playlist_entries:
                    if not isfile(music_folder + entry):
                        print(fg.red + entry)
                        basename = process_entry(entry)
                        print(fg.rs + f'Searching for {basename}...')
                        search_music(basename)
                # TODO when the playlist is finished, show all changes in list
                # The Smiths/Complete/034 - Girlfriend in a Coma (2011 Remaster).flac -> The Smiths/Strangeways, Here We Come/04 - Girlfriend in a Coma (2011 Remaster).flac
                for entry in playlist_entries:
                    print('')
    else:
        input(fg.red + f'Internal error: {playlist_path} is not a file.')
