#!/bin/bash
mpv $(python3 extract.py $1) --no-video
