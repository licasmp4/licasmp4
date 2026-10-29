# Gera as artes animadas (SVG pixel art) do README do perfil.
# Uso: python3 tools/pixel.py  → escreve em assets/
import os, random

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(OUT, exist_ok=True)

BG, NOITE, ROXO = '#07060b', '#120a1f', '#2a1240'
ROSA, CIANO, SANGUE, OSSO, VIOLETA = '#ff2e88', '#3cf0ff', '#b3123a', '#e8e0f0', '#8a5cff'

# ---------- fonte pixel 5x7 ----------
F = {
'A':'01110 10001 10001 11111 10001 10001 10001','B':'11110 10001 10001 11110 10001 10001 11110',
'C':'01111 10000 10000 10000 10000 10000 01111','D':'11110 10001 10001 10001 10001 10001 11110',
'E':'11111 10000 10000 11110 10000 10000 11111','F':'11111 10000 10000 11110 10000 10000 10000',
'G':'01111 10000 10000 10011 10001 10001 01111','H':'10001 10001 10001 11111 10001 10001 10001',
'I':'11111 00100 00100 00100 00100 00100 11111','J':'00111 00010 00010 00010 00010 10010 01100',
'K':'10001 10010 10100 11000 10100 10010 10001','L':'10000 10000 10000 10000 10000 10000 11111',
'M':'10001 11011 10101 10101 10001 10001 10001','N':'10001 11001 10101 10011 10001 10001 10001',
'O':'01110 10001 10001 10001 10001 10001 01110','P':'11110 10001 10001 11110 10000 10000 10000',
'Q':'01110 10001 10001 10001 10101 10010 01101','R':'11110 10001 10001 11110 10100 10010 10001',
'S':'01111 10000 10000 01110 00001 00001 11110','T':'11111 00100 00100 00100 00100 00100 00100',
'U':'10001 10001 10001 10001 10001 10001 01110','V':'10001 10001 10001 10001 10001 01010 00100',
'W':'10001 10001 10001 10101 10101 10101 01010','X':'10001 10001 01010 00100 01010 10001 10001',
'Y':'10001 10001 01010 00100 00100 00100 00100','Z':'11111 00001 00010 00100 01000 10000 11111',
'0':'01110 10011 10101 10101 10101 11001 01110','1':'00100 01100 00100 00100 00100 00100 01110',
'2':'01110 10001 00001 00010 00100 01000 11111','3':'11110 00001 00001 01110 00001 00001 11110',
'4':'00010 00110 01010 10010 11111 00010 00010','5':'11111 10000 11110 00001 00001 10001 01110',
'6':'01110 10000 10000 11110 10001 10001 01110','7':'11111 00001 00010 00100 01000 01000 01000',
'8':'01110 10001 10001 01110 10001 10001 01110','9':'01110 10001 10001 01111 00001 00001 01110',
'.':'00000 00000 00000 00000 00000 01100 01100','!':'00100 00100 00100 00100 00100 00000 00100',
'-':'00000 00000 00000 01110 00000 00000 00000',':':'00000 01100 01100 00000 01100 01100 00000',
'/':'00001 00010 00010 00100 01000 01000 10000','?':'01110 10001 00001 00010 00100 00000 00100',
"'":'00100 00100 01000 00000 00000 00000 00000',' ':'00000 00000 00000 00000 00000 00000 00000',
'>':'01000 00100 00010 00001 00010 00100 01000','_':'00000 00000 00000 00000 00000 00000 11111',
'+':'00000 00100 00100 11111 00100 00100 00000','·':'00000 00000 00000 00100 00000 00000 00000',
'Ç':'01111 10000 10000 10000 10000 10000 01111 00100 01100','Ã':'01101 10010 01110 10001 10001 11111 10001 10001 10001',
'Õ':'01101 10010 01110 10001 10001 10001 10001 10001 01110','É':'00010 00100 11111 10000 10000 11110 10000 10000 11111',
'Ó':'00010 00100 01110 10001 10001 10001 10001 10001 01110','Á':'00010 00100 01110 10001 10001 11111 10001 10001 10001',
'@':'01110 10001 10111 10101 10111 10000 01111','~':'00000 00000 01000 10101 00010 00000 00000',
}

def runs(rows):
    """[(x,y,w)] juntando pixels vizinhos na horizontal."""
    out = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            if row[x] == '1':
                s = x
                while x < len(row) and row[x] == '1': x += 1
                out.append((s, y, x - s))
            else:
                x += 1
    return out

