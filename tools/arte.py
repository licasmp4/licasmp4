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
def guild_card():
    W, H = 1200, 400
    p = [f'<defs>{defs_papel("pp")}<linearGradient id="fundo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{MADEIRA}"/><stop offset="1" stop-color="#160e08"/></linearGradient>'
         f'<radialGradient id="fogo" cx=".5" cy="1" r=".7"><stop offset="0" stop-color="#ff8a2a" stop-opacity=".35"/><stop offset="1" stop-color="#ff8a2a" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="brilho" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="tit"><text x="600" y="92" text-anchor="middle" font-family="{SERIF}" font-size="40" font-weight="bold" letter-spacing="10">GUILD CARD</text></clipPath></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#fundo)"/>']
    # tábuas de madeira
    for y in range(0, H, 50):
        p.append(f'<rect x="0" y="{y}" width="{W}" height="2" fill="#000" opacity=".35"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#fogo)" class="fg"/>')
    # o cartão
    cx, cy, cw, ch = 110, 34, 980, 330
    p.append(f'<rect x="{cx+8}" y="{cy+10}" width="{cw}" height="{ch}" fill="#000" opacity=".45"/>')
    p.append(f'<g filter="url(#pp)"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="url(#ppv)"/></g>')
    p.append(f'<rect x="{cx+14}" y="{cy+14}" width="{cw-28}" height="{ch-28}" fill="none" stroke="{TINTA2}" stroke-width="2"/>')
    p.append(f'<rect x="{cx+20}" y="{cy+20}" width="{cw-40}" height="{ch-40}" fill="none" stroke="{TINTA2}" stroke-width="1"/>')
    # título com brilho passando
    p.append(f'<text x="600" y="92" text-anchor="middle" font-family="{SERIF}" font-size="40" font-weight="bold" letter-spacing="10" fill="{TINTA}">GUILD CARD</text>')
    p.append(f'<g clip-path="url(#tit)"><rect class="sh" x="-200" y="50" width="160" height="60" fill="url(#brilho)"/></g>')
    p.append(f'<path d="M370 110 H830" stroke="{TINTA2}" stroke-width="1.5"/><path d="M590 110 l10 -6 l10 6 l-10 6z" fill="{GUILDA}"/>')
    # brasão
    p.append(f'<g class="bz">{brasao(270, 225, 1.25)}</g>')
    # campos
    campos = [('Caçador', 'Lucas Luiz  ·  licas.mp3'),
              ('Formação', 'Full Stack Python — Projeto Farol'),
              ('Cursos', 'Java Full Stack (EBAC) · IA (SENAI)'),
              ('Caçadas', 'MHGU · MH4U · MHP3rd · MHFU')]
    for i, (k, v) in enumerate(campos):
        y = 160 + i * 46
        p.append(f'<text x="430" y="{y}" font-family="{SERIF}" font-size="17" font-style="italic" fill="{TINTA2}">{k}</text>')
        p.append(f'<text x="560" y="{y}" font-family="{SERIF}" font-size="22" fill="{TINTA}">{v}</text>')
        p.append(f'<path d="M560 {y+10} H1040" stroke="{TINTA2}" stroke-width=".8" stroke-dasharray="2 4" opacity=".7"/>')
    # selo de cera
    p.append(f'<g transform="translate(1010 300)"><g class="selo"><circle r="34" fill="{GUILDA}"/><circle r="27" fill="none" stroke="#5e1a10" stroke-width="2"/>'
             f'<path d="M-30 -10 q-10 4 -8 14 M30 12 q10 -2 8 -12 M-8 32 q4 10 14 6" stroke="{GUILDA}" stroke-width="7" stroke-linecap="round" fill="none"/>'
             f'<text y="9" text-anchor="middle" font-family="{SERIF}" font-size="26" font-weight="bold" fill="#e9b9a8">L</text></g></g>')
    p.append(brasas(W, H, 26, H + 4))
    css = (CSS_BRASA +
           '.sh{animation:sh 5s ease-in-out infinite}@keyframes sh{0%,40%{transform:translateX(0)}100%{transform:translateX(1100px)}}'
           '.fg{animation:fg 2.6s ease-in-out infinite}@keyframes fg{50%{opacity:.6}}'
           '.selo{transform-box:fill-box;transform-origin:center;animation:selo 6s ease-in-out infinite}@keyframes selo{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(-2deg)}}'
           '.bz{animation:bz 4s ease-in-out infinite}@keyframes bz{50%{opacity:.85}}')
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

# ================= RODAPÉ =================
def rodape():
    W, H = 900, 150
    p = [f'<defs><radialGradient id="f" cx=".5" cy=".9" r=".6"><stop offset="0" stop-color="#ff8a2a" stop-opacity=".45"/><stop offset="1" stop-color="#ff8a2a" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" rx="10" fill="{MADEIRA}"/>',
         f'<rect width="{W}" height="{H}" rx="10" fill="url(#f)" class="fg"/>',
         f'<text x="{W//2}" y="64" text-anchor="middle" font-family="{SERIF}" font-size="34" font-style="italic" font-weight="bold" fill="{OURO2}">Happy hunting!</text>',
         f'<text x="{W//2}" y="96" text-anchor="middle" font-family="{SERIF}" font-size="16" fill="#c8b48e">nos vemos na próxima caçada</text>',
         brasas(W, H, 14, H + 4)]
    css = CSS_BRASA + '.fg{animation:fg 2.6s ease-in-out infinite}@keyframes fg{50%{opacity:.55}}'
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
