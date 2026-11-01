# Recursos de campaña · Black Friday 2026

Página para el equipo, igual que `../hero-halloween-2026.html`, con el hero en vivo, el kit
comercial (piezas + mensaje listo para copiar), qué decimos y en qué orden, las semanas, los colores
y las reglas. Al publicarla (push de Wilker) queda en
`https://segurosfly.github.io/Brochures/propuestas/black-friday-2026/`.

**Estado (01/11/2026): MAQUETA 1**, pendiente de visto bueno de Wilker. El PDF se genera después.

## Una sola fuente de datos: `campana.json`

Todos los textos, la oferta, el legal, los pilares, las piezas, las semanas y los colores viven en
`campana.json`. De ahí salen:

| Salida | Archivo | Cómo |
|---|---|---|
| Página de recursos | `index.html` | `python3 generar.py` |
| Piezas (imágenes) | `piezas/*.png` (+ `.svg` editable) | `python3 generar.py` |
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
- `piezas/pase_hsm_1600x837.png` — pase de abordar (plantilla de mensaje / cabecera de correo).

## Requisitos para regenerar

- Python 3 con `cairosvg` y `Pillow` (`pip install cairosvg pillow`).
- Exo 2 instalada: copiar `SegurosFly-AI-System/01_BRAND/fonts/Exo2-*.otf` a la carpeta de fuentes
  (Mac: doble clic → Instalar; Linux: `~/.fonts` + `fc-cache -f`).
- Para el PDF: Google Chrome o Chromium (en el Mac de Wilker ya está Chrome).

## Pieza: pase de abordar (Black Friday)

Versión Black Friday del pase de Halloween («Perder este vuelo SÍ da susto»), que los asesores envían a
prospectos. Mismo esquema (pase + talón dorado + beneficios + aliados) con el concepto de noviembre:
fondo negro, lámpara LED, «BLACK FRIDAY» itálica blanco + oro, maletas + celular con eSIM.
- Oferta: **hasta 75% · todo noviembre** (INICIO hoy → FIN 30 nov). No es oferta relámpago: si se
  quiere una por horas o por fecha clave (Buen Fin, Black Friday, Cyber Monday), se agrega otra
  pieza en el JSON con su condición confirmada por Wilker.
- Beneficios: Asistencia médica 24/7 (primero, siempre) · eSIM gratis* · Salas VIP* (*planes seleccionados).
- Aliados del pie: Meta Verified, AirHelp, Priority Pass, Rentcars (en blanco). Koris/Lloyd's no entra:
  su logo solo existe en JPG con fondo.

## Pendientes

- Visto bueno de Wilker a la maqueta.
- Originales de Jéssica (chat 1080×1080, estado 1080×1920, plantilla 1600×837): en el PDF están en
  baja resolución. Se agregan a `piezas/` y se marca `estado: "lista"` en el JSON.
- Versiones del pase para chat (1080×1080) y estado (1080×1920).
- `piezas/hero_captura.png` (captura del hero para el PDF) y generar el PDF.