def texto(t, x, y, s, cor, extra='', esp=1):
    """Texto em pixel: s = tamanho do pixel."""
    rs, cx = [], x
    for ch in t.upper():
        g = F.get(ch, F['?']).split()
        topo = -2 if len(g) == 9 and ch != 'Ç' else 0  # acento em cima sobe 2 linhas
        for gx, gy, w in runs(g):
            rs.append(f'<rect x="{cx+gx*s}" y="{y+(gy+topo)*s}" width="{w*s}" height="{s}"/>')
        cx += (5 + esp) * s
    return f'<g fill="{cor}" {extra}>' + ''.join(rs) + '</g>'

def largura(t, s, esp=1):
    return len(t) * (5 + esp) * s - esp * s

def sprite(arte, x, y, s, paleta, extra=''):
    """arte: linhas de caracteres; cada caractere aponta para uma cor da paleta ('.' = vazio)."""
    rs = []
    for gy, row in enumerate(arte):
        gx = 0
        while gx < len(row):
            c = row[gx]
            if c in paleta:
                s0 = gx
                while gx < len(row) and row[gx] == c: gx += 1
                rs.append(f'<rect x="{x+s0*s}" y="{y+gy*s}" width="{(gx-s0)*s}" height="{s}" fill="{paleta[c]}"/>')
            else:
                gx += 1
    return f'<g {extra}>' + ''.join(rs) + '</g>'

def svg(w, h, corpo, css=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" shape-rendering="crispEdges">'
            f'<style>{css}</style>{corpo}</svg>')

