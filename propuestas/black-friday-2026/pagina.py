"""Página de recursos de la campaña (index.html), generada desde campana.json.

La misma página sirve para leer en pantalla y para imprimir: el PDF descargable
sale de esta página (estilos @media print), así que nunca se desalinean.
"""
import base64, html, json, shutil, subprocess
from pathlib import Path

e = lambda s: html.escape(str(s), quote=True)
ORO = '#F8B133'
PDF_NOMBRE = 'recursos-black-friday-2026.pdf'


def _fuentes(raiz):
    out = ''
    for peso, archivo in [(900, 'Exo2-Black.otf'), (900, 'Exo2-BlackItalic.otf'), (800, 'Exo2-ExtraBold.otf'),
                          (700, 'Exo2-Bold.otf'), (600, 'Exo2-SemiBold.otf'), (400, 'Exo2-Regular.otf')]:
        b = (raiz / 'SegurosFly-AI-System/01_BRAND/fonts' / archivo).read_bytes()
        estilo = 'italic' if 'Italic' in archivo else 'normal'
        out += (f"@font-face{{font-family:'Exo 2';src:url(data:font/otf;base64,{base64.b64encode(b).decode()});"
                f"font-weight:{peso};font-style:{estilo}}}")
    return out


def _assets_cupon(raiz):
    """Logo y aliados en blanco (data URI) para el generador de cupón del navegador."""
    import generar as g
    d = json.loads((Path(__file__).resolve().parent / 'campana.json').read_text(encoding='utf-8'))
    logo, _ = g.img64(raiz / 'SegurosFly-AI-System/01_BRAND/logo/logo_blanco_fondo_oscuro.png', 600)
    aliados = [g.img64(a['archivo'], 400, blanco=True)[0] for a in d['aliados']]
    return {'logo': logo, 'aliados': aliados}


def generar(D, aqui):
    raiz = aqui.parents[2]
    c = D['campana']; o = D['oferta']; m = D['mensaje']
    hay_pdf = (aqui / PDF_NOMBRE).exists()

    # Kit comercial
    kit = ''
    for p in D['piezas']:
        if p.get('estado') == 'descartada':
            continue
        if p.get('archivo') and (aqui / p['archivo']).exists():
            w, h = p['tamano']
            img = (f'<img src="{e(p["archivo"])}" alt="{e(p.get("alt",""))}" loading="lazy">'
                   f'<div class="acciones no-print"><button data-copiar-img="{e(p["archivo"])}">Copiar imagen</button>'
                   f'<a class="btn" href="{e(p["archivo"])}" download>Descargar</a></div>')
        else:
            w, h = p['tamano']
            img = f'<div class="pendiente">Pendiente: {e(p.get("nota",""))}</div>'
        msg = ''
        if p.get('mensaje_sugerido'):
            msg = (f'<div class="msg"><span class="eb">Mensaje sugerido</span><p>{e(p["mensaje_sugerido"])}</p>'
                   f'<button class="no-print" data-copiar-txt="{e(p["mensaje_sugerido"])}">Copiar texto</button></div>')
        usos = ' · '.join(u.replace('_', ' ') for u in p.get('usos', []))
        kit += (f'<article class="pieza"><div class="marco">{img}</div><div class="info"><h3>{e(p["nombre"])}</h3>'
                f'<p class="meta">{e(p["formato"])} · {w}×{h} · <span class="estado {e(p["estado"])}">{e(p["estado"].replace("_"," "))}</span></p>'
                f'<p class="meta">Sirve para: {e(usos)}</p>{msg}</div></article>')

    pilares = ''.join(
        f'<tr><td class="n">{x["orden"]}</td><td><b class="oro">{e(x["etiqueta"])}</b><br>{e(x["texto"])}</td>'
        f'<td>{e(x.get("guardarrail","—"))}</td></tr>' for x in sorted(D['pilares'], key=lambda x: x['orden']))
    semanas = ''.join(f'<tr><td class="oro">{e(s["id"])} · {e(s["fechas"])}</td><td>{e(s["foco"])}</td><td>{e(s["ads"])}</td></tr>'
                      for s in D['semanas'])
    paleta = ''.join(f'<div class="color"><span style="background:{x["hex"]}"></span><b>{e(x["nombre"])}</b>'
                     f'<code>{x["hex"]}</code><small>{e(x["papel"])}{(" · " + e(x["uso"])) if x.get("uso") else ""}</small></div>'
                     for x in D['paleta'])
    fechas = ''.join(f'<li><b>{e(f["nombre"])}</b> · {e(f["fecha"].replace("2026-","").replace("/"," → "))}'
                     f'{" · solo México" if f["mercados"]==["MX"] else ""}</li>' for f in c['fechas_clave'])
    prohibido = ''.join(f'<li>{e(x)}</li>' for x in m['prohibido'])
    mercados = ''.join(f'<li>{e(x)}</li>' for x in c['notas_mercado'])
    origen = ''.join(f'<li><b>{e(x["quien"])}</b>: {e(x["aporte"])}</li>' for x in c['origen'])
    franja = ' <b class="oro">✦</b> '.join(e(x) for x in D['franja'])

    pdf_btn = (f'<a class="btn oro" href="{PDF_NOMBRE}" download>Descargar PDF</a>' if hay_pdf
               else '<span class="btn apagado" title="Se genera al aprobar la maqueta">PDF: tras aprobar la maqueta</span>')

    doc = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(c["nombre"])} · Recursos de campaña · SegurosFly</title>
