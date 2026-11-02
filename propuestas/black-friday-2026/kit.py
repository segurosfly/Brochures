"""Kit de WhatsApp para el equipo comercial (Black Friday 2026), desde campana.json → kit.

Por cada tema: chat 1080×1080 y estado 1080×1920 (y 1600×837 si `plantilla: true`), en JPG.
Mismo lenguaje que el hero de la web: fondo negro, lámpara LED de tubo, oro solo en lo que
importa, maletas + celular con eSIM, azul de marca solo como resplandor.

Lo llama generar.py. Requiere cairosvg, Pillow y Exo 2 instalada (ver LEEME.md).
"""
import io
from pathlib import Path

import cairosvg
from PIL import Image, ImageFont

import generar as g

ORO, MED, CEL = g.ORO, g.MED, g.CEL
F = g.F
e = g.e
FONTS = [Path.home() / '.fonts', Path.home() / 'Library/Fonts', g.RAIZ / 'SegurosFly-AI-System/01_BRAND/fonts']
ARCH = {(900, False): 'Exo2-Black.otf', (900, True): 'Exo2-BlackItalic.otf', (800, False): 'Exo2-ExtraBold.otf',
        (700, False): 'Exo2-Bold.otf', (600, False): 'Exo2-SemiBold.otf'}
_cache = {}


def _font(peso, italica, tam):
    k = (peso, italica, tam)
    if k not in _cache:
        nombre = ARCH[(peso, italica)]
        ruta = next((d / nombre for d in FONTS if (d / nombre).exists()), None)
        _cache[k] = ImageFont.truetype(str(ruta), tam)
    return _cache[k]


def ancho(txt, peso, tam, italica=False, esp=0):
    return _font(peso, italica, tam).getlength(txt) + esp * max(len(txt) - 1, 0)


def txt(t, x, y, tam, peso=800, color='#fff', alin='start', max_w=None, italica=False, esp=0, opac=1):
    """Texto SVG; si no cabe en max_w, baja el tamaño hasta que quepa."""
    if max_w:
        while tam > 10 and ancho(t, peso, tam, italica, esp) > max_w:
            tam -= 1
    st = ' font-style="italic"' if italica else ''
    ls = f' letter-spacing="{esp}"' if esp else ''
    op = f' fill-opacity="{opac}"' if opac != 1 else ''
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{alin}" {F} font-weight="{peso}" font-size="{tam}"{st}{ls} '
            f'fill="{color}"{op}>{e(t)}</text>')


def tam_que_cabe(t, peso, tam, max_w, italica=False):
    while tam > 10 and ancho(t, peso, tam, italica) > max_w:
        tam -= 1
    return tam


