# Sistema de estilos

Documento de referencia del CSS y del JavaScript del sitio. Antes de escribir
CSS nuevo, léelo entero: casi siempre la clase que falta ya existe.

- **Fuente del CSS:** `static/css/main.css` (~40 KB sin comprimir, un solo
  archivo, sin `@import`).
- **Fuente del JS:** `static/js/main.js` (~10 KB, un solo archivo, sin
  dependencias).
- **Tokens y componentes:** definidos en el propio CSS, con el porqué de cada
  decisión comentada.

## Las tres reglas

1. **Ningún color ni espaciado literal en un componente.** Todo sale de un
   token de la sección `01. TOKENS`. Cambiar la marca es cambiar ese bloque, y
   nada más.
2. **Cada componente es autónomo.** Define su propia caja y no depende de la
   sección donde vive. Si necesita variantes, se añaden como modificadores
   (`bloque--variante`), nunca como selectores sueltos que se pueden pisar.
3. **Antes de añadir una clase, comprobar si ya existe una que haga lo mismo.**
   El CSS duplicado es la primera causa de que un sistema de diseño se pudra.

## Índice

- [Tokens](#tokens)
- [Convenciones de nombres](#convenciones-de-nombres)
- [Inventario de componentes](#inventario-de-componentes)
- [Cómo construir una página nueva](#cómo-construir-una-página-nueva)
- [Responsive](#responsive)
- [Accesibilidad](#accesibilidad)
- [JavaScript](#javascript)
- [Rendimiento](#rendimiento)
- [Reglas de formato](#reglas-de-formato)

---

## Tokens

Todos viven en `:root`, al principio de `main.css`. Hay cuatro familias.

### Color

La paleta es **índigo (marca) + naranja (acento) + verde (WhatsApp)**.

Se nombran por **función**, no por color, para que cambiar la paleta no obligue
a tocar los componentes:

| Token | Uso |
| --- | --- |
| `--color-bg` / `--color-bg-soft` / `--color-bg-inverse` | Fondo de página, de sección alterna y de bloque oscuro |
| `--color-text` / `--color-text-muted` | Texto principal y secundario |
| `--color-text-inverse` / `--color-text-inverse-muted` | Texto sobre fondo oscuro |
| `--color-border` / `--color-border-strong` | Separadores y bordes |
| `--color-primary` / `--color-primary-hover` / `--color-primary-soft` | Marca: enlaces, iconos, botones |
| `--color-accent` / `--color-accent-hover` / `--color-accent-soft` | Acento: lo que quiero que se vea |
| `--color-whatsapp` / `--color-whatsapp-hover` | Solo botones de WhatsApp |

Los tonos crudos (`--indigo-600`, `--orange-500`, …) están disponibles, pero
**solo se usan para construir los tokens semánticos** de esta tabla. Un
componente que escribe `--indigo-600` directamente está saltándose el sistema.

### Espaciado

Escala de 4 px, `--space-1` (4 px) a `--space-9` (96 px). No hay valores
intermedios: un `--space-3.5` rompe la alineación vertical entre tarjetas.

### Tipografía

- `--font-sans` — pila del sistema. **No añadir webfonts** sin justificar el
  coste: una fuente externa son ~100 KB, una petición bloqueante y una fuente de
  reserva mal configurada.
- `--text-xs` … `--text-4xl` — escala fluida con `clamp()`. El texto se adapta
  al ancho sin media queries, lo que evita saltos entre breakpoints.
- `--leading-tight` / `--leading-snug` / `--leading-normal` — interlineado.

### Layout

`--container-max` (72 rem), `--container-narrow` (46 rem), `--header-height` y
la escala de `--z-*` (`header`, `mobile-nav`, `float`).

### Rejibrar

```css
:root {
  --color-primary: #0f766e;   /* verde azulado */
  --color-primary-hover: #115e59;
  --color-primary-soft: #ccfbf1;
  --color-accent: #db2777;    /* magenta */
  --color-accent-hover: #be185d;
  --color-accent-soft: #fce7f3;
}
```

Y actualizar los tres colores que quedan fuera del CSS: `--theme-color` en
`base.html`, `"theme_color"` en `static/manifest.webmanifest` y las constantes de
`landing/management/commands/build_og_image.py`.

---

## Convenciones de nombres

BEM-lite, sin `@apply` ni nada que requiera compilación:

```
.bloque            elemento de nivel superior
.bloque__elemento   parte interna de un bloque
.bloque--variante  modificación del bloque
```

- Todo en minúsculas y con guiones: `.service-card__title`, no `.serviceCardTitle`.
- El guion separa palabras del nombre: `.site-nav__list`, no `.sitenav_list`.
- Los modificadores se declaran siempre **junto a su bloque**, nunca sueltos
  al final del archivo: así se lee todo el componente en un solo sitio.

---

## Inventario de componentes

Cada uno es autónomo. El markup es de ejemplo y se puede copiar tal cual.

### `.container` / `.container--narrow`

Ancho máximo del contenido y centrado.

```html
<div class="container">…</div>
<div class="container container--narrow">…</div>
```

### `.section` + `.section__header`

Una banda vertical de contenido. `--services`, `--process`, `--coverage`,
`--faq` y `--contact` solo añaden el color de fondo cuando hace falta.

```html
<section class="section" id="mi-seccion" aria-labelledby="mi-seccion-title">
  <div class="container">
    <header class="section__header">
      <h2 class="section__title" id="mi-seccion-title">Título</h2>
      <p class="section__intro">Texto de apoyo.</p>
    </header>
    …
  </div>
</section>
```

> `aria-labelledby` no es opcional: apunta al `<h2>` de la sección. Sin él, un
> lector de pantalla anuncia la sección sin decir de qué trata.

### `.btn` + modificadores

`.btn` define la caja. Las variantes solo cambian el color, nunca la forma: por
eso todos los botones del sitio tienen la misma silueta.

| Modificador | Cuándo usarlo |
| --- | --- |
| `--primary` | Acción principal de una pantalla (índigo) |
| `--whatsapp` | **Siempre** que el destino sea WhatsApp (verde) |
| `--ghost` | Acción secundaria, no debe competir con la principal |
| `--sm` / `--lg` | Tamaño. Por defecto es mediano |
| `--block` | Ancho completo, en columnas estrechas o móvil |

```html
<a class="btn btn--primary btn--lg" href="…">Cotizar</a>
<a class="btn btn--whatsapp" href="…" target="_blank" rel="noopener">
  {% include "partials/icon.html" with name="whatsapp" %}
  <span>WhatsApp</span>
</a>
```

### `.card`

Caja de contenido con borde, sombra sutil y elevación al pasar el cursor. Base
de las tarjetas de servicio y de cobertura.

### `.brand`

Logotipo + nombre. La marca usa `currentColor`, así que el mismo bloque funciona
sobre fondo claro (`.brand`) y en el pie (`.brand--footer`).

### `.badge`

Etiqueta compacta. En el hero muestra una modalidad de cobertura (título +
detalle); sobre fondo oscuro usa translucidez y `backdrop-filter`.

### `.service-card`, `.coverage__card`

Tarjetas con icono, título, descripción y enlace de consulta. Cada una lleva su
propio `id` para poder enlazarse por ancla.

### `.steps` / `.step`

Proceso numerado. Usa `<ol>`, no `<div>`: la numeración es una lista ordenada y
los lectores de pantalla la anuncian como tal.

### `.faq` / `.faq__item`

Preguntas frecuentes con `<details>`/`<summary>` nativo. **Sin JavaScript**: el
marker es un `+` dibujado con pseudoelementos que gira al abrirse. Añadir
`[open]` en el HTML abre la respuesta por defecto.

### `.cta-banner`

Bloque de conversión final: fondo índigo, título, texto y botón. Cambia a
disposición horizontal a partir de 768 px.

### `.site-header` / `.mobile-nav`

Barra fija (`sticky`, no `fixed`) con navegación y CTA. El panel móvil lleva
`hidden` en el HTML y lo gestiona `main.js`; sin JS, no hay panel, pero los
enlaces del pie siguen accesibles.

### `.site-footer`

Cuatro columnas: marca y cobertura, servicios, navegación y contacto. La
primera ocupa dos del grid (`grid-column: span 2`).

### `.whatsapp-float`

Botón circular de WhatsApp. Lleva `hidden` en el HTML y `main.js` lo muestra
tras 600 px de scroll. El CSS solo lo activa a partir de 1024 px, porque en
móvil taparía el contenido y ya hay CTA visibles.

### `.status-page` + `.checklist`

Páginas de estado (404, gracias). `.status-page__code` aplica un degradado al
texto con `background-clip: text`; el `color` sólido declarado antes actúa de
respaldo si el navegador no lo soporta.

### `.visually-hidden`

Oculta visualmente sin ocultar de lectores de pantalla. **No usar `display:
none` para ocultar texto**: lo elimina del árbol de accesibilidad.

### `.skip-link`

Enlace de salto al contenido. Invisible hasta que recibe foco por teclado.

---

## Cómo construir una página nueva

1. **Crear el template** en `templates/<app>/<pagina>.html` con
   `{% extends "base.html" %}` y `{% load landing_tags %}`.
2. **Definir los datos** en `landing/content.py` y exponerlos en la vista.
   Nunca escribir el copy del cliente dentro del HTML.
3. **Meter el JSON-LD** desde la vista con `build_structured_data(crumbs=…)`.
4. **Componer con los componentes existentes.** Si hace falta uno nuevo, crear
   su bloque en la sección `06. COMPONENTES` del CSS con su comentario, y
   documentarlo aquí.
5. **Añadir la ruta** en `landing/urls.py` y decidir si entra al sitemap.
6. **Validar**: `ruff check .`, `djlint templates/ --check`,
   `python manage.py check`.

Si la página es un estado (error, confirmación), reutilizar `.status-page` y
añadir `noindex=True` a la vista.

---

## Responsive

Mobile-first: los estilos base son para móvil y cada bloque de la sección `08`
amplía. Solo dos puntos de corte, suficientes para este sitio:

| Punto | Ancho | Qué cambia |
| --- | --- | --- |
| — | < 768 px | Móvil: una columna, menú desplegable, botones a ancho completo bajo 480 px |
| `48rem` | ≥ 768 px | Tableta: navegación horizontal, hero a dos columnas, CTA del banner en fila |
| `64rem` | ≥ 1024 px | Escritorio: aparece el botón flotante de WhatsApp |

Las rejillas **no necesitan media queries**: usan
`repeat(auto-fit, minmax(min(100%, 18rem), 1fr))`, que ya se ajusta al número de
columnas que caben. El `min(100%, …)` es lo que evita que en un móvil estrecho
la columna mínima desborde.

---

## Accesibilidad

Verificado, no supuesto:

- **Contraste**: todos los pares texto/fondo alcanzan AA (≥ 4.5:1). El texto
  secundario sobre índigo 950 es `#c7d2fe` sobre `#1e1b4b` (≈ 9:1).
- **Foco**: `:focus-visible` dibuja un anillo de 2 px. El `outline` **no se
  elimina en ningún sitio**: es requisito, no decoración.
- **Movimiento**: `prefers-reduced-motion: reduce` desactiva el scroll suave y
  todas las transiciones, y muestra los bloques animados en su estado final.
- **Contraste alto**: `prefers-contrast: high` oscurece el texto secundario y
  engorda los bordes de las tarjetas.
- **Teclado**: el menú móvil cierra con `Escape` y devuelve el foco al botón;
  los enlaces del panel se cierran al pulsarlos.
- **Semántica**: un `<h1>` por página, `<ol>` para el proceso, `<details>` para
  la FAQ, `<nav aria-label>` para cada bloque de enlaces.
- **Iconos**: todos con `aria-hidden="true"` y `focusable="false"`. El significado
  lo aporta el texto al lado.

---

## JavaScript

Cuatro módulos en un IIFE, sin dependencias, cargado con `defer`.

**Regla que gobierna todo el archivo: el sitio funciona completo sin él.** El JS
solo mejora; nunca es la única vía a un contenido o una acción.

| Módulo | Qué hace | Sin JS |
| --- | --- | --- |
| `setupMobileNav()` | Abre y cierra el panel; cierra con `Escape` o clic fuera | No hay panel, pero los enlaces del pie funcionan |
| `setupScrollSpy()` | Marca con `aria-current` la sección visible | Los enlaces navegan a su ancla |
| `setupReveal()` | Anima la entrada de `[data-reveal]` al hacer scroll | Todo el contenido es visible |
| `setupFloatingCta()` | Muestra el botón flotante tras 600 px | El botón no aparece |

### Animaciones: la clase `.js`

El CSS **oculta** `[data-reveal]` solo cuando `.js` está en `<html>`:

```css
[data-reveal] { opacity: 1; }
.js [data-reveal] { opacity: 0; transform: translateY(1.5rem); }
.js [data-reveal].is-visible { opacity: 1; transform: none; }
```

La clase la añade un `<script>` inline en el `<head>` de `base.html`, antes de
que se pinte el cuerpo. Si el JS no carga, el contenido se ve desde el
principio. **Nunca inviertas esta lógica**: ocultar por defecto y mostrar con JS
significa páginas en blanco cuando algo falla.

### `IntersectionObserver`, no `scroll`

Los tres observadores usan `IntersectionObserver` en lugar de escuchar `scroll`:
el navegador notifica cuando toca, y el callback no se ejecuta en cada píxel.
El listener de `scroll` del botón flotante va con `{ passive: true }`.

### Dos tipos de icono

| | Iconos de interfaz | Logotipos de marca |
| --- | --- | --- |
| Partial | `partials/icon.html` | `partials/brand_icon.html` |
| Origen | Google Material Symbols | Archivos `.svg` en `static/img/icons/` |
| Cómo se carga | SVG en línea | `<img>` |
| Color | Hereda `currentColor` | Su color propio, fijo |

```html
{% load static %}
{% comment %}Icono de interfaz{% endcomment %}
{% include "partials/icon.html" with name="desktop_windows" %}

{% comment %}Logotipo de marca{% endcomment %}
{% include "partials/brand_icon.html" with name="whatsapp" size=24 %}
```

**Por qué dos sistemas.** Un icono de interfaz es genérico y debe adaptarse al
tema, así que va en línea y pinta con `currentColor`. Un logotipo es una
identidad: no se puede recolorear sin dejar de ser el logotipo, así que va en
su propio archivo y se carga con `<img>`. Tenerlos separados además permite
verificar los trazados de un vistazo y sustituirlos sin tocar código.

### Iconos de interfaz (Material Symbols)

Las claves son los nombres oficiales, para buscarlos en
<https://fonts.google.com/icons>:

`desktop_windows` · `apps` · `tune` · `build` · `support_agent` ·
`local_shipping` · `public` · `home` · `chat` · `map` · `verified` ·
`keyboard_arrow_down` · `menu`

Disponibles para reutilizar: `bolt`, `schedule`, `description`, `handyman`.

Al añadir uno: mantén `viewBox="0 0 24 24"`, `stroke-width="2"` (el grosor
estándar de Material), `fill="none"`, `aria-hidden="true"` y
`focusable="false"`.

### Logotipos de marca

Archivos reales en `static/img/icons/`, con su trazado oficial:

`whatsapp` · `windows` · `vlc` · `firefox` · `chrome` · `opera` · `ubuntu` ·
`linux` · `libreoffice` · `android` · `apple`

**No hay librería ni CDN de iconos**, por decisión del proyecto: una fuente de
iconos por CDN serían ~40 KB y una petición bloqueante a un tercero, y el sitio
no debe depender de que ese servicio esté disponible. Los archivos pesan entre
0.4 y 5 KB y se sirven desde el propio dominio.

Origen y licencia de cada archivo en
[`static/img/icons/README.md`](../static/img/icons/README.md). ⚠️ **`windows.svg`
es el único sin licencia clara** (Microsoft retiró su logotipo de Simple Icons y
no publica un SVG con licencia para terceros); está marcado ahí.

`width`/`height` se escriben siempre en el `<img>`: reserva el espacio antes de
que el SVG cargue y evita el desplazamiento de layout.

## Rendimiento

| Decisión | Por qué |
| --- | --- |
| Un solo archivo CSS | Una petición en lugar de N. Sin `@import`, que además es bloqueante |
| Un solo archivo JS, `defer` | No bloquea el render; se ejecuta tras el HTML |
| Tipografía del sistema | Cero webfonts: sin peticiones, sin CLS, sin FOUT |
| SVG inline en vez de sprites o `<img>` | Cero peticiones y `currentColor` gratis |
| Gradientes CSS en vez de imágenes de fondo | Cero bytes en la respuesta |
| Sin librería, sin framework | Nada que mantener ni que actualizar |
| Animar solo `opacity` y `transform` | Son las únicas propiedades que el navegador optimiza sin recalcular el layout |

Con 40 KB sin comprimir, **gzip o Brotli en el servidor** dejan la transferencia
por debajo de 6 KB. Configura la compresión estática en el servidor de
producción: es la mayor mejora disponible y no cuesta código.

`STATIC_ASSET_VERSION` en `settings.py` es la versión manual de la caché del
navegador. **Súbela en cada despliegue que toque CSS, JS o imágenes**, o los
usuarios seguirán viendo la versión anterior.

---

## Reglas de formato

Las aplica djLint (`profile = "django"`, `indent = 2`, `max_line_length = 100`):

- Un elemento por línea cuando tiene varios atributos, uno por línea.
- Atributo `class` siempre el primero.
- Cierre siempre explícito: `<rect />`, `<path />`. Nunca `<rect>` a secas.
- Sangría de 2 espacios.

```bash
djlint templates/ --check      # verificar
djlint templates/ --reformat   # corregir
```

Nota: djLint **expande los SVG** de `partials/icon.html` a ~10 líneas cada uno.
Eso es correcto según la configuración del repo; el archivo sigue siendo
pequeño en peso (7.8 KB) porque lo que crece son saltos de línea.