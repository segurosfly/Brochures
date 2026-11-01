#!/usr/bin/env python3
"""
Genera los recursos de la campaña Black Friday 2026 a partir de campana.json.

  python3 generar.py            → piezas/*.png + index.html
  python3 generar.py --pdf      → además recursos-black-friday-2026.pdf (requiere Chromium; ver LEEME.md)

Todo texto sale de campana.json: para cambiar algo se cambia allí, no aquí.
Requisitos: Python 3, cairosvg, Pillow y la familia Exo 2 instalada
(SegurosFly-AI-System/01_BRAND/fonts/Exo2-*.otf → ~/.fonts y `fc-cache -f`).
"""
import base64, html, io, json, os, sys
from pathlib import Path

import cairosvg
from PIL import Image

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]                     # segurosfly-dev/
D = json.loads((AQUI / 'campana.json').read_text(encoding='utf-8'))
ORO, MED, CEL = '#F8B133', '#123550', '#6A9CD9'
F = 'font-family="Exo 2"'
e = lambda s: html.escape(str(s), quote=True)


def img64(ruta, ancho=None, blanco=False):
    p = (AQUI / ruta).resolve() if not Path(ruta).is_absolute() else Path(ruta)
    im = Image.open(p).convert('RGBA')
    if blanco:  # logos de aliados en blanco sobre negro (los originales son oscuros o de color)
        bb = im.getchannel('A').point(lambda a: 255 if a > 20 else 0).getbbox()
        if bb: im = im.crop(bb)
        a = im.getchannel('A')
        im = Image.new('RGBA', im.size, (255, 255, 255, 255)); im.putalpha(a)
    if ancho and im.width > ancho:
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode(), im.size


LOGO, LOGO_SIZE = img64(RAIZ / 'SegurosFly-AI-System/01_BRAND/logo/logo_blanco_fondo_oscuro.png', 600)


# ───────────────────────── piezas ─────────────────────────
def maletas(x, y, s=1.0):
    """Las dos maletas + el celular con eSIM del concepto (mismo dibujo que la web)."""
    esq = lambda w, h: (
        f'<path d="M8 18V10a2 2 0 0 1 2-2h8M{w-18} 8h8a2 2 0 0 1 2 2v8M8 {h-18}v8a2 2 0 0 0 2 2h8M{w-18} {h-8}h8a2 2 0 0 0 2-2v-8" '
        f'fill="none" stroke="{ORO}" stroke-width="4" stroke-linecap="round"/>')
    g = f'<g transform="translate({x},{y}) scale({s})">'
    # grande
    g += (f'<rect x="28" y="0" width="34" height="34" rx="6" fill="none" stroke="#3a3a42" stroke-width="5"/>'
          f'<g transform="translate(0,30)"><rect width="92" height="132" rx="16" fill="url(#maleta)" stroke="#2a2a30" stroke-width="2"/>'
          f'<path d="M24 16v100M46 16v100M68 16v100" stroke="#ffffff" stroke-opacity=".07" stroke-width="3"/>{esq(92,132)}</g>'
          f'<circle cx="18" cy="168" r="7" fill="#2b2b31"/><circle cx="74" cy="168" r="7" fill="#2b2b31"/>'
          f'<g transform="translate(-22,58) rotate(-8)"><rect width="30" height="24" rx="5" fill="{ORO}"/>'
          f'<path d="M15 5l7 3v5c0 4-3.5 6.5-7 8-3.5-1.5-7-4-7-8V8z" fill="none" stroke="#0a0a0a" stroke-width="2.6" stroke-linejoin="round"/>'
          f'<path d="M11.5 13l2.5 2.5 4-4.5" fill="none" stroke="#0a0a0a" stroke-width="2.6" stroke-linecap="round"/></g>')
    # celular
    g += (f'<g transform="translate(104,110) rotate(-9)"><rect width="34" height="64" rx="7" fill="#0c0c0f" stroke="{ORO}" stroke-width="3"/>'
          f'<rect x="5" y="6" width="24" height="52" rx="4" fill="{MED}"/>'
          f'<path d="M10 30v-3M14 30v-6M18 30v-9M22 30v-12" stroke="{ORO}" stroke-width="2.6" stroke-linecap="round"/>'
          f'<text x="17" y="44" text-anchor="middle" {F} font-weight="900" font-size="8.5" fill="{ORO}">eSIM</text></g>')
    # chica
    g += (f'<path d="M160 88v-14a8 8 0 0 1 8-8h14a8 8 0 0 1 8 8v14" fill="none" stroke="#3a3a42" stroke-width="5"/>'
          f'<g transform="translate(146,86)"><rect width="72" height="88" rx="14" fill="url(#maleta)" stroke="#2a2a30" stroke-width="2"/>'
          f'<path d="M26 14v60M46 14v60" stroke="#ffffff" stroke-opacity=".07" stroke-width="3"/>{esq(72,88)}</g>')
    return g + '</g>'