# ── íconos (24×24, centrados en 0,0), en negro sobre círculo oro ──
I = {
    'cruz': '<path d="M-3.5-9h7v5.5H9v7H3.5V9h-7V3.5H-9v-7h5.5z" fill="#0a0a0a"/>',
    'chip': ('<path d="M-6-9h8l5 5v13h-13z" fill="none" stroke="#0a0a0a" stroke-width="2.4" stroke-linejoin="round"/>'
             '<rect x="-3" y="-2" width="7" height="7" rx="1" fill="#0a0a0a"/>'),
    'vip': ('<path d="M-9 2v-5a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v5" fill="none" stroke="#0a0a0a" stroke-width="2.4"/>'
            '<rect x="-10" y="1" width="20" height="6" rx="2" fill="#0a0a0a"/><path d="M-8 7v3M8 7v3" stroke="#0a0a0a" stroke-width="2.4"/>'),
    'calendario': ('<rect x="-9" y="-7" width="18" height="16" rx="2.5" fill="none" stroke="#0a0a0a" stroke-width="2.4"/>'
                   '<path d="M-9-2h18M-4-10v5M4-10v5" stroke="#0a0a0a" stroke-width="2.4" stroke-linecap="round"/>'
                   '<path d="M-3 4l2.2 2.2L4 1.6" fill="none" stroke="#0a0a0a" stroke-width="2.4" stroke-linecap="round"/>'),
    'maleta': ('<rect x="-8" y="-5" width="16" height="14" rx="2.5" fill="#0a0a0a"/>'
               '<path d="M-3.5-5v-3h7v3" fill="none" stroke="#0a0a0a" stroke-width="2.4"/>'),
    'eu': ''.join(f'<circle cx="{8*__import__("math").cos(i*0.5236):.2f}" cy="{8*__import__("math").sin(i*0.5236):.2f}" r="1.7" fill="#0a0a0a"/>' for i in range(12)),
    'pasaporte': ('<rect x="-7" y="-9.5" width="14" height="19" rx="2" fill="#0a0a0a"/>'
                  f'<circle cx="0" cy="-1.5" r="3.6" fill="none" stroke="{ORO}" stroke-width="1.6"/>'
                  f'<path d="M-3.5 5.5h7" stroke="{ORO}" stroke-width="1.6"/>'),
    'avion': ('<path d="M-10 1.2 Q-10-.8-7-.8H6Q10-.8 11 0.6Q10 2 6 2H-7Q-10 2-10 1.2Z M-6-.6-9-7h3l6 6.4Z M1 1.8-4 9h3l7-7.2Z" '
              'fill="#0a0a0a"/>'),
    'laptop': ('<rect x="-8" y="-7" width="16" height="11" rx="1.5" fill="none" stroke="#0a0a0a" stroke-width="2.4"/>'
               '<path d="M-10.5 7h21" stroke="#0a0a0a" stroke-width="2.8" stroke-linecap="round"/>'),
    'escudo': ('<path d="M0-9.5l8 3.2v5.3c0 5.2-3.6 8.4-8 10-4.4-1.6-8-4.8-8-10v-5.3z" fill="#0a0a0a"/>'
               f'<path d="M-3.4 0l2.4 2.4 4.4-4.8" fill="none" stroke="{ORO}" stroke-width="2.2" stroke-linecap="round"/>'),
    'familia': ('<circle cx="-5" cy="-5" r="3.2" fill="#0a0a0a"/><circle cx="5" cy="-5" r="3.2" fill="#0a0a0a"/>'
                '<circle cx="0" cy="1" r="2.4" fill="#0a0a0a"/><path d="M-10 9v-3a4 4 0 0 1 4-4h2M10 9v-3a4 4 0 0 0-4-4h-2" '
                'fill="none" stroke="#0a0a0a" stroke-width="2.6"/><path d="M-3.4 9.5v-1.5a3.4 3.4 0 0 1 6.8 0v1.5z" fill="#0a0a0a"/>'),
    'reloj': ('<circle r="9" fill="none" stroke="#0a0a0a" stroke-width="2.4"/>'
              '<path d="M0-5v5.5l3.6 2.4" fill="none" stroke="#0a0a0a" stroke-width="2.4" stroke-linecap="round"/>'),
}


def chip(x, y, h, icono, texto, tam, max_w=None):
    """Píldora con círculo oro + ícono y texto blanco. Devuelve (svg, ancho)."""
    r = h / 2 - 9
    tam = tam_que_cabe(texto, 800, tam, (max_w - h - 30) if max_w else 9999)
    w = h + ancho(texto, 800, tam) + 30
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="#0f0f12" stroke="{ORO}" stroke-opacity=".55" stroke-width="2"/>'
         f'<circle cx="{x + h/2:.0f}" cy="{y + h/2:.0f}" r="{r:.0f}" fill="{ORO}"/>'
         f'<g transform="translate({x + h/2:.1f},{y + h/2:.1f}) scale({r/13:.3f})">{I[icono]}</g>'
         + txt(texto, x + h + 6, y + h / 2 + tam * 0.36, tam, 800))
    return s, w


def fila_chips(chips, x, y, h, tam, max_total, gap=16):
    """Tres píldoras en fila; reduce la letra hasta que entren en max_total."""
    while tam > 12:
        anchos = [h + ancho(t, 800, tam) + 30 for _, t in chips]
        if sum(anchos) + gap * (len(chips) - 1) <= max_total:
            break
        tam -= 1
    s = ''
    for ic, t in chips:
        part, w = chip(x, y, h, ic, t, tam)
        s += part
        x += w + gap
    return s


