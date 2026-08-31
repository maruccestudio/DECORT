---
name: sync-shared-blocks
description: Detecta y corrige deriva en el menu de navegacion y el pie de pagina cuando deben ser identicos entre paginas del sitio DECORT MARUCC. Usar cuando se edite el nav o el footer en una pagina, antes de dar por cerrada la tarea, o cuando se sospeche que alguna pagina quedo desincronizada tras un cambio anterior.
---

# Sincronizar bloques compartidos (nav / footer)

## Por que existe esta skill

Auditado el historial completo del proyecto (274 commits), el patron que
mas veces ha costado tiempo **no es Tailwind**: es la falta de una unica
fuente de verdad para bloques que deben ser identicos en todas las
paginas. Aparece una y otra vez:

- "Fix: unifica @id de LocalBusiness en paginas restantes"
- "Fix: tracking de Meta Pixel en WhatsApp, og:locale y unificacion de NAP"
- "fix: unificar los 3 botones flotantes en una columna derecha"
- Y el 27-08-2026: el footer de `cortinas-a-medida.html` llevaba semanas
  con una paleta de grises distinta (`neutral-500`/`600` en vez de
  `neutral-400`) sin que nadie lo notara.

Cada vez que se edita el nav o el footer a mano en 12-18 archivos, hay
riesgo real de que uno quede desincronizado. Esta skill lo detecta y,
si se pide explicitamente, lo corrige.

## Que SI toca

- `<nav>...</nav>` -- el menu (Colecciones / Showroom / Nosotros / Contacto)
- `<footer>...</footer>` -- datos de contacto, enlaces a colecciones, NAP visible, copyright

## Que NUNCA toca, bajo ningun concepto

Esto es innegociable porque afecta a SEO/GEO. La skill **no opera** sobre:

- `<title>`, `<meta name="description">`, `rel="canonical"`, `hreflang`
- Cualquier bloque `<script type="application/ld+json">` (Service, FAQPage,
  BreadcrumbList, LocalBusiness) -- estos son intencionalmente distintos
  por pagina y una sincronizacion ciega los rompe
- `<h1>` y el contenido principal del `<main>`/body de la pagina
- El bloque "Tambien te puede interesar" -- **cada pagina enlaza a
  colecciones distintas a proposito**, no es candidato a sincronizar
  aunque su HTML se parezca

Si se detecta que el nav o el footer de una pagina concreta tiene
contenido añadido a proposito (ej. `contacto.html` incluye horario y
zona de servicio que las demas paginas no llevan), **no se sincroniza
sin preguntar antes**: puede ser una decision de diseno, no deriva.

## Como usarla

### 1. Comprobar sin tocar nada (modo por defecto, siempre seguro)

```bash
python .claude/skills/sync-shared-blocks/scripts/sync_block.py \
  --tag footer \
  --ref cortinas-blackout.html \
  --targets contacto.html cortinas-a-medida.html cortinas-enrollables.html \
            cortinas-verticales.html estor-de-tela.html motorizacion.html \
            paneles-japoneses.html para-arquitectos.html para-hoteles.html \
            plisadas.html precio-cortinas-a-medida.html showroom-movil.html \
            sobre-nosotros.html venecianas.html visillos.html \
            como-medir-ventana-cortinas.html cortinas-palma-de-mallorca.html
```

Esto **nunca escribe nada**. Solo informa que paginas difieren y muestra
el diff.

### 2. Aplicar la correccion (solo si se decide que la deriva es un bug)

Anadir `--apply` al mismo comando, **dentro de una rama** (el script se
niega a escribir si estas en `main`). Tras aplicar:

1. `npm run build` si el bloque corregido introdujo clases de Tailwind
   nuevas (comprobar con `grep` contra `public/output.css`, recordando
   que los selectores CSS escapan `[`, `]`, `%`, `:` y que este proyecto
   redefine `hover` dentro de un unico `@media(hover:hover)`)
2. Verificar visualmente en el navegador (Playwright/preview) antes de
   comitear: 0 imagenes rotas, 0 enlaces sin `href`, el bloque se ve igual
3. Commit + rama + "subelo" cuando el usuario lo pida, como siempre en
   este proyecto -- nunca push directo a main sin confirmar

### 3. Que hacer si el script dice "AMBIGUO"

Significa que la pagina tiene mas de un `<nav>` o `<footer>` (o ninguno).
No adivinar: mirar el archivo a mano antes de decidir.

## Paginas que NO forman parte del grupo "footer identico"

Verificado el 27-08-2026, no asumir que se puede anadir sin comprobar:

- `index.html` -- footer mas grande, propio de la home
- `curtains-mallorca.html` -- version en ingles, footer con menos columnas
  a proposito (contenido distinto, no traduccion 1:1)
- `aviso-legal.html`, `politica-privacidad.html`, `politica-cookies.html`
  -- footer simplificado, propio de paginas legales
- `contacto.html` -- footer con horario y zona de servicio añadidos;
  pendiente de decision del usuario, no tocar sin preguntar
