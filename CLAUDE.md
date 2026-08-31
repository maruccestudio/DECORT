# DECORT MARUCC -- notas tecnicas del repo

Sitio estatico (HTML + Tailwind CSS), sin framework JS, desplegado en
Vercel al hacer push a `main`. Repo: `maruccestudio/DECORT`.

## La trampa mas repetida en 274 commits: falta de fuente unica de verdad

Nav, footer y algun bloque de schema (NAP/LocalBusiness) deben ser
identicos en varias paginas, pero cada pagina es un HTML independiente:
se editan a mano en 12-18 archivos y algo termina desincronizado. Ha
pasado con NAP, con el @id de LocalBusiness, con los botones flotantes,
y el 27-08-2026 con el color del footer de una sola pagina.

**Antes de dar por cerrado un cambio en `<nav>` o `<footer>`, correr:**
```bash
python .claude/skills/sync-shared-blocks/scripts/sync_block.py \
  --tag footer --ref cortinas-blackout.html --targets <resto-de-paginas>
```
Ver `.claude/skills/sync-shared-blocks/SKILL.md` para la lista de
paginas que son legitimamente distintas (home, la version en ingles,
las 3 legales, y `contacto.html`) -- esas NO se sincronizan.

**El bloque "Tambien te puede interesar" es la excepcion que confirma
la regla:** cada pagina enlaza a colecciones distintas a proposito. No
es deriva, no se sincroniza.

## Tailwind: output.css es un build purgado, no editar reglas a mano

`public/output.css` se genera con `npm run build`
(`tailwindcss -i ./src/input.css -o ./public/output.css --minify`) y
solo incluye las clases que Tailwind detecta en el HTML/JS actual.

Dos trampas de verificacion que ya han costado tiempo:

1. **Los selectores CSS escapan `[`, `]`, `%`, `:`, `/`.** Buscar
   `grayscale-[30%]` literal en el archivo no encuentra nada; el
   selector real es `.grayscale-\[30\%\]{`. Verificar con
   `grep -o '\.grayscale-[^{]*{' public/output.css`, no con texto literal.
2. **El proyecto redefine el variant `hover`** (`tailwind.config.js`)
   para envolverlo en un unico bloque `@media (hover:hover) and
   (pointer:fine){...}`. Ninguna clase `hover:` aparece como selector de
   nivel superior; hay que buscar dentro de ese bloque, no con
   `grep '.hover\:X{'`.

**Regla practica:** si se añade una clase de Tailwind nueva en el HTML,
correr `npm run build` antes de dar el cambio por verificado. No asumir
que una clase "no existe" sin comprobar con el escapado correcto.

## Flujo de git en este proyecto

- Nunca commits ni push directos a `main`. Siempre rama nueva
  (`git checkout -b tipo/nombre-descriptivo`).
- Commitear con mensaje explicando el porque, no solo el que.
- **Preguntar antes de pushear** ("¿hago push?") y antes de mergear a
  `main` ("¿subelo?"). El usuario decide cuando.
- Tras el merge a `main`, Vercel despliega solo. Verificar en produccion
  con `curl`, dando margen a la propagacion de CDN (10-20s, a veces mas).

## Otros datos utiles

- Formulario de contacto: Web3Forms, mismo `public/form.css`/`form.js`
  en todas las paginas que lo llevan. Cada pagina manda su propio
  `subject` y `data-form-name` para distinguir el origen del lead.
- Paleta de marca: terracota `#A05034`, arena/piedra como fondo, oliva
  como acento secundario. Ver el manual de marca en la memoria del
  proyecto para el detalle completo -- este archivo es solo lo tecnico.
- Medicion: WhatsApp, telefono y el envio del formulario disparan Google
  Ads + GA4 + Meta a la vez, condicionados al consentimiento de cookies.
