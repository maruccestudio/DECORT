# Genera proyecto-cortinas-portals-nous.html y proyectos.html sobre el andamiaje de showroom-movil.html
import re, sys
from pathlib import Path
from PIL import Image

ROOT = Path(sys.argv[1])
S = (ROOT / "showroom-movil.html").read_text(encoding="utf-8")
DOM = "https://www.decortmarucc.com"
IMG = ROOT / "public/images"

top = S[:S.index("<title>")]
common_head = S[S.index("<script>\n(function () {"):S.index("</head>")]
body_open = S[S.index("<body"):S.index("    <!-- Breadcrumb -->")]
tail = S[S.index("    </main>"):]

WA_SVG = re.search(r'<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">.*?</svg>', S, re.S).group(0)
TEL_SVG = re.search(r'(<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"[^>]*><path[^>]*d="M13\.832.*?</svg>)', S, re.S).group(1)
CHEV = '<li><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" class="ico-svg" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m9 18l6-6l-6-6"/></svg></li>'
WA_HREF = "https://wa.me/34641354788?text=Hola%2C%20me%20gustar%C3%ADa%20pedir%20presupuesto"
P = "portals-nous-"


def widths(name):
    # solo "<nombre>-<ancho>": sin esto "dormitorio-blackout" recogia tambien "dormitorio-blackout-visillo"
    return sorted({int(p.stem[len(P + name) + 1:]) for p in IMG.glob(f"{P}{name}-*.webp") if p.stem[len(P + name) + 1:].isdigit()})


def img(name, alt, sizes, eager=False, cls="w-full h-auto"):
    ws = widths(name)
    assert ws, name
    mid = ws[1] if len(ws) > 1 else ws[0]
    w, h = Image.open(IMG / f"{P}{name}-{mid}.webp").size
    srcset = ", ".join(f"/public/images/{P}{name}-{x}.webp {x}w" for x in ws)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="/public/images/{P}{name}-{mid}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}" {load} class="{cls}">')


def fig(name, alt, cap=None, sizes="(min-width: 1024px) 40vw, (min-width: 640px) 50vw, 100vw", cls="", eager=False, rounded="rounded-2xl"):
    c = f'\n                <figcaption class="mt-3 text-xs leading-relaxed text-neutral-600 font-body">{cap}</figcaption>' if cap else ""
    return f'''<figure class="{cls}">
                {img(name, alt, sizes, eager, "w-full h-auto " + rounded)}{c}
            </figure>'''


def prose(*paras):
    return "\n".join(f'<p class="text-base md:text-[17px] leading-[1.75] text-neutral-700 font-body mb-6 [text-wrap:pretty]">{p}</p>' for p in paras)


def h2(t):
    return f'<h2 class="text-3xl md:text-5xl font-light tracking-tight font-display text-neutral-800 leading-[1.05] mb-8 [text-wrap:balance]">{t}</h2>'


FAQ = [
    ("¿Se pueden motorizar cortinas fruncidas?",
     "Sí. El frunce se cose sobre una cinta que se engancha a los carros del riel motorizado, igual que en una cortina manual. Lo que cambia es el cálculo: el motor se elige según el ancho y el peso de cada paño, y el riel se deja preparado para que la cortina abra y cierre siempre con el mismo pliegue."),
    ("¿Cuánto se tarda en vestir una vivienda completa?",
     "Depende del número de cortinas y de los tejidos. En esta villa de Portals Nous fueron más de 30 cortinas, con visillos de gran formato y blackout en los dormitorios, y se confeccionaron y montaron en mes y medio desde la confirmación del presupuesto."),
    ("¿Trabajáis con project managers, arquitectos e interioristas?",
     "Sí. Visitamos la obra con el muestrario completo, proponemos confecciones y tejidos para cada estancia, coordinamos con la domótica y con el resto de gremios, y entregamos la vivienda con las cortinas montadas y funcionando. Un solo interlocutor para todo el capítulo de cortinas."),
]


