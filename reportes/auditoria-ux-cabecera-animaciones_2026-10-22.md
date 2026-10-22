# Auditoría de diseño, botones y animaciones — 22-10-2026

Tres revisiones con las skills del proyecto, sobre la web en local (igual que producción):

1. **impeccable · audit**: diseño, accesibilidad, contraste y antipatrones. Usa PRODUCT.md y DESIGN.md como referencia y pasa su detector automático.
2. **web-design-guidelines**: botones, menús, desplegables, formulario y FAQ, contra las pautas de Vercel.
3. **improve-animations**: todas las animaciones, con el criterio de Emil Kowalski.

Cada hallazgo se ha comprobado en el código o en el navegador. Los falsos positivos se descartan al final.

---

## Nota global (impeccable): 14/20 — "Bien"

| Área | Nota | Lo más importante |
|---|---|---|
| Accesibilidad | 3/4 | En el móvil, los enlaces del menú miden 15 px de alto (mínimo recomendado: 24-44 px) |
| Rendimiento | 3/4 | Carga rápida. Dos animaciones infinitas (los pulsos) repintan sin parar |
| Responsive | 3/4 | Sin desbordes. Falla el tamaño táctil del menú |
| Sistema de diseño | 3/4 | Colores en tokens. Hay algunos hex escritos a mano en estilos sueltos |
| Antipatrones | 2/4 | **Etiquetas en mayúsculas encima de casi cada sección** en las páginas nuevas (de 5 a 8 por página) |

---

## 1. La cabecera (lo que viste)

| # | Prioridad | Qué pasa | Dato medido | Arreglo |
|---|---|---|---|---|
| 1 | **P1** | **"COLECCIONES" en mayúsculas y el resto no** (solo en la home) | Al desplegable de la home le falta la clase que quita las mayúsculas, igual que al botón de antes | Igualar las mayúsculas en todo el menú |
| 2 | **P1** | **Se pierde sobre la foto** | Menú de 11 px, peso 500, gris oscuro sobre una cortina gris claro; fondo transparente hasta que se hace scroll | Velo claro desde el primer momento (no solo al hacer scroll), texto a 13 px y más oscuro |
| 3 | **P1** | **Ningún botón de acción en la cabecera** | PRODUCT.md dice que "Reservar tu visita gratis" debe verse sin scroll; en la cabecera solo hay navegación | Botón terracota **"Pedir visita"** a la derecha, al WhatsApp y con seguimiento |
| 4 | **P1** | **Menú del móvil muy pequeño** (páginas interiores) | "Colecciones", "Blog" y "Contacto" a 10 px y 15 px de alto | Subir a 12-13 px y ampliar la zona táctil a 44 px de alto (con padding, sin cambiar el aspecto) |
| 5 | P2 | El menú interior usa espaciado de mayúsculas (`tracking-widest`) sobre texto en minúsculas | 1 px de espaciado entre letras: queda raro en minúsculas | Quitar ese espaciado en los enlaces |
| 6 | P2 | La home y el resto de páginas tienen cabeceras distintas | La home es fija con menú de pantalla completa; las interiores son estáticas y sin botón | Mismo tamaño, misma tipografía y mismo botón en las dos |

**Mayúsculas o minúsculas:** las tres revisiones coinciden. **Menú y botones de navegación con inicial mayúscula y el resto en minúscula.** Las mayúsculas espaciadas solo para etiquetas cortas, y con moderación (ver el punto 3).

## 2. Botones, menús y desplegables (web-design-guidelines)

```text
index.html:447 — el logo es <a href="#" onclick> → debe ser href="/" (o "#hero") sin JS
public/js/contacto-whatsapp.js:335 — el desplegable se cierra con Escape pero el foco no vuelve a "Colecciones"
public/js/contacto-whatsapp.js:335 — al salir del panel con Tab, el desplegable queda abierto
index.html, cortinas-*.html — falta <meta name="theme-color"> (la barra del navegador del móvil no toma el color de la marca)
páginas interiores — no hay estilo :focus-visible propio (solo el de la home, index.html:226); con teclado, el foco apenas se ve sobre arena
```

