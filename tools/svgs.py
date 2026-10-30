# Títulos de seção (aparelho Y2K com LCD) e painel de formação, em SVG animado.
import os, sys
OUT = sys.argv[1]
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"

def salvar(nome, w, h, corpo, css=''):
    with open(os.path.join(OUT, nome), 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><style>{css}</style>{corpo}</svg>')
    print(nome)

def titulo(nome, texto, cara, hora):
    W, H = 900, 76
    p = ['<defs><linearGradient id="pl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f7ff"/><stop offset=".5" stop-color="#a9b6d6"/><stop offset="1" stop-color="#6d7ba6"/></linearGradient>'
         '<radialGradient id="b1" cx=".35" cy=".3" r=".7"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#3a7bff"/><stop offset="1" stop-color="#101848"/></radialGradient>'
         '<radialGradient id="b2" cx=".35" cy=".3" r=".7"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#ff5fae"/><stop offset="1" stop-color="#101848"/></radialGradient>'
         '<filter id="gl"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
         f'<rect x="2" y="4" width="{W-4}" height="{H-8}" rx="34" fill="url(#pl)" stroke="#26305e" stroke-width="3"/>',
         f'<rect x="9" y="11" width="{W-18}" height="{H-22}" rx="27" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="1.5"/>',
         '<circle cx="40" cy="38" r="11" fill="url(#b1)"/><circle cx="70" cy="38" r="11" fill="url(#b2)"/>',
         f'<rect x="96" y="17" width="{W-130}" height="42" rx="8" fill="#0d2a14"/><rect x="99" y="20" width="{W-136}" height="36" rx="6" fill="#123b1c"/>']
    # linhas de LCD
    p.append(''.join(f'<rect x="100" y="{y}" width="{W-138}" height="1" fill="#000" opacity=".25"/>' for y in range(22, 56, 3)))
    p.append(f'<g filter="url(#gl)"><text x="118" y="46" font-family="{MONO}" font-size="22" font-weight="bold" fill="#7dff8a">▶ {texto}<tspan class="cur">_</tspan></text>'
             f'<text x="{W-200}" y="46" font-family="{MONO}" font-size="20" font-weight="bold" fill="#7dff8a" text-anchor="end">{hora[:2]}<tspan class="pi">:</tspan>{hora[3:]}</text>'
             f'<text x="{W-52}" y="46" font-family="{MONO}" font-size="20" font-weight="bold" fill="#ff6fb8" text-anchor="end" class="cara">{cara}</text></g>')
    css = ('.cur{animation:c 1s steps(1) infinite}@keyframes c{50%{opacity:0}}'
           '.pi{animation:c 1s steps(1) infinite}'
           '.cara{animation:k 4s steps(1) infinite}@keyframes k{0%,92%{opacity:1}93%,96%{opacity:.2}}')
    salvar(nome, W, H, ''.join(p), css)

def formacao():
    W, H = 900, 330
    itens = [('Full Stack Python', 'Projeto Farol · Associação Wise Madness (Bauru)', 'concluído'),
             ('Java Full Stack', 'EBAC · Java, HTML, CSS e JavaScript', 'concluído'),
             ('Inteligência Artificial', 'SENAI', 'concluído'),
             ('todo o resto', 'aprendido por conta própria, projeto atrás de projeto', 'sempre')]
    p = ['<defs><pattern id="gr" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#788cff" stroke-opacity=".1"/></pattern></defs>',
         f'<rect width="{W}" height="{H}" fill="#080a2e"/><rect width="{W}" height="{H}" fill="url(#gr)"/>',
         f'<rect x="3" y="3" width="{W-6}" height="{H-6}" fill="none" stroke="#7f9bff" stroke-width="2"/>',
         f'<text x="20" y="34" font-family="{MONO}" font-size="16" font-weight="bold" fill="#e8ecff">memory <tspan fill="#ffd23c">training</tspan></text>',
         f'<text x="{W-20}" y="34" font-family="{MONO}" font-size="14" fill="#5a6bc0" text-anchor="end">description</text>',
         f'<rect x="20" y="46" width="{W-40}" height="1" fill="#7f9bff"/>']
    for i, (t, d, st) in enumerate(itens):
        y = 92 + i * 60
        sel = i == 0
        p.append(f'<g class="li" style="animation-delay:{i*0.6}s">'
                 f'<text x="34" y="{y}" font-family="{MONO}" font-size="20" font-weight="bold" fill="#ffffff">{t}</text>'
                 f'<text x="34" y="{y+24}" font-family="{MONO}" font-size="15" fill="#b9c6ff">{d}</text>'
                 f'<rect x="{W-170}" y="{y-20}" width="136" height="26" rx="5" fill="{"#123b1c" if st != "sempre" else "#3b1230"}"/>'
                 f'<text x="{W-102}" y="{y-2}" font-family="{MONO}" font-size="14" font-weight="bold" fill="{"#7dff8a" if st != "sempre" else "#ff6fb8"}" text-anchor="middle">{st}</text></g>')
    p.append(f'<rect class="sel" x="20" y="64" width="{W-40}" height="54" fill="#7f9bff" opacity=".12"/>')
    css = ('.sel{animation:s 6s steps(1) infinite}@keyframes s{0%{transform:translateY(0)}25%{transform:translateY(60px)}50%{transform:translateY(120px)}75%{transform:translateY(180px)}}'
           '.li{animation:l 6s steps(1) infinite}@keyframes l{0%,100%{opacity:1}}')
    salvar('formacao.svg', W, H, ''.join(p), css)

titulo('t-sobre.svg', 'SOBRE MIM', '(˘ω˘)', '02:44')
titulo('t-formacao.svg', 'FORMAÇÃO', '(・ω・)', '03:12')
titulo('t-projetos.svg', 'MEMÓRIAS / PROJETOS', '(っ˘ω˘ς)', '04:20')
titulo('t-jogos.svg', 'JOGOS QUE ME CONFORTAM', '(^ω^)', '01:07')
titulo('t-ferramentas.svg', 'FERRAMENTAS', '(•ω•)', '05:55')
titulo('t-atividade.svg', 'ATIVIDADE', '(￣ω￣;)', '23:59')
formacao()