def pase_hsm(p):
    t = p['textos']
    W, H = p['tamano']
    aliados = ''
    ax = 330
    for a in D['aliados']:
        src, (w0, h0) = img64(a['archivo'], 400, blanco=True)
        h = 30; w = w0 * h / h0
        aliados += f'<image href="{src}" x="{ax:.0f}" y="{H-56}" width="{w:.0f}" height="{h}" opacity=".9"/>'
        ax += w + 46
    talon = ''
    for i, (lab, val) in enumerate(t['talon']):
        talon += (f'<text x="1036" y="{300 + i*64}" {F} font-weight="800" font-size="14" letter-spacing="2.4" fill="#0a0a0a" fill-opacity=".7">{e(lab)}</text>'
                  f'<text x="1036" y="{328 + i*64}" {F} font-weight="900" font-size="24" fill="#0a0a0a">{e(val)}</text>')
    benef = ''
    bx = 300
    iconos = [f'<path d="M-6-2h4v-4h4v4h4v4H2v4h-4V2h-4z" fill="{ORO}"/>',
              f'<rect x="-6" y="-8" width="12" height="16" rx="2" fill="none" stroke="{ORO}" stroke-width="2.4"/>',
              f'<rect x="-8" y="-5" width="16" height="10" rx="3" fill="none" stroke="{ORO}" stroke-width="2.4"/>']
    for i, b in enumerate(t['beneficios']):
        benef += f'<g transform="translate({bx},{640})">{iconos[i]}</g><text x="{bx+16}" y="{647}" {F} font-weight="800" font-size="21" fill="#fff">{e(b)}</text>'
        bx += 16 + len(b) * 11.4 + 46
    barras = ''.join(f'<rect x="{1040 + i*7.4:.1f}" y="566" width="{(2.2 if i % 3 else 4.4):.1f}" height="50" fill="#0a0a0a"/>' for i in range(27))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
 <radialGradient id="res" cx="50%" cy="100%" r="62%"><stop offset="0" stop-color="{CEL}" stop-opacity=".45"/><stop offset=".38" stop-color="{MED}" stop-opacity=".8"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
 <radialGradient id="cono" cx="50%" cy="0%" r="70%"><stop offset="0" stop-color="{ORO}" stop-opacity=".26"/><stop offset="1" stop-color="{ORO}" stop-opacity="0"/></radialGradient>
 <linearGradient id="tubo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff7e3"/><stop offset=".45" stop-color="#ffffff"/><stop offset="1" stop-color="{ORO}"/></linearGradient>
 <linearGradient id="maleta" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2c2c33"/><stop offset=".45" stop-color="#141417"/><stop offset="1" stop-color="#08080a"/></linearGradient>
 <linearGradient id="talon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc54d"/><stop offset="1" stop-color="{ORO}"/></linearGradient>
 <filter id="glow" x="-20%" y="-300%" width="140%" height="700%"><feGaussianBlur stdDeviation="9"/></filter>
 <filter id="sombra" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="#000" flood-opacity=".75"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="#000"/>