def faq_html():
    out = []
    for q, a in FAQ:
        out.append(f'''                <details class="group border-b border-arena-300/60">
                    <summary class="flex justify-between items-center cursor-pointer text-sm font-semibold font-body text-neutral-700 py-5 list-none select-none">
                        <span>{q}</span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" class="ico-svg text-terracotta-400 group-open:hidden shrink-0 ml-4" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14m-7-7v14"/></svg>
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" class="ico-svg text-terracotta-400 hidden group-open:block shrink-0 ml-4" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14"/></svg>
                    </summary>
                    <p class="text-sm text-neutral-600 pb-5 leading-relaxed font-body">{a}</p>
                </details>''')
    return "\n".join(out)


def head(title, desc, url, og_img, ld, preload=None):
    pre = f'\n    <link rel="preload" as="image" href="/public/images/{preload[0]}" imagesrcset="{preload[1]}" imagesizes="{preload[2]}">' if preload else ""
    return f'''{top}<title>{title}</title>
    <meta name="description" content="{desc}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{DOM}/public/images/{og_img}">
    <meta property="og:image:alt" content="{title}">
    <meta property="og:url" content="{DOM}/{url}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="DECORT MARUCC">
    <meta property="og:locale" content="es_ES">
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{DOM}/public/images/{og_img}">{pre}
    <link rel="canonical" href="{DOM}/{url}">
    <link rel="preload" href="/public/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/public/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="/public/output.css">
    <script type="application/ld+json">
{ld}
    </script>
    {common_head}</head>
'''


def crumbs(items):
    lis = []
    for i, (name, href) in enumerate(items):
        if href:
            lis.append(f'<li><a href="{href}" class="hover:text-terracotta-500 transition-colors">{name}</a></li>')
        else:
            lis.append(f'<li class="text-neutral-700 font-medium">{name}</li>')
        if i < len(items) - 1:
            lis.append(CHEV)
    return f'''    <!-- Breadcrumb -->
    <nav aria-label="Ruta de navegación" class="px-6 md:px-12 py-3 border-b border-arena-400/20 bg-arena-50">
        <ol class="flex items-center gap-2 text-[11px] font-body text-neutral-600 max-w-7xl mx-auto">
            {"".join(lis)}
        </ol>
    </nav>

    <main id="contenido">
'''


import json


FEAT = "rounded-tl-[48px] md:rounded-tl-[110px] rounded-br-[48px] md:rounded-br-[110px] rounded-tr-[8px] rounded-bl-[8px]"
FEAT_R = "rounded-tr-[48px] md:rounded-tr-[110px] rounded-bl-[48px] md:rounded-bl-[110px] rounded-tl-[8px] rounded-br-[8px]"
SOFT = "rounded-[8px]"

S_FULL = "(min-width: 1280px) 1216px, 100vw"
S_7 = "(min-width: 1024px) 700px, 100vw"
S_HALF = "(min-width: 1024px) 600px, 50vw"
S_3 = "(min-width: 1024px) 400px, (min-width: 640px) 33vw, 50vw"


def pic(name, alt, sizes, aspect, round_=SOFT, cap=None, cls="", inv=False):
    capc = "text-neutral-400" if inv else "text-neutral-600"
    c = f'<figcaption class="mt-3 text-xs {capc} font-body">{cap}</figcaption>' if cap else ""
    return (f'<figure class="{cls}">{img(name, alt, sizes, False, f"w-full h-auto {aspect} object-cover {round_}")}{c}</figure>')


def tres(items, inv=False):
    """Tres fotos iguales en fila; en movil, dos arriba y la tercera apaisada debajo."""
    a, b, c = items
    return f'''<div class="grid grid-cols-2 sm:grid-cols-3 gap-3 md:gap-6">
                {pic(*a, S_3, "aspect-[3/4]", inv=inv)}
                {pic(*b, S_3, "aspect-[3/4]", inv=inv)}
                {pic(*c, S_3, "aspect-[3/2] sm:aspect-[3/4]", cls="col-span-2 sm:col-span-1", inv=inv)}
            </div>'''


