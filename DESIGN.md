---
name: DECORT MARUCC
description: Showroom móvil de cortinas a medida para Baleares — calidez mediterránea con precisión de arquitecto
colors:
  terracotta-primary: "#A0633B"
  terracotta-deep: "#73422a"
  terracotta-soft: "#f9e8da"
  arena-bg: "#FAF7F2"
  arena-warm: "#EBE3D6"
  arena-border: "#D4C5A9"
  oliva-accent: "#8B8B3D"
  oliva-soft: "#eeeedd"
  ink: "#262626"
  muted: "#737373"
typography:
  display:
    fontFamily: "Cormorant Garamond, Georgia, serif"
    fontSize: "clamp(2.5rem, 7vw, 6rem)"
    fontWeight: 300
    lineHeight: 0.95
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.625rem"
    fontWeight: 500
    letterSpacing: "0.15em"
rounded:
  current-card-extreme: "120px / 160px"
  current-card-standard: "24px"
  current-button: "9999px (pill)"
spacing:
  section-y: "5rem–8rem (py-20 a py-32)"
  card-gap: "2rem–3rem (gap-8 a gap-12)"
components:
  button-primary:
    backgroundColor: "{colors.terracotta-primary}"
    textColor: "#ffffff"
    rounded: "9999px"
    padding: "14px 32px"
  button-primary-hover:
    backgroundColor: "{colors.terracotta-deep}"
---

# Design System: DECORT MARUCC

## 1. Overview

**Creative North Star: "El Showroom Móvil"**

El diferencial real de DECORT MARUCC no es la cortina, es que el showroom viaja hasta el cliente. Todo el sistema visual debe sentirse como esa promesa: cercano, portátil, sin la fricción de una tienda bajo fluorescentes. Cálido pero preciso — el lenguaje sensorial de la marca (lino, luz tamizada, calidez mediterránea) convive con el rigor de quien mide con láser y confecciona a medida. No es lujo ostentoso ni frialdad de showroom corporativo: es calma estructural con materiales nobles a la vista.

Este sistema rechaza explícitamente: fotografía de stock genérica, interiores fríos/impersonales, lenguaje de miedo o superlativos vacíos, y — de cara al rediseño en curso — el "scaffolding" genérico de IA (esquinas extremas sin propósito, eyebrows uniformes en cada sección, numeración decorativa que no representa una secuencia real, grids de cards idénticas sin variación).

**Key Characteristics:**
- Paleta de tierra mediterránea (terracota/arena/oliva), nunca el cream-default genérico de IA
- Serif editorial (Cormorant Garamond) + sans técnico (Inter) — contraste deliberado, no dos sans similares
- Superficies planas en reposo; la elevación aparece solo como respuesta a interacción
- CTA de "visita gratuita" siempre presente y nunca escondido tras scroll

## 2. Colors

Paleta de tierra mediterránea: terracota cocida al sol, arena de playa, hoja de olivo — el paisaje de Baleares traducido a interfaz.

### Primary
- **Terracota** (`#A0633B`): botones principales, acentos, highlights, CTA. Es el color que "actúa" — nunca decorativo puro.

### Secondary
- **Oliva** (`#8B8B3D`): badges, etiquetas secundarias, detalles puntuales (ej. "Baleares" en el hero). Uso deliberadamente escaso.

### Neutral
- **Arena** (`#FAF7F2` a `#EBE3D6`): fondos de sección, superficies cálidas. No es el "cream AI-default" — es un token de marca con nombre propio, ya presente en el brandbook.
- **Ink** (`#262626`): texto principal, headings.
- **Muted** (`#737373`): texto secundario, descripciones de card.

### Named Rules
**La Regla de la Tierra.** Ningún color entra al sistema si no tiene un referente físico mediterráneo (terracota, arena, oliva, piedra de Santanyí). Nada de azules corporativos ni morados de gradiente.

## 3. Typography

**Display Font:** Cormorant Garamond (fallback Georgia, serif)
**Body Font:** Inter (fallback system-ui, sans-serif)

**Character:** Serif editorial de peso ligero para titulares (con acentos itálicos en terracota) contra un sans técnico y legible para el cuerpo — el eje de contraste clásico "elegancia editorial + claridad funcional", nunca dos fuentes de la misma familia.