<meta name="robots" content="noindex">
<style>{_fuentes(raiz)}{CSS}</style></head><body>
<header class="top"><div class="wrap">
 <div><p class="eb">{e(c["eyebrow"])}</p>
 <h1><i>BLACK <span class="oro">FRIDAY</span></i> <small>2026 · Recursos de campaña</small></h1>
 <p class="lead">{e(o["titular"])} {e(o["complemento"])} · {e(c["vigencia"]["texto"])}</p></div>
 <nav class="no-print">{pdf_btn}<a class="btn" href="campana.json" download>Datos (JSON)</a></nav>
</div></header>
<main class="wrap">

<section id="hero"><h2><span class="num">1</span> El hero de la web, funcionando</h2>
<p>Móvil y escritorio. Lámpara LED, maletas + celular con eSIM, avioncito y franja que corre.
Pasa el mouse por las maletas (escritorio) para ver el mensaje.</p>
<iframe class="no-print" src="hero.html" title="Hero Black Friday" loading="lazy"></iframe>
<img class="solo-print" src="piezas/hero_captura.png" alt="Hero Black Friday (captura)">
</section>

<section id="concepto"><h2><span class="num">2</span> En 4 puntos</h2>
<div class="grid4">
 <div class="card"><span class="eb">Título</span><p class="big"><i>BLACK <span class="oro">FRIDAY</span></i></p>
 <p>{e(m["h1"])} · {e(m["bajada"])}</p></div>
 <div class="card"><span class="eb">Oferta</span><p class="big oro">{e(o["titular"])}</p>
 <p>{e(o["complemento"])}. {e(o["condicion"])}.</p></div>
 <div class="card"><span class="eb">Colores</span><p class="big">Negro · <span class="oro">oro</span></p>
 <p>Tres colores (60-30-10) y el azul de marca solo como resplandor.</p></div>
 <div class="card"><span class="eb">Mensaje</span><p class="big">Lo principal primero</p>
 <p>Asistencia médica y emergencias 24/7; equipaje, eSIM y dispositivos «y además».</p></div>
</div>
<div class="nota"><b>Regla del 75%:</b> {e(o["regla"])} <br><b>Antes de publicar:</b> {e(o["requisito_previo"])}</div>
</section>

