#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_block.py -- detecta y corrige deriva en bloques HTML que deben ser
identicos entre paginas (nav, footer). NUNCA toca title/meta/canonical/
hreflang/JSON-LD/H1/contenido principal: solo opera dentro de la etiqueta
indicada (<footer>...</footer> o <nav>...</nav>).

Modo por defecto: solo lectura (--check). Nunca escribe nada salvo que
se pase --apply de forma explicita.

Uso:
  # Solo mirar si hay deriva (no escribe nada)
  python sync_block.py --tag footer --ref cortinas-blackout.html \\
      --targets pagina1.html pagina2.html ...

  # Aplicar de verdad (copia el bloque de --ref a cada --targets)
  python sync_block.py --tag footer --ref cortinas-blackout.html \\
      --targets pagina1.html pagina2.html --apply
"""
import argparse
import difflib
import io
import subprocess
import sys


def extraer_bloque(html: str, tag: str):
    open_tag = f'<{tag}'
    close_tag = f'</{tag}>'
    i = html.find(open_tag)
    if i == -1:
        return None, None, None
    j = html.find(close_tag, i)
    if j == -1:
        return None, None, None
    j += len(close_tag)
    if html.find(open_tag, j) != -1:
        # hay una segunda ocurrencia: la pagina tiene mas de un bloque con
        # este tag y no podemos saber cual es el compartido. Nos negamos.
        return None, None, None
    return html[i:j], i, j


def rama_actual():
    r = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                        capture_output=True, text=True)
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', required=True, choices=['footer', 'nav'],
                     help='Etiqueta HTML a sincronizar. Solo footer o nav: '
                          'nunca title/meta/head/schema.')
    ap.add_argument('--ref', required=True,
                     help='Pagina que se considera la version correcta.')
    ap.add_argument('--targets', required=True, nargs='+',
                     help='Paginas a comparar/corregir. Nunca "*", siempre '
                          'una lista explicita decidida por una persona.')
    ap.add_argument('--apply', action='store_true',
                     help='Escribe los cambios. Sin esto, solo informa.')
    args = ap.parse_args()

    ref_html = io.open(args.ref, encoding='utf-8').read()
    ref_bloque, _, _ = extraer_bloque(ref_html, args.tag)
    if ref_bloque is None:
        print(f'ERROR: no se pudo extraer <{args.tag}> de {args.ref} '
              f'de forma no ambigua. Nada que hacer.')
        sys.exit(1)

    if args.apply and rama_actual() == 'main':
        print('ERROR: --apply rehusado en la rama main. '
              'Crea una rama primero (git checkout -b ...).')
        sys.exit(1)

    con_deriva = []
    for f in args.targets:
        if f == args.ref:
            continue
        html = io.open(f, encoding='utf-8').read()
        bloque, i, j = extraer_bloque(html, args.tag)
        if bloque is None:
            print(f'  {f:38s}  AMBIGUO o sin <{args.tag}> -- se salta')
            continue
        if bloque == ref_bloque:
            print(f'  {f:38s}  identico')
            continue

        con_deriva.append(f)
        print(f'  {f:38s}  *** DERIVA ***')
        diff = difflib.unified_diff(
            ref_bloque.splitlines(keepends=True),
            bloque.splitlines(keepends=True),
            fromfile=f'{args.ref} (referencia)', tofile=f)
        for linea in list(diff)[:12]:
            print('      ' + linea.rstrip())

        if args.apply:
            nuevo = html[:i] + ref_bloque + html[j:]
            io.open(f, 'w', encoding='utf-8').write(nuevo)
            print(f'      -> corregido')

    print('')
    if con_deriva and not args.apply:
        print(f'{len(con_deriva)} pagina(s) con deriva. Nada se ha escrito '
              f'(modo --check). Repite con --apply para corregir, dentro '
              f'de una rama.')
    elif con_deriva:
        print(f'{len(con_deriva)} pagina(s) corregidas. Recuerda recompilar '
              f'el CSS si el bloque introdujo clases nuevas (npm run build) '
              f'y verificar en el navegador antes de comitear.')
    else:
        print('Sin deriva. Todo consistente.')


if __name__ == '__main__':
    main()