def seis(items):
    """Seis fotos iguales: 3 x 2 en escritorio, 2 x 3 en movil."""
    fotos = "\n                ".join(pic(n, a, "(min-width: 1024px) 400px, 50vw", "aspect-[3/4]") for n, a in items)
    return f'''<div class="grid grid-cols-2 lg:grid-cols-3 gap-3 md:gap-6">
                {fotos}
            </div>'''


def cuatro(items):
    """Cuatro fotos iguales: 2 x 2 en movil, en fila en escritorio."""
    fotos = "\n                ".join(pic(n, a, "(min-width: 1024px) 300px, 50vw", "aspect-[3/4]") for n, a in items)
    return f'''<div class="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-6">
                {fotos}
            </div>'''


def dos(items, aspect="aspect-[4/5]", inv=False):
    a, b = items
    return f'''<div class="grid grid-cols-2 gap-3 md:gap-6">
                {pic(*a, S_HALF, aspect, inv=inv)}
                {pic(*b, S_HALF, aspect, inv=inv)}
            </div>'''


def texto(titulo, *paras, inv=False):
    col = "text-white" if inv else "text-neutral-800"
    pc = "text-neutral-300" if inv else "text-neutral-700"
    ps = "\n".join(f'<p class="text-base leading-[1.75] {pc} font-body mb-5 [text-wrap:pretty]">{p}</p>' for p in paras)
    return f'''<h2 class="text-3xl md:text-[2.75rem] font-light tracking-tight font-display {col} leading-[1.05] mb-6 [text-wrap:balance]">{titulo}</h2>
                {ps}'''


def lado(texto_html, foto_html, foto_izq=False, align="items-center"):
    """Texto (5 col) junto a una foto grande (7 col), centrados en vertical."""
    t = f'<div class="lg:col-span-5 [&>p:last-child]:mb-0 {"lg:order-2 lg:pl-6" if foto_izq else "lg:pr-6"}">\n                {texto_html}\n            </div>'
    f = f'<div class="lg:col-span-7 {"lg:order-1" if foto_izq else ""}">{foto_html}</div>'
    return f'''<div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 {align}">
            {t}
            {f}
        </div>'''


def ancha(name, alt, round_, cap=None):
    return f'''<figure class="px-4 md:px-12">
        <div class="max-w-7xl mx-auto">
            {img(name, alt, S_FULL, False, "w-full h-auto " + round_)}
            {f'<figcaption class="mt-3 px-2 text-xs text-neutral-600 font-body">{cap}</figcaption>' if cap else ""}
        </div>
    </figure>'''


ENLACE = 'class="text-terracotta-600 underline underline-offset-4 decoration-terracotta-300 hover:decoration-terracotta-600"'
SEC = "px-6 md:px-12"


def ficha_html(items):
    """Datos clave del proyecto en una sola franja (Leandro: pocos datos, que la gente no lee tanto)."""
    filas = "\n".join(
        f'''                <div>
                    <dt class="text-xs font-medium text-terracotta-600 font-body mb-1">{k}</dt>
                    <dd class="text-base md:text-lg font-display text-neutral-800 leading-snug">{v}</dd>
                </div>''' for k, v in items)
    return f'''<section aria-labelledby="datos" class="px-6 md:px-12 py-10 md:py-14">
        <h2 id="datos" class="sr-only">Datos del proyecto</h2>
        <dl class="max-w-7xl mx-auto grid grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-6 border-y border-arena-300/70 py-6 md:py-8">
{filas}
        </dl>
    </section>'''

# ---------------------------------------------------------------------------
# Proyecto: reforma integral junto al Pueblo Espanol (Palma)
# (cabecera, consentimiento, menu y pie: andamiaje de showroom-movil.html)
# ---------------------------------------------------------------------------
P = "reforma-palma-"
URL = "proyecto-cortinas-reforma-palma.html"
TITLE = "Cortinas de lino para dormitorio y comedor en Palma | DECORT"
DESC = "Reforma integral junto al Pueblo Español, en Palma: cortinas fruncidas de lino en mezcla, blackout para los dormitorios y ventanales de 3 metros en el comedor."
HERO = "dormitorio-vigas-panoramica"
HERO_SIZES = "(min-width: 1280px) 1216px, 100vw"

