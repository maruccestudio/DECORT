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
# Proyecto: finca Can Ferragut (Ponent, Mallorca), cortinas mediterraneas de lino blanco
# (cabecera, consentimiento, menu y pie: andamiaje de showroom-movil.html)
# ---------------------------------------------------------------------------
P = "can-ferragut-"
URL = "proyecto-cortinas-mediterraneas-can-ferragut.html"
TITLE = "Visillos blancos de lino para una casa rústica | DECORT"
DESC = "Finca Can Ferragut, en Ponent (Mallorca): visillos blancos de lino en toda la casa, herrajes negros bajo vigas de madera y estores enrollables. En un mes."
# Portada vertical (elegida por Leandro): el arco con las vigas y los visillos al fondo
HERO = "arco-comedor-visillos"
HERO_SIZES = "(min-width: 1024px) 600px, 100vw"

FAQ = [
    ("¿Qué cortinas quedan bien en una casa rústica?",
     "Las que acompañan en lugar de imponerse: tejidos naturales como el lino, colores claros que hagan de contrapunto a la madera y la piedra, y herrajes discretos. En esta casa de Can Ferragut, visillo de lino blanco con riel y barras en negro, a juego con la carpintería y las vigas."),
    ("¿Se puede poner solo visillo en un dormitorio?",
     "Sí, si no se busca oscuridad total. El visillo da privacidad y tamiza la luz del sol sin oscurecer la habitación. Es lo que eligió la clienta en toda la casa; si más adelante quisiera oscurecer, se puede añadir un blackout en un segundo riel."),
    ("¿Qué se pone donde el techo es muy bajo?",
     "Donde no hay altura para que una cortina caiga con proporción, un estor enrollable se coloca dentro del hueco o pegado al marco y libera el espacio. En esta casa lo usamos en la zona de techo bajo, con el resto de la vivienda en visillo."),
]

ld = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Article",
            "@id": f"{DOM}/{URL}#article",
            "headline": "Cortinas mediterráneas para la finca Can Ferragut, en Ponent, Mallorca",
            "description": DESC,
            "image": [f"{DOM}/public/images/{P}{HERO}-1200.webp", f"{DOM}/public/images/{P}salon-visillos-blancos-1200.webp"],
            "datePublished": "2026-10-25",
            "dateModified": "2026-10-25",
            "inLanguage": "es-ES",
            "author": {"@id": f"{DOM}/#business"},
            "publisher": {"@id": f"{DOM}/#business"},
            "mainEntityOfPage": f"{DOM}/{URL}",
            "about": [
                {"@type": "Thing", "name": "Visillos blancos de lino"},
                {"@type": "Thing", "name": "Cortinas para casas rústicas"},
                {"@type": "Thing", "name": "Cortinas mediterráneas"},
                {"@type": "Thing", "name": "Estores enrollables"}
            ],
            "contentLocation": {"@type": "Place", "name": "Ponent, Mallorca",
                                "address": {"@type": "PostalAddress", "addressRegion": "Islas Baleares", "addressCountry": "ES"}}
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{DOM}/"},
                {"@type": "ListItem", "position": 2, "name": "Proyectos", "item": f"{DOM}/proyectos.html"},
                {"@type": "ListItem", "position": 3, "name": "Finca Can Ferragut", "item": f"{DOM}/{URL}"}
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
    ("Ubicación", "Ponent, Mallorca"),
    ("Encargo", "Clienta particular"),
    ("Alcance", "Toda la casa, solo visillo"),
    ("Plazo", "Un mes"),
]

BENEFICIOS = [
    ("El showroom, en casa", "Las telas se eligieron sobre la mesa de la clienta, con la luz y los materiales de su propia casa."),
    ("Una solución por techo", "Riel en el techo donde era plano, soportes a pared bajo las vigas y estor enrollable donde el techo baja."),
    ("Un mismo lenguaje", "Lino blanco y herrajes negros en toda la vivienda: la casa se lee como un conjunto, estancia a estancia."),
    ("Un mes, de principio a fin", "Visita, presupuesto, confección y montaje con nuestro propio equipo en un mes."),
]
benef = "\n".join(
    f'''                <div class="py-6 border-t border-white/15">
                    <h3 class="text-xl md:text-2xl font-light font-display text-white mb-2">{t}</h3>
                    <p class="text-sm leading-relaxed text-neutral-300 font-body max-w-md">{d}</p>
                </div>''' for t, d in BENEFICIOS)

