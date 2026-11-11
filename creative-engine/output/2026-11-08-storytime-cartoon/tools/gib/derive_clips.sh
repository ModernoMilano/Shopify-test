#!/bin/sh
# Bewerkte clips die de montage gebruikt in plaats van het origineel (uitvoeren in de map met clipsG/).
# N02: eerste 2,05 s vertraagd tot 2,6 s; daarna gaan haar ogen blauw open (het startbeeld heeft de ogen dicht).
ffmpeg -loglevel error -y -i clipsG/N02.mp4 -vf "trim=0:2.05,setpts=1.29*PTS,minterpolate=fps=24:mi_mode=blend" -an -c:v libx264 -crf 14 -pix_fmt yuv420p clipsG/N02s.mp4
# N13: eerste 1,29 s vooruit en dan achteruit, zodat de twee vingers de hele regel omhoog blijven.
ffmpeg -loglevel error -y -i clipsG/N13.mp4 -filter_complex "[0:v]trim=0:1.29,setpts=PTS-STARTPTS,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[v]" -map "[v]" -an -c:v libx264 -crf 14 -pix_fmt yuv420p clipsG/N13p.mp4
# N06: eerste 1,83 s vertraagd tot 2,29 s; daarna vervormt zijn gezicht bij het rillen (controle 11 nov).
ffmpeg -loglevel error -y -i clipsG/N06.mp4 -vf "trim=0:1.83,setpts=1.30*PTS,minterpolate=fps=24:mi_mode=blend" -an -c:v libx264 -crf 14 -pix_fmt yuv420p clipsG/N06s.mp4
# N20: eerste 3,0 s vertraagd tot 3,6 s; daarna kijkt zij op en gaan haar ogen lichter (amber) open (controle 11 nov).
ffmpeg -loglevel error -y -i clipsG/N20.mp4 -vf "trim=0:3.0,setpts=1.24*PTS,minterpolate=fps=24:mi_mode=blend" -an -c:v libx264 -crf 14 -pix_fmt yuv420p clipsG/N20s.mp4
# N22: eerste 2,8 s vertraagd tot 3,6 s; daarna laat hij zijn hoofd zakken en klopt zijn gezicht niet meer (controle 11 nov).
ffmpeg -loglevel error -y -i clipsG/N22.mp4 -vf "trim=0:2.8,setpts=1.31*PTS,minterpolate=fps=24:mi_mode=blend" -an -c:v libx264 -crf 14 -pix_fmt yuv420p clipsG/N22s.mp4
