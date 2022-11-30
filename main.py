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

def process_entry(entry):
    basename = entry.split('/')[-1]
    basename_no_ext = basename.split('.')[0]
    if basename_no_ext[0].isnumeric():
        song_title = re.sub(r'\d+ - ', '' , basename_no_ext)
    else:
        song_title = basename_no_ext
    if re.search(r'\(.*?\)', song_title):
        inside_parentheses = re.search(r'\(.*?\)', song_title).group(0)
        if "remaster" in inside_parentheses.lower():
            song_title = re.sub(r'\(.*?\)', '' , song_title).strip()
    return song_title




for playlist in os.listdir(playlist_folder):
    playlist_path = join(playlist_folder, playlist)
    if isfile(playlist_path):
        with open(playlist_path,'r',encoding = 'utf-8') as f:
                playlist_entries = f.read().splitlines()
                print(f'Checking playlist: {playlist}...')
                for entry in playlist_entries:
                    if not isfile(music_folder + entry):
                        print(f"{entry} is not a file, searching...")
                        basename = process_entry(entry)
                        result = os.popen(f'fd "{basename}" {music_folder}').read().strip()
                        if result:
                            print(fg.green + f'Song found at "{result}"')
                        else:
                            print(fg.red + f'File with basename "{basename}" not found.')
                            search = input('Search for filename manually: ')
                            result = os.popen(f'fd "{search}" {music_folder}').read().strip()
                            if result:
                                print(fg.green + f'Song found at "{result}"')
                            else:
                                print(fg.red + 'ok')
                input('...')
    else:
        input(fg.red + f'Internal error: {playlist_path} is not a file.')
