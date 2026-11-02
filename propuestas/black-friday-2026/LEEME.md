# Recursos de campaña · Black Friday 2026

Página para el equipo, igual que `../hero-halloween-2026.html`, con el hero en vivo, el kit
comercial (piezas + mensaje listo para copiar), qué decimos y en qué orden, las semanas, los colores
y las reglas. Al publicarla (push de Wilker) queda en
`https://segurosfly.github.io/Brochures/propuestas/black-friday-2026/`.

**Estado (01/11/2026):** publicada, con el kit de WhatsApp (19 imágenes) y el generador de cupón. El PDF se genera después.

## Una sola fuente de datos: `campana.json`

Todos los textos, la oferta, el legal, los pilares, las piezas, las semanas y los colores viven en
`campana.json`. De ahí salen:

| Salida | Archivo | Cómo |
|---|---|---|
| Página de recursos | `index.html` | `python3 generar.py` |
| Kit de WhatsApp (imágenes) | `piezas/bf_*.jpg` | `python3 generar.py` (dibuja `kit.py`) |
| PDF descargable | `recursos-black-friday-2026.pdf` | `python3 generar.py --pdf` (la misma página impresa, A4 horizontal) |
| Correos (más adelante) | — | Bloque `email` del JSON: qué bloques reutilizar y qué imagen va de cabecera |

Regla: **para cambiar un texto se cambia en `campana.json` y se regenera**; nunca a mano en el HTML
ni en la imagen. Así página, piezas, PDF y correos dicen siempre lo mismo.

## Archivos

- `campana.json` — los datos.
- `generar.py` — dibuja las piezas (SVG → PNG con cairosvg) y llama a `pagina.py`.
- `pagina.py` — arma `index.html`; sus estilos de impresión son los del PDF.
- `hero.html` — copia del prototipo aprobado (`paginaweb-nextjs/docs/temporadas/black-friday-2026-prototipo.html`)
  con la barra de notas oculta; la página lo muestra en un marco.
- `kit.py` — dibuja el kit de WhatsApp desde el bloque `kit` de `campana.json`.
- `piezas/bf_<tema>_chat.jpg` (1080×1080), `bf_<tema>_estado.jpg` (1080×1920) y `bf_general_1600x837.jpg` (plantilla HSM / cabecera de correo).

## Requisitos para regenerar

- Python 3 con `cairosvg` y `Pillow` (`pip install cairosvg pillow`).
- Exo 2 instalada: copiar `SegurosFly-AI-System/01_BRAND/fonts/Exo2-*.otf` a la carpeta de fuentes
  (Mac: doble clic → Instalar; Linux: `~/.fonts` + `fc-cache -f`).
- Para el PDF: Google Chrome o Chromium (en el Mac de Wilker ya está Chrome).

## Kit de WhatsApp para el equipo comercial (01/11/2026)

Las piezas **se hacen aquí**, como el kit de Halloween: nadie externo las entrega (Wilker, 01/11). Bloque `kit` de
`campana.json`: 9 temas (general, anticipación, vuelo en oferta, Europa, Argentina, eSIM, dispositivos/Tech Protection,
familia en diciembre y Cyber Monday 30/11), cada uno con chat 1080×1080 + estado 1080×1920 y su mensaje sugerido; el
general además en 1600×837. En la página: «Copiar imagen» (la pasa a PNG para el portapapeles: pegar con Ctrl/Cmd + V en
WhatsApp Web o Kommo), «Descargar» y «Copiar texto».
Reglas que ya cumplen los textos: «hasta» siempre junto al 75% y a «asistencia de viaje»; asistencia médica 24/7
siempre presente; eSIM y Salas VIP «en planes seleccionados»; Tech Protection como complemento pagado (USD 22/viajero,
nunca «incluido»); Schengen = «cumple los requisitos», nunca «requisito de ingreso»; sin sílabas AN·TI·CÍ·PA·TE.
Para cambiar un texto o agregar un tema: editar `kit.temas` y correr `python3 generar.py`.

## Pieza: pase de abordar — DESCARTADA (01/11/2026)

La versión «hasta 75% · todo noviembre» repetía el descuento de la campaña y no aportaba nada. El pase de
abordar de Halloween funciona porque anuncia un descuento **ADICIONAL** al macro (cupón: 40% hoy hasta las
8 PM para quien sale de mañana a 5 días). Se rehace como cupón adicional real dentro de la **central de
materiales HSM para Kommo**, que se desarrolla aparte: `docs/CENTRAL-MATERIALES-HSM.md` (raíz de
segurosfly-dev). El dibujo (`generar.py → pase_hsm()`) se conserva para reutilizarlo con esos datos.

## Generador de cupón adicional (sección 4 de la página, 01/11/2026)

Lo pidió Wilker: que el equipo comercial ponga el % y salga la imagen lista para adjuntar.
- Archivo: `generador-cupon.js` (se incrusta en `index.html` al regenerar). Dibuja en un `<canvas>` del navegador;
  no envía nada a ningún servidor.
- Campos: % adicional · texto de arriba (segmento: «¿Sales de mañana a 5 días?», «¿Ya tienes tu vuelo?», grupo,
  Europa, «Solo para ti» u otro) · válido hasta (fecha y hora; por defecto hoy 8:00 p. m.) · cliente, asesor y
  código del cupón (opcionales) · formato.
- Salidas: **JPG** 1600×837 (adjunto/plantilla) o 1080×1080 (chat), con nombre
  `cupon-bf-{pct}pct-{fecha}-{cliente}-{tamaño}.jpg`; «Copiar imagen» (PNG al portapapeles).
- La pieza: pase de abordar Black Friday (negro y oro, lámpara, maletas) con «EXTRA {pct}% DE DESCUENTO ADICIONAL»,
  «Asistencia médica 24/7» como primer beneficio y el legal «Adicional al descuento de la web, sobre ese precio».
- **Regla:** el % debe existir como cupón en el CMS con la misma vigencia antes de enviar la imagen (la página lo
  recuerda). El sistema guarda cupones por fecha, sin hora: el «hasta las 8 p. m.» lo cumple el asesor.
- Logo y aliados en blanco salen de `generar.py` (`img64(..., blanco=True)`) al regenerar.

## Pendientes

- Visto bueno de Wilker a la maqueta.
- `piezas/hero_captura.png` (captura del hero para el PDF) y generar el PDF.