def defs(W, H, cy_res=1.0):
    return f'''<defs>
 <radialGradient id="res" cx="50%" cy="{cy_res*100:.0f}%" r="70%"><stop offset="0" stop-color="{CEL}" stop-opacity=".42"/><stop offset=".4" stop-color="{MED}" stop-opacity=".78"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
 <radialGradient id="cono" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{ORO}" stop-opacity=".26"/><stop offset="1" stop-color="{ORO}" stop-opacity="0"/></radialGradient>
 <linearGradient id="tubo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff7e3"/><stop offset=".45" stop-color="#ffffff"/><stop offset="1" stop-color="{ORO}"/></linearGradient>
 <linearGradient id="maleta" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2c2c33"/><stop offset=".45" stop-color="#141417"/><stop offset="1" stop-color="#08080a"/></linearGradient>
 <linearGradient id="caja" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc54d"/><stop offset="1" stop-color="{ORO}"/></linearGradient>
 <filter id="glow" x="-20%" y="-300%" width="140%" height="700%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="#000"/><rect width="{W}" height="{H}" fill="url(#res)"/>'''


def lampara(x1, x2, y, rx_cono, ry_cono):
    cx = (x1 + x2) / 2
    return (f'<ellipse cx="{cx}" cy="{y + 7}" rx="{rx_cono}" ry="{ry_cono}" fill="url(#cono)"/>'
            f'<rect x="{x1}" y="{y}" width="{x2-x1}" height="14" rx="7" fill="{ORO}" filter="url(#glow)" opacity=".9"/>'
            f'<rect x="{x1}" y="{y}" width="{x2-x1}" height="14" rx="7" fill="url(#tubo)"/>'
            f'<rect x="{x1-20}" y="{y-3}" width="22" height="20" rx="4" fill="#3a3a40"/><rect x="{x2-2}" y="{y-3}" width="22" height="20" rx="4" fill="#3a3a40"/>')


def _logo_recortado():
    """Logo blanco sin el margen transparente del PNG (si no, sale diminuto)."""
    import base64
    im = Image.open(g.RAIZ / 'SegurosFly-AI-System/01_BRAND/logo/logo_blanco_fondo_oscuro.png').convert('RGBA')
    im = im.crop(im.getchannel('A').getbbox())
    im = im.resize((700, round(im.height * 700 / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode(), im.size


LOGO, LOGO_SIZE = _logo_recortado()


def logo(x, y, h):
    """Logo de alto h (ya sin márgenes). Devuelve el SVG."""
    return f'<image href="{LOGO}" x="{x:.0f}" y="{y:.0f}" width="{LOGO_SIZE[0]*h/LOGO_SIZE[1]:.0f}" height="{h}"/>'


def pill(t, x, y, tam):
    w = ancho(t, 900, tam, esp=tam * 0.18) + tam * 1.6
    h = tam * 1.9
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h:.0f}" rx="{h/2:.0f}" fill="{ORO}"/>'
            + txt(t, x + tam * 0.8, y + h / 2 + tam * 0.36, tam, 900, '#0a0a0a', esp=round(tam * 0.18, 1)))


def caja_oferta(K, x, y, w, h):
    o = K['oferta']
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="url(#caja)"/>'
            + txt(o['arriba'], x + w / 2, y + h * 0.27, round(h * 0.15), 900, '#0a0a0a', 'middle', esp=4)
            + txt(f"{o['grande']} {o['abajo']}", x + w / 2, y + h * 0.78, round(h * 0.42), 900, '#0a0a0a', 'middle',
                  max_w=w - 28, italica=True))


def lado_oferta(K, x, y, tam, max_w):
    o = K['oferta']
    return (txt(o['linea1'], x, y, tam, 800, '#fff', max_w=max_w)
            + txt(o['linea2'], x, y + tam * 1.35, round(tam * 0.82), 700, ORO, max_w=max_w))


def pie(t, W, H, y, tam):
    return (f'<rect x="0" y="{y}" width="{W}" height="2" fill="{ORO}" opacity=".55"/>'
            + txt(t['legal'], 60, y + 44, tam, 600, '#c8ccd2', max_w=W - 120 - ancho('segurosfly.com', 900, tam + 8) - 30)
            + txt('segurosfly.com', W - 60, y + 46, tam + 8, 900, ORO, 'end'))