<rect width="{W}" height="{H}" fill="url(#res)"/>
<!-- lámpara LED de tubo -->
<ellipse cx="800" cy="40" rx="560" ry="230" fill="url(#cono)"/>
<rect x="290" y="22" width="1020" height="14" rx="7" fill="{ORO}" filter="url(#glow)" opacity=".9"/>
<rect x="290" y="22" width="1020" height="14" rx="7" fill="url(#tubo)"/>
<rect x="270" y="19" width="22" height="20" rx="4" fill="#3a3a40"/><rect x="1308" y="19" width="22" height="20" rx="4" fill="#3a3a40"/>
<!-- logo + titular -->
<image href="{LOGO}" x="40" y="44" width="{LOGO_SIZE[0]*150/LOGO_SIZE[1]:.0f}" height="150"/>
<text x="900" y="92" text-anchor="middle" {F} font-weight="800" font-size="21" letter-spacing="6" fill="{ORO}">{e(t['eyebrow'])}</text>
<text x="890" y="174" text-anchor="end" {F} font-weight="900" font-style="italic" font-size="76" fill="#fff">{e(D['mensaje']['titulo']['linea1_blanco'])}</text><text x="912" y="174" {F} font-weight="900" font-style="italic" font-size="76" fill="{ORO}">{e(D['mensaje']['titulo']['linea1_oro'])}</text>
<!-- pase -->
<g transform="translate(215,228) rotate(-2.2)" filter="url(#sombra)">
 <rect x="0" y="0" width="1040" height="440" rx="26" fill="#121214" stroke="#2a2a30" stroke-width="2"/>
 <path d="M26 0H780V70H0V26A26 26 0 0 1 26 0Z" fill="#050506"/>
 <text x="40" y="47" {F} font-weight="900" font-size="25" letter-spacing="6" fill="#fff">{e(t['pase_cabecera'])}</text>
 <text x="740" y="47" text-anchor="end" {F} font-weight="900" font-size="18" letter-spacing="3.5" fill="{ORO}">{e(t['pase_campana'])}</text>
 <text x="40" y="118" {F} font-weight="800" font-size="15" letter-spacing="2.4" fill="#9aa3ad">{e(t['desde_label'])}</text>
 <text x="40" y="178" {F} font-weight="900" font-size="66" fill="#fff">{e(t['desde'])}</text>
 <line x1="200" y1="158" x2="560" y2="158" stroke="#fff" stroke-opacity=".35" stroke-width="3" stroke-dasharray="7 7"/>
 <path transform="translate(372,148)" d="M2 10 Q2 8 5 8 L28 8 Q33 8 36 10.3 Q33 12 28 12 L5 12 Q2 12 2 10Z M4 8.4 L1 3 L5 3 L10 8.4Z M15 11.6 L10 18 L13 18 L21 11.6Z" fill="{ORO}"/>
 <text x="740" y="118" text-anchor="end" {F} font-weight="800" font-size="15" letter-spacing="2.4" fill="#9aa3ad">{e(t['hasta_label'])}</text>
 <text x="740" y="178" text-anchor="end" {F} font-weight="900" font-size="66" fill="#fff">{e(t['hasta'])}</text>
 <text x="40" y="236" {F} font-weight="800" font-size="15" letter-spacing="2.4" fill="#9aa3ad">{e(t['salida_label'])}</text>
 <text x="40" y="274" {F} font-weight="800" font-size="32" fill="#fff">{e(t['salida'])}</text>
 <text x="40" y="324" {F} font-weight="800" font-size="15" letter-spacing="2.4" fill="#9aa3ad">{e(t['cierre_label'])}</text>
 <text x="40" y="362" {F} font-weight="900" font-size="32" fill="{ORO}">{e(t['cierre'])}</text>
 <text x="740" y="232" text-anchor="end" {F} font-weight="900" font-size="20" letter-spacing="5" fill="#fff">{e(t['pct_label'])}</text>
 <text x="752" y="360" text-anchor="end" {F} font-weight="900" font-size="150" fill="{ORO}" letter-spacing="-3">{e(t['pct'])}</text>
 <text x="740" y="400" text-anchor="end" {F} font-weight="900" font-size="18" letter-spacing="3" fill="#fff">{e(t['pct_sub'])}</text>
 <line x1="782" y1="20" x2="782" y2="420" stroke="#000" stroke-width="5" stroke-dasharray="9 9"/>
 <path d="M790 0H1014A26 26 0 0 1 1040 26V414A26 26 0 0 1 1014 440H790Z" fill="url(#talon)"/>
</g>
<g transform="rotate(-2.2 215 228)">
 {talon}
 <g transform="translate(1040,478) rotate(-7)"><rect width="196" height="52" rx="10" fill="none" stroke="#0a0a0a" stroke-width="4"/>
 <text x="98" y="35" text-anchor="middle" {F} font-weight="900" font-size="22" letter-spacing="2.5" fill="#0a0a0a">{e(t['sello'])}</text></g>
 {barras}
</g>
{benef}
{maletas(26, 560, 1.05)}
<!-- pie: aliados + vigencia -->
<rect x="0" y="{H-80}" width="{W}" height="80" fill="#0a0a0c"/>
<rect x="0" y="{H-80}" width="{W}" height="2" fill="{ORO}" opacity=".7"/>
<text x="40" y="{H-44}" {F} font-weight="700" font-size="17" fill="#c8ccd2">Nuestros aliados</text>
<text x="40" y="{H-22}" {F} font-weight="700" font-size="17" fill="#c8ccd2">en cada detalle</text>
{aliados}
<text x="{W-40}" y="{H-46}" text-anchor="end" {F} font-weight="900" font-size="26" fill="{ORO}">{e(D['contacto']['web'])}</text>
<text x="{W-40}" y="{H-20}" text-anchor="end" {F} font-weight="600" font-size="15" fill="#c8ccd2">{e(t['pie'])}</text>
</svg>'''


def generar_piezas():
    hechas = []
    for p in D['piezas']:
        if p['id'] == 'pase-hsm' and p.get('estado') != 'descartada':
            svg = pase_hsm(p)
            (AQUI / 'piezas').mkdir(exist_ok=True)
            (AQUI / 'piezas' / 'pase_hsm_1600x837.svg').write_text(svg, encoding='utf-8')
            cairosvg.svg2png(bytestring=svg.encode(), write_to=str(AQUI / p['archivo']))
            hechas.append(p['archivo'])
    return hechas


if __name__ == '__main__':
    print('piezas:', generar_piezas())
    import pagina
    pagina.generar(D, AQUI)
    print('index.html listo')
    if '--pdf' in sys.argv:
        pagina.pdf(AQUI)
