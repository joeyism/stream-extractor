#!/bin/python3
import sys

from PyInquirer import style_from_dict, Token, prompt, Separator
mpv_exists=False
try:
    import mpv
except:
    mpv_exists=False

import prompt as p
import extract

url = sys.argv[1]
show_types = ["shows", "cable", "movies"]
questions = [
        {
            "type": "rawlist",
            "name": "show_type",
            "message": "Pick a show type",
            "choices": show_types
        }
    ]
answers = prompt(questions, style=p.style)
show_type = answers["show_type"]

m3u8_url = extract.run(url, show_type=show_type)
if mpv_exists:
    player = mpv.MPV(video=False, input_default_bindings=True, input_vo_keyboard=True)
    print("Playing {}".format(m3u8_url))
    player.play(m3u8_url)
    player.wait_for_playback()
else:
    bashCommand = "mpv {} --no-video".format(m3u8_url)
    print("Running ")
    print(bashCommand)
    import subprocess
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    output, error = process.communicate()
    print(output, error)