### Hierarchy
- **Display** (font-light, clamp hasta 6rem, leading 0.85–0.95): H1 de hero y H2 de sección. Itálico terracota para la palabra que lleva el énfasis emocional.
- **Title** (font-semibold, text-lg a text-2xl): nombres de producto en cards, títulos de card.
- **Body** (font-normal, text-sm a text-base): descripciones, párrafos. Line-height relajado (1.6).
- **Label** (text-[10px], uppercase, tracking-widest): eyebrows, badges, metadatos de card. Máximo contraste de peso contra el display.

### Named Rules
**La Regla del Eje de Contraste.** Display y body nunca comparten familia tipográfica ni "temperatura" visual — uno es editorial, el otro técnico. Es lo único que impide que el conjunto se sienta genérico.

## 4. Elevation

Sistema plano por defecto. Las cards no tienen sombra en reposo; la sombra aparece únicamente como respuesta a `:hover`, nunca como decoración estática. Esto ya es la filosofía correcta del sitio actual y se mantiene — no se suman capas de profundidad permanentes.

### Shadow Vocabulary
- **hover-lift** (`shadow-lg` a `shadow-2xl`, tinte terracota al 10-30% de opacidad): aparece solo en `:hover` sobre cards interactivas, acompañado de una elevación sutil (`-translate-y-2`).

### Named Rules
**La Regla del Reposo Plano.** Si una sombra es visible sin que el usuario esté interactuando con el elemento, es decoración, no elevación funcional — no se permite.

## 5. Components

### Buttons
- **Shape:** pill (`rounded-full`) — el único lugar del sistema donde el full-pill es correcto.
- **Primary:** fondo terracota-500, texto blanco, uppercase, tracking-widest, padding 14px/32px.
- **Hover:** fondo terracota-600 + `scale-105` + sombra terracota tenue.
- **Secondary:** borde arena-400, texto neutral-600, mismo pill shape, fondo transparente.

### Cards / Containers
- **Corner Style:** dos tratamientos conviven a propósito — `rounded-3xl` (24px) en Proceso/Testimonios, y esquinas asimétricas extremas `rounded-tl/br-[120px]/[160px]` en Colecciones y `rounded-[40px]/[60px]` en Showroom. **Decisión de marca confirmada**: el radio extremo es intencional, "el toque distinto" del sistema — no es deuda de diseño ni se debe proponer reemplazarlo en auditorías futuras (ver `feedback_diseno_web` en memoria del proyecto).
- **Background:** blanco sobre fondo arena, o arena-200 como placeholder de imagen.
- **Shadow Strategy:** ver Elevación — plano en reposo, hover-lift en interacción.
- **Border:** `border-arena-300/50`, casi invisible en reposo, se acentúa a `terracotta-300` en hover.
- **Internal Padding:** generoso, `p-7` a `p-8`.

### Navigation
- Header fijo con blur al hacer scroll (`backdrop-filter: blur(12px)`), fondo sólido implícito — uso funcional de glassmorphism, no decorativo. Menú móvil fullscreen (no dropdown).

### Eyebrows / Labels (componente distintivo)
- `text-[10px] uppercase tracking-widest` acompañado de una línea horizontal de 4rem en terracota al 30% de opacidad. Repetido casi idénticamente arriba de cada sección — es el patrón que la Fase 1 va a variar para que no lea como scaffolding genérico, sin perder la función de "kicker editorial".

## 6. Do's and Don'ts

### Do:
- **Do** usar terracota como el único color que "actúa" (CTA, acentos) — nunca más del 10-15% de la superficie de cualquier pantalla.
- **Do** mantener el eje de contraste serif+sans en toda página nueva.
- **Do** dejar las cards planas en reposo; la sombra se gana con interacción, no se regala.
- **Do** anclar cada decisión de color a un referente físico mediterráneo (terracota, arena, oliva).

### Don't:
- **Don't** usar fotografía de stock genérica o interiores fríos/impersonales — viola directamente el anti-referente de marca.
- **Don't** aplicar el límite genérico de 32px de impeccable a las esquinas de Colecciones/Showroom — el radio extremo actual es una decisión de marca confirmada, no deuda de diseño.
- **Don't** poner un eyebrow uniforme arriba de cada sección sin variar cadencia — es el "scaffolding" de IA que este rediseño busca eliminar.
- **Don't** numerar una secuencia (01, 02, 03...) si no representa un orden real — la numeración se gana, no se aplica por reflejo de "así se ven los landing pages".
- **Don't** repetir el mismo shell de card para productos conceptualmente distintos sin ninguna variación.
- **Don't** usar lenguaje negativo o de miedo en ningún copy ("no te equivoques", "evita el error de...").