WA_PRO = 'data-wa-msg="Hola, vengo de vuestra web (proyecto de Can Ferragut). Solicito información sobre cortinas para mi casa."'

main = f'''
    <article>

    <!-- Apertura -->
    <header class="{SEC} pt-14 md:pt-20">
        <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-end">
            <div class="lg:col-span-6">
                <p class="text-sm font-body text-terracotta-600 mb-6">Proyecto · Ponent, Mallorca</p>
                <h1 class="text-5xl md:text-6xl lg:text-[4.75rem] font-light tracking-tight font-display text-neutral-800 leading-[0.98] mb-8 [text-wrap:balance]">
                    Cortinas <span class="italic text-terracotta-500">mediterráneas</span> para la finca Can Ferragut, en Ponent, Mallorca
                </h1>
                <p class="text-lg md:text-2xl font-display text-neutral-700 leading-snug [text-wrap:pretty]">
                    Visillos blancos de lino en toda la vivienda, herrajes negros bajo las vigas de madera y una idea sencilla: cortinas mediterráneas que no compiten con la casa, la acompañan.
                </p>
            </div>
            <figure class="lg:col-span-6">
                <img src="/public/images/{P}{HERO}-800.webp" srcset="{hero_srcset}" sizes="{HERO_SIZES}" width="800" height="1422" alt="Arco con techo de vigas de madera que da al comedor, con visillos blancos de lino de suelo a techo a lo largo de los ventanales" fetchpriority="high" class="w-full h-auto aspect-[4/5] object-cover {FEAT}">
            </figure>
        </div>
    </header>

    {ficha_html(FICHA)}

    <!-- Fotos de apertura (7305 y 7306, elegidas por Leandro para ir arriba) -->
    <section class="{SEC} pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto">
            {dos([("paso-arco-cocina", "Paso bajo vigas de madera con visillo blanco de lino junto a un arco que da a la cocina"),
                  ("paso-vigas-visillo", "Visillos blancos de lino colgados de una barra negra bajo las vigas, con el arco de la cocina al fondo")], "aspect-[4/5]")}
        </div>
    </section>

    <!-- El encargo -->
    <section class="{SEC} pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto space-y-14 md:space-y-20">
        {lado(texto('El encargo: <span class="italic text-terracotta-500">toda la casa</span>',
                    'Una clienta particular nos llamó para vestir su casa completa. Fuimos con el showroom móvil y desplegamos el muestrario sobre su mesa: tejidos, colores y herrajes, vistos con la luz de cada estancia.',
                    'La elección fue clara desde el principio: lino blanco, a juego con las paredes, y herrajes en negro, como la carpintería y las vigas.'),
              pic("muestrario-en-casa", "Muestrario de tejidos para cortinas desplegado sobre una mesa de madera durante la visita", S_7, "aspect-[4/5]", FEAT_R, "El muestrario, sobre la mesa de la clienta."), align="items-start")}
            {tres([("eleccion-tejidos-tableta", "Muestras de tejidos en tonos naturales junto a una tableta con el plano de la casa"),
                   ("herrajes-negros", "Soportes y barras de cortina en negro preparados para el montaje"),
                   ("tejido-lino-blanco", "Paño de lino blanco con cabezal fruncido sobre un sofá")])}
        </div>
    </section>

    <!-- Solo visillo -->
    <section class="{SEC} pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto space-y-14 md:space-y-20">
        {lado(texto('Solo visillo: <span class="italic text-terracotta-500">luz tamizada</span> y privacidad',
                    f'La clienta no quería oscuridad total en ningún momento, ni siquiera en los dormitorios. Toda la casa lleva <a href="/visillos.html" {ENLACE}>visillos blancos de lino</a>: dan privacidad y tamizan el sol de Mallorca sin quitar la luz.',
                    'Un mismo tejido de punta a punta, para que la casa se lea como un conjunto y no como una suma de habitaciones.'),
              pic("salon-visillos-blancos", "Salón con sofá blanco y visillos blancos de lino de suelo a techo", S_7, "aspect-[4/5]", FEAT), foto_izq=True, align="items-end")}
            {tres([("salon-sofa-visillo", "Salón con visillos blancos de lino tamizando la luz sobre el sofá"),
                   ("dormitorio-visillo-luz", "Dormitorio con visillo blanco de lino delante de la ventana"),
                   ("dormitorio-escritorio-visillo", "Dormitorio con escritorio de madera y visillo blanco a contraluz")])}
        </div>
    </section>

    <!-- Lo rustico y el blanco: bloque oscuro -->
    <section class="{SEC} py-20 md:py-28 bg-neutral-900 text-white">
        <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16 items-start">
            <div class="lg:col-span-5 lg:sticky lg:top-10">
                {texto('El reto: lo rústico y <span class="italic text-terracotta-400">el blanco</span>',
                       'Aquí no había grandes alturas. El desafío era otro: que unas cortinas blancas convivieran con las vigas de madera, los arcos y la carpintería oscura sin borrar el carácter de la casa.',
                       'La respuesta es mediterránea: tejido natural, color claro y herrajes que repiten el negro de la casa. Cortinas que no invaden el diseño ni el estilo, sino que lo acompañan.', inv=True)}
            </div>
            <div class="lg:col-span-7 space-y-3 md:space-y-6">
                {pic("pasillo-arco-vigas", "Pasillo con arco y techo de vigas de madera vestido con visillos blancos de lino", S_7, "aspect-[4/5]", FEAT, "Bajo el arco, el lino blanco frente a la madera.", inv=True)}
                {dos([("salon-vigas-visillo", "Salón con techo de vigas de madera y visillo blanco de lino junto a la puerta"),
                      ("dormitorio-cama-visillos", "Dormitorio con cama blanca y visillos de lino frente a la terraza")], "aspect-[2/3]", inv=True)}
            </div>
        </div>
    </section>

    <!-- Herrajes -->
    <section class="{SEC} py-20 md:py-28">
        <div class="max-w-7xl mx-auto space-y-14 md:space-y-20">
        {lado(texto('Herrajes negros: <span class="italic text-terracotta-500">techo plano y vigas</span>',
                    'Donde el techo era plano, riel de techo y cortina de suelo a techo. Donde aparecía una viga de madera, el mismo sistema que en nuestro proyecto de <a href="/proyecto-cortinas-reforma-palma.html" ' + ENLACE + '>reforma en Palma</a>: barra con soportes a pared, en negro.',
                    'El negro repite el de la carpintería y los detalles de la casa, y el herraje se convierte en un trazo más del diseño.'),
              pic("barra-negra-puerta", "Barra negra con soporte a pared sobre una puerta de madera, con visillo blanco de lino", S_7, "aspect-[4/5]", FEAT_R), align="items-start")}
            {tres([("soporte-pared-viga", "Soporte negro de barra de cortina fijado a la pared junto a una viga de madera"),
                   ("puerta-madera-visillo", "Puerta de madera con visillo blanco de lino de suelo a techo"),
                   ("visillo-arco-cocina", "Visillo blanco de lino junto a un arco con vistas a la cocina")])}
        </div>
    </section>

    <!-- Techo bajo -->
    <section class="{SEC} pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto">
        {lado(texto('Donde el techo baja: <span class="italic text-terracotta-500">estores enrollables</span>',
                    f'En una zona de la casa el techo es muy bajo y una cortina no habría caído con proporción. Allí pusimos <a href="/cortinas-enrollables.html" {ENLACE}>estores enrollables</a> blancos: se recogen arriba, liberan el espacio y mantienen la misma luz suave que el resto de la vivienda.'),
              pic("estor-enrollable-medicion", "Estor enrollable blanco en una ventana bajo un techo de vigas, medido a mano con cinta métrica", S_7, "aspect-[4/5]", FEAT), foto_izq=True, align="items-end")}
        </div>
    </section>

    <!-- Montaje -->
    <section class="{SEC} pb-20 md:pb-28">
        <div class="max-w-7xl mx-auto">
            <div class="max-w-2xl mb-10 md:mb-14">
                {texto('En <span class="italic text-terracotta-500">un mes</span>, terminada',
                       'De la visita al último visillo colgado pasó un mes. Medimos, confeccionamos y montamos con nuestro propio equipo, y la clienta tuvo la casa terminada sin coordinar a nadie más.')}
            </div>
            {tres([("montaje-escalera", "Instalador en una escalera colgando cortinas bajo un techo de vigas"),
                   ("visillo-orquidea", "Visillo blanco de lino junto a una orquídea y un cuadro en tonos tierra"),
                   ("visillo-terraza", "Visillo blanco de lino junto a la puerta de la terraza con una butaca blanca")])}
        </div>
    </section>

    <!-- Lo que recibio la clienta -->
    <section class="{SEC} py-20 md:py-28 bg-neutral-900 text-white">
        <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-16">
            <div class="lg:col-span-4">
                <h2 class="text-3xl md:text-5xl font-light tracking-tight font-display leading-[1.05] [text-wrap:balance]">Lo que recibió <span class="italic text-terracotta-400">la clienta</span></h2>
            </div>
            <div class="lg:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-x-12">
{benef}
            </div>
        </div>
    </section>

    <!-- Antes y despues: el mismo dormitorio sin cortinas y con visillo -->
    <section class="{SEC} pt-20 md:pt-28">
        <div class="max-w-7xl mx-auto">
            <h2 class="text-3xl md:text-[2.75rem] font-light tracking-tight font-display text-neutral-800 leading-[1.05] mb-10 md:mb-14 [text-wrap:balance]">Antes y <span class="italic text-terracotta-500">después</span></h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-6">
                <figure class="relative">
                    {img("dormitorio-cama-panoramica", "El dormitorio principal antes de las cortinas: puerta a la terraza y paredes blancas sin vestir", "(min-width: 1280px) 600px, (min-width: 768px) 50vw, 100vw", False, "w-full h-auto aspect-[3/2] object-cover " + FEAT)}
                    <figcaption class="absolute top-4 left-4 px-3 py-1 rounded-full bg-white/90 text-xs font-semibold font-body text-neutral-800">Antes</figcaption>
                </figure>
                <figure class="relative">
                    {img("dormitorio-visillos-panoramica", "El mismo dormitorio con visillos blancos de lino de suelo a techo tamizando la luz de la terraza", "(min-width: 1280px) 600px, (min-width: 768px) 50vw, 100vw", False, "w-full h-auto aspect-[3/2] object-cover " + FEAT_R)}
                    <figcaption class="absolute top-4 left-4 px-3 py-1 rounded-full bg-terracotta-600 text-xs font-semibold font-body text-white">Después</figcaption>
                </figure>
            </div>
            <p class="mt-4 text-xs text-neutral-600 font-body">Dormitorio principal: del cristal desnudo a la luz tamizada por el lino, de suelo a techo.</p>
        </div>
    </section>

    <section class="{SEC} pt-6 md:pt-8">
        <div class="max-w-7xl mx-auto">
            {dos([("visillo-planta", "Visillo blanco de lino de suelo a techo junto a una planta en una esquina"),
                  ("visillo-contraventana", "Visillos blancos a ambos lados de una ventana con contraventanas de madera")], "aspect-[4/5]")}
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

    <!-- CTA: clienta particular, asi que el CTA va al particular -->
    <section id="cta-final" class="py-20 md:py-28 px-6 md:px-12 bg-terracotta-600 text-white">
        <div class="max-w-3xl mx-auto text-center">
            <h2 class="text-3xl md:text-5xl font-light tracking-tight font-display mb-6 leading-tight [text-wrap:balance]">¿Quieres vestir tu casa de principio a fin?</h2>
            <p class="text-base text-white/90 max-w-xl mx-auto mb-10 font-body leading-relaxed">Vamos a tu casa con el muestrario completo, elegimos contigo tejidos y herrajes y te lo entregamos montado, en cualquier punto de Mallorca.</p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <a href="{WA_HREF}" {WA_PRO} target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-3 px-10 py-4 bg-white text-terracotta-700 hover:bg-arena-100 rounded-full text-xs font-semibold uppercase tracking-widest transition duration-300 font-body">
                    {WA_SVG} Solicitar visita gratuita
                </a>
                <a href="tel:+34641354788" class="inline-flex items-center gap-3 px-10 py-4 border border-white/40 hover:border-white text-white rounded-full text-xs font-semibold uppercase tracking-widest transition duration-300 font-body">
                    {TEL_SVG}
                    +34 641 35 47 88
                </a>
            </div>
            <p class="mt-8 text-sm font-body"><a href="/showroom-movil.html" class="underline underline-offset-4 decoration-white/50 hover:decoration-white">Cómo funciona el showroom móvil</a></p>
        </div>
    </section>

'''

page = head(TITLE, DESC, URL, f"{P}{HERO}-1200.webp", ld,
            (f"{P}{HERO}-800.webp", hero_srcset, HERO_SIZES)) + body_open + crumbs([("Inicio", "/"), ("Proyectos", "/proyectos.html"), ("Finca Can Ferragut", None)]) + main + tail
(ROOT / URL).write_text(page, encoding="utf-8")
print("ok", URL)
