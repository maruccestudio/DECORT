#!/usr/bin/env python3
"""Prepara una foto para la web de DECORT MARUCC.

Uso (desde ANTIGRAVITY_DECORT):
    python tools/optimizar_imagen.py ORIGEN NOMBRE [--ratio 3:4] [--focus-y 0.5]

Genera public/images/NOMBRE-480.webp, -800.webp y -1125.webp, sin EXIF
(una foto de la casa de un cliente puede llevar la ubicacion GPS), y baja la
calidad solo lo necesario para entrar en el presupuesto de peso de cada ancho.
Imprime los atributos srcset/width/height listos para pegar en el <img>.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

# KB maximos por ancho. Mas pesado que esto empieza a notarse en movil.
BUDGET_KB = {480: 35, 800: 70, 1125: 120}
MIN_QUALITY = 55


def crop_ratio(im, ratio, fx, fy):
    rw, rh = (int(v) for v in ratio.split(":"))
    w, h = im.size
    if w * rh >= h * rw:  # imagen mas ancha que el ratio: recorta a los lados
        new_w, new_h = round(h * rw / rh), h
    else:  # imagen mas alta: recorta arriba y abajo
        new_w, new_h = w, round(w * rh / rw)
    left = min(max(round(fx * w - new_w / 2), 0), w - new_w)
    top = min(max(round(fy * h - new_h / 2), 0), h - new_h)
    return im.crop((left, top, left + new_w, top + new_h))


def save_fitting(im, path, budget_kb, quality):
    while True:
        im.save(path, "WEBP", quality=quality, method=6)  # sin exif= : no se copian metadatos
        kb = path.stat().st_size / 1024
        if kb <= budget_kb or quality <= MIN_QUALITY:
            return kb, quality
        quality -= 4


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("name", help="nombre base descriptivo, sin extension (nosotros-marcado-de-tela)")
    ap.add_argument("--ratio", help="recorte ANCHO:ALTO, por ejemplo 3:4")
    ap.add_argument("--focus-x", type=float, default=0.5, help="centro horizontal del recorte, 0 a 1")
    ap.add_argument("--focus-y", type=float, default=0.5, help="centro vertical del recorte, 0 a 1")
    ap.add_argument("--widths", default="480,800,1125")
    ap.add_argument("--quality", type=int, default=74)
    ap.add_argument("--out", default="public/images")
    a = ap.parse_args()

    im = ImageOps.exif_transpose(Image.open(a.src)).convert("RGB")
    if a.ratio:
        im = crop_ratio(im, a.ratio, a.focus_x, a.focus_y)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    srcset, rows = [], []
    for w in sorted({int(v) for v in a.widths.split(",")}):
        if w > im.width:
            print(f"aviso: el original mide {im.width}px, se omite {w}px", file=sys.stderr)
            continue
        h = round(im.height * w / im.width)
        p = out / f"{a.name}-{w}.webp"
        kb, q = save_fitting(im.resize((w, h), Image.LANCZOS), p, BUDGET_KB.get(w, 120), a.quality)
        srcset.append(f"/{out.as_posix()}/{p.name} {w}w")
        rows.append((w, h, kb, q, BUDGET_KB.get(w, 120)))

    for w, h, kb, q, b in rows:
        print(f"{w:>5} x {h:<5} {kb:6.1f} KB  q{q}  presupuesto {b} KB  {'OK' if kb <= b else 'SE PASA'}")
    mid = rows[len(rows) // 2]
    print(f'\nsrcset="{", ".join(srcset)}"')
    print(f'src="/{out.as_posix()}/{a.name}-{mid[0]}.webp" width="{mid[0]}" height="{mid[1]}"')


if __name__ == "__main__":
    main()
