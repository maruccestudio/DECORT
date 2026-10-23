"""Regenera las fotos del proyecto de Portals Nous en alta calidad.

Uso (desde ANTIGRAVITY_DECORT):  python tools/fotos_portals_nous.py

Cada foto sale en 480/800/1200/1600 px (sin pasar del ancho del original),
calidad 84 y nunca por debajo de 74, sin suavizado. El movil sigue bajando la
de 480; las grandes solo las piden pantallas anchas o de alta densidad.
Prefijo 'portals-nous-' (nombre nuevo: las imagenes se cachean 30 dias).
"""
import subprocess
import sys
from pathlib import Path

SRC = Path("../CORTINAS/PROYECTOS/01-VICTORIA 31/SELECCION WEB")

# nombre, original, recorte, centro vertical
FOTOS = [
    ("salon-visillos-lino", "00_04.JPEG", "3:2", 0.5),
    ("obra-antes", "00_ANTES 01.JPEG", "3:4", 0.5),
    ("fachada", "00_25.JPEG", "3:2", 0.5),
    ("tejidos-mesa", "00_09.JPEG", "3:4", 0.5),
    ("seleccion-tejidos-comedor", "00_13.JPEG", "3:4", 0.5),
    ("muestras-lino", "00_17.JPEG", "3:4", 0.5),
    ("salon-visillo-fruncido", "00_03.JPEG", "3:4", 0.5),
    ("salon-panoramica", "00_20.JPEG", "16:9", 0.5),
    ("caida-visillo-suelo", "00_21.JPEG", "2:3", 0.5),
    ("cabezal-fruncido", "00_16.JPEG", "2:3", 0.5),
    ("visillo-sofa", "00_08.JPEG", "3:4", 0.5),
    ("pasillo-visillos", "00_19.JPEG", "2:3", 0.5),
    ("visillos-luz-suelo", "00_VISILLOS.JPEG", "3:4", 0.5),
    ("montaje-gran-formato", "00_MONTAJE VICTORIA.JPG", "3:4", 0.45),
    ("montaje-escalera", "00_MONTAJE 02.JPEG", "3:4", 0.5),
    ("visillo-altura-techo", "00_23.JPEG", "2:3", 0.5),
    ("dormitorio-blackout", "00_DORMITORIO.JPEG", "3:4", 0.5),
    ("dormitorio-blackout-visillo", "00_14.JPEG", "2:3", 0.5),
    ("dormitorio-terraza", "00_02.JPEG", "3:4", 0.5),
    ("blackout-vista-piscina", "00_026.JPEG", "3:4", 0.5),
    ("revision-dormitorio", "00_12.JPEG", "2:3", 0.5),
    ("planta-baja-luz", "00_15.JPEG", "16:9", 0.5),
    ("ajuste-visillo", "00_01.JPEG", "3:4", 0.5),
    ("preparacion-cortinas", "00_18.JPEG", "2:3", 0.5),
    ("entrega-visillos", "00_24.JPEG", "2:3", 0.5),
    ("dormitorio-lectura", "00_10.JPEG", "2:3", 0.5),
    ("salon-vista-general", "00_05.JPEG", "3:2", 0.5),
    ("visillo-detalle-lino", "00_22.JPEG", "2:3", 0.5),
    ("medicion-obra", "00_MEDICION.jpg", "2:3", 0.55),
    ("motores-riel", "00_MOTORES.jpg", "2:3", 0.4),
    ("eleccion-visillo", "00_TELAS VISILLO.jpg", "4:5", 0.45),
    ("muestras-blackout", "00_TELAS BLACKOUT.jpg", "3:4", 0.5),
    ("paso-visillos-planta-baja", "00_PLANTA BAJA PASO.jpg", "3:4", 0.55),
    ("pasillo-final", "IMG_9324.JPEG", "3:4", 0.5),
    ("salon-lampara", "IMG_9327.JPEG", "3:4", 0.5),
]

# Las apaisadas ocupan todo el ancho (1216 px): en pantallas de densidad 2 piden ~2400.
ANCHOS = "480,800,1200,1600"
ANCHOS_PANO = "480,800,1200,1600,2000"

solo = set(sys.argv[1:])
for name, src, ratio, fy in FOTOS:
    if solo and name not in solo:
        continue
    print(f"== {name}", flush=True)
    subprocess.run([sys.executable, "tools/optimizar_imagen.py", str(SRC / src), f"portals-nous-{name}",
                    "--ratio", ratio, "--focus-y", str(fy), "--widths", ANCHOS_PANO if ratio in ("3:2", "16:9") else ANCHOS,
                    "--quality", "84", "--min-quality", "74"], check=True)
