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

URL = "proyecto-cortinas-portals-nous.html"
TITLE = "Cortinas motorizadas para ventanales grandes | DECORT"
DESC = "Proyecto real en Mallorca: más de 30 cortinas motorizadas y fruncidas para ventanales grandes, con visillos de lino y poliéster y blackout. En seis semanas."
HERO = "salon-visillos-lino"
HERO_SIZES = "(min-width: 1280px) 1216px, 100vw"

ld = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Article",
            "@id": f"{DOM}/{URL}#article",
            "headline": "Una villa en Portals Nous con cortinas de gran formato",
            "description": DESC,
            "image": [f"{DOM}/public/images/{P}{HERO}-1200.webp", f"{DOM}/public/images/{P}salon-panoramica-1200.webp"],
            "datePublished": "2026-10-23",
            "dateModified": "2026-10-23",
            "inLanguage": "es-ES",
            "author": {"@id": f"{DOM}/#business"},
            "publisher": {"@id": f"{DOM}/#business"},
            "mainEntityOfPage": f"{DOM}/{URL}",
            "about": [
                {"@type": "Thing", "name": "Cortinas fruncidas a medida"},
                {"@type": "Thing", "name": "Visillos de lino"},
                {"@type": "Thing", "name": "Cortinas blackout"},
                {"@type": "Thing", "name": "Cortinas motorizadas con domótica"}
            ],
            "contentLocation": {"@type": "Place", "name": "Portals Nous, Calvià, Mallorca",
                                "address": {"@type": "PostalAddress", "addressLocality": "Portals Nous", "addressRegion": "Islas Baleares", "addressCountry": "ES"}}
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{DOM}/"},
                {"@type": "ListItem", "position": 2, "name": "Proyectos", "item": f"{DOM}/proyectos.html"},
                {"@type": "ListItem", "position": 3, "name": "Villa en Portals Nous", "item": f"{DOM}/{URL}"}
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

V2 = "(min-width: 1024px) 30vw, (min-width: 640px) 50vw, 100vw"
V3 = "(min-width: 1024px) 26vw, (min-width: 640px) 33vw, 50vw"
WIDE = "(min-width: 1280px) 1216px, 100vw"

FICHA = [
    ("Ubicación", "Portals Nous, Calvià"),
    ("Encargo", "Project manager de la obra"),
    ("Cortinas", "Más de 30, fruncidas y motorizadas"),
    ("Plazo", "Mes y medio"),
]


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

BENEFICIOS = [
    ("Un solo interlocutor", "El project manager habló con una persona para todo el capítulo de cortinas: propuesta, medición, confección, montaje y puesta en marcha con la domótica."),
    ("El showroom, en obra", "Llevamos el muestrario completo a la casa. Los tejidos se eligieron con la luz real de cada estancia, no bajo los fluorescentes de una tienda."),
    ("Criterio de confección", "Para cada hueco se decidió qué cortina, qué tejido y qué volumen de frunce. Una propuesta pensada para la arquitectura de la casa, no un catálogo."),
    ("Medición de precisión", "En una obra que se está terminando, cada centímetro cuenta: alturas de techo, cajeados de riel y caída hasta el suelo, tomados uno a uno."),
    ("Domótica resuelta", "Rieles motorizados y motores elegidos para el peso y el ancho de cada paño, preparados para integrarse en el sistema de la vivienda."),
    ("Plazo de obra", "Más de 30 cortinas confeccionadas y montadas en mes y medio, al ritmo de una vivienda que tenía fecha de entrega."),
]
benef = "\n".join(
    f'''                <div class="py-6 border-t border-white/15">
                    <h3 class="text-xl md:text-2xl font-light font-display text-white mb-2">{t}</h3>
                    <p class="text-sm leading-relaxed text-neutral-300 font-body max-w-md">{d}</p>
                </div>''' for t, d in BENEFICIOS)

WA_PRO = 'data-wa-msg="Hola, vengo de vuestra web (proyecto de Portals Nous). Tengo un proyecto de arquitectura o interiorismo y solicito información sobre cortinas."'

# Maquetacion v2 (23-10): rejillas ordenadas, imagen por encima del texto, esquinas opuestas en las destacadas.
# Se inserta en proyecto.py sustituyendo el bloque main = f'''...'''

