#!/bin/bash
# uso: r.sh "query" pasta  → renderiza quadros (sobrescreve os PNGs)
cd /tmp/claude-501/lp && mkdir -p "$2" && ./quadros "file:///tmp/claude-501/lp/cenas.html?$1" "$2" >/dev/null || echo "FAIL $1"