FAQ = [
    ("¿Se pueden poner cortinas en un techo inclinado con vigas?",
     "Sí. Cuando el techo no permite un riel en el foseado, el riel va a la pared con soportes. En esta reforma de Palma usamos soporte doble para llevar dos rieles, visillo y blackout, en negro a juego con la iluminación y los interruptores de la casa."),
    ("¿Cuánto se tarda en poner cortinas en una reforma integral?",
     "Depende del número de cortinas y de los tejidos. En esta vivienda junto al Pueblo Español, de la confirmación del presupuesto al montaje pasó menos de un mes: medimos, confeccionamos y montamos nosotros."),
    ("¿Qué cortinas oscurecen un dormitorio por completo?",
     "Un blackout confeccionado a medida, con el riel en el foseado o por encima del marco y los paños un poco más anchos que la ventana. Con un visillo por detrás, el dormitorio queda a oscuras para el descanso y con privacidad durante el día."),
]

ld = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Article",
            "@id": f"{DOM}/{URL}#article",
            "headline": "Reforma integral junto al Pueblo Español: cortinas de lino para toda la casa",
            "description": DESC,
            "image": [f"{DOM}/public/images/{P}{HERO}-1200.webp", f"{DOM}/public/images/{P}comedor-ventanal-grande-1200.webp"],
            "datePublished": "2026-10-25",
            "dateModified": "2026-10-25",
            "inLanguage": "es-ES",
            "author": {"@id": f"{DOM}/#business"},
            "publisher": {"@id": f"{DOM}/#business"},
            "mainEntityOfPage": f"{DOM}/{URL}",
            "about": [
                {"@type": "Thing", "name": "Cortinas de lino a medida"},
                {"@type": "Thing", "name": "Cortinas blackout para dormitorio"},
                {"@type": "Thing", "name": "Cortinas para comedor"},
                {"@type": "Thing", "name": "Cortinas fruncidas"}
            ],
            "contentLocation": {"@type": "Place", "name": "Palma, Mallorca",
                                "address": {"@type": "PostalAddress", "addressLocality": "Palma", "addressRegion": "Islas Baleares", "addressCountry": "ES"}}
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{DOM}/"},
                {"@type": "ListItem", "position": 2, "name": "Proyectos", "item": f"{DOM}/proyectos.html"},
                {"@type": "ListItem", "position": 3, "name": "Reforma integral en Palma", "item": f"{DOM}/{URL}"}
            ]
        },
        {
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]
        }
    ]
}, ensure_ascii=False, indent=4)

hero_ws = widths(HERO)
hero_srcset = ", ".join(f"/public/images/{P}{HERO}-{x}.webp {x}w" for x in hero_ws)

FICHA = [
    ("Ubicación", "Junto al Pueblo Español, Palma"),
    ("Encargo", "Project manager de la promoción"),
    ("Alcance", "Reforma integral: toda la vivienda"),
    ("Plazo", "Menos de un mes"),
]

BENEFICIOS = [
    ("El showroom, en obra", "Las telas se eligieron en la propia casa, con su luz y sus materiales, y el presupuesto salió de esa visita."),
    ("Un solo interlocutor", "Medición, confección y montaje con nuestro equipo, coordinado con el project manager."),
    ("Una solución por techo", "Riel en el foseado donde se podía y riel a pared con soporte doble bajo las vigas."),
    ("Acabado de taller", "Confección fruncida, bajos de 10 cm y costuras invisibles en todos los paños."),
]
benef = "\n".join(
    f'''                <div class="py-6 border-t border-white/15">
                    <h3 class="text-xl md:text-2xl font-light font-display text-white mb-2">{t}</h3>
                    <p class="text-sm leading-relaxed text-neutral-300 font-body max-w-md">{d}</p>
                </div>''' for t, d in BENEFICIOS)

