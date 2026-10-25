"""Fotos del proyecto de reforma integral junto al Pueblo Espanol (Palma).

Uso (desde ANTIGRAVITY_DECORT):  python tools/fotos_reforma_palma.py
Mismos ajustes que tools/fotos_portals_nous.py: alta calidad, sin suavizar.
Sin recorte: la proporcion final la pone el CSS (aspect + object-cover).
"""
import subprocess
import sys
from pathlib import Path

SRC = Path("../CORTINAS/PROYECTOS/03-MAZAGÁN 31/Selección web")

# nombre, original
FOTOS = [
    ("dormitorio-vigas-panoramica", "IMG_0054.JPEG"),
    ("ajuste-visillo-ventana", "IMG_0049.JPEG"),
    ("dormitorio-vigas-visillo", "IMG_0052.JPEG"),
    ("dormitorio-abrir-visillo", "IMG_0041.JPEG"),
    ("dormitorio-luz-tamizada", "IMG_0045.JPEG"),
    ("dormitorio-blackout-visillo", "IMG_0048.JPEG"),
    ("textura-blackout-lino", "IMG_0050.JPEG"),
    ("comedor-ventanal-grande", "IMG_0069.JPEG"),
    ("comedor-ventanal-correderas", "IMG_0072.JPEG"),
    ("ventanal-desde-la-puerta", "IMG_0067.JPEG"),
    ("riel-negro-pared-vigas", "IMG_0058.JPEG"),
    ("cabezal-riel-negro", "IMG_0057.JPEG"),
    ("dormitorio-techo-inclinado", "IMG_0056.JPEG"),
    ("foseado-luz-visillo", "IMG_0060.JPEG"),
    ("foseado-escritorio", "IMG_0062.JPEG"),
    ("foseado-ventana", "IMG_0064.JPEG"),
    ("dormitorio-foseado-luz", "IMG_0066.JPEG"),
    ("montaje-escalera", "IMG_0028.JPEG"),
    ("colgando-visillo", "IMG_0031.JPEG"),
    ("detalle-visillo-lino", "IMG_0024.JPEG"),
    ("luz-al-fondo", "IMG_0068.JPEG"),
]

solo = set(sys.argv[1:])
for name, src in FOTOS:
    if solo and name not in solo:
        continue
    print(f"== {name}", flush=True)
    anchos = "480,800,1200,1600,2000" if name == "dormitorio-vigas-panoramica" else "480,800,1200,1600"
    subprocess.run([sys.executable, "tools/optimizar_imagen.py", str(SRC / src), f"reforma-palma-{name}",
                    "--widths", anchos, "--quality", "84", "--min-quality", "74"], check=True)
