# Gebruik: vochain.sh in.mp3 uit.wav [tempo]
# De VO-keten uit de brief: high-pass, wat warmte, minder modder, presence, de-esser, compressie 3:1, stilte eraf.
# tempo blijft 1.0 (het scriptpanel: niet in tempo rekken; vertragen gaat met een geschreven pauze in de tekst).
t=${3:-1.0}
ffmpeg -v error -y -i "$1" -af "aresample=48000,highpass=f=70,equalizer=f=110:t=q:w=1:g=1.5,equalizer=f=300:t=q:w=1.2:g=-2,equalizer=f=3800:t=q:w=1.5:g=1.5,deesser=i=0.35,acompressor=threshold=-22dB:ratio=3:attack=8:release=140:makeup=2,rubberband=tempo=$t:formant=preserved:pitchq=quality,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08,areverse" -ar 48000 -ac 2 "$2"
