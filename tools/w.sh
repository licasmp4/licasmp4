#!/bin/bash
# uso: w.sh pasta saida.webp ms-por-quadro qualidade
img2webp -loop 0 -lossy -q $4 -m 4 -d $3 $1/q*.png -o $2 >/dev/null 2>&1 || echo "FAIL $1"