# Esquinas de marca: dos puntas opuestas muy redondeadas, las otras dos casi rectas.
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

main = f'''
    <article>

    <!-- Apertura -->
    <header class="{SEC} pt-14 md:pt-24 pb-10 md:pb-14">
        <div class="max-w-7xl mx-auto">
            <p class="text-sm font-body text-terracotta-600 mb-6">Proyecto · Portals Nous, Calvià</p>
            <h1 class="text-5xl md:text-7xl lg:text-[6rem] font-light tracking-tight font-display text-neutral-800 leading-[0.95] mb-8 max-w-5xl [text-wrap:balance]">
                Una villa en Portals Nous con <span class="italic text-terracotta-500">cortinas de gran formato</span>
            </h1>
            <p class="text-lg md:text-2xl font-display text-neutral-700 leading-snug max-w-3xl [text-wrap:pretty]">
                Más de treinta cortinas fruncidas y motorizadas para los ventanales grandes de una villa en final de obra: visillos de techo a suelo en la planta baja, blackout decorativo en los dormitorios y todo integrado en la domótica de la casa.
            </p>
        </div>
    </header>

    <figure class="px-4 md:px-12">
        <div class="max-w-7xl mx-auto">
            <img src="/public/images/{P}{HERO}-800.webp" srcset="{hero_srcset}" sizes="{HERO_SIZES}" width="800" height="533" alt="Salón de la villa de Portals Nous con cortinas motorizadas fruncidas que cubren los ventanales grandes de suelo a techo" fetchpriority="high" class="w-full h-auto {FEAT}">
            <figcaption class="mt-3 px-2 text-xs text-neutral-600 font-body">Salón principal. Visillo de lino y poliéster con confección fruncida, motorizado.</figcaption>
        </div>
    </figure>

    {ficha_html(FICHA)}

    <!-- El encargo -->
    <section class="{SEC} pb-10 md:pb-14">
        <div class="max-w-7xl mx-auto">
        {lado(texto('El encargo: <span class="italic text-terracotta-500">gran formato</span> y domótica',
                    'El encargo nos llegó del project manager de la obra, con la casa a punto de entregarse: cortinas para toda la vivienda, a medida, sin margen en el calendario.',
                    'Ventanales grandes, de suelo a techo, paños de más de seis metros y una condición desde el primer día: cortinas motorizadas, integradas en la domótica de la casa.'),
              pic("obra-antes", "La vivienda en obra, con andamios en la fachada y los ventanales ya colocados", S_7, "aspect-[4/5]", FEAT_R, "La casa, semanas antes de la entrega."), align="items-start")}
        </div>
    </section>

    {ancha("fachada", "Fachada blanca de la villa en Portals Nous con grandes ventanales y terrazas en las dos plantas", FEAT, "Ventanales de suelo a techo en las dos plantas.")}

    <!-- La visita -->
    <section class="{SEC} py-20 md:py-28">
        <div class="max-w-7xl mx-auto space-y-14 md:space-y-20">
        {lado(texto('La visita: <span class="italic text-terracotta-500">el showroom</span>, en la obra',
                    'Fuimos a la casa con todos nuestros catálogos. Sobre la mesa del comedor, con la luz real de los ventanales, elegimos confección y tejido para cada estancia: visillos con textura para la planta baja y blackout para los dormitorios, comparados en mano.',
                    'Y desde el primer día, un dato que lo condicionaba todo: <strong class="font-semibold text-neutral-800">la vivienda entera lleva domótica</strong>.'),
              pic("eleccion-visillo", "Manos sosteniendo muestras de visillo de trama abierta en tonos piedra y gris durante la elección de tejidos", S_7, "aspect-[4/5]", FEAT, "Elección del visillo, con la luz de la propia casa."), foto_izq=True)}
            {cuatro([("seleccion-tejidos-comedor", "Tejidos de muestra extendidos sobre la mesa del comedor durante la visita a la obra"),
                     ("tejidos-mesa", "Muestras de visillo desplegadas sobre la mesa del comedor con vistas al jardín"),
                     ("muestras-lino", "Detalle de muestras de tejido plegadas en tonos piedra junto a unas velas"),
                     ("muestras-blackout", "Muestrario de tejidos blackout en tonos gris y topo para los dormitorios")])}
        </div>
    </section>

    <!-- Planta baja -->
    {ancha("salon-panoramica", "Vista panorámica del salón con visillos recogidos a ambos lados de los ventanales", FEAT_R)}

    <section class="{SEC} pt-14 md:pt-20 pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto space-y-14 md:space-y-20">
        {lado(texto('Planta baja: <span class="italic text-terracotta-500">intimidad</span> sin perder la luz',
                    f'Para toda la planta baja, solo visillo: intimidad frente al exterior sin renunciar a la luz de Mallorca. Elegimos un <a href="/visillos.html" {ENLACE}>visillo de mezcla de lino y poliéster</a>, con la textura del lino pero más estable frente al sol y la humedad.',
                    'Son <strong class="font-semibold text-neutral-800">cortinas fruncidas</strong>: pliegues blandos y regulares que, a contraluz, tamizan la luz en lugar de cortarla.'),
              pic("salon-visillo-fruncido", "Sofá del salón frente a los visillos fruncidos con la luz de la tarde", S_7, "aspect-[4/5]", FEAT), align="items-end")}
            {tres([("visillo-sofa", "Visillo en primer plano junto al sofá del salón"),
                   ("paso-visillos-planta-baja", "Paso acristalado de la planta baja vestido con visillos de suelo a techo, con una cortina recién confeccionada en brazos"),
                   ("caida-visillo-suelo", "Bajo del visillo rozando el suelo de piedra")])}
        </div>
    </section>

    <!-- Gran formato -->
    <section class="{SEC} py-20 md:py-28 bg-neutral-900 text-white">
        <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-start">
            <div class="lg:col-span-5 lg:sticky lg:top-10">
                <p class="font-display font-light text-6xl md:text-8xl leading-none text-terracotta-400 mb-2 whitespace-nowrap">6,00 × 3,20 m</p>
                <p class="text-sm text-neutral-400 font-body mb-10">Algunos paños de la planta baja superan los 6 metros de largo.</p>
                {texto('El reto: cortinas de <span class="italic text-terracotta-400">gran formato</span>',
                       'En cortinas para ventanales grandes, lo sencillo se vuelve precisión: mantener el frunce regular en más de seis metros de tejido, que el bajo quede a la misma altura en todo el recorrido y que riel y motor arrastren ese peso con suavidad, día tras día.',
                       'Todo montado en altura, con la casa ya terminada alrededor.', inv=True)}
            </div>
            <div class="lg:col-span-7 space-y-3 md:space-y-6">
                {pic("montaje-gran-formato", "Instalador sobre una escalera montando el visillo de gran formato en el salón", S_7, "aspect-[4/5]", FEAT, "Montaje de los paños de más de 6 m.", inv=True)}
                {dos([("montaje-escalera", "Ajuste del visillo desde la escalera junto al ventanal del salón"),
                      ("visillo-altura-techo", "Visillo colgando desde el techo, de más de tres metros de altura")], "aspect-[2/3]", inv=True)}
                {dos([("cabezal-fruncido", "Detalle del cabezal fruncido del visillo con el mar y la piscina al fondo"),
                      ("pasillo-visillos", "Pasillo acristalado de la planta baja vestido con visillos de suelo a techo")], "aspect-[2/3]", inv=True)}
            </div>
        </div>
    </section>

    <!-- Planta alta -->
    <section class="{SEC} py-20 md:py-28">
        <div class="max-w-7xl mx-auto space-y-14 md:space-y-20">
        {lado(texto('Planta alta: <span class="italic text-terracotta-500">blackout decorativo</span> y visillo',
                    f'En los dormitorios, el encargo cambió: oscuridad total para dormir y privacidad de día. La respuesta fue una doble cortina en cada ventana.',
                    f'Por delante, un <a href="/cortinas-blackout.html" {ENLACE}>blackout decorativo</a> con aspecto textil, que oscurece por completo sin perder calidez. Por detrás, el mismo visillo de la planta baja: de día, la casa se lee como una sola pieza.'),
              pic("dormitorio-lectura", "Lectura junto al ventanal del dormitorio, con la cortina blackout recogida y el visillo dejando pasar la luz", S_7, "aspect-[4/5]", FEAT_R, "Dormitorio: blackout recogido y visillo para el día."), foto_izq=True)}
            {seis([("dormitorio-blackout", "Dormitorio con cortinas blackout en tono topo abiertas hacia el pinar y el mar"),
                     ("dormitorio-blackout-visillo", "Ventanal del dormitorio con cortina blackout y visillo en dos capas"),
                     ("blackout-vista-piscina", "Cortina blackout recogida a mano junto a la terraza con vistas a la piscina y la bahía"),
                     ("dormitorio-terraza", "Cortinas de dormitorio junto a la puerta de la terraza con el jardín al fondo"),
                   ("visillos-luz-suelo", "Visillo del dormitorio a contraluz dibujando franjas de luz sobre el suelo de madera"),
                   ("revision-dormitorio", "Revisión final de las cortinas del dormitorio antes de la entrega")])}
        </div>
    </section>

    <!-- Domotica -->
    {ancha("planta-baja-luz", "Salón y comedor de la planta baja con visillos en todos los ventanales y vistas al jardín", FEAT)}

    <section class="{SEC} pt-14 md:pt-20 pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto">
        {lado(texto('Motorización y <span class="italic text-terracotta-500">domótica</span>',
                    'Son cortinas motorizadas de principio a fin: cada paño lleva su riel eléctrico, con el motor dimensionado para su ancho y su peso, y preparado para integrarse en el sistema de la vivienda.',
                    f'Nadie tiene que tirar de una cortina de seis metros: el salón se abre por la mañana y los dormitorios se oscurecen por la noche sin tocar un tejido. Más en <a href="/motorizacion.html" {ENLACE}>motorización de cortinas</a>.'),
              dos([("medicion-obra", "Medición del ventanal en obra con cinta métrica y el plano acotado en una tableta"),
                   ("motores-riel", "Motores de cortina instalados en el riel del techo, cableados para la domótica antes de colgar los paños")], "aspect-[2/3]"))}
        </div>
    </section>

    <!-- Plazo -->
    <section class="{SEC} pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto">
            <div class="max-w-2xl mb-10 md:mb-14">
                {texto('Más de 30 cortinas en <span class="italic text-terracotta-500">mes y medio</span>',
                       'De la confirmación del presupuesto a la última cortina colgada pasaron seis semanas. Un plazo así solo es posible cuando la medición es buena a la primera y quien confecciona es quien monta.')}
            </div>
            {tres([("preparacion-cortinas", "Preparación de las cortinas confeccionadas sobre el sofá antes del montaje"),
                     ("ajuste-visillo", "Ajuste a mano del visillo en el salón junto al sofá"),
                     ("entrega-visillos", "Entrada de la casa con los visillos ya montados")])}
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

    <section class="px-4 md:px-12 pt-20 md:pt-28 pb-6 md:pb-8">
        <div class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-2 gap-6">
            {pic("pasillo-final", "Pasillo acristalado con visillos de suelo a techo a lo largo de todo el recorrido", "(min-width: 1280px) 600px, (min-width: 640px) 50vw, 100vw", "aspect-[3/4]", FEAT)}
            {pic("salon-lampara", "Salón con visillos y cortinas recogidas junto a los ventanales, con vistas al mar y una gran lámpara de fibras", "(min-width: 1280px) 600px, (min-width: 640px) 50vw, 100vw", "aspect-[3/4]", FEAT_R)}
        </div>
    </section>
    {ancha("salon-vista-general", "Vista general del salón con visillos a ambos lados de la chimenea y el sofá en L", FEAT_R, "Villa en Portals Nous, entregada.")}

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
            <p class="text-base text-white/90 max-w-xl mx-auto mb-10 font-body leading-relaxed">Contáctanos y te ayudaremos. Vamos a la obra con el muestrario, proponemos confecciones y tejidos, resolvemos la motorización y entregamos montado, en toda Mallorca.</p>
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
            (f"{P}{HERO}-800.webp", hero_srcset, HERO_SIZES)) + body_open + crumbs([("Inicio", "/"), ("Proyectos", "/proyectos.html"), ("Villa en Portals Nous", None)]) + main + tail
(ROOT / URL).write_text(page, encoding="utf-8")

# El indice (proyectos.html) se edita a mano: lista varios proyectos y este script lo sobrescribiria.
print("ok", URL)