def salvar(nome, conteudo):
    with open(os.path.join(OUT, nome), 'w') as f: f.write(conteudo)
    print(nome, len(conteudo) // 1024, 'KB')

random.seed(7)
FONTE_MONO = "ui-monospace,'SF Mono',Menlo,Consolas,'Courier New',monospace"

# ================= BANNER =================
def banner():
    W, H = 1200, 340
    p = []
    p.append(f'<defs><linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG}"/><stop offset=".6" stop-color="{NOITE}"/><stop offset="1" stop-color="#2b0d2e"/></linearGradient>'
             f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".35"/></pattern></defs>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#ceu)"/>')
    # estrelas piscando
    for i in range(70):
        x, y = random.randrange(0, W, 4), random.randrange(0, 200, 4)
        d = random.choice([2, 3, 4, 5]); b = round(random.random() * 4, 1)
        cor = random.choice([OSSO, OSSO, CIANO, ROSA])
        p.append(f'<rect class="tw" style="animation-duration:{d}s;animation-delay:{b}s" x="{x}" y="{y}" width="4" height="4" fill="{cor}"/>')
    # lua pixel
    lua = ['....XXXXXX....', '..XXXXXXXXXX..', '.XXXXXXXXXXXX.', '.XXXXXXXXXXOX.', 'XXXXXXXXXXXXXX', 'XXXOXXXXXXXXXX',
           'XXXXXXXXXXXXXX', 'XXXXXXXOXXXXXX', 'XXXXXXXXXXXXXX', '.XXXXXXXXXXXX.', '.XXOXXXXXXXXX.', '..XXXXXXXXXX..', '....XXXXXX....']
    p.append(f'<circle cx="1004" cy="96" r="88" fill="{ROSA}" opacity=".10" class="glow"/>')
    p.append(sprite(lua, 948, 40, 8, {'X': '#f3d9e6', 'O': '#d6a9c2'}))
    # morcegos
    asa1 = ['X.....X', 'XX.X.XX', '.XXXXX.', '..X.X..']
    asa2 = ['.......', '..X.X..', 'XXXXXXX', 'X.....X']
    for i, (y, dur, beg) in enumerate([(120, 14, 0), (70, 19, 6), (160, 23, 11)]):
        p.append(f'<g><animateTransform attributeName="transform" type="translate" from="-80 {y}" to="{W+80} {y-40}" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                 f'<g class="bat1">{sprite(asa1, 0, 0, 4, {"X": "#0b0710"})}</g><g class="bat2">{sprite(asa2, 0, 0, 4, {"X": "#0b0710"})}</g></g>')
    # silhueta gótica (catedral + prédios)
    sky = []
    def pinaculo(x, w, h, alt):
        base = H - 40
        sky.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h+40}"/>')
        n = w // 8
        for k in range(n):
            ww = w - k * 8
            if ww <= 0: break
            sky.append(f'<rect x="{x+k*4}" y="{base-h-(k+1)*alt}" width="{ww}" height="{alt}"/>')
        sky.append(f'<rect x="{x+w//2-2}" y="{base-h-(n+1)*alt-16}" width="4" height="16"/>')
    pinaculo(40, 48, 90, 10); pinaculo(100, 32, 60, 8); sky.append(f'<rect x="0" y="{H-80}" width="240" height="80"/>')
    pinaculo(250, 64, 140, 12); pinaculo(330, 40, 100, 10); pinaculo(206, 40, 100, 10)
    sky.append(f'<rect x="196" y="{H-110}" width="190" height="110"/>')
    for x, h in [(400, 70), (440, 120), (500, 90), (560, 150), (620, 80), (700, 110), (760, 60), (820, 130), (880, 90), (930, 70)]:
        sky.append(f'<rect x="{x}" y="{H-40-h}" width="{random.choice([40,48,56])}" height="{h+40}"/>')
    pinaculo(990, 56, 120, 12); pinaculo(1060, 40, 80, 10); pinaculo(1110, 64, 150, 12)
    sky.append(f'<rect x="980" y="{H-90}" width="220" height="90"/>')
    p.append(f'<g fill="#0a0710">{"".join(sky)}</g>')
    # janelas acesas
    for i in range(46):
        x = random.choice(list(range(10, 1190, 8)))
        y = random.randrange(H - 150, H - 50, 8)
        cor = random.choice([ROSA, CIANO, '#ffb3d1', VIOLETA])
        d = random.choice([3, 5, 7, 9]); b = round(random.random() * 6, 1)
        p.append(f'<rect class="win" style="animation-duration:{d}s;animation-delay:{b}s" x="{x}" y="{y}" width="4" height="8" fill="{cor}"/>')
    # rosácea da catedral
    ros = ['..XXX..', '.XOXOX.', 'XOXCXOX', 'XXCCCXX', 'XOXCXOX', '.XOXOX.', '..XXX..']
    p.append(sprite(ros, 268, H - 122, 4, {'X': '#3a1450', 'O': ROSA, 'C': CIANO}, 'class="glow"'))
    # chuva
    chuva = []
    for i in range(60):
        x = random.randrange(0, W, 4); y = random.randrange(-H, H, 4)
        chuva.append(f'<rect x="{x}" y="{y}" width="2" height="{random.choice([12,16,20])}"/>')
    p.append(f'<g fill="{CIANO}" opacity=".18"><animateTransform attributeName="transform" type="translate" from="0 0" to="-40 {H}" dur="1.6s" repeatCount="indefinite"/>{"".join(chuva)}</g>')
    p.append(f'<g fill="{CIANO}" opacity=".18" transform="translate(0 -{H})"><animateTransform attributeName="transform" type="translate" from="40 -{H}" to="0 0" dur="1.6s" repeatCount="indefinite"/>{"".join(chuva)}</g>')
    # nome com glitch
    nome, s = 'LICAS.MP3', 11
    nx = (W - largura(nome, s)) // 2 - 120
    ny = 70
    p.append(texto(nome, nx - 4, ny, s, CIANO, 'class="gC" opacity=".85"'))
    p.append(texto(nome, nx + 4, ny, s, ROSA, 'class="gR" opacity=".85"'))
    p.append(texto(nome, nx, ny, s, OSSO, 'class="gM"'))
    sub = 'DEV · ROM HACKER · CAÇADOR'
    p.append(texto(sub, nx + 4, ny + 7 * s + 26, 3, '#c9b8d8'))
    p.append(f'<rect class="cur" x="{nx + 4 + largura(sub, 3) + 8}" y="{ny + 7*s + 26}" width="10" height="21" fill="{ROSA}"/>')
    # chão + névoa
    p.append(f'<rect x="0" y="{H-40}" width="{W}" height="40" fill="#0a0710"/>')
    p.append(f'<rect x="0" y="{H-44}" width="{W}" height="4" fill="{ROSA}" opacity=".55" class="glow"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    css = ('.tw{animation:tw 3s steps(2) infinite}@keyframes tw{50%{opacity:.15}}'
           '.win{animation:win 5s steps(1) infinite}@keyframes win{0%,70%{opacity:1}71%,85%{opacity:.1}86%{opacity:1}}'
           '.glow{animation:gl 4s ease-in-out infinite}@keyframes gl{50%{opacity:.45}}'
           '.cur{animation:cur 1s steps(1) infinite}@keyframes cur{50%{opacity:0}}'
           '.bat1{animation:b1 .4s steps(1) infinite}.bat2{animation:b2 .4s steps(1) infinite}'
           '@keyframes b1{50%{opacity:0}}@keyframes b2{0%{opacity:0}50%{opacity:1}}'
           '.gC{animation:gc 3.2s steps(1) infinite}.gR{animation:gr 3.2s steps(1) infinite}.gM{animation:gm 3.2s steps(1) infinite}'
           '@keyframes gc{0%,88%,100%{transform:translate(0,0)}90%{transform:translate(-10px,3px)}94%{transform:translate(8px,-2px)}}'
           '@keyframes gr{0%,88%,100%{transform:translate(0,0)}90%{transform:translate(10px,-3px)}94%{transform:translate(-8px,2px)}}'
           '@keyframes gm{0%,89%,100%{opacity:1}91%{opacity:.4}93%{opacity:1}95%{opacity:.6}}')
    salvar('banner.svg', svg(W, H, ''.join(p), css))

# ================= TÍTULOS DE SEÇÃO =================
def titulo(nome, t, icone, cores):
    s = 5
    w = largura(t, s) + 110
    H = 56
    p = []
    p.append(sprite(icone, 0, 8, 5, cores, 'class="bob"'))
    p.append(texto(t, 62 + 3, 10 + 3, s, ROSA, 'opacity=".55"'))
    p.append(texto(t, 62, 10, s, OSSO, 'class="fl"'))
    p.append(f'<rect x="62" y="{10+7*s+6}" width="{largura(t,s)}" height="3" fill="{ROSA}" class="ln"/>')
    css = ('.bob{animation:bob 1.6s steps(2) infinite}@keyframes bob{50%{transform:translateY(-4px)}}'
           '.fl{animation:fl 6s steps(1) infinite}@keyframes fl{0%,94%,100%{opacity:1}95%{opacity:.3}97%{opacity:1}98%{opacity:.5}}'
           '.ln{transform-origin:62px 0;animation:ln 3s ease-in-out infinite}@keyframes ln{0%,100%{transform:scaleX(.25)}50%{transform:scaleX(1)}}')
    salvar(nome, svg(w, H, ''.join(p), css))

CAVEIRA = ['.XXXXXX.', 'XXXXXXXX', 'XOOXXOOX', 'XOOXXOOX', 'XXXXXXXX', '.XX..XX.', '.X.XX.X.', '..XXXX..']
CORACAO = ['.XX.XX.', 'XXXXXXX', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...']
ESPADA = ['......X', '.....XX', '....XX.', 'X..XX..', '.XXX...', '..XX...', '.X..X..', 'X......']
RAIO = ['...XX', '..XX.', '.XX..', 'XXXXX', '..XX.', '.XX..', 'XX...']

# ================= TERMINAL (sobre mim) =================
def terminal():
    W, H = 860, 300
    linhas = [
        ('$ whoami', ROSA),
        ('lucas gonzaga luiz · licas.mp3 · bauru/sp', OSSO),
        ('$ cat sobre.txt', ROSA),
        ('estudante de ADS · dev de apps, sites e ferramentas com IA', OSSO),
        ('traduzo jogos pra pt-BR (MH4U, MHGU, Banquet for Fools)', OSSO),
        ('áudio hi-res, hardware, linux e streams na twitch', OSSO),
        ('$ status', ROSA),
        ('caçando bugs com a greatsword nas costas_', CIANO),
    ]
    p = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="0" fill="{BG}" stroke="{ROXO}" stroke-width="2"/>',
         f'<rect x="1" y="1" width="{W-2}" height="34" fill="{NOITE}"/>',
         f'<rect x="1" y="35" width="{W-2}" height="2" fill="{ROSA}" opacity=".6"/>']
    for i, c in enumerate([SANGUE, VIOLETA, CIANO]):
        p.append(f'<rect x="{18+i*22}" y="12" width="12" height="12" fill="{c}"/>')
    p.append(texto('LICAS@ABISMO: ~', W // 2 - largura('LICAS@ABISMO: ~', 2) // 2, 11, 2, '#8d7aa3'))
    t = 0.4
    for i, (l, cor) in enumerate(linhas):
        y = 70 + i * 28
        n = len(l); dur = max(0.5, n * 0.035)
        p.append(f'<clipPath id="c{i}"><rect x="24" y="{y-20}" width="0" height="28"><animate attributeName="width" from="0" to="{W}" dur="{dur:.2f}s" begin="{t:.2f}s" fill="freeze" calcMode="discrete" values="{";".join(str(int(W*k/n)) for k in range(n+1))}" keyTimes="{";".join(f"{k/n:.4f}" for k in range(n+1))}"/></rect></clipPath>')
        p.append(f'<text clip-path="url(#c{i})" x="24" y="{y}" font-family="{FONTE_MONO}" font-size="17" fill="{cor}">{l}</text>')
        t += dur + (0.5 if l.startswith('$') else 0.25)
    p.append(f'<rect class="cur" x="{24 + 0}" y="{70 + 7*28 + 8}" width="10" height="4" fill="{CIANO}"/>')
    p.append(f'<pattern id="sc" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1" fill="#000" opacity=".3"/></pattern><rect width="{W}" height="{H}" fill="url(#sc)"/>')
    css = '.cur{animation:cur 1s steps(1) infinite}@keyframes cur{50%{opacity:0}}'
    salvar('terminal.svg', svg(W, H, ''.join(p), css))

# ================= DIVISOR (batimento) =================
def divisor():
    W, H = 1200, 40
    pts = []
    x = 0
    seg = [(0, 0)] * 6 + [(0, -4), (0, 4), (0, -14), (0, 12), (0, -2)] + [(0, 0)] * 9
    ys = []
    for i in range(0, W // 8 + 1):
        dy = seg[i % len(seg)][1]
        ys.append(20 + dy)
    rects = ''.join(f'<rect x="{i*8}" y="{min(ys[i], ys[i-1] if i else ys[i])}" width="8" height="{abs(ys[i]-(ys[i-1] if i else ys[i]))+3}"/>' for i in range(len(ys)))
    p = [f'<g fill="{ROSA}" opacity=".25">{rects}</g>',
         f'<clipPath id="v"><rect x="-240" y="0" width="240" height="{H}"><animate attributeName="x" from="-240" to="{W}" dur="3.2s" repeatCount="indefinite"/></rect></clipPath>',
         f'<g fill="{ROSA}" clip-path="url(#v)">{rects}</g>']
    salvar('divisor.svg', svg(W, H, ''.join(p)))

# ================= CARDS DE PROJETO =================
CLAWD = ['..OOOOOOOO..', '..OOOOOOOO..', 'OOOKOOOOKOOO', 'OOOKOOOOKOOO', '..OOOOOOOO..', '..OOOOOOOO..', '..O.O..O.O..', '..O.O..O.O..']
WYVERN = ['.....X......X', '....XX.....XX', '...XXXXXXXXX.', '..XXXXXXXXXX.', '.XXOOXXXXXXX.', 'XXXOOXXXXXXX.', 'XXXXXXXXXXX..',
          'XXXXXXXXXX...', '.XWXWXWXX....', '..XXXXXX.....', '...XXXX......']
CEREBRO = ['...PPPPPP...', '.PPLPPLPPPP.', 'PPLPPPPLPPLP', 'PLPPLPPPPLPP', 'PPPLPPLPPPPP', 'PLPPPPPLPPLP', '.PPLPPPPPLP.',
           '..PPPP.PPP..', '......PP....', '......PP....']
FONE = ['...XXXXXX...', '..XX....XX..', '.XX......XX.', '.X........X.', 'XX........XX', 'X..........X', 'PPP......PPP',
        'PPP......PPP', 'PPP......PPP', '.P........P.']

def card(nome, titulo_, linhas, tags, arte, paleta, acento, privado=False, extra_arte=''):
    W, H = 580, 220
    p = [f'<rect x="2" y="2" width="{W-4}" height="{H-4}" fill="{BG}"/>',
         f'<rect x="2" y="2" width="{W-4}" height="{H-4}" fill="none" stroke="{ROXO}" stroke-width="4"/>',
         f'<rect x="2" y="2" width="{W-4}" height="{H-4}" fill="none" stroke="{acento}" stroke-width="4" stroke-dasharray="24 300" class="run"/>']
    # cantos pixel
    for cx, cy in [(0, 0), (W - 12, 0), (0, H - 12), (W - 12, H - 12)]:
        p.append(f'<rect x="{cx}" y="{cy}" width="12" height="12" fill="{acento}"/>')
    # moldura do ícone
    p.append(f'<rect x="26" y="26" width="128" height="128" fill="{NOITE}" stroke="{ROXO}" stroke-width="2"/>')
    p.append(f'<rect x="26" y="146" width="128" height="8" fill="{acento}" opacity=".35" class="glow"/>')
    s = 8
    aw, ah = len(arte[0]) * s, len(arte) * s
    p.append(sprite(arte, 26 + (128 - aw) // 2, 26 + (128 - ah) // 2, s, paleta, 'class="bob"'))
    p.append(extra_arte)
    p.append(texto(titulo_, 178 + 3, 30 + 3, 4, acento, 'opacity=".5"'))
    p.append(texto(titulo_, 178, 30, 4, OSSO))
    for i, l in enumerate(linhas):
        p.append(f'<text x="178" y="{96 + i*24}" font-family="{FONTE_MONO}" font-size="16" fill="#cdbfdc">{l}</text>')
    x = 178
    for t in tags:
        w = len(t) * 9 + 20
        p.append(f'<rect x="{x}" y="164" width="{w}" height="26" fill="{NOITE}" stroke="{acento}" stroke-width="2"/>')
        p.append(f'<text x="{x+10}" y="182" font-family="{FONTE_MONO}" font-size="13" fill="{acento}">{t}</text>')
        x += w + 8
    if privado:
        p.append(f'<rect x="{W-120}" y="26" width="96" height="24" fill="{SANGUE}"/>')
        p.append(texto('PRIVADO', W - 114, 31, 2, OSSO))
    css = ('.run{animation:run 4s linear infinite}@keyframes run{to{stroke-dashoffset:-1592}}'
           '.bob{animation:bob 1.2s steps(2) infinite}@keyframes bob{50%{transform:translateY(-6px)}}'
           '.glow{animation:gl 2.4s ease-in-out infinite}@keyframes gl{50%{opacity:.1}}'
           '.nota{animation:nota 2.4s ease-out infinite}@keyframes nota{0%{transform:translateY(0);opacity:0}20%{opacity:1}100%{transform:translateY(-40px);opacity:0}}'
           '.pisca{animation:pi 1.8s steps(1) infinite}@keyframes pi{50%{opacity:.2}}')
    salvar(nome, svg(W, H, ''.join(p), css))

NOTA = ['..XX', '..X.', '..X.', 'XXX.', 'XX..']
FAISCA = ['.X.', 'XXX', '.X.']

# ================= CENA MONSTER HUNTER =================
def mh():
    W, H = 1200, 300
    p = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    for i in range(40):
        x, y = random.randrange(0, W, 4), random.randrange(0, 150, 4)
        p.append(f'<rect class="tw" style="animation-delay:{round(random.random()*3,1)}s" x="{x}" y="{y}" width="4" height="4" fill="{OSSO}" opacity=".7"/>')
    # olhos do monstro na mata
    for (x, y, d) in [(150, 150, 0), (990, 130, 2.5), (1080, 175, 5)]:
        p.append(f'<g class="olho" style="animation-delay:{d}s"><rect x="{x}" y="{y}" width="12" height="8" fill="{SANGUE}"/><rect x="{x+28}" y="{y}" width="12" height="8" fill="{SANGUE}"/>'
                 f'<rect x="{x+4}" y="{y+2}" width="4" height="4" fill="#ffd0d8"/><rect x="{x+32}" y="{y+2}" width="4" height="4" fill="#ffd0d8"/></g>')
    # árvores góticas
    arv = []
    for x in range(0, W, 56):
        h = random.choice([120, 150, 180, 140])
        arv.append(f'<rect x="{x+24}" y="{H-40-h}" width="12" height="{h}"/>')
        for k in range(5):
            ww = 56 - k * 10
            arv.append(f'<rect x="{x+30-ww//2}" y="{H-40-h+k*14+10}" width="{ww}" height="10"/>')
    p.append(f'<g fill="#0e0918" opacity=".95">{"".join(arv)}</g>')
    p.append(f'<rect x="0" y="{H-40}" width="{W}" height="40" fill="#0a0710"/>')
    # fogueira + carne no espeto
    cx, by = W // 2, H - 40
    p.append(f'<ellipse cx="{cx}" cy="{by}" rx="160" ry="22" fill="{ROSA}" opacity=".12" class="glow"/>')
    lenha = ['XXX......XXX', '.XXXX..XXXX.', '...XXXXXX...']
    p.append(sprite(lenha, cx - 48, by - 24, 8, {'X': '#4a2a22'}))
    chama1 = ['....X.....', '...XX..X..', '..XYX.XX..', '.XYYXXYX..', '.XYWYYYX..', 'XYYWWYYYX.', 'XYWWWWYYX.', '.XYWWWYX..']
    chama2 = ['.....X....', '..X..XX...', '..XX.XYX..', '..XYXXYYX.', '..XYYYWYX.', '.XYYYWWYYX', '.XYYWWWWYX', '..XYWWWYX.']
    pal = {'X': SANGUE, 'Y': ROSA, 'W': '#ffd6e8'}
    p.append(sprite(chama1, cx - 40, by - 88, 8, pal, 'class="f1"'))
    p.append(sprite(chama2, cx - 40, by - 88, 8, pal, 'class="f2"'))
    # espeto
    p.append(f'<rect x="{cx-120}" y="{by-118}" width="8" height="94" fill="#3a2a2e"/><rect x="{cx+112}" y="{by-118}" width="8" height="94" fill="#3a2a2e"/>')
    p.append(f'<rect x="{cx-128}" y="{by-122}" width="256" height="6" fill="#6b5560"/>')
    carne_crua = ['..RRRRRR..', '.RRRRRRRR.', 'RRRRRRRRRB', 'RRRRRRRRBB', '.RRRRRRRB.', '..RRRRR...']
    carne_ok = ['..MMMMMM..', '.MMNMMNMM.', 'MMMMMMMMMB', 'MMNMMMMMBB', '.MMMMMNMB.', '..MMMMM...']
    osso = ['XX', 'XX']
    p.append(f'<g class="assa"><g class="cru">{sprite(carne_crua, cx-40, by-140, 8, {"R": "#c2405b", "B": OSSO})}</g>'
             f'<g class="ok">{sprite(carne_ok, cx-40, by-140, 8, {"M": "#8a4a2a", "N": "#c27a3a", "B": OSSO})}</g></g>')
    p.append(sprite(osso, cx - 56, by - 124, 8, {'X': OSSO}))
    # faíscas
    for i in range(10):
        x = cx - 40 + random.randrange(0, 80, 4)
        p.append(f'<rect class="fa" style="animation-delay:{round(i*0.3,1)}s" x="{x}" y="{by-90}" width="4" height="4" fill="{ROSA}"/>')
    # greatsword fincada
    gs = ['..XX..', '..XX..', 'GGGGGG', '..HH..', '..HH..', '.SSSS.', '.SWWS.', '.SWWS.', '.SWWS.', '.SWWS.', '.SWWS.', '.SWWS.', '.SWWS.', '.SWWS.', '.SWWS.', '..SS..']
    p.append(sprite(gs, cx + 220, by - 120, 8, {'X': '#3a2a2e', 'G': VIOLETA, 'H': '#5a3a40', 'S': '#8f8aa0', 'W': '#d8d4e6'}))
    p.append(f'<rect x="{cx+228}" y="{by-128}" width="32" height="8" fill="{CIANO}" opacity=".5" class="glow"/>')
    # texto
    t = 'SO TASTY!'
    p.append(f'<g class="pop">{texto(t, cx - largura(t, 6)//2 + 3, 30 + 3, 6, SANGUE)}{texto(t, cx - largura(t, 6)//2, 30, 6, OSSO)}</g>')
    sub = 'BANQUETE DEPOIS DA CAÇADA'
    p.append(texto(sub, cx - largura(sub, 2) // 2, 92, 2, '#8d7aa3'))
    css = ('.tw{animation:tw 3s steps(2) infinite}@keyframes tw{50%{opacity:.1}}'
           '.olho{animation:ol 7s steps(1) infinite}@keyframes ol{0%,8%{opacity:1}9%,11%{opacity:0}12%,60%{opacity:1}61%,100%{opacity:0}}'
           '.glow{animation:gl 1.6s ease-in-out infinite}@keyframes gl{50%{opacity:.04}}'
           '.f1{animation:f1 .5s steps(1) infinite}.f2{animation:f2 .5s steps(1) infinite}@keyframes f1{50%{opacity:0}}@keyframes f2{0%{opacity:0}50%{opacity:1}}'
           '.cru{animation:cru 6s steps(1) infinite}.ok{animation:ok 6s steps(1) infinite}@keyframes cru{0%,59%{opacity:1}60%,100%{opacity:0}}@keyframes ok{0%,59%{opacity:0}60%,100%{opacity:1}}'
           '.assa{animation:assa .9s steps(2) infinite}@keyframes assa{50%{transform:translateY(-4px)}}'
           '.fa{animation:fa 2.4s steps(6) infinite}@keyframes fa{0%{transform:translateY(0);opacity:1}100%{transform:translateY(-110px);opacity:0}}'
           '.pop{animation:pop 6s steps(1) infinite}@keyframes pop{0%,59%{opacity:0}60%,100%{opacity:1}}')
    salvar('monster-hunter.svg', svg(W, H, ''.join(p), css))

# ================= RODAPÉ (stamina) =================
def rodape():
    W, H = 1200, 110
    t = 'RECUPERANDO STAMINA PRO PRÓXIMO COMMIT'
    p = [texto(t, (W - largura(t, 3)) // 2, 14, 3, '#8d7aa3')]
    bx, bw = 300, 600
    p.append(f'<rect x="{bx-4}" y="58" width="{bw+8}" height="28" fill="{NOITE}" stroke="{ROXO}" stroke-width="4"/>')
    seg = ''.join(f'<rect x="{bx + i*20}" y="62" width="16" height="20"/>' for i in range(bw // 20))
    p.append(f'<clipPath id="st"><rect x="{bx}" y="58" width="0" height="30"><animate attributeName="width" values="0;{bw};{bw}" keyTimes="0;.8;1" dur="5s" repeatCount="indefinite" calcMode="discrete"/></rect></clipPath>')
    # versão "em degraus": anima por pedaços de 20px
    n = bw // 20
    vals = ';'.join(str(min(bw, k * 20)) for k in range(n + 1)) + f';{bw};{bw}'
    kts = ';'.join(f'{0.8*k/n:.4f}' for k in range(n + 1)) + ';0.9;1'
    p[-1] = f'<clipPath id="st"><rect x="{bx}" y="58" width="0" height="30"><animate attributeName="width" values="{vals}" keyTimes="{kts}" dur="5s" repeatCount="indefinite" calcMode="discrete"/></rect></clipPath>'
    p.append(f'<g fill="#2a1a2e">{seg}</g><g fill="#ffd23c" clip-path="url(#st)">{seg}</g>')
    salvar('rodape.svg', svg(W, H, ''.join(p)))

banner()
titulo('t-sobre.svg', 'SOBRE MIM', CAVEIRA, {'X': OSSO, 'O': BG})
titulo('t-projetos.svg', 'PROJETOS', ESPADA, {'X': CIANO})
titulo('t-arsenal.svg', 'ARSENAL', RAIO, {'X': ROSA})
titulo('t-cacadas.svg', 'CAÇADAS', CORACAO, {'X': SANGUE})
titulo('t-mh.svg', 'MONSTER HUNTER', CAVEIRA, {'X': SANGUE, 'O': BG})
terminal()
divisor()
card('card-clawdeck.svg', 'CLAWDECK', ['Os terminais do Claude Code, o site', 'e o celular num app só.'],
     ['Mac', 'Windows', 'Linux', 'Electron'], CLAWD, {'O': '#d97757', 'K': '#1a0f14'}, ROSA,
     extra_arte=''.join(f'<rect class="pisca" style="animation-delay:{d}s" x="{x}" y="{y}" width="6" height="6" fill="{CIANO}"/>' for x, y, d in [(40, 40, 0), (134, 50, .6), (44, 130, 1.2)]))
card('card-mhlauncher.svg', 'MHLAUNCHER', ['Os ports de Monster Hunter no PC', 'num lugar só, em português.'],
     ['C#', 'Windows', 'Linux', 'pt-BR'], WYVERN, {'X': SANGUE, 'O': '#ffd23c', 'W': OSSO}, SANGUE,
     extra_arte=''.join(sprite(FAISCA, x, y, 4, {'X': '#ffd23c'}, f'class="pisca" style="animation-delay:{d}s"') for x, y, d in [(36, 36, 0), (130, 120, .9)]))
card('card-neurocraft.svg', 'NEUROCRAFT', ['Bots que jogam Minecraft de verdade:', 'minerando, craftando e construindo.'],
     ['Node.js', 'Mineflayer', 'Claude'], CEREBRO, {'P': ROSA, 'L': '#ffb3d1'}, CIANO, privado=True,
     extra_arte=''.join(f'<rect class="pisca" style="animation-delay:{d}s" x="{x}" y="{y}" width="4" height="4" fill="{CIANO}"/>' for x, y, d in [(48, 60, 0), (128, 70, .4), (60, 120, .8), (120, 40, 1.2)]))
card('card-earshare.svg', 'EARSHARE', ['Vários fones. Uma música.', 'Cada um do seu jeito.'],
     ['Swift', 'macOS', 'Spotify'], FONE, {'X': OSSO, 'P': VIOLETA}, VIOLETA, privado=True,
     extra_arte=''.join(sprite(NOTA, x, 100, 4, {'X': CIANO}, f'class="nota" style="animation-delay:{d}s"') for x, d in [(40, 0), (124, 1.2)]))
mh()
rodape()
