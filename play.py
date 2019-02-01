#!/bin/python3
import extract
import sys
import mpv

url = sys.argv[1]
m3u8_url = extract.run(url)
player = mpv.MPV(video=False, input_default_bindings=True, input_vo_keyboard=True)
print("Playing {}".format(m3u8_url))
player.play(m3u8_url)
player.wait_for_playback()