**Lo que ya cumple:** enlace "Saltar al contenido", `aria-expanded` en el menú del móvil, formulario con `label`, `autocomplete`, `type` correcto y mensajes con `aria-live`, botón desactivado mientras envía con "Enviando…", imágenes con `width`/`height`, hovers solo en dispositivos con ratón (el menú no se queda "pegado" al tocar en el móvil), y el desplegable hecho con `<details>` nativo, que funciona con teclado y lector de pantalla.

## 3. Antipatrones de diseño (impeccable)

- **P1 — Etiqueta en mayúsculas encima de cada sección** ("CÓMO FUNCIONA", "TEJIDOS", "MEDIDAS"…). Las páginas nuevas llevan de 5 a 8; la home, 4. Es justo lo que DESIGN.md dice que hay que variar y el patrón más reconocible de una web hecha con IA. Lo metí yo en las páginas nuevas a través del generador. **Arreglo:** dejarla solo donde aporta (1-2 por página) y quitarla del resto.
- P3 — El bloque "Más soluciones a medida" son 6 tarjetas de texto idénticas. Sirve como solución provisional; cuando haya fotos, pasarán a ser tarjetas con imagen como las demás.
- Sin problema: el detector marca Inter y Cormorant como "fuentes muy usadas". **Se ignora:** es una decisión de marca cerrada.

## 4. Animaciones (improve-animations)

| # | Severidad | Dónde | Qué pasa | Arreglo |
|---|---|---|---|---|
| 1 | MEDIA | Desplegable de Colecciones | Aparece de golpe, sin decir de dónde sale | Entrada de 180 ms: opacidad 0→1 y `scale(0.97)→1`, desde la esquina superior derecha, curva `cubic-bezier(0.23, 1, 0.32, 1)`. Cierre instantáneo |
| 2 | MEDIA | FAQ (`<details>`) | Al abrir una pregunta, el texto salta | Altura animada con `::details-content` + `interpolate-size` (Chrome/Edge; en el resto abre como ahora), 250 ms |
| 3 | MEDIA | Botón de WhatsApp y punto terracota (index.html:84-89, 165-171) | Pulso infinito cada 2 s que repinta la sombra sin parar: distrae y gasta batería | Que pulse 3 veces al aparecer y se quede quieto |
| 4 | BAJA | Botones principales | Al pasar el ratón crecen (`scale-105`), pero al pulsar no responden | Añadir `active:scale-[0.97]` con 160 ms: el botón "se hunde" al tocarlo, también en el móvil |
| 5 | BAJA | Subrayado `.hover-line` (index.html:111) | Anima `width`, que obliga a recalcular el diseño | Cambiar a `transform: scaleX()` desde la izquierda |
| 6 | BAJA | Rejilla de colecciones de la home | El escalonado llega a 0,7 s: la última tarjeta tarda en aparecer | Limitar el retraso a 0,3 s |

**Lo que ya está bien:** la curva propia `cubic-bezier(0.16, 1, 0.3, 1)` es correcta; las entradas al hacer scroll respetan "reducir movimiento" y nunca dejan contenido oculto sin JS; el menú del móvil (500 ms, ease-out) entra en el margen de un cajón; y los hovers solo se activan con ratón.

---

## Descartado por falso positivo
- "Imagen rota" en index.html:493: es un comentario del código que contiene el texto `<img>`.
- "Solo una fuente" en las páginas interiores: el detector no ve la Cormorant, que se carga por la clase `font-display`.
- "Fuente muy usada": decisión de marca.

## Propuesta de orden

1. **Cabecera nueva** (puntos 1-6 de la sección 1): mayúsculas iguales, velo y contraste, botón "Pedir visita", zona táctil en el móvil y misma cabecera en todas las páginas. → `impeccable polish` sobre la cabecera.
2. **Quitar etiquetas sobrantes** en las páginas nuevas. → `impeccable quieter`.
3. **Desplegable y FAQ con movimiento**, foco que vuelve al cerrar, pulsos limitados y respuesta al pulsar los botones. → Planes de `improve-animations` y arreglos de `web-design-guidelines`.
4. **theme-color y foco visible** en todas las páginas.