<section id="kit"><h2><span class="num">3</span> Kit para el equipo comercial</h2>
<p>Cada pieza con su mensaje listo para copiar. En WhatsApp, primero la imagen y luego el texto.</p>
<div class="kit">{kit}</div></section>

<section id="cupon"><h2><span class="num">4</span> Generador de cupón adicional</h2>
<p>Para el prospecto que necesita un empujón: un pase de abordar con un <b class="oro">descuento ADICIONAL</b> al de la web
(como el de Halloween). Escribe el %, la vigencia y, si quieres, el nombre del cliente, el tuyo y el código; la imagen se
genera sola y la descargas en <b>JPG</b> para adjuntarla en WhatsApp/Kommo.</p>
<div class="nota no-print"><b>Antes de enviarlo:</b> el <span id="cu-aviso-pct">%</span> tiene que existir como cupón en el CMS
(Cupones) con la misma vigencia. Es <b>adicional</b> y se aplica <b>sobre el precio ya rebajado</b> de la web: un 40% extra no
se suma al 75%. Si el cupón no existe, no envíes la imagen.</div>
<div class="cupon no-print"><form id="cu-form" onsubmit="return false">
 <label>% adicional<input id="cu-pct" type="number" min="1" max="90" value="40"></label>
 <label>Para quién (arriba)<select id="cu-seg">
  <option>¿SALES DE MAÑANA A 5 DÍAS?</option><option>¿YA TIENES TU VUELO?</option><option>¿VIAJAN EN GRUPO?</option>
  <option>¿VIAJAS A EUROPA?</option><option>SOLO PARA TI</option><option value="__otro">Otro texto…</option></select>
  <input id="cu-seg-otro" type="text" maxlength="40" placeholder="Escribe el texto" style="display:none"></label>
 <label>Válido hasta<input id="cu-vence" type="datetime-local"></label>
 <label>Nombre del cliente (opcional)<input id="cu-cliente" type="text" maxlength="22" placeholder="María"></label>
 <label>Tu nombre (opcional)<input id="cu-asesor" type="text" maxlength="16" placeholder="Guillermo"></label>
 <label>Código del cupón (opcional)<input id="cu-codigo" type="text" maxlength="12" placeholder="BF40HOY"></label>
 <label>Formato<select id="cu-formato"><option value="hsm">Adjunto / plantilla 1600×837</option><option value="chat">Chat cuadrado 1080×1080</option></select></label>
 <div class="acciones"><button id="cu-jpg" class="btn oro" type="button">Descargar JPG</button><button id="cu-copiar" type="button">Copiar imagen</button></div>
</form><div class="cu-vista"><canvas id="cu-canvas" width="1600" height="837"></canvas></div></div>
</section>

<section id="pilares"><h2><span class="num">5</span> Qué decimos y en qué orden</h2>
<table><thead><tr><th>#</th><th>Tarjeta (etiqueta · texto)</th><th>Cuidado con</th></tr></thead><tbody>{pilares}</tbody></table>
<p class="franja">{franja}</p>
<p class="legal"><b>Legal corto:</b> {e(D["legal"]["corto"])}<br><b>Legal largo:</b> {e(D["legal"]["largo"])}</p>
</section>

<section id="semanas"><h2><span class="num">6</span> Semana a semana</h2>
<table><thead><tr><th>Semana</th><th>Foco</th><th>Ads</th></tr></thead><tbody>{semanas}</tbody></table>
<div class="grid2"><div class="card"><span class="eb">Fechas clave</span><ul>{fechas}</ul></div>
<div class="card"><span class="eb">Por país</span><ul>{mercados}</ul></div></div>
</section>

<section id="colores"><h2><span class="num">7</span> Colores y letra</h2>
<div class="paleta">{paleta}</div><p>{e(D["tipografia"])}</p></section>

<section id="reglas"><h2><span class="num">8</span> Lo que no hacemos</h2><ul>{prohibido}</ul>
<p class="meta">De dónde sale:</p><ul>{origen}</ul></section>

