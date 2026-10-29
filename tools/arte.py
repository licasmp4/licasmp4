# Gera as artes animadas (SVG) do README do perfil, no clima da Guilda de Monster Hunter.
# Uso: python3 tools/arte.py  → escreve em assets/
import os, random

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(OUT, exist_ok=True)
random.seed(4)

PAPEL, PAPEL2, TINTA, TINTA2 = '#efe2c4', '#e2cfa6', '#3b2a1a', '#6b5238'
MADEIRA, MADEIRA2, OURO, OURO2, GUILDA = '#2a1c12', '#3d2919', '#c9a24a', '#f2d68a', '#8c2a1c'
SERIF = "Georgia,'Times New Roman',serif"

def salvar(nome, w, h, corpo, css=''):
    with open(os.path.join(OUT, nome), 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><style>{css}</style>{corpo}</svg>')
    print(nome)

# papel envelhecido: textura + bordas irregulares
def defs_papel(id_):
    return (f'<filter id="{id_}" x="-2%" y="-2%" width="104%" height="104%">'
            f'<feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="3" result="n"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="7" result="d"/>'
            f'<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="8" result="g"/>'
            f'<feColorMatrix in="g" type="matrix" values="0 0 0 0 .35  0 0 0 0 .25  0 0 0 0 .12  0 0 0 .22 0" result="gg"/>'
            f'<feComposite in="gg" in2="d" operator="in" result="gr"/>'
            f'<feMerge><feMergeNode in="d"/><feMergeNode in="gr"/></feMerge></filter>'
            f'<radialGradient id="{id_}v" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="{PAPEL}"/><stop offset="1" stop-color="{PAPEL2}"/></radialGradient>')

def brasas(w, h, n, base):
    out = []
    for i in range(n):
        x = random.randrange(20, w - 20); d = round(random.uniform(4, 8), 1); b = round(random.uniform(0, 8), 1)
        r = random.choice([1.5, 2, 2.5])
        out.append(f'<circle class="br" style="animation-duration:{d}s;animation-delay:-{b}s" cx="{x}" cy="{base}" r="{r}" fill="{random.choice([OURO2, "#ff9a3c", "#ffcf6b"])}"/>')
    return ''.join(out)

CSS_BRASA = ('.br{animation:br 6s linear infinite;opacity:0}'
             '@keyframes br{0%{transform:translate(0,0);opacity:0}10%{opacity:.9}100%{transform:translate(18px,-260px);opacity:0}}')

# brasão da guilda (escudo + duas espadas cruzadas)
def brasao(cx, cy, s, cor=TINTA):
    return (f'<g transform="translate({cx} {cy}) scale({s})" fill="none" stroke="{cor}" stroke-width="3" stroke-linejoin="round">'
            f'<path d="M-46 -40 L46 40 M46 -40 L-46 40" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M-52 -46 l12 0 M52 -46 l-12 0 M-56 -38 l8 -8 M56 -38 l-8 -8" stroke-width="4"/>'
            f'<path d="M0 -34 C18 -34 30 -28 30 -28 L30 4 C30 24 14 34 0 42 C-14 34 -30 24 -30 4 L-30 -28 C-30 -28 -18 -34 0 -34Z" fill="{GUILDA}" stroke="{cor}"/>'
            f'<path d="M0 -20 L6 -6 L20 -6 L9 3 L13 17 L0 9 L-13 17 L-9 3 L-20 -6 L-6 -6Z" fill="{OURO2}" stroke="none"/>'
            f'</g>')

# ================= GUILD CARD (banner) =================
import base64
OURO_GRAD = ('<linearGradient id="ouro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0b8"/><stop offset=".35" stop-color="#e2b955"/>'
             '<stop offset=".55" stop-color="#9a6a1e"/><stop offset=".75" stop-color="#e8c46a"/><stop offset="1" stop-color="#7a5418"/></linearGradient>')

def madeira(id_):
    # veios de madeira: ruído esticado na horizontal, colorido de marrom
    return (f'<filter id="{id_}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".003 .09" numOctaves="4" seed="11"/>'
            f'<feColorMatrix type="matrix" values="0 0 0 0 .20  0 0 0 0 .12  0 0 0 0 .07  0 0 0 0 1"/>'
            f'<feComponentTransfer><feFuncA type="table" tableValues="0 .9"/></feComponentTransfer>'
            f'<feComposite in2="SourceGraphic" operator="in"/></filter>')

def filigrana(x, y, sx, sy, cor):
    # arabesco de canto
    return (f'<g transform="translate({x} {y}) scale({sx} {sy})" fill="none" stroke="{cor}" stroke-width="2" stroke-linecap="round">'
            f'<path d="M0 46 V10 Q0 0 10 0 H46"/><path d="M8 54 V18 Q8 8 18 8 H54" stroke-width="1"/>'
            f'<path d="M18 18 q14 2 16 16 q-10 -2 -16 -16z" fill="{cor}" stroke="none"/>'
            f'<path d="M46 0 q10 -8 20 0 q-10 6 -20 0z M0 46 q-8 10 0 20 q6 -10 0 -20z" fill="{cor}" stroke="none"/>'
            f'<circle cx="26" cy="26" r="3" fill="{cor}" stroke="none"/></g>')

def guild_card():
    W, H = 1200, 460
    foto = base64.b64encode(open(os.path.join(os.path.dirname(__file__), 'retrato.jpg'), 'rb').read()).decode()
    p = [f'<defs>{defs_papel("pp")}{madeira("veio")}{OURO_GRAD}'
         f'<linearGradient id="fundo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2516"/><stop offset="1" stop-color="#140c06"/></linearGradient>'
         f'<radialGradient id="fogo" cx=".5" cy="1.05" r=".75"><stop offset="0" stop-color="#ff9a3c" stop-opacity=".55"/><stop offset=".5" stop-color="#ff7a1a" stop-opacity=".15"/><stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="vin" cx=".5" cy=".5" r=".72"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>'
         f'<radialGradient id="mancha"><stop offset="0" stop-color="#8a6a3a" stop-opacity=".22"/><stop offset="1" stop-color="#8a6a3a" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="brilho" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
         f'<radialGradient id="cera" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#c0473a"/><stop offset=".7" stop-color="#8c2a1c"/><stop offset="1" stop-color="#5a160c"/></radialGradient>'
         f'<clipPath id="rt"><circle cx="0" cy="0" r="80"/></clipPath>'
         f'<clipPath id="tit"><text x="640" y="112" text-anchor="middle" font-family="{SERIF}" font-size="50" font-weight="bold" letter-spacing="14">GUILD CARD</text></clipPath>'
         f'<filter id="sombra" x="-10%" y="-10%" width="130%" height="140%"><feGaussianBlur stdDeviation="10"/></filter></defs>',
         # mesa
         f'<rect width="{W}" height="{H}" fill="url(#fundo)"/>',
         f'<rect width="{W}" height="{H}" fill="#000" filter="url(#veio)"/>']
    for y in (0, 118, 236, 354):
        p.append(f'<rect x="0" y="{y}" width="{W}" height="3" fill="#0b0603" opacity=".8"/>')
    p.append(f'<rect class="fg" width="{W}" height="{H}" fill="url(#fogo)"/>')
    # cartão (levemente torto, como se tivesse sido jogado na mesa)
    cx, cy, cw, ch = 110, 36, 1000, 380
    p.append(f'<g transform="rotate(-1.2 600 230)">')
    p.append(f'<rect x="{cx+10}" y="{cy+16}" width="{cw}" height="{ch}" fill="#000" opacity=".6" filter="url(#sombra)"/>')
    p.append(f'<g filter="url(#pp)"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="url(#ppv)"/></g>')
    for (mx, my, r) in [(300, 360, 90), (930, 110, 70), (1040, 380, 60), (180, 90, 50)]:
        p.append(f'<circle cx="{mx}" cy="{my}" r="{r}" fill="url(#mancha)"/>')
    p.append(f'<rect x="{cx+16}" y="{cy+16}" width="{cw-32}" height="{ch-32}" fill="none" stroke="{TINTA2}" stroke-width="2.5"/>')
    p.append(f'<rect x="{cx+24}" y="{cy+24}" width="{cw-48}" height="{ch-48}" fill="none" stroke="{TINTA2}" stroke-width="1"/>')
    for (fx, fy, sx, sy) in [(cx+30, cy+30, 1, 1), (cx+cw-30, cy+30, -1, 1), (cx+30, cy+ch-30, 1, -1), (cx+cw-30, cy+ch-30, -1, -1)]:
        p.append(filigrana(fx, fy, sx, sy, '#7a5a34'))
    # título em ouro com contorno
    p.append(f'<text x="640" y="112" text-anchor="middle" font-family="{SERIF}" font-size="50" font-weight="bold" letter-spacing="14" fill="url(#ouro)" stroke="#4a3010" stroke-width="1.6" paint-order="stroke">GUILD CARD</text>')
    p.append(f'<g clip-path="url(#tit)"><rect class="sh" x="250" y="60" width="140" height="70" fill="url(#brilho)"/></g>')
    p.append(f'<path d="M420 134 H600 M680 134 H860" stroke="#7a5a34" stroke-width="1.5"/>'
             f'<path d="M640 124 l14 10 l-14 10 l-14 -10z" fill="{GUILDA}" stroke="#4a3010" stroke-width="1"/>'
             f'<circle cx="610" cy="134" r="3" fill="#7a5a34"/><circle cx="670" cy="134" r="3" fill="#7a5a34"/>')
    # medalhão com o retrato
    mx, my = 280, 236
    p.append(f'<g transform="translate({mx} {my})">')
    p.append(f'<circle r="104" fill="#000" opacity=".25" transform="translate(4 6)"/>')
    p.append(f'<circle r="100" fill="url(#ouro)" stroke="#4a3010" stroke-width="2"/>')
    p.append(''.join(f'<rect x="-3" y="-99" width="6" height="10" fill="#6a4a14" transform="rotate({k*15})"/>' for k in range(24)))
    p.append(f'<circle r="86" fill="#2a1c12"/>')
    p.append(f'<image href="data:image/jpeg;base64,{foto}" x="-80" y="-80" width="160" height="160" clip-path="url(#rt)" preserveAspectRatio="xMidYMid slice"/>')
    p.append(f'<circle r="80" fill="none" stroke="#f2d68a" stroke-width="2"/><circle r="86" fill="none" stroke="#4a3010" stroke-width="2"/>')
    p.append('</g>')
    # faixa com o apelido embaixo do medalhão
    p.append(f'<g transform="translate({mx} {my+112})"><path d="M-112 -16 H112 L100 0 L112 16 H-112 L-100 0Z" fill="{GUILDA}" stroke="#4a1208" stroke-width="2"/>'
             f'<path d="M-112 -16 l-18 4 l10 12 l-10 12 l18 -12z M112 -16 l18 4 l-10 12 l10 12 l-18 -12z" fill="#6a1a10"/>'
             f'<text y="6" text-anchor="middle" font-family="{SERIF}" font-size="17" font-weight="bold" letter-spacing="4" fill="#f2d68a">LICAS.MP3</text></g>')
    # nome e campos
    p.append(f'<text x="440" y="190" font-family="{SERIF}" font-size="44" font-weight="bold" fill="{TINTA}">Lucas Luiz</text>')
    p.append(f'<text x="442" y="216" font-family="{SERIF}" font-size="16" font-style="italic" fill="{TINTA2}">Caçador da Guilda · Bauru, SP</text>')
    campos = [('FORMAÇÃO', 'Full Stack Python — Projeto Farol'),
              ('CURSOS', 'Java Full Stack (EBAC) · IA (SENAI)'),
              ('OFÍCIO', 'apps, sites e ferramentas com IA'),
              ('CAÇADAS', 'MHGU · MH4U · MHP3rd · MHFU')]
    for i, (k, v) in enumerate(campos):
        y = 262 + i * 36
        p.append(f'<text x="442" y="{y}" font-family="{SERIF}" font-size="12" font-weight="bold" letter-spacing="3" fill="{GUILDA}">{k}</text>')
        p.append(f'<text x="560" y="{y}" font-family="{SERIF}" font-size="20" fill="{TINTA}">{v}</text>')
        p.append(f'<path d="M560 {y+11} H990" stroke="{TINTA2}" stroke-width=".8" stroke-dasharray="1 4" opacity=".8"/>')
    # selo de cera
    p.append(f'<g transform="translate(1030 352)"><g class="selo">'
             f'<path d="M-40 4 q-10 14 -2 22 q8 -2 6 -14z M30 26 q8 14 18 8 q-4 -10 -14 -12z M-6 40 q2 12 12 12 q2 -8 -6 -14z" fill="#7a1e12"/>'
             f'<circle r="42" fill="url(#cera)"/><circle r="32" fill="none" stroke="#5a160c" stroke-width="2.5"/><circle r="32" fill="none" stroke="#e08a78" stroke-width="1" opacity=".4" transform="translate(-1 -1)"/>'
             f'{brasao(0, 0, .42, "#5a160c")}</g></g>')
    p.append('</g>')
    # poeira na luz e brasas
    for i in range(18):
        x = random.randrange(120, 1080); y = random.randrange(60, 400); d = round(random.uniform(7, 12), 1); b = round(random.uniform(0, 10), 1)
        p.append(f'<circle class="po" style="animation-duration:{d}s;animation-delay:-{b}s" cx="{x}" cy="{y}" r="1.4" fill="#fff3d0"/>')
    p.append(brasas(W, H, 30, H + 4))
    p.append(f'<rect width="{W}" height="{H}" fill="url(#vin)"/>')
    css = (CSS_BRASA +
           '.sh{animation:sh 6s ease-in-out infinite}@keyframes sh{0%,45%{transform:translateX(0)}100%{transform:translateX(620px)}}'
           '.fg{animation:fg 3.1s ease-in-out infinite}@keyframes fg{0%,100%{opacity:1}23%{opacity:.75}41%{opacity:.95}63%{opacity:.7}81%{opacity:.9}}'
           '.selo{animation:selo 7s ease-in-out infinite}@keyframes selo{0%,100%{transform:rotate(-10deg)}50%{transform:rotate(-4deg)}}'
           '.po{animation:po 9s ease-in-out infinite;opacity:0}@keyframes po{0%{transform:translate(0,0);opacity:0}30%{opacity:.55}70%{opacity:.35}100%{transform:translate(30px,-40px);opacity:0}}')
    salvar('guild-card.svg', W, H, ''.join(p), css)

# ================= TÍTULOS DE SEÇÃO =================
def titulo(nome, t):
    W, H = 900, 70
    p = [f'<path d="M20 48 H{W-20}" stroke="{OURO}" stroke-width="1.5" opacity=".6"/>',
         f'<path d="M20 48 l-10 -6 v12z M{W-20} 48 l10 -6 v12z" fill="{OURO}"/>',
         f'<g class="gem"><path d="M{W//2} 34 l14 14 l-14 14 l-14 -14z" fill="{GUILDA}" stroke="{OURO2}" stroke-width="2"/></g>',
         f'<text x="20" y="34" font-family="{SERIF}" font-size="28" font-weight="bold" letter-spacing="3" fill="{OURO2}">{t}</text>']
    css = '.gem{transform-box:fill-box;transform-origin:center;animation:gem 3s ease-in-out infinite}@keyframes gem{50%{transform:scale(1.25) rotate(45deg)}}'
    salvar(nome, W, H, ''.join(p), css)

# ================= QUESTS (projetos) =================
def quest(nome, estrelas, titulo_, objetivo, local, cliente, carimbo, cacadores='Lucas'):
    W, H = 580, 286
    p = [f'<defs>{defs_papel("pp")}</defs>',
         f'<rect x="10" y="14" width="{W-20}" height="{H-22}" fill="#000" opacity=".4"/>',
         f'<g filter="url(#pp)"><rect x="4" y="6" width="{W-20}" height="{H-22}" fill="url(#ppv)"/></g>',
         # prego
         f'<circle cx="{W//2-6}" cy="20" r="7" fill="#7a6a58"/><circle cx="{W//2-8}" cy="18" r="2.5" fill="#cbbba5"/>']
    # faixa de estrelas
    p.append(f'<text x="32" y="56" font-family="{SERIF}" font-size="15" letter-spacing="2" fill="{GUILDA}">'
             + ''.join(f'<tspan class="st" style="animation-delay:{i*.18}s">★</tspan>' for i in range(estrelas)) + '</text>')
    p.append(f'<text x="32" y="92" font-family="{SERIF}" font-size="30" font-weight="bold" fill="{TINTA}">{titulo_}</text>')
    p.append(f'<path d="M32 104 H{W-52}" stroke="{TINTA2}" stroke-width="1"/>')
    linhas = [('Objetivo', objetivo), ('Local', local), ('Cliente', cliente), ('Caçadores', cacadores)]
    y = 132
    for k, v in linhas:
        for j, parte in enumerate(v if isinstance(v, list) else [v]):
            if j == 0:
                p.append(f'<text x="32" y="{y}" font-family="{SERIF}" font-size="14" font-style="italic" fill="{TINTA2}">{k}</text>')
            p.append(f'<text x="122" y="{y}" font-family="{SERIF}" font-size="16" fill="{TINTA}">{parte}</text>')
            y += 24
        y += 4
    cor = GUILDA if carimbo == 'PRIVADA' else '#2e5a3a'
    p.append(f'<g class="ca" transform="translate({W-110} 66) rotate(-12)"><rect x="-62" y="-20" width="124" height="40" fill="none" stroke="{cor}" stroke-width="3" opacity=".85"/>'
             f'<text y="8" text-anchor="middle" font-family="{SERIF}" font-size="20" font-weight="bold" letter-spacing="3" fill="{cor}" opacity=".85">{carimbo}</text></g>')
    css = ('.st{animation:st 2.4s ease-in-out infinite}@keyframes st{0%,70%,100%{fill:' + GUILDA + '}80%{fill:' + OURO + '}}'
           '.ca{animation:ca 5s ease-in-out infinite}@keyframes ca{0%,100%{opacity:1}50%{opacity:.75}}')
    salvar(nome, W, H, ''.join(p), css)

# ================= PLACA DO GORE MAGALA =================
def placa_gore():
    W, H = 900, 150
    ROXO, ROXO2 = '#7a3cff', '#c18cff'
    p = [f'<defs><radialGradient id="aura" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="{ROXO}" stop-opacity=".55"/><stop offset="1" stop-color="{ROXO}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="fd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0d0812"/><stop offset=".5" stop-color="#1c1026"/><stop offset="1" stop-color="#0d0812"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" rx="10" fill="url(#fd)"/>',
         f'<ellipse class="au" cx="{W//2}" cy="{H//2}" rx="380" ry="80" fill="url(#aura)"/>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="none" stroke="{ROXO}" stroke-opacity=".5" stroke-width="2"/>']
    # partículas do vírus frenético subindo
    for i in range(34):
        x = random.randrange(30, W - 30); d = round(random.uniform(3, 6), 1); b = round(random.uniform(0, 6), 1)
        p.append(f'<circle class="vi" style="animation-duration:{d}s;animation-delay:-{b}s" cx="{x}" cy="{H+6}" r="{random.choice([1.5,2,2.5,3])}" fill="{random.choice([ROXO, ROXO2, "#e2c6ff"])}"/>')
    p.append(f'<text x="{W//2}" y="64" text-anchor="middle" font-family="{SERIF}" font-size="15" letter-spacing="8" fill="{ROXO2}">O MONSTRO MAIS AURA</text>')
    p.append(f'<text class="nm" x="{W//2}" y="112" text-anchor="middle" font-family="{SERIF}" font-size="46" font-weight="bold" letter-spacing="12" fill="#f1e6ff">GORE MAGALA</text>')
    css = ('.au{transform-box:fill-box;transform-origin:center;animation:au 3.2s ease-in-out infinite}@keyframes au{50%{transform:scale(1.12);opacity:.6}}'
           '.vi{animation:vi 5s linear infinite;opacity:0}@keyframes vi{0%{transform:translate(0,0);opacity:0}15%{opacity:.9}100%{transform:translate(-14px,-150px);opacity:0}}'
           '.nm{animation:nm 3.2s ease-in-out infinite}@keyframes nm{50%{fill:#c18cff}}')
    salvar('placa-gore-magala.svg', W, H, ''.join(p), css)

# ================= TREINAMENTOS (formação) =================
def treinamentos():
    W, H = 900, 300
    itens = [('Full Stack Python', 'Projeto Farol — Associação Wise Madness, Bauru', 'CONCLUÍDO'),
             ('Java Full Stack', 'EBAC — Java, HTML, CSS e JavaScript', 'CONCLUÍDO'),
             ('Inteligência Artificial', 'SENAI', 'CONCLUÍDO'),
             ('Todo o resto', 'na raça: projeto atrás de projeto', 'SEMPRE')]
    p = [f'<defs>{defs_papel("pp")}</defs>',
         f'<rect x="10" y="12" width="{W-20}" height="{H-20}" fill="#000" opacity=".4"/>',
         f'<g filter="url(#pp)"><rect x="4" y="4" width="{W-20}" height="{H-20}" fill="url(#ppv)"/></g>',
         f'<text x="40" y="48" font-family="{SERIF}" font-size="14" font-style="italic" letter-spacing="2" fill="{TINTA2}">Registro da Área de Treinamento</text>',
         f'<path d="M40 60 H{W-56}" stroke="{TINTA2}" stroke-width="1"/>']
    for i, (t, d, st) in enumerate(itens):
        y = 98 + i * 52
        p.append(f'<g class="it" style="animation-delay:{i*.35}s"><path d="M44 {y-12} l10 10 l16 -20" fill="none" stroke="{GUILDA}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<text x="86" y="{y}" font-family="{SERIF}" font-size="21" font-weight="bold" fill="{TINTA}">{t}</text>'
                 f'<text x="86" y="{y+20}" font-family="{SERIF}" font-size="15" fill="{TINTA2}">{d}</text>'
                 f'<text x="{W-60}" y="{y+4}" text-anchor="end" font-family="{SERIF}" font-size="13" font-weight="bold" letter-spacing="3" fill="{GUILDA if st == "SEMPRE" else "#2e5a3a"}">{st}</text></g>')
    css = '.it{animation:it 4s ease-in-out infinite}@keyframes it{0%,100%{opacity:1}8%{opacity:.55}16%{opacity:1}}'
    salvar('treinamentos.svg', W, H, ''.join(p), css)

# ================= RODAPÉ (QUEST COMPLETE) =================
def rodape():
    W, H = 1200, 300
    p = [f'<defs>{madeira("veio")}{OURO_GRAD}'
         f'<linearGradient id="fundo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e1d11"/><stop offset="1" stop-color="#120a05"/></linearGradient>'
         f'<radialGradient id="luz" cx=".5" cy=".42" r=".55"><stop offset="0" stop-color="#ffcf6b" stop-opacity=".45"/><stop offset="1" stop-color="#ffcf6b" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="vin" cx=".5" cy=".5" r=".72"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>'
         f'<linearGradient id="fita" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b23a2a"/><stop offset=".5" stop-color="#8c2a1c"/><stop offset="1" stop-color="#5e1a10"/></linearGradient>'
         f'<linearGradient id="brilho" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="tq"><text x="600" y="150" text-anchor="middle" font-family="{SERIF}" font-size="58" font-weight="bold" letter-spacing="10">QUEST COMPLETE</text></clipPath></defs>',
         f'<rect width="{W}" height="{H}" rx="14" fill="url(#fundo)"/>',
         f'<rect width="{W}" height="{H}" rx="14" fill="#000" filter="url(#veio)"/>',
         f'<rect class="lz" width="{W}" height="{H}" fill="url(#luz)"/>']
    # raios de luz girando atrás da faixa
    raios = ''.join(f'<path d="M0 0 L{round(700*__import__("math").cos(__import__("math").radians(k*15-1.5)),1)} {round(700*__import__("math").sin(__import__("math").radians(k*15-1.5)),1)} '
                    f'L{round(700*__import__("math").cos(__import__("math").radians(k*15+1.5)),1)} {round(700*__import__("math").sin(__import__("math").radians(k*15+1.5)),1)}Z"/>' for k in range(24))
    p.append(f'<g transform="translate(600 130)"><g class="rz" fill="#ffd98a" opacity=".06">{raios}</g></g>')
    # faixa vermelha com pontas dobradas
    p.append(f'<g class="pop"><path d="M250 92 H950 L930 132 L950 172 H250 L270 132Z" fill="url(#fita)" stroke="#3e0e06" stroke-width="2"/>'
             f'<path d="M250 92 l-50 14 l22 26 l-22 26 l50 14z M950 92 l50 14 l-22 26 l22 26 l-50 14z" fill="#5e1a10" stroke="#3e0e06" stroke-width="2"/>'
             f'<path d="M262 100 H938 M262 164 H938" stroke="#f2d68a" stroke-width="1.5" opacity=".7"/>'
             f'<text x="600" y="150" text-anchor="middle" font-family="{SERIF}" font-size="58" font-weight="bold" letter-spacing="10" fill="url(#ouro)" stroke="#3e0e06" stroke-width="2" paint-order="stroke">QUEST COMPLETE</text>'
             f'<g clip-path="url(#tq)"><rect class="sh" x="200" y="90" width="150" height="80" fill="url(#brilho)"/></g></g>')
    # brilhos (estrelinhas de 4 pontas)
    for i, (x, y, d) in enumerate([(230, 70, 0), (980, 80, .7), (300, 200, 1.4), (900, 205, 2.1), (600, 62, 1.0), (1040, 150, 2.6), (160, 150, 1.8)]):
        p.append(f'<g transform="translate({x} {y})"><path class="tw" style="animation-delay:{d}s" d="M0 -12 L3 -3 L12 0 L3 3 L0 12 L-3 3 L-12 0 L-3 -3Z" fill="#fff3c4"/></g>')
    p.append(f'<text x="600" y="232" text-anchor="middle" font-family="{SERIF}" font-size="30" font-style="italic" font-weight="bold" fill="#f2d68a">Happy hunting!</text>')
    p.append(f'<text x="600" y="262" text-anchor="middle" font-family="{SERIF}" font-size="16" letter-spacing="2" fill="#c8b48e">obrigado pela visita · nos vemos na próxima caçada</text>')
    p.append(brasas(W, H, 22, H + 4))
    p.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#vin)"/>')
    css = (CSS_BRASA +
           '.rz{animation:rz 40s linear infinite}@keyframes rz{to{transform:rotate(360deg)}}'
           '.lz{animation:lz 3s ease-in-out infinite}@keyframes lz{50%{opacity:.6}}'
           '.pop{transform-origin:600px 132px;animation:pop 6s cubic-bezier(.2,1.4,.4,1) infinite}@keyframes pop{0%{transform:scale(.6);opacity:0}8%{transform:scale(1.04);opacity:1}14%,100%{transform:scale(1);opacity:1}}'
           '.sh{animation:sh 6s ease-in-out infinite}@keyframes sh{0%,20%{transform:translateX(0)}60%,100%{transform:translateX(700px)}}'
           '.tw{transform-box:fill-box;transform-origin:center;animation:tw 2.8s ease-in-out infinite}@keyframes tw{0%,100%{transform:scale(.2);opacity:0}50%{transform:scale(1);opacity:1}}')
    salvar('rodape.svg', W, H, ''.join(p), css)

guild_card()
placa_gore()
treinamentos()
titulo('t-treino.svg', 'TREINAMENTO')
titulo('t-sobre.svg', 'SOBRE MIM')
titulo('t-quests.svg', 'QUADRO DE QUESTS')
titulo('t-monstros.svg', 'MONSTROS FAVORITOS')
titulo('t-equipamento.svg', 'EQUIPAMENTO')
titulo('t-registro.svg', 'REGISTRO DE CAÇADAS')
quest('quest-clawdeck.svg', 6, 'Clawdeck',
      ['Os terminais do Claude Code, o site', 'e o celular num app só'],
      'Mac · Windows · Linux', 'Quem programa com IA', 'ABERTA')
quest('quest-mhlauncher.svg', 7, 'MHLAUNCHER',
      ['Os ports de Monster Hunter no PC', 'num lugar só, em português'],
      'Windows · Linux', 'Todo caçador do Brasil', 'ABERTA', 'Lucas &amp; Ataenas')
quest('quest-neurocraft.svg', 5, 'Neurocraft',
      ['Bots que jogam Minecraft de verdade:', 'minerando, craftando e construindo'],
      'Node.js · Mineflayer · Claude', 'Servidor dos amigos', 'PRIVADA')
quest('quest-earshare.svg', 4, 'EarShare',
      ['Vários fones tocando a mesma música,', 'cada um com o seu volume e equalizador'],
      'macOS · Swift', 'Quem divide o som', 'PRIVADA')
rodape()
