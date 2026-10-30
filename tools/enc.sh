#!/bin/bash
# uso: enc.sh pasta saida.gif fps cores [filtro-extra,]
ffmpeg -loglevel error -y -framerate $3 -i $1/q%03d.png -vf "${5}split[a][b];[a]palettegen=max_colors=${4}:stats_mode=full[p];[b][p]paletteuse=dither=none" -loop 0 $2