WA_PRO = 'data-wa-msg="Hola, vengo de vuestra web (proyecto de reforma en Palma). Tengo un proyecto de arquitectura o interiorismo y solicito información sobre cortinas."'

main = f'''
    <article>

    <!-- Apertura -->
    <header class="{SEC} pt-14 md:pt-24 pb-10 md:pb-14">
        <div class="max-w-7xl mx-auto">
            <p class="text-sm font-body text-terracotta-600 mb-6">Proyecto · Palma</p>
            <h1 class="text-5xl md:text-7xl lg:text-[6rem] font-light tracking-tight font-display text-neutral-800 leading-[0.95] mb-8 max-w-5xl [text-wrap:balance]">
                Reforma integral junto al Pueblo Español: <span class="italic text-terracotta-500">cortinas de lino para toda la casa</span>
            </h1>
            <p class="text-lg md:text-2xl font-display text-neutral-700 leading-snug max-w-3xl [text-wrap:pretty]">
                Cortinas fruncidas en lino en mezcla para una vivienda reformada de arriba abajo en Palma: oscurecimiento total en los dormitorios, ventanales de tres metros en el comedor y una casa entera en tonos naturales.
            </p>
        </div>
    </header>

    <figure class="px-4 md:px-12">
        <div class="max-w-7xl mx-auto">
            <img src="/public/images/{P}{HERO}-800.webp" srcset="{hero_srcset}" sizes="{HERO_SIZES}" width="800" height="450" alt="Dormitorio con techo de vigas vistas y cortinas de lino en mezcla de suelo a techo en una vivienda reformada en Palma" fetchpriority="high" class="w-full h-auto aspect-[16/9] object-cover {FEAT}">
            <figcaption class="mt-3 px-2 text-xs text-neutral-600 font-body">Dormitorio bajo vigas: visillo de lino en mezcla y blackout, con confección fruncida.</figcaption>
        </div>
    </figure>

    {ficha_html(FICHA)}

    <!-- El encargo -->
    <section class="{SEC} pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto">
        {lado(texto('El encargo: <span class="italic text-terracotta-500">toda la vivienda</span>',
                    'El project manager de la promoción nos encargó las cortinas de una reforma integral en Palma, junto al Pueblo Español. Una casa reformada de arriba abajo, con una paleta de tonos naturales que las cortinas tenían que continuar.',
                    'Llevamos el showroom móvil a la obra. Las telas y las confecciones se decidieron allí mismo, con la luz de cada estancia, y de esa visita salió el presupuesto.'),
              pic("ajuste-visillo-ventana", "Ajuste a mano de un visillo de lino en mezcla junto a la ventana de un dormitorio", S_7, "aspect-[4/5]", FEAT_R, "Visillo de lino en mezcla, ajustado a mano."), align="items-start")}
        </div>
    </section>

    <!-- Dormitorios -->
    <section class="{SEC} pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto space-y-14 md:space-y-20">
        {lado(texto('Dormitorios: <span class="italic text-terracotta-500">oscurecimiento total</span> y privacidad',
                    f'En cada dormitorio, dos capas. Un <a href="/cortinas-blackout.html" {ENLACE}>blackout</a> que deja la habitación a oscuras para el descanso, y por detrás un <a href="/visillos.html" {ENLACE}>visillo de lino en mezcla</a> que da privacidad durante el día sin quitar la luz.',
                    'Todas son <strong class="font-semibold text-neutral-800">cortinas fruncidas</strong>, con bajos de 10 cm y costuras invisibles: el paño cae limpio de techo a suelo, sin marcas a la vista.'),
              pic("dormitorio-vigas-visillo", "Dormitorio con vigas vistas, visillo de lino en mezcla y cortinas blackout a los lados de la ventana", S_7, "aspect-[4/5]", FEAT), foto_izq=True, align="items-end")}
            {cuatro([("dormitorio-abrir-visillo", "Dormitorio con visillo de lino en mezcla delante de la ventana y cortina blackout recogida"),
                     ("dormitorio-luz-tamizada", "Luz tamizada por un visillo de lino en mezcla en un dormitorio de tonos naturales"),
                     ("dormitorio-blackout-visillo", "Cortina blackout y visillo en el mismo riel de un dormitorio"),
                     ("textura-blackout-lino", "Detalle de la caída de una cortina en tono arena junto a la ventana")])}
        </div>
    </section>

    <!-- Comedor: bloque oscuro -->
    <section class="{SEC} py-20 md:py-28 bg-neutral-900 text-white">
        <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-start">
            <div class="lg:col-span-5 lg:sticky lg:top-10">
                <p class="font-display font-light text-6xl md:text-8xl leading-none text-terracotta-400 mb-2 whitespace-nowrap">3,00 × 3,05 m</p>
                <p class="text-sm text-neutral-400 font-body mb-10">Cada uno de los dos ventanales del comedor.</p>
                {texto('Comedor: <span class="italic text-terracotta-400">ventanales grandes</span>, solo visillo',
                       'En el comedor, dos ventanales de tres metros de ancho por más de tres de alto. Aquí la casa pedía luz, así que solo visillo de lino en mezcla: tamiza el sol de la tarde y da intimidad hacia el exterior.',
                       'En cortinas para ventanales grandes, el detalle se nota más: un frunce regular de punta a punta y un bajo que cae igual en todo el ancho.', inv=True)}
            </div>
            <div class="lg:col-span-7 space-y-3 md:space-y-6">
                {pic("comedor-ventanal-grande", "Comedor con ventanales de suelo a techo vestidos con visillo de lino en mezcla", S_7, "aspect-[4/5]", FEAT, "Uno de los dos ventanales del comedor.", inv=True)}
                {dos([("comedor-ventanal-correderas", "Visillo de lino en mezcla recogido junto a las correderas del comedor"),
                      ("ventanal-desde-la-puerta", "Vista desde la puerta de un dormitorio con vigas hacia el ventanal con visillo")], "aspect-[2/3]", inv=True)}
            </div>
        </div>
    </section>

    <!-- Techos con vigas -->
    <section class="{SEC} py-20 md:py-28">
        <div class="max-w-7xl mx-auto space-y-14 md:space-y-20">
        {lado(texto('Techos con vigas: <span class="italic text-terracotta-500">riel a pared en negro</span>',
                    'Donde el techo era inclinado, con vigas vistas, no había foseado para esconder el riel. La solución fue un riel a pared con soporte doble, para llevar el blackout y el visillo en la misma ventana.',
                    'Lo elegimos en negro, a juego con la iluminación y los interruptores de la vivienda: el riel pasa a formar parte del diseño en lugar de esconderse.'),
              pic("riel-negro-pared-vigas", "Riel negro a pared con soporte doble bajo un techo de vigas vistas", S_7, "aspect-[4/5]", FEAT_R), align="items-start")}
            {dos([("cabezal-riel-negro", "Cabezal fruncido de un visillo colgado de un riel negro"),
                  ("dormitorio-techo-inclinado", "Dormitorio con techo inclinado de vigas y cortinas de suelo a techo")], "aspect-[4/5]")}
        </div>
    </section>

    <!-- Foseados iluminados -->
    <section class="{SEC} pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto">
            <div class="max-w-2xl mb-10 md:mb-14">
                {texto('Foseados <span class="italic text-terracotta-500">iluminados</span>',
                       'Donde el techo lo permitía, el riel va dentro del foseado. La luz indirecta baña el tejido desde arriba y la cortina se lee como una pared de lino, de suelo a techo.')}
            </div>
            {cuatro([("foseado-luz-visillo", "Visillo de lino en mezcla bañado por la luz de un foseado iluminado"),
                     ("foseado-escritorio", "Cortina en un foseado iluminado junto a un escritorio de madera"),
                     ("foseado-ventana", "Cortina de lino en mezcla colgada de un foseado con luz junto a la ventana"),
                     ("dormitorio-foseado-luz", "Dormitorio con cortinas de pared a pared bajo un foseado iluminado")])}
        </div>
    </section>

    <!-- Montaje y plazo -->
    <section class="{SEC} pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto space-y-14 md:space-y-20">
        {lado(texto('Montaje en <span class="italic text-terracotta-500">menos de un mes</span>',
                    'Al ser una obra pequeña, de la confirmación del presupuesto a la última cortina colgada pasó menos de un mes. Medimos, confeccionamos y montamos con nuestro propio equipo.',
                    'Cada paño se cuelga, se ajusta y se revisa en la casa antes de entregarla.'),
              pic("luz-al-fondo", "Vista desde la puerta de un dormitorio con vigas hacia un ventanal con visillo y luz natural", S_7, "aspect-[4/5]", FEAT), foto_izq=True, align="items-end")}
            {tres([("montaje-escalera", "Montaje de un visillo de lino en mezcla desde una escalera"),
                   ("colgando-visillo", "Colgando un visillo en el riel junto al techo"),
                   ("detalle-visillo-lino", "Detalle de la trama de un visillo de lino en mezcla a contraluz")])}
        </div>
    </section>

    <!-- Lo que recibio el cliente -->
    <section class="{SEC} py-20 md:py-28 bg-neutral-900 text-white">
        <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16">
            <div class="lg:col-span-4">
                <h2 class="text-3xl md:text-5xl font-light tracking-tight font-display leading-[1.05] [text-wrap:balance]">Lo que recibió <span class="italic text-terracotta-400">el cliente</span></h2>
            </div>
            <div class="lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-x-12">
{benef}
            </div>
        </div>
    </section>

    </article>

    <!-- FAQ -->
    <section class="px-6 md:px-12 py-20 md:py-28">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl md:text-4xl font-light tracking-tight font-display text-neutral-800 mb-8">Preguntas sobre este proyecto</h2>
{faq_html()}
        </div>
    </section>

    <!-- CTA profesionales -->
    <section id="cta-final" class="py-20 md:py-28 px-6 md:px-12 bg-terracotta-600 text-white">
        <div class="max-w-3xl mx-auto text-center">
            <h2 class="text-3xl md:text-5xl font-light tracking-tight font-display mb-6 leading-tight [text-wrap:balance]">¿Eres project manager, arquitecto o interiorista y necesitas cortinas para tu proyecto?</h2>
            <p class="text-base text-white/90 max-w-xl mx-auto mb-10 font-body leading-relaxed">Contáctanos y te ayudaremos. Vamos a la obra con el muestrario, proponemos confecciones y tejidos, resolvemos cada techo y entregamos montado, en toda Mallorca.</p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <a href="{WA_HREF}" {WA_PRO} target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-3 px-10 py-4 bg-white text-terracotta-700 hover:bg-arena-100 rounded-full text-xs font-semibold uppercase tracking-widest transition duration-300 font-body">
                    {WA_SVG} Hablar de tu proyecto
                </a>
                <a href="tel:+34641354788" class="inline-flex items-center gap-3 px-10 py-4 border border-white/40 hover:border-white text-white rounded-full text-xs font-semibold uppercase tracking-widest transition duration-300 font-body">
                    {TEL_SVG}
                    +34 641 35 47 88
                </a>
            </div>
            <p class="mt-8 text-sm font-body"><a href="/para-arquitectos.html" class="underline underline-offset-4 decoration-white/50 hover:decoration-white">Cómo trabajamos con estudios y obras</a></p>
        </div>
    </section>

'''

page = head(TITLE, DESC, URL, f"{P}{HERO}-1200.webp", ld,
            (f"{P}{HERO}-800.webp", hero_srcset, HERO_SIZES)) + body_open + crumbs([("Inicio", "/"), ("Proyectos", "/proyectos.html"), ("Reforma integral en Palma", None)]) + main + tail
(ROOT / URL).write_text(page, encoding="utf-8")
print("ok", URL)
