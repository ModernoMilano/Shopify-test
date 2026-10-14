#!/bin/bash
# Wacht op het gladmaken en het knippen van de stemmen, bouwt dan per stem de montage (build_edit_v3.py) en rendert
# (film3.py): Grady en Holden met Portra 400, en Grady zonder filter om te vergelijken.
cd ~/tw
mkdir -p ~/film/out
while ! grep -q KLAAR vid/s/all.log; do sleep 10; done
while ! grep -q KLAAR ~/film/vo/split_holden.log; do sleep 10; done
render() { stem=$1; look=$2; tag=$stem${look:+-$look}
  python3 build_edit_v3.py $stem $look > ~/film/out/build-$tag.log 2>&1 || { echo "FOUT build $tag"; return; }
  mkdir -p ~/film/out/w-$tag && cd ~/film/out/w-$tag && python3 ~/tw/film3.py ~/film/out/film-edit-$tag.json ~/film/out/$tag.mp4 > ~/film/out/film-$tag.log 2>&1 && echo "ok $tag" || echo "FOUT film $tag"
  cd ~/tw; }
render grady portra
render holden portra
render grady
echo KLAAR
