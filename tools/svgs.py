# Títulos de seção (aparelho Y2K com LCD) e painel de formação, em SVG animado.
import os, sys
OUT = sys.argv[1]
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"

def salvar(nome, w, h, corpo, css=''):
    with open(os.path.join(OUT, nome), 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><style>{css}</style>{corpo}</svg>')
    print(nome)

def titulo(nome, texto, cara, hora, fechada):
    W, H = 900, 76
    p = ['<defs><linearGradient id="pl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f7ff"/><stop offset=".5" stop-color="#a9b6d6"/><stop offset="1" stop-color="#6d7ba6"/></linearGradient>'
         '<radialGradient id="b1" cx=".35" cy=".3" r=".7"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#3a7bff"/><stop offset="1" stop-color="#101848"/></radialGradient>'
         '<radialGradient id="b2" cx=".35" cy=".3" r=".7"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#ff5fae"/><stop offset="1" stop-color="#101848"/></radialGradient>'
         f'<clipPath id="cp"><rect x="2" y="4" width="{W-4}" height="{H-8}" rx="34"/></clipPath>'
         '<linearGradient id="br" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
         '<filter id="gl"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
         f'<rect x="2" y="4" width="{W-4}" height="{H-8}" rx="34" fill="url(#pl)" stroke="#26305e" stroke-width="3"/>',
         f'<rect x="9" y="11" width="{W-18}" height="{H-22}" rx="27" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="1.5"/>',
         '<circle cx="40" cy="38" r="15" fill="#3a7bff" opacity=".0" class="ha"/><circle cx="70" cy="38" r="15" fill="#ff5fae" opacity=".0" class="hb"/>'
         '<circle cx="40" cy="38" r="11" fill="url(#b1)"/><circle cx="70" cy="38" r="11" fill="url(#b2)"/>',
         f'<rect x="96" y="17" width="{W-130}" height="42" rx="8" fill="#0d2a14"/><rect x="99" y="20" width="{W-136}" height="36" rx="6" fill="#123b1c"/>']
    # linhas de LCD
    p.append(''.join(f'<rect x="100" y="{y}" width="{W-138}" height="1" fill="#000" opacity=".25"/>' for y in range(22, 56, 3)))
    p.append(f'<g filter="url(#gl)"><text x="118" y="46" font-family="{MONO}" font-size="22" font-weight="bold" fill="#7dff8a">▶ {texto}<tspan class="cur">_</tspan></text>'
             f'<text x="{W-200}" y="46" font-family="{MONO}" font-size="20" font-weight="bold" fill="#7dff8a" text-anchor="end">{hora[:2]}<tspan class="pi">:</tspan>{hora[3:]}</text>'
             f'<text x="{W-52}" y="46" font-family="{MONO}" font-size="20" font-weight="bold" fill="#ff6fb8" text-anchor="end" class="ab">{cara}</text>'
             f'<text x="{W-52}" y="46" font-family="{MONO}" font-size="20" font-weight="bold" fill="#ff6fb8" text-anchor="end" class="fe">{fechada}</text>'
             + ''.join(f'<rect x="{W-330 + k*9}" y="24" width="6" height="28" fill="{"#7dff8a" if k % 2 else "#ff6fb8"}" class="eq" style="animation-duration:{0.5 + (k*37 % 5)/10}s;animation-delay:-{k*0.13:.2f}s"/>' for k in range(6))
             + '</g>'
             f'<g clip-path="url(#cp)"><rect class="gl" x="-160" y="0" width="120" height="{H}" fill="url(#br)" transform="skewX(-20)"/></g>')
    css = ('.cur{animation:c 1s steps(1) infinite}@keyframes c{50%{opacity:0}}'
           '.pi{animation:c 1s steps(1) infinite}'
           '.ab{animation:k 4s steps(1) infinite}.fe{opacity:0;animation:f 4s steps(1) infinite}'
           '@keyframes k{0%,90%{opacity:1}91%,96%{opacity:0}}@keyframes f{0%,90%{opacity:0}91%,96%{opacity:1}}'
           '.eq{transform-box:fill-box;transform-origin:50% 100%;animation:e .6s ease-in-out infinite alternate}@keyframes e{from{transform:scaleY(.15)}to{transform:scaleY(1)}}'
           '.gl{animation:g 5s ease-in-out infinite}@keyframes g{0%{transform:translateX(0) skewX(-20deg)}35%,100%{transform:translateX(1100px) skewX(-20deg)}}'
           '.ha{animation:h 2s ease-in-out infinite}.hb{animation:h 2s ease-in-out -1s infinite}@keyframes h{0%,100%{opacity:0}50%{opacity:.45}}')
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
    p.append(f'<g class="sel"><rect x="20" y="64" width="{W-40}" height="54" fill="#7f9bff" opacity=".12"/>'
             '<path class="bt" d="M24 80h4v-2h4v2h2v-2h4v2h2v6h-2v2h-2v2h-2v2h-2v2h-2v-2h-2v-2h-2v-2h-2v-2h-2z" fill="#ff4fb6" transform="translate(-4 8) scale(.7)"/></g>')
    css = ('.sel{animation:s 6s steps(1) infinite}@keyframes s{0%{transform:translateY(0)}25%{transform:translateY(60px)}50%{transform:translateY(120px)}75%{transform:translateY(180px)}}'
           '.bt{animation:b .8s steps(1) infinite}@keyframes b{50%{opacity:.3}}')
    salvar('formacao.svg', W, H, ''.join(p), css)

titulo('t-sobre.svg', 'SOBRE MIM', '(˘ω˘)', '02:44', '(-ω-)')
titulo('t-formacao.svg', 'FORMAÇÃO', '(・ω・)', '03:12', '(-ω-)')
titulo('t-projetos.svg', 'MEMÓRIAS / PROJETOS', '(っ˘ω˘ς)', '04:20', '(っ-ω-ς)')
titulo('t-hobbies.svg', 'HOBBIES', '(^ω^)', '03:33', '(-ω-)')
titulo('t-ferramentas.svg', 'FERRAMENTAS', '(•ω•)', '05:55', '(-ω-)')
titulo('t-atividade.svg', 'ATIVIDADE', '(￣ω￣;)', '23:59', '(-ω-;)')
formacao()
