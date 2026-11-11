#!/bin/sh
# Bewerkte clips die de montage gebruikt in plaats van het origineel (uitvoeren in de map met clipsG/).
# N02: eerste 2,05 s vertraagd tot 2,6 s; daarna gaan haar ogen blauw open (het startbeeld heeft de ogen dicht).
ffmpeg -loglevel error -y -i clipsG/N02.mp4 -vf "trim=0:2.05,setpts=1.29*PTS,minterpolate=fps=24:mi_mode=blend" -an -c:v libx264 -crf 14 -pix_fmt yuv420p clipsG/N02s.mp4
# N13: eerste 1,29 s vooruit en dan achteruit, zodat de twee vingers de hele regel omhoog blijven.
ffmpeg -loglevel error -y -i clipsG/N13.mp4 -filter_complex "[0:v]trim=0:1.29,setpts=PTS-STARTPTS,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[v]" -map "[v]" -an -c:v libx264 -crf 14 -pix_fmt yuv420p clipsG/N13p.mp4
