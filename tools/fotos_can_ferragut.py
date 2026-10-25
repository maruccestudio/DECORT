"""Fotos del proyecto de la finca Can Ferragut (Ponent, Mallorca) con visillos blancos de lino.

Uso (desde ANTIGRAVITY_DECORT):  python tools/fotos_can_ferragut.py
Mismos ajustes que los otros proyectos: alta calidad, sin suavizar, sin recorte
(la proporcion la pone el CSS). Las mcc-*.png son fotos ya editadas por Leandro:
no se toca luz ni color.
"""
import subprocess
import sys
from pathlib import Path

SRC = Path("../CORTINAS/PROYECTOS/02-INA/web")

FOTOS = [
    ("dormitorio-visillos-panoramica", "IMG_7331.a.jpg"),
    ("muestrario-en-casa", "87508D33-B10E-474B-A028-6C88C8423970.jpg"),
    ("eleccion-tejidos-tableta", "IMG_6306.JPEG"),
    ("herrajes-negros", "IMG_7249.JPEG"),
    ("tejido-lino-blanco", "mcc-1.png"),
    ("salon-visillos-blancos", "IMG_7310.JPEG"),
    ("salon-sofa-visillo", "IMG_7312.JPEG"),
    ("dormitorio-visillo-luz", "IMG_7339.JPEG"),
    ("dormitorio-escritorio-visillo", "IMG_7340.JPEG"),
    ("dormitorio-cama-visillos", "IMG_7330.JPEG"),
    ("pasillo-arco-vigas", "IMG_7317.JPEG"),
    ("salon-vigas-visillo", "IMG_7321.JPEG"),
    ("arco-comedor-visillos", "mcc-6.png"),
    ("barra-negra-puerta", "IMG_7325.JPEG"),
    ("soporte-pared-viga", "IMG_7289.JPEG"),
    ("puerta-madera-visillo", "mcc-5.png"),
    ("visillo-arco-cocina", "mcc-3.png"),
    # recortada sin la cara del montador (pedido de Leandro): solo la mano con la cinta
    ("estor-enrollable-medicion", "recortes/IMG_7318-sin-cara.jpg"),
    ("montaje-escalera", "IMG_7292.JPEG"),
    ("visillo-orquidea", "IMG_7299.JPEG"),
    ("visillo-terraza", "mcc-2.png"),
    ("dormitorio-cama-panoramica", "IMG_7260.a.jpg"),
    ("visillo-planta", "mcc-4.png"),
    ("visillo-contraventana", "IMG_7337.JPEG"),
]

solo = set(sys.argv[1:])
for name, src in FOTOS:
    if solo and name not in solo:
        continue
    print(f"== {name}", flush=True)
    anchos = "480,800,1200,1600,2000" if name.endswith("panoramica") else "480,800,1200,1600"
    subprocess.run([sys.executable, "tools/optimizar_imagen.py", str(SRC / src), f"can-ferragut-{name}",
                    "--widths", anchos, "--quality", "84", "--min-quality", "74"], check=True)
