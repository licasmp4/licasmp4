# Gera as partes vivas do perfil (pager, diário dos sonhos e a parede do livro de visitas).
# Roda de hora em hora pela Action "vivo" e publica no branch "vivo".
import datetime, hashlib, json, os, sys, urllib.request
from zoneinfo import ZoneInfo

USUARIO = 'licasmp4'
REPO = 'licasmp4/licasmp4'
ISSUE_LIVRO = 1
OUT = sys.argv[1] if len(sys.argv) > 1 else 'vivo'
TOKEN = os.environ.get('GH_TOKEN', '')
MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"
SERIF = "'Times New Roman',Georgia,serif"
MAO = "'Bradley Hand','Segoe Print','Comic Sans MS',cursive"

def api(url, dados=None):
    req = urllib.request.Request(url, data=json.dumps(dados).encode() if dados else None,
                                 headers={'Authorization': f'Bearer {TOKEN}', 'User-Agent': 'licas-vivo', 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def salvar(nome, w, h, corpo, css=''):
    with open(os.path.join(OUT, nome), 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><style>{css}</style>{corpo}</svg>')

agora = datetime.datetime.now(ZoneInfo('America/Sao_Paulo'))

# ---------- dados ----------
def sinais():
    try:
        ev = api(f'https://api.github.com/users/{USUARIO}/events/public?per_page=30')
    except Exception:
        ev = []
    ultimo, repo = None, None
    for e in ev:
        if not e.get('public'):
            continue  # nunca mostrar nada de repositório privado
        t = datetime.datetime.fromisoformat(e['created_at'].replace('Z', '+00:00'))
        if ultimo is None:
            ultimo = t
        if e['type'] == 'PushEvent' and repo is None:
            repo = e['repo']['name'].split('/')[-1]
    return ultimo, repo

def sequencia():
    q = 'query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'
    try:
        d = api('https://api.github.com/graphql', {'query': q, 'variables': {'u': USUARIO}})
        cal = d['data']['user']['contributionsCollection']['contributionCalendar']
    except Exception:
        return 0, 0
    dias = [x for w in cal['weeks'] for x in w['contributionDays']]
    dias.sort(key=lambda x: x['date'])
    hoje = agora.date().isoformat()
    seq = 0
    for x in reversed(dias):
        if x['date'] > hoje:
            continue
        if x['contributionCount'] > 0:
            seq += 1
        elif x['date'] == hoje:
            continue
        else:
            break
    return seq, cal['totalContributions']

def visitantes():
    nomes = []
    try:
        pag = 1
        while True:
            cs = api(f'https://api.github.com/repos/{REPO}/issues/{ISSUE_LIVRO}/comments?per_page=100&page={pag}')
            if not cs:
                break
            for c in cs:
                login = c['user']['login']
                if c['user']['type'] == 'Bot' or login == USUARIO:
                    continue
                if login in nomes:
                    nomes.remove(login)
                nomes.append(login)
            pag += 1
    except Exception:
        pass
    return nomes[::-1]  # mais recente primeiro

# ---------- pager ----------
def pager(ultimo, repo, seq, total):
    W, H = 420, 250
    if ultimo:
        horas = (datetime.datetime.now(datetime.timezone.utc) - ultimo).total_seconds() / 3600
        sinal = 'agora mesmo' if horas < 1 else (f'há {int(horas)}h' if horas < 48 else f'há {int(horas // 24)} dias')
    else:
        sinal = 'sem sinal'
    h = agora.hour
    humor = '(-ω-) zzz' if h < 6 else '(˘ω˘)' if h < 12 else '(•ω•)' if h < 18 else '(°ω°)' if h < 22 else '(;ω;)'
    linhas = [f'{agora:%H:%M} · bauru', f'último sinal: {sinal}', f'mexendo em: {repo or "???"}',
              f'dias acordado: {seq}', f'contribuições: {total}', f'humor: {humor}']
    p = ['<defs><linearGradient id="cp" x1="0" x2="1"><stop offset="0" stop-color="#7a7e76"/><stop offset=".45" stop-color="#cfd3c6"/><stop offset="1" stop-color="#5e625a"/></linearGradient>'
         '<filter id="gl"><feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         '<clipPath id="tl"><rect x="56" y="44" width="250" height="118" rx="4"/></clipPath></defs>',
         f'<rect x="20" y="16" width="{W-40}" height="{H-32}" rx="30" fill="url(#cp)" stroke="#232622" stroke-width="3"/>',
         '<rect x="44" y="34" width="274" height="138" rx="8" fill="#151915"/>',
         '<rect x="56" y="44" width="250" height="118" rx="4" fill="#a9b8a2" class="lcd"/>']
    corpo = ''.join(f'<text x="66" y="{63 + k*18}" font-family="{MONO}" font-size="13" font-weight="bold" fill="#141a12">{esc(l)}</text>' for k, l in enumerate(linhas))
    p.append(f'<g clip-path="url(#tl)" filter="url(#gl)">{corpo}</g>')
    p.append(''.join(f'<rect x="56" y="{y}" width="250" height="1" fill="#000" opacity=".12"/>' for y in range(46, 160, 3)))
    # botões e LED
    p.append('<circle cx="352" cy="60" r="7" fill="#ff3b4f" class="led"/>')
    for k in range(3):
        p.append(f'<rect x="{340}" y="{88 + k*28}" width="34" height="18" rx="6" fill="#2a2e2a"/>')
    p.append(f'<text x="181" y="200" font-family="{MONO}" font-size="12" fill="#2a2e2a" text-anchor="middle">PAGER DO SONHO · atualiza sozinho</text>')
    css = ('.led{animation:l 1.2s steps(1) infinite}@keyframes l{50%{opacity:.2}}'
           '.lcd{animation:c 6s ease-in-out infinite}@keyframes c{0%,100%{fill:#a9b8a2}50%{fill:#98a892}}')
    salvar('pager.svg', W, H, ''.join(p), css)

# ---------- diário dos sonhos ----------
SONHOS = [
    'sonhei que o clawdeck tinha dentes. ele sorria toda vez que eu dava commit.',
    'tinha uma estátua no fim do corredor. ela não falava, só virava a cabeça devagar.',
    'acordei às 02:44 de novo. o pager tocou mas ninguém tava ligando.',
    'o gore magala tava no meu quarto. a tv ligou sozinha e mostrava minha cara.',
    'sonhei que o código compilava de primeira. aí eu soube que era sonho.',
    'as estátuas do corredor mudaram de lugar. só uma delas tava olhando pra mim.',
    'tinha uma música tocando no fone mas o fone tava na mesa.',
    'um bicho grandão de gorro dormia no meu quarto. eu deixei.',
    'eu traduzia um jogo inteiro e todas as falas diziam "boa noite".',
    'a casa da neve tinha uma janela a mais. ninguém lembrava dela.',
    'um bot do minecraft me mandou mensagem: "tô cavando pra baixo. não me espera."',
    'sonhei com a fita. no fim dela tinha eu dormindo, assistindo.',
    'o papel de parede tinha flores e as flores cantavam baixinho.',
    'pedi pra ia fazer um sonho bom. ela fez esse.',
]

def diario():
    W, H = 900, 150
    sem = agora.isocalendar()
    t = SONHOS[(sem[0] * 53 + sem[1]) % len(SONHOS)]
    data = f'{agora:%d/%m} · semana {sem[1]}'
    # quebra em linhas de ~62 caracteres
    pal, linhas, l = t.split(), [], ''
    for w in pal:
        if len(l) + len(w) > 60:
            linhas.append(l.strip()); l = ''
        l += w + ' '
    linhas.append(l.strip())
    p = [f'<rect width="{W}" height="{H}" rx="6" fill="#0c0b0d"/>',
         ''.join(f'<rect x="30" y="{56 + k*26}" width="{W-60}" height="1" fill="#cfc8bc" opacity=".08"/>' for k in range(4)),
         f'<rect x="70" y="0" width="1" height="{H}" fill="#ff3b4f" opacity=".25"/>',
         f'<text x="88" y="34" font-family="{MONO}" font-size="13" fill="#8a8478">diário dos sonhos · {esc(data)}</text>',
         f'<text x="{W-24}" y="34" font-family="{MONO}" font-size="13" fill="#ff3b4f" text-anchor="end" class="rec">● troca toda semana</text>']
    for k, l in enumerate(linhas[:3]):
        p.append(f'<text x="88" y="{76 + k*28}" font-family="{MAO}" font-size="22" fill="#e8e2d6" class="tx" style="animation-delay:{k*0.4}s">{esc(l)}</text>')
    css = ('.rec{animation:r 1.6s steps(1) infinite}@keyframes r{50%{opacity:.25}}'
           '.tx{animation:t 7s ease-in-out infinite}@keyframes t{0%,100%{opacity:1}48%{opacity:1}50%{opacity:.55}52%{opacity:1}}')
    salvar('diario.svg', W, H, ''.join(p), css)

# ---------- parede do livro de visitas ----------
def parede(nomes):
    W, H = 900, 300
    p = ['<defs><pattern id="fl" width="48" height="48" patternUnits="userSpaceOnUse">'
         '<rect width="48" height="48" fill="#2e2a22"/><rect x="0" width="6" height="48" fill="#332e24"/><rect x="24" width="6" height="48" fill="#332e24"/>'
         '<g fill="#5a3038"><rect x="10" y="8" width="5" height="5"/><rect x="6" y="12" width="5" height="5"/><rect x="14" y="12" width="5" height="5"/><rect x="10" y="16" width="5" height="5"/></g>'
         '<g fill="#3a3e46"><rect x="34" y="32" width="5" height="5"/><rect x="30" y="36" width="5" height="5"/><rect x="38" y="36" width="5" height="5"/><rect x="34" y="40" width="5" height="5"/></g>'
         '</pattern><radialGradient id="vn" cx=".5" cy=".5" r=".75"><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#fl)"/>',
         f'<rect x="300" y="0" width="14" height="{H}" fill="#2a1a10" opacity=".35"/>']
    if not nomes:
        p.append(f'<text x="{W/2}" y="{H/2}" font-family="{MAO}" font-size="30" fill="#d0343f" text-anchor="middle" transform="rotate(-3 {W/2} {H/2})">ninguém assinou ainda.</text>')
        p.append(f'<text x="{W/2}" y="{H/2 + 40}" font-family="{MAO}" font-size="22" fill="#d0343f" text-anchor="middle" transform="rotate(-2 {W/2} {H/2})">seja o primeiro.</text>')
    for k, n in enumerate(nomes[:14]):
        hh = int(hashlib.md5(n.encode()).hexdigest(), 16)
        col, lin = k % 3, k // 3
        x = 90 + col * 280 + (hh % 60); y = 70 + lin * 52 + (hh >> 8) % 18
        rot = ((hh >> 16) % 14) - 7
        tam = 24 + (hh >> 24) % 10
        cls = ' class="pi"' if k == 0 else ''
        p.append(f'<text x="{x}" y="{y}" font-family="{MAO}" font-size="{tam}" fill="#d0343f" stroke="#1a0606" stroke-width=".6" opacity=".92" transform="rotate({rot} {x} {y})"{cls}>{esc(n)}</text>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#vn)"/>')
    p.append(f'<text x="24" y="{H-18}" font-family="{MONO}" font-size="13" fill="#cfc8bc" opacity=".75">{len(nomes)} nome(s) na parede · comenta na issue #1 e o teu aparece aqui</text>')
    p.append(f'<rect x="{W-140}" y="{H-46}" width="10" height="0" fill="#7a0a14" class="pinga"/>')
    css = ('.pi{animation:p 2.4s steps(1) infinite}@keyframes p{0%,80%{opacity:.9}82%{opacity:.2}86%{opacity:.9}90%{opacity:.3}}'
           '.pinga{animation:g 5s ease-in infinite}@keyframes g{0%{height:0}80%{height:40px;opacity:1}100%{height:46px;opacity:0}}')
    salvar('parede.svg', W, H, ''.join(p), css)

os.makedirs(OUT, exist_ok=True)
u, r = sinais()
s, t = sequencia()
pager(u, r, s, t)
diario()
parede(visitantes())
print('ok', agora.isoformat(), r, s, t)
