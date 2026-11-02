/* Generador de cupón ADICIONAL (pase de abordar) — Black Friday 2026.
 *
 * El asesor escribe el % adicional, la vigencia y (opcional) el cliente, el
 * asesor y el código; la página dibuja la pieza en un <canvas> y la descarga
 * en JPG (o la copia al portapapeles en PNG). Todo pasa en el navegador: no se
 * envía nada a ningún servidor.
 *
 * Reglas (docs/CENTRAL-MATERIALES-HSM.md):
 * - Es un descuento ADICIONAL al de la web, aplicado SOBRE ese precio.
 * - El % tiene que existir como cupón en el CMS antes de enviarlo.
 * - Lo principal primero: «Asistencia médica 24/7» va de primer beneficio.
 *
 * Recibe las imágenes (logo y aliados en blanco) en window.CUPON_ASSETS.
 */
(function () {
  const ORO = '#F8B133', MED = '#123550', CEL = '#6A9CD9'
  const $ = (id) => document.getElementById(id)
  const A = window.CUPON_ASSETS || { logo: null, aliados: [] }
  const imgs = {}
  const cargar = (src) => new Promise((ok) => { if (!src) return ok(null); const i = new Image(); i.onload = () => ok(i); i.onerror = () => ok(null); i.src = src })

  const MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
  const DIAS = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
  function hora12(d) {
    let h = d.getHours(); const m = d.getMinutes(); const pm = h >= 12
    h = h % 12 || 12
    return `${h}:${String(m).padStart(2, '0')} ${pm ? 'p. m.' : 'a. m.'}`
  }
  function esHoy(d) { const n = new Date(); return d.toDateString() === n.toDateString() }
  function fechaCorta(d) { return esHoy(d) ? 'Hoy' : `${DIAS[d.getDay()]} ${d.getDate()} ${MESES[d.getMonth()]}` }

  function datos() {
    const pct = Math.max(1, Math.min(90, parseInt($('cu-pct').value || '0', 10) || 0))
    const vence = $('cu-vence').value ? new Date($('cu-vence').value) : new Date()
    let seg = $('cu-seg').value
    if (seg === '__otro') seg = ($('cu-seg-otro').value || '').trim()
    return {
      pct, vence, seg: seg.toUpperCase(),
      cliente: ($('cu-cliente').value || '').trim(),
      asesor: ($('cu-asesor').value || '').trim(),
      codigo: ($('cu-codigo').value || '').trim().toUpperCase(),
      formato: $('cu-formato').value,
    }
  }

  /* Ajusta el tamaño de letra hasta que el texto quepa en `max` px. */
  function fit(ctx, txt, peso, tam, max, estilo = '') {
    let s = tam
    do { ctx.font = `${estilo} ${peso} ${s}px "Exo 2"`.trim(); s -= 1 } while (ctx.measureText(txt).width > max && s > 8)
    return s + 1
  }
  function texto(ctx, txt, x, y, { peso = 800, tam = 20, color = '#fff', alin = 'left', max = 2000, esp = 0, estilo = '' } = {}) {
    fit(ctx, txt, peso, tam, max, estilo)
    ctx.fillStyle = color; ctx.textAlign = alin; ctx.textBaseline = 'alphabetic'
    if (esp && 'letterSpacing' in ctx) ctx.letterSpacing = `${esp}px`
    ctx.fillText(txt, x, y)
    if ('letterSpacing' in ctx) ctx.letterSpacing = '0px'
  }
  function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r) }

  function lampara(ctx, x1, x2, y) {
    const g = ctx.createRadialGradient((x1 + x2) / 2, y, 10, (x1 + x2) / 2, y, (x2 - x1) * 0.55)
    g.addColorStop(0, 'rgba(248,177,51,.26)'); g.addColorStop(1, 'rgba(248,177,51,0)')
    ctx.fillStyle = g; ctx.fillRect(x1 - 200, y, x2 - x1 + 400, 420)
    ctx.save(); ctx.shadowColor = ORO; ctx.shadowBlur = 28
    const t = ctx.createLinearGradient(0, y, 0, y + 14); t.addColorStop(0, '#fff7e3'); t.addColorStop(0.45, '#fff'); t.addColorStop(1, ORO)
    ctx.fillStyle = t; rr(ctx, x1, y, x2 - x1, 14, 7); ctx.fill(); ctx.restore()
    ctx.fillStyle = '#3a3a40'; rr(ctx, x1 - 20, y - 3, 22, 20, 4); ctx.fill(); rr(ctx, x2 - 2, y - 3, 22, 20, 4); ctx.fill()
  }

  function maletas(ctx, x, y, s) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    const cuerpo = (bx, by, w, h) => {
      const g = ctx.createLinearGradient(bx, by, bx + w, by + h); g.addColorStop(0, '#2c2c33'); g.addColorStop(0.45, '#141417'); g.addColorStop(1, '#08080a')
      ctx.fillStyle = g; rr(ctx, bx, by, w, h, 14); ctx.fill()
      ctx.strokeStyle = ORO; ctx.lineWidth = 4; ctx.lineCap = 'round'
      const c = 12
      ctx.beginPath()
      ctx.moveTo(bx + 8, by + 8 + c); ctx.lineTo(bx + 8, by + 8); ctx.lineTo(bx + 8 + c, by + 8)
      ctx.moveTo(bx + w - 8 - c, by + 8); ctx.lineTo(bx + w - 8, by + 8); ctx.lineTo(bx + w - 8, by + 8 + c)
      ctx.moveTo(bx + 8, by + h - 8 - c); ctx.lineTo(bx + 8, by + h - 8); ctx.lineTo(bx + 8 + c, by + h - 8)
      ctx.moveTo(bx + w - 8 - c, by + h - 8); ctx.lineTo(bx + w - 8, by + h - 8); ctx.lineTo(bx + w - 8, by + h - 8 - c)
      ctx.stroke()
    }
    ctx.strokeStyle = '#3a3a42'; ctx.lineWidth = 5; ctx.strokeRect(28, 0, 34, 34)
    cuerpo(0, 30, 92, 132)
    ctx.fillStyle = '#2b2b31'; [18, 74].forEach((cx) => { ctx.beginPath(); ctx.arc(cx, 168, 7, 0, 7); ctx.fill() })
    // etiqueta con escudo ✓
    ctx.save(); ctx.translate(-22, 58); ctx.rotate(-0.14); ctx.fillStyle = ORO; rr(ctx, 0, 0, 30, 24, 5); ctx.fill()
    ctx.strokeStyle = '#0a0a0a'; ctx.lineWidth = 2.6; ctx.lineJoin = 'round'
    ctx.beginPath(); ctx.moveTo(15, 5); ctx.lineTo(22, 8); ctx.lineTo(22, 13); ctx.quadraticCurveTo(22, 17, 15, 21); ctx.quadraticCurveTo(8, 17, 8, 13); ctx.lineTo(8, 8); ctx.closePath(); ctx.stroke()
    ctx.beginPath(); ctx.moveTo(11.5, 13); ctx.lineTo(14, 15.5); ctx.lineTo(18, 11); ctx.stroke(); ctx.restore()
    // celular
    ctx.save(); ctx.translate(104, 110); ctx.rotate(-0.16)
    ctx.fillStyle = '#0c0c0f'; rr(ctx, 0, 0, 34, 64, 7); ctx.fill(); ctx.strokeStyle = ORO; ctx.lineWidth = 3; ctx.stroke()
    ctx.fillStyle = MED; rr(ctx, 5, 6, 24, 52, 4); ctx.fill()
    ctx.strokeStyle = ORO; ctx.lineWidth = 2.6; ctx.beginPath(); [[10, 3], [14, 6], [18, 9], [22, 12]].forEach(([bx, h]) => { ctx.moveTo(bx, 30); ctx.lineTo(bx, 30 - h) }); ctx.stroke()
    texto(ctx, 'eSIM', 17, 44, { peso: 900, tam: 8.5, color: ORO, alin: 'center' }); ctx.restore()
    // chica
    ctx.strokeStyle = '#3a3a42'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(160, 88); ctx.lineTo(160, 74); ctx.arcTo(160, 66, 168, 66, 8); ctx.lineTo(182, 66); ctx.arcTo(190, 66, 190, 74, 8); ctx.lineTo(190, 88); ctx.stroke()
    cuerpo(146, 86, 72, 88)
    ctx.restore()
  }

  /* Pieza base 1600×837 (plantilla de mensaje / adjunto). */
  function dibujarHSM(cv, d) {
    const W = 1600, H = 837
    cv.width = W; cv.height = H
    const ctx = cv.getContext('2d')
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H)
    const r = ctx.createRadialGradient(W / 2, H, 30, W / 2, H, W * 0.62)
    r.addColorStop(0, 'rgba(106,156,217,.45)'); r.addColorStop(0.38, 'rgba(18,53,80,.8)'); r.addColorStop(1, 'rgba(0,0,0,0)')
    ctx.fillStyle = r; ctx.fillRect(0, 0, W, H)
    lampara(ctx, 290, 1310, 22)

    if (imgs.logo) { const h = 150; ctx.drawImage(imgs.logo, 40, 44, imgs.logo.width * h / imgs.logo.height, h) }
    texto(ctx, d.seg || 'CUPÓN ADICIONAL', 900, 92, { peso: 800, tam: 22, color: ORO, alin: 'center', max: 760, esp: 5 })
    texto(ctx, 'BLACK', 890, 174, { peso: 900, tam: 76, color: '#fff', alin: 'right', estilo: 'italic' })
    texto(ctx, 'FRIDAY', 912, 174, { peso: 900, tam: 76, color: ORO, alin: 'left', estilo: 'italic' })

    const fecha = fechaCorta(d.vence), hora = hora12(d.vence)
    // pase
    ctx.save(); ctx.translate(215, 228); ctx.rotate(-2.2 * Math.PI / 180)
    ctx.shadowColor = 'rgba(0,0,0,.75)'; ctx.shadowBlur = 40; ctx.shadowOffsetY = 18
    ctx.fillStyle = '#121214'; rr(ctx, 0, 0, 1040, 440, 26); ctx.fill(); ctx.shadowColor = 'transparent'
    ctx.strokeStyle = '#2a2a30'; ctx.lineWidth = 2; ctx.stroke()
    ctx.fillStyle = '#050506'; ctx.beginPath(); ctx.moveTo(26, 0); ctx.lineTo(780, 0); ctx.lineTo(780, 70); ctx.lineTo(0, 70); ctx.lineTo(0, 26); ctx.arcTo(0, 0, 26, 0, 26); ctx.fill()
    texto(ctx, 'PASE DE ABORDAR', 40, 47, { peso: 900, tam: 25, esp: 6 })
    texto(ctx, 'CUPÓN ADICIONAL · BLACK FRIDAY', 740, 47, { peso: 900, tam: 17, color: ORO, alin: 'right', esp: 3, max: 400 })
    texto(ctx, 'DESDE', 40, 118, { peso: 800, tam: 15, color: '#9aa3ad', esp: 2.4 })
    texto(ctx, 'HOY', 40, 178, { peso: 900, tam: 66 })
    ctx.setLineDash([7, 7]); ctx.strokeStyle = 'rgba(255,255,255,.35)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(200, 158); ctx.lineTo(500, 158); ctx.stroke(); ctx.setLineDash([])
    ctx.fillStyle = ORO; ctx.beginPath(); ctx.ellipse(350, 158, 18, 4, 0, 0, 7); ctx.fill(); ctx.beginPath(); ctx.moveTo(345, 156); ctx.lineTo(337, 146); ctx.lineTo(342, 146); ctx.lineTo(354, 156); ctx.fill(); ctx.beginPath(); ctx.moveTo(345, 160); ctx.lineTo(338, 170); ctx.lineTo(343, 170); ctx.lineTo(354, 160); ctx.fill()
    texto(ctx, 'HASTA', 740, 118, { peso: 800, tam: 15, color: '#9aa3ad', alin: 'right', esp: 2.4 })
    texto(ctx, esHoy(d.vence) ? hora.replace(' p. m.', ' PM').replace(' a. m.', ' AM') : `${d.vence.getDate()} ${MESES[d.vence.getMonth()].toUpperCase()}`, 740, 178, { peso: 900, tam: 62, alin: 'right', max: 260 })
    texto(ctx, 'PARA', 40, 236, { peso: 800, tam: 15, color: '#9aa3ad', esp: 2.4 })
    texto(ctx, d.cliente || 'Ti, viajero', 40, 274, { peso: 800, tam: 32, max: 330 })
    texto(ctx, 'CIERRE DE PUERTA', 40, 324, { peso: 800, tam: 15, color: '#9aa3ad', esp: 2.4 })
    texto(ctx, `${fecha} · ${hora}`, 40, 362, { peso: 900, tam: 32, color: ORO, max: 330 })
    texto(ctx, 'EXTRA', 740, 232, { peso: 900, tam: 20, alin: 'right', esp: 5 })
    texto(ctx, `${d.pct}%`, 752, 360, { peso: 900, tam: 150, color: ORO, alin: 'right', max: 400 })
    texto(ctx, 'DE DESCUENTO ADICIONAL', 740, 400, { peso: 900, tam: 18, alin: 'right', esp: 3, max: 400 })
    ctx.setLineDash([9, 9]); ctx.strokeStyle = '#000'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(782, 20); ctx.lineTo(782, 420); ctx.stroke(); ctx.setLineDash([])
    const tg = ctx.createLinearGradient(0, 0, 0, 440); tg.addColorStop(0, '#ffc54d'); tg.addColorStop(1, ORO)
    ctx.fillStyle = tg; ctx.beginPath(); ctx.moveTo(790, 0); ctx.lineTo(1014, 0); ctx.arcTo(1040, 0, 1040, 26, 26); ctx.lineTo(1040, 414); ctx.arcTo(1040, 440, 1014, 440, 26); ctx.lineTo(790, 440); ctx.fill()
    const talon = [['EMBARQUE', esHoy(d.vence) ? 'Solo por hoy' : `Hasta el ${d.vence.getDate()} ${MESES[d.vence.getMonth()]}`], ['PUERTA', d.asesor ? `Asesor: ${d.asesor}` : 'Tu asesor'], ['ASIENTO', 'Con respaldo']]
    talon.forEach(([l, v], i) => {
      texto(ctx, l, 818, 72 + i * 64, { peso: 800, tam: 14, color: 'rgba(10,10,10,.7)', esp: 2.4 })
      texto(ctx, v, 818, 100 + i * 64, { peso: 900, tam: 24, color: '#0a0a0a', max: 200 })
    })
    ctx.save(); ctx.translate(822, 250); ctx.rotate(-0.12)
    ctx.strokeStyle = '#0a0a0a'; ctx.lineWidth = 4; rr(ctx, 0, 0, 196, 52, 10); ctx.stroke()
    texto(ctx, d.codigo ? `CÓDIGO ${d.codigo}` : 'ÚLTIMO LLAMADO', 98, 35, { peso: 900, tam: 21, color: '#0a0a0a', alin: 'center', max: 176, esp: 2 })
    ctx.restore()
    ctx.fillStyle = '#0a0a0a'; for (let i = 0; i < 27; i++) ctx.fillRect(820 + i * 7.4, 338, i % 3 ? 2.2 : 4.4, 50)
    ctx.restore()

    // beneficios: lo principal primero
    const benef = ['✚  Asistencia médica 24/7', 'eSIM gratis*', 'Salas VIP*']
    let bx = 300
    benef.forEach((b) => { texto(ctx, b, bx, 647, { peso: 800, tam: 21 }); ctx.font = '800 21px "Exo 2"'; bx += ctx.measureText(b).width + 52 })
    maletas(ctx, 26, 560, 1.05)

    // pie
    ctx.fillStyle = '#0a0a0c'; ctx.fillRect(0, H - 80, W, 80); ctx.fillStyle = ORO; ctx.globalAlpha = 0.7; ctx.fillRect(0, H - 80, W, 2); ctx.globalAlpha = 1
    texto(ctx, 'Nuestros aliados', 40, H - 44, { peso: 700, tam: 17, color: '#c8ccd2' })
    texto(ctx, 'en cada detalle', 40, H - 22, { peso: 700, tam: 17, color: '#c8ccd2' })
    let ax = 330
    ;(imgs.aliados || []).forEach((im) => { if (!im) return; const h = 30, w = im.width * h / im.height; ctx.globalAlpha = 0.9; ctx.drawImage(im, ax, H - 56, w, h); ctx.globalAlpha = 1; ax += w + 46 })
    texto(ctx, 'segurosfly.com', W - 40, H - 46, { peso: 900, tam: 26, color: ORO, alin: 'right' })
    texto(ctx, `Adicional al descuento de la web, sobre ese precio · *En planes seleccionados · Válido hasta ${fecha.toLowerCase()} ${hora}`, W - 40, H - 20, { peso: 600, tam: 14, color: '#c8ccd2', alin: 'right', max: 1000 })
  }

  /* Versión chat 1080×1080: la pieza base escalada sobre fondo negro, con título arriba. */
  function dibujarChat(cv, d) {
    const base = document.createElement('canvas'); dibujarHSM(base, d)
    cv.width = 1080; cv.height = 1080
    const ctx = cv.getContext('2d')
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 1080, 1080)
    const r = ctx.createRadialGradient(540, 1080, 30, 540, 1080, 760); r.addColorStop(0, 'rgba(106,156,217,.4)'); r.addColorStop(0.4, 'rgba(18,53,80,.75)'); r.addColorStop(1, 'rgba(0,0,0,0)')
    ctx.fillStyle = r; ctx.fillRect(0, 0, 1080, 1080)
    const gl = ctx.createRadialGradient(540, 120, 10, 540, 120, 520); gl.addColorStop(0, 'rgba(248,177,51,.18)'); gl.addColorStop(1, 'rgba(248,177,51,0)')
    ctx.fillStyle = gl; ctx.fillRect(0, 0, 1080, 300)
    texto(ctx, 'TIENES UN', 540, 150, { peso: 800, tam: 30, color: ORO, alin: 'center', esp: 6 })
    texto(ctx, `${d.pct}% EXTRA`, 540, 240, { peso: 900, tam: 96, color: '#fff', alin: 'center', estilo: 'italic', max: 980 })
    ctx.drawImage(base, 0, 0, 1600, 837, 0, 290, 1080, 565)
    texto(ctx, 'Responde este chat para aplicarlo', 540, 950, { peso: 800, tam: 34, alin: 'center' })
    texto(ctx, 'Adicional al descuento Black Friday de la web', 540, 1000, { peso: 600, tam: 24, color: '#c8ccd2', alin: 'center' })
  }

  async function render() {
    await document.fonts.ready
    await Promise.all([document.fonts.load('900 40px "Exo 2"'), document.fonts.load('italic 900 40px "Exo 2"'), document.fonts.load('800 20px "Exo 2"')])
    const d = datos()
    const cv = $('cu-canvas')
    if (d.formato === 'chat') dibujarChat(cv, d); else dibujarHSM(cv, d)
    $('cu-aviso-pct').textContent = `${d.pct}%`
  }

  function nombreArchivo() {
    const d = datos()
    const f = `${d.vence.getFullYear()}${String(d.vence.getMonth() + 1).padStart(2, '0')}${String(d.vence.getDate()).padStart(2, '0')}`
    const cli = d.cliente ? '-' + d.cliente.normalize('NFD').replace(/[^\w]+/g, '-').toLowerCase().replace(/-+$/,'') : ''
    return `cupon-bf-${d.pct}pct-${f}${cli}-${d.formato === 'chat' ? '1080x1080' : '1600x837'}.jpg`
  }

  async function iniciar() {
    imgs.logo = await cargar(A.logo)
    imgs.aliados = await Promise.all((A.aliados || []).map(cargar))
    // vencimiento por defecto: hoy a las 8:00 p. m. (o mañana si ya pasó)
    const v = new Date(); v.setHours(20, 0, 0, 0); if (v < new Date()) v.setDate(v.getDate() + 1)
    const loc = new Date(v.getTime() - v.getTimezoneOffset() * 60000).toISOString().slice(0, 16)
    $('cu-vence').value = loc
    $('cu-seg').addEventListener('change', () => { $('cu-seg-otro').style.display = $('cu-seg').value === '__otro' ? 'block' : 'none'; render() })
    document.querySelectorAll('#cu-form input, #cu-form select').forEach((el) => el.addEventListener('input', render))
    $('cu-jpg').onclick = async () => {
      await render()
      $('cu-canvas').toBlob((b) => { const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = nombreArchivo(); a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 4000) }, 'image/jpeg', 0.92)
    }
    $('cu-copiar').onclick = async () => {
      await render()
      $('cu-canvas').toBlob(async (b) => {
        try { await navigator.clipboard.write([new ClipboardItem({ 'image/png': b })]); $('cu-copiar').textContent = '¡Copiada!' } catch { $('cu-copiar').textContent = 'Usa «Descargar JPG»' }
        setTimeout(() => ($('cu-copiar').textContent = 'Copiar imagen'), 1800)
      }, 'image/png')
    }
    render()
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar()
})()