<section id="datos"><h2><span class="num">9</span> Los datos, para lo que viene</h2>
<p>Todo lo de esta página sale de <code>campana.json</code>: textos, oferta, legal, piezas, semanas y colores.
Así la misma fuente alimenta la web, las piezas, este PDF y, más adelante, los correos de email marketing
(bloques listos: título, H1, bajada, oferta, pilares 1–4, CTA y legal largo; imagen de cabecera: el pase de abordar).</p>
</section>
</main>
<footer class="wrap"><p>SegurosFly · {e(c["nombre"])} · {e(D["version"])} · uso interno</p></footer>
<script>window.CUPON_ASSETS={json.dumps(_assets_cupon(raiz))};</script>
<script>{(aqui / 'generador-cupon.js').read_text(encoding='utf-8')}</script>
<script>
document.querySelectorAll('[data-copiar-txt]').forEach(b=>b.onclick=async()=>{{await navigator.clipboard.writeText(b.dataset.copiarTxt);b.textContent='¡Copiado!';setTimeout(()=>b.textContent='Copiar texto',1500)}});
document.querySelectorAll('[data-copiar-img]').forEach(b=>b.onclick=async()=>{{try{{const r=await fetch(b.dataset.copiarImg);const bl=await r.blob();await navigator.clipboard.write([new ClipboardItem({{[bl.type]:bl}})]);b.textContent='¡Copiada!'}}catch(x){{b.textContent='Usa Descargar'}}setTimeout(()=>b.textContent='Copiar imagen',1800)}});
</script></body></html>'''
    (aqui / 'index.html').write_text(doc, encoding='utf-8')


def pdf(aqui):
    """PDF = esta misma página impresa (A4 horizontal). Necesita Chromium/Chrome."""
    for exe in ['chromium', 'chromium-browser', 'google-chrome',
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']:
        if shutil.which(exe) or Path(exe).exists():
            subprocess.run([exe, '--headless=new', '--no-pdf-header-footer', f'--print-to-pdf={aqui / PDF_NOMBRE}',
                            (aqui / 'index.html').as_uri()], check=True)
            return
    raise SystemExit('No hay Chrome/Chromium para generar el PDF (ver LEEME.md).')


CSS = '''
*{box-sizing:border-box}html,body{margin:0;background:#000;color:#fff;font-family:'Exo 2',sans-serif;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.oro{color:#F8B133}.eb{display:block;color:#F8B133;font-weight:800;font-size:12px;letter-spacing:2.5px;text-transform:uppercase}
.top{border-bottom:2px solid #F8B133;background:radial-gradient(ellipse 60% 120% at 50% 0%,rgba(248,177,51,.14),transparent 70%),#000;padding:34px 0 26px}
.top .wrap{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap}
h1{margin:6px 0 4px;font-size:54px;font-weight:900;line-height:1}h1 small{font-size:18px;font-weight:700;color:#cfd3da;font-style:normal;margin-left:8px}
.lead{margin:6px 0 0;color:#cfd3da;font-size:18px}
nav{display:flex;gap:10px;flex-wrap:wrap}
.btn,button{display:inline-block;font-family:inherit;font-size:14px;font-weight:700;padding:10px 18px;border-radius:999px;border:1px solid #444;background:#141416;color:#fff;text-decoration:none;cursor:pointer}
.btn.oro{background:#F8B133;border-color:#F8B133;color:#000}.btn.apagado{opacity:.55;cursor:default}
section{padding:38px 0 8px;border-bottom:1px solid #1d1d20}
h2{font-size:28px;font-weight:900;margin:0 0 10px;display:flex;align-items:center;gap:12px}
.num{display:inline-flex;width:34px;height:34px;border-radius:50%;background:#F8B133;color:#000;font-size:18px;align-items:center;justify-content:center}
p{color:#cfd3da}
iframe{width:100%;height:1080px;border:1px solid #2a2a30;border-radius:14px;background:#111}
.solo-print{display:none}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
.card{background:#121214;border:1px solid #26262b;border-radius:16px;padding:18px}.card p{margin:6px 0 0}
.card .big{color:#fff;font-weight:900;font-size:22px;line-height:1.15}.card .big.oro{color:#F8B133}
.nota{margin-top:16px;padding:14px 18px;border-left:4px solid #F8B133;background:#121214;border-radius:8px;color:#cfd3da}
.kit{display:grid;gap:18px}
.cupon{display:grid;grid-template-columns:minmax(260px,330px) minmax(0,1fr);gap:18px;margin-top:14px;background:#0e0e10;border:1px solid #26262b;border-radius:16px;padding:16px}
#cu-form{display:flex;flex-direction:column;gap:10px}
#cu-form label{display:flex;flex-direction:column;gap:4px;font-size:13px;color:#cfd3da;font-weight:700}
#cu-form input,#cu-form select{font-family:inherit;font-size:15px;padding:9px 10px;border-radius:10px;border:1px solid #333;background:#141416;color:#fff}
#cu-pct{font-size:22px!important;font-weight:900;color:#F8B133!important}
.cu-vista canvas{width:100%;height:auto;border-radius:10px;display:block;background:#000}
@media (max-width:860px){.cupon{grid-template-columns:1fr}}
.pieza{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:18px;background:#0e0e10;border:1px solid #26262b;border-radius:16px;padding:16px}
.marco img{width:100%;border-radius:10px;display:block}
.pendiente{aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;text-align:center;padding:20px;border:1px dashed #555;border-radius:10px;color:#999}
.acciones{display:flex;gap:8px;margin-top:10px}
.info h3{margin:0 0 4px;font-size:20px}.meta{margin:2px 0;font-size:13px;color:#9aa3ad}
.estado{font-weight:800;text-transform:uppercase;font-size:11px;letter-spacing:1px;padding:2px 8px;border-radius:999px;background:#26262b;color:#ddd}
.estado.maqueta{background:#F8B133;color:#000}.estado.pendiente_original{background:#3a2a10;color:#F8B133}
.msg{margin-top:12px;background:#141416;border-radius:12px;padding:12px 14px}.msg p{margin:6px 0 10px;color:#fff;font-size:14.5px}
table{width:100%;border-collapse:collapse;margin:8px 0;font-size:15px}
th{text-align:left;color:#F8B133;font-weight:800;border-bottom:2px solid #F8B133;padding:8px}
td{border-bottom:1px solid #222;padding:9px 8px;vertical-align:top;color:#e6e8eb}td.n{color:#F8B133;font-weight:900;width:36px}
.franja{margin-top:14px;padding:10px 14px;border-bottom:2px solid #F8B133;background:#0b0b0c;font-weight:800;text-transform:uppercase;font-size:13px;letter-spacing:1px;color:#fff}
.legal{font-size:13.5px}
.paleta{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
.color{background:#121214;border:1px solid #26262b;border-radius:14px;padding:12px;display:flex;flex-direction:column;gap:3px}
.color span{height:56px;border-radius:10px;border:1px solid #333}.color small{color:#9aa3ad}
ul{color:#cfd3da}code{color:#F8B133}
footer p{color:#666;font-size:12px;padding:24px 0}
@media (max-width:860px){.grid4,.paleta{grid-template-columns:1fr 1fr}.pieza{grid-template-columns:1fr}h1{font-size:40px}}
@page{size:A4 landscape;margin:12mm}
@media print{
 html,body{background:#000;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 .no-print{display:none!important}.solo-print{display:block;width:100%;border-radius:10px}
 section{break-inside:avoid;page-break-before:always;border:0;padding-top:0}
 section#hero{page-break-before:auto}
 .pieza{break-inside:avoid}
}
'''
