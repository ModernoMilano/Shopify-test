#!/bin/bash
# Gladmaken (smooth.py) van alle clips voor 'You Will Look Twice': de 1080p-versie waar die er is, anders de 480p-draft;
# bestaande clips uit vid/sm; piano2 met --raw-from=auto (komt tot stilstand); seraB blijft ruw (twinkelende lichten).
cd ~/tw
job() { src=$1; key=$2; extra=$3; [ -s vid/s/$key.mp4 ] && exit 0; python3 smooth.py "$src" vid/s/$key.mp4 $extra > vid/s/$key.log 2>&1 && echo "ok $key" || echo "FOUT $key"; }
export -f job
{
for s in H01 H02 H03 V02 V12; do echo "vid/final/$s.mp4 $s"; done
for s in V01 V03 V04 V05 V06 V08 V10 V11; do echo "vid/$s.mp4 $s"; done
echo "vid/sm/piano2_raw.mp4 piano2 --raw-from=auto"
for s in lagoA lagoB seraA seraD tbB; do echo "vid/sm/${s}_raw.mp4 $s"; done
} | xargs -P 3 -L 1 bash -c 'job $0 $1 $2'
echo KLAAR