def svg_chat(K, t):
    W = H = 1080
    s = defs(W, H)
    s += lampara(140, 940, 26, 520, 260)
    s += logo(60, 80, 66)
    s += g.maletas(708, 92, 1.55)
    s += pill(t['pill'], 60, 300, 30)
    tam = min(tam_que_cabe(t['l1'], 900, 82, 960), tam_que_cabe(t['l2'], 900, 82, 960))
    s += txt(t['l1'], 60, 455, tam, 900) + txt(t['l2'], 60, 455 + tam * 1.12, tam, 900, ORO)
    ysub = 455 + tam * 1.12 + 70
    for i, l in enumerate(t['sub']):
        s += txt(l, 60, ysub + i * 44, 34, 700, '#d7dbe0', max_w=960)
    yo = ysub + 44 * len(t['sub']) + 30
    s += caja_oferta(K, 60, yo, 262, 132) + lado_oferta(K, 350, yo + 60, 36, 670)
    s += fila_chips(t['chips'], 60, yo + 132 + 36, 72, 28, 960)
    s += pie(t, W, H, H - 76, 19)
    return W, H, s


def svg_estado(K, t):
    W, H = 1080, 1920
    s = defs(W, H)
    s += lampara(140, 940, 210, 560, 330)
    s += logo(W / 2 - LOGO_SIZE[0] * 80 / LOGO_SIZE[1] / 2, 272, 80)
    s += g.maletas(W / 2 - 240 * 2.6 / 2 + 26, 420, 2.6)
    s += pill(t['pill'], 70, 930, 34)
    tam = min(tam_que_cabe(t['l1'], 900, 100, 940), tam_que_cabe(t['l2'], 900, 100, 940))
    s += txt(t['l1'], 70, 1100, tam, 900) + txt(t['l2'], 70, 1100 + tam * 1.12, tam, 900, ORO)
    ysub = 1100 + tam * 1.12 + 78
    for i, l in enumerate(t['sub']):
        s += txt(l, 70, ysub + i * 50, 38, 700, '#d7dbe0', max_w=940)
    yo = ysub + 50 * len(t['sub']) + 40
    s += caja_oferta(K, 70, yo, 300, 150) + lado_oferta(K, 400, yo + 68, 40, 610)
    s += fila_chips(t['chips'], 70, yo + 150 + 44, 78, 30, 940)
    s += pie(t, W, H, 1730, 21)
    return W, H, s


def svg_plantilla(K, t):
    W, H = 1600, 837
    s = defs(W, H, 1.05)
    s += lampara(300, 1300, 22, 620, 240)
    s += logo(60, 74, 70)
    s += g.maletas(1170, 300, 1.75)
    s += pill(t['pill'], 60, 214, 28)
    tam = min(tam_que_cabe(t['l1'], 900, 78, 1060), tam_que_cabe(t['l2'], 900, 78, 1060))
    s += txt(t['l1'], 60, 352, tam, 900) + txt(t['l2'], 60, 352 + tam * 1.12, tam, 900, ORO)
    yo = 352 + tam * 1.12 + 56
    s += caja_oferta(K, 60, yo, 250, 124) + lado_oferta(K, 336, yo + 58, 34, 740)
    s += fila_chips(t['chips'], 60, yo + 124 + 32, 64, 25, 1060)
    s += pie(t, W, H, H - 72, 17)
    return W, H, s


def _jpg(W, H, cuerpo, destino):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{cuerpo}</svg>'
    png = cairosvg.svg2png(bytestring=svg.encode())
    Image.open(io.BytesIO(png)).convert('RGB').save(destino, 'JPEG', quality=90, optimize=True, progressive=True)


def archivos(t):
    """Nombres de archivo de un tema (relativos a la carpeta de la campaña)."""
    a = {'chat': f'piezas/bf_{t["id"]}_chat.jpg', 'estado': f'piezas/bf_{t["id"]}_estado.jpg'}
    if t.get('plantilla'):
        a['plantilla'] = f'piezas/bf_{t["id"]}_1600x837.jpg'
    return a


def generar(D, aqui, solo=None):
    K = D['kit']
    (aqui / 'piezas').mkdir(exist_ok=True)
    hechas = []
    for t in K['temas']:
        if solo and t['id'] not in solo:
            continue
        a = archivos(t)
        for clave, fn in (('chat', svg_chat), ('estado', svg_estado), ('plantilla', svg_plantilla)):
            if clave in a:
                _jpg(*fn(K, t), aqui / a[clave])
                hechas.append(a[clave])
    return hechas
