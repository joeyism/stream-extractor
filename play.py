#!/bin/python3
import sys

from PyInquirer import style_from_dict, Token, prompt, Separator
import mpv

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
answers = prompt(questions, style=extract.style)
show_type = answers["show_type"]

m3u8_url = extract.run(url, show_type=show_type)
player = mpv.MPV(video=False, input_default_bindings=True, input_vo_keyboard=True)
print("Playing {}".format(m3u8_url))
player.play(m3u8_url)
player.wait_for_playback()
