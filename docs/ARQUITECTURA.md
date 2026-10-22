# Arquitectura técnica — Soporte PC Managua

Documento de referencia para desarrolladores humanos y asistentes de IA que trabajan en
este repositorio. Describe el estado real del proyecto, las decisiones tomadas y lo que
falta por construir.

Documentos relacionados:

- [`NEGOCIO.md`](NEGOCIO.md) — contexto del negocio.
- [`ESTILOS.md`](ESTILOS.md) — sistema de diseño, tokens y componentes.

## Principios del proyecto

- **KISS**: código simple, legible, sin complicaciones innecesarias.
- **Código siempre en inglés, documentación siempre en español**. Esto incluye nombres de
  variables, funciones, clases y mensajes de commit; los comentarios, docstrings, README y
  los archivos de `/docs/` van en español.
- **Claridad sobre ingeniosidad**: el código debe poder leerse de un vistazo por otro
  desarrollador.
- **Cada cambio se acompaña de su actualización en la documentación** correspondiente.
- **Sin Node.js**: el proyecto es 100% Python. No se introducen `package.json`, Prettier,
  ESLint ni Stylelint.

## Stack

| Componente | Tecnología | Versión |
|---|---|---|
| Framework | Django | 6.1.2 |
| Lenguaje | Python | 3.12 |
| Base de datos | SQLite (vía Django) | — |
| Variables de entorno | python-dotenv | 1.2.4 |
| Imágenes | Pillow | 11.3.0 |
| Lint + format Python | Ruff | 0.14.1 |
| Lint + format templates | djLint | 1.36.4 |

Dependencias declaradas en `requirements.txt` (runtime + calidad).
Configuración de herramientas en `pyproject.toml`.

## Estructura del proyecto

```
soportepc/
├── core/                  # Paquete del proyecto (configuración central)
│   ├── settings.py        # Settings de Django
│   ├── urls.py            # URLs raíz
│   ├── asgi.py            # Entrada ASGI
│   └── wsgi.py            # Entrada WSGI
├── landing/               # App del sitio público
│   ├── apps.py            # AppConfig
│   ├── content.py         # Copy del sitio en constantes Python
│   ├── structured_data.py # Generador de JSON-LD
│   ├── views.py           # Vistas públicas + SEO técnico
│   ├── urls.py            # Rutas (con app_name = "landing")
│   ├── templatetags/
│   │   └── landing_tags.py  # Filtro `whatsapp_link`
│   ├── management/commands/
│   │   └── build_og_image.py  # Genera imagen social e iconos
│   ├── models.py          # Vacío: el contenido vive en `content.py`
│   ├── admin.py
│   └── migrations/
├── templates/             # Templates HTML (a nivel de proyecto)
│   ├── base.html          # Esqueleto común: head SEO, header, footer
│   ├── 404.html
│   ├── partials/          # header, footer, iconos, JSON-LD
│   └── landing/           # home.html, thanks.html
├── static/                # Estáticos: css/, js/, img/, manifest
│   ├── css/main.css       # Sistema de diseño completo
│   ├── js/main.js         # JS vanilla, 4 módulos
│   └── img/               # og-home.png, iconos, favicon.svg
├── docs/                  # Documentación (incluye ESTILOS.md)
├── manage.py
├── requirements.txt
├── pyproject.toml
└── .secret                # Variables de entorno (no versionado)
```

### Apps

- **`core`** — no es una app instalable; es el paquete que contiene la configuración del
  proyecto (`settings.py`, `urls.py`, etc.). Todas las apps están en `INSTALLED_APPS` de
  `core/settings.py`.
- **`landing`** — la app del sitio público. Registrada en `INSTALLED_APPS` como
  `landing.apps.LandingConfig`. Tiene `app_name = "landing"`, así que sus rutas se
  referencian siempre con el namespace: `{% url 'landing:home' %}`.

  Reparte sus responsabilidades en cuatro piezas, en vez de acumularlo todo en las
  vistas:

  | Archivo | Responsabilidad |
  |---|---|
  | `content.py` | El copy del sitio en constantes Python. Sin modelos ni base de datos. |
  | `structured_data.py` | Construye el JSON-LD con `json.dumps`. |
  | `views.py` | Vistas sin estado: eligen template y arman el contexto. |
  | `templatetags/landing_tags.py` | Filtro `whatsapp_link` (ver más abajo). |

### Por qué el contenido son constantes y no modelos

`landing/content.py` es la fuente de verdad de todo el texto visible: hero,
servicios, proceso, cobertura, FAQ y metadatos SEO.

Se eligió así, y no con modelos de Django, porque:

- El contenido es estático y solo lo edita el desarrollador.
- Evita migraciones y fixtures para un sitio que no tiene CMS.
- El JSON-LD se genera con `json.dumps` desde Python; en la plantilla, un
  `{{ valor }}` produciría `&quot;` dentro del JSON y los buscadores no lo
  parsearían.

La forma de los diccionarios está pensada para que la migración a modelos sea
mecánica si el contenido llega a necesitar edición por parte de un cliente.

### El filtro `whatsapp_link`

Django **no permite llamar funciones con argumentos en una plantilla**:
`{{ whatsapp mensaje }}` es error de sintaxis. Por eso la vista expone
`whatsapp` como función (para uso desde Python) y `landing_tags.py` la expone
además como filtro, que es la única vía que el lenguaje soporta:

```html
{% load landing_tags %}
<a href="{{ 'Hola, necesito ayuda'|whatsapp_link }}">…</a>
```

El argumento de un filtro tampoco puede ser una expresión compleja, así que el
patrón es siempre el mismo: la vista aplana los datos y el template usa una
variable simple.

## Configuración (`core/settings.py`)

### Variables de entorno

Se leen desde un archivo `.secret` en la raíz del proyecto, cargado con
`load_dotenv(BASE_DIR / ".secret")`. El archivo está en `.gitignore` y **no se versiona**.

| Variable | Default | Descripción |
|---|---|---|
| `DJANGO_SECRET_KEY` | clave insegura de Django | Clave secreta. **Definir siempre en producción.** |
| `DJANGO_DEBUG` | `False` | Se activa solo con el string exacto `True`. Nunca en producción. |
| `DJANGO_SITE_URL` | `http://localhost:8000` | URL pública del sitio, **sin barra final**. Fuente de verdad para `canonical`, `og:url`, `sitemap.xml` y `robots.txt`. |
| `DJANGO_WHATSAPP_NUMBER` | `50555025301` | Número en formato internacional, **solo dígitos** (ej. `+50555555555` sin `+` ni espacios). Origen de todos los enlaces `wa.me`. |
| `DJANGO_PHONE_DISPLAY` | `5502-5301` | Cómo se muestra el número al usuario. |
| `DJANGO_OG_IMAGE` | `img/og-home.png` | Ruta relativa a `STATIC_URL` de la imagen social (1200×630). |

`SITE_URL` aplica `.rstrip("/")` a la variable, así que el valor con barra final se
normaliza automáticamente.

> **Importante:** si `DJANGO_SITE_URL` no se define en producción, el sitemap y los
> canonicals emitirán URLs de `localhost`.

### Datos del negocio (`settings.BUSINESS`)

Un diccionario con nombre, teléfono, cobertura, idioma, imagen social y
coordenadas. Es la fuente de verdad de esos datos: los consumen las vistas, el
JSON-LD, el pie de página y los enlaces de WhatsApp.

```python
BUSINESS = {
    "name": "Soporte PC Managua",
    "tagline": "…",
    "whatsapp_number": "50555025301",   # desde DJANGO_WHATSAPP_NUMBER
    "phone_display": "5502-5301",       # desde DJANGO_PHONE_DISPLAY
    "coverage_remote": "Toda Nicaragua",
    "coverage_onsite": "Toda Managua",
    "language": "es-NI",
    "og_image": "img/og-home.png",      # desde DJANGO_OG_IMAGE
    "og_image_alt": "…",
    "geo": {"latitude": 12.1150, "longitude": -86.2362},
}
```

Cambiar el teléfono o la cobertura nunca obliga a tocar vistas ni templates.

### Base de datos

SQLite en `db.sqlite3` (raíz del proyecto, ignorado por git). No hay configuración de
múltiples bases de datos.

### Estáticos y media

```python
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

`static/` contiene el código fuente de los estáticos (CSS, JS, imágenes) y **sí** se
versiona. `staticfiles/` es el destino de `collectstatic` y está ignorado. `media/`
contiene archivos subidos por el usuario y también está ignorado.

```python
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATIC_CACHE_TIMEOUT = 60 * 60 * 24 * 30   # 30 días
STATIC_ASSET_VERSION = "1"
```

`STATIC_CACHE_TIMEOUT` solo aplica con `DEBUG=False`; en desarrollo Django ignora
la caché para que los cambios en CSS se vean de inmediato.

> **`STATIC_ASSET_VERSION` es manual y es un paso obligatorio en cada despliegue.**
> Sin subirla, los navegadores y el CDN seguirán sirviendo la versión anterior
> del CSS o del JS durante 30 días. Si prefieres gestionarlo automáticamente,
> `ManifestStaticFilesStorage` lo resuelve por hash de contenido (requiere
> `collectstatic` en cada despliegue).

> **Compresión:** el CSS son ~40 KB sin comprimir. Con `gzip` o `Brotli` en el
> servidor baja de 6 KB. Configúrala en el servidor de producción: es la mayor
> mejora de rendimiento disponible y no cuesta código.

### Internacionalización

```python
LANGUAGE_CODE = "es-ni"
TIME_ZONE = "America/Managua"
USE_I18N = True
USE_TZ = True
```

## Frontend

Sin framework, sin librería, sin build. Tres archivos versionados y nada más.

### Decisiones

| Decisión | Motivo |
|---|---|
| CSS puro en un archivo | Una petición en lugar de N. Sin `@import`, que además es bloqueante |
| JS vanilla en un archivo | Cuatro módulos, sin dependencias que mantener ni actualizar |
| Tipografía del sistema | Cero webfonts: sin peticiones, sin CLS, sin FOUT |
| SVG en línea (Material Symbols) | Cero peticiones y `currentColor` gratis, sin fuente externa |
| Logotipos de marca como `.svg` local | Trazado oficial real, servido desde el propio dominio |
| Gradientes CSS | Cero bytes en la respuesta frente a una imagen de fondo |
| `<details>` para la FAQ | Accesible por teclado y plegable **sin JavaScript** |

El sistema de diseño está documentado en [`ESTILOS.md`](ESTILOS.md): tokens,
convenciones, inventario de componentes y cómo construir una página nueva sin
escribir CSS.

### Rendimiento

El sitio carga **un HTML, un CSS, un JS y un SVG** en la ruta crítica. Los
iconos y la ilustración del hero son SVG en línea; la única imagen real es
`og-home.png`, que los buscadores descargan desde `og:image`, nunca el visitante.

Hay **dos sistemas de iconos**, con propósitos distintos:

**1. Iconos de interfaz — Google Material Symbols** (Apache License 2.0) en
`partials/icon.html`. Van en línea y pintan con `currentColor`. Se copian los
trazados en vez de enlazar la fuente por CDN porque una fuente de iconos serían
~40 KB y una petición bloqueante a un tercero, y porque así el sitio no depende
de que Google Fonts esté disponible.

**2. Logotipos de marca** — archivos `.svg` en `static/img/icons/`, cargados con
`<img>` desde `partials/brand_icon.html`. Un logotipo no puede recolorearse sin
dejar de ser el logotipo, así que va en su propio archivo. Los trazados son los
oficiales de [Simple Icons](https://simpleicons.org) (CC0-1.0), con WhatsApp,
Chrome, Firefox, Opera, VLC, Ubuntu, Linux, LibreOffice, Android y Apple.

**No hay librería ni CDN de iconos.** Es una decisión deliberada: añade peso y
una dependencia externa para algo que son unos pocos KB servidos desde el propio
dominio. El origen y la licencia de cada archivo están documentados en
`static/img/icons/README.md`.

El sitio es **completamente funcional sin JavaScript**: el CSS solo oculta
elementos animados cuando la clase `.js` está en `<html>`, y cada módulo de
`main.js` degrada por separado.

### SEO

Todo el `head` se construye en `templates/base.html` con bloques, y
`landing/structured_data.py` genera el JSON-LD con `json.dumps`.

- `title` y `meta description` con longitudes verificadas (≤ 60 / ≤ 160).
- `canonical` y `hreflang="es-ni"` construidos desde `SITE_URL`, **nunca** desde
  el host de la petición (que en desarrollo es `localhost`).
- Open Graph completo y Twitter Card `summary_large_image`.
- JSON-LD con `ProfessionalService` (con catálogo de servicios), `FAQPage` y
  `BreadcrumbList`, todo desde las mismas constantes que el HTML visible.
- `robots.txt` y `sitemap.xml` como vistas (`landing/views.py`), para que la URL
  del sitemap se derive de `SITE_URL`.
- `noindex` en las páginas de estado (404 y gracias), que no van al sitemap.

> El JSON-LD debe repetir **exactamente** lo que el usuario ve. Un dato
> estructurado que contradice la página es una penalización manual de Google.
> Por eso se genera desde `content.py` y no se escribe a mano.

### Imagen social

```bash
python manage.py build_og_image
```

Genera con Pillow tres archivos en `static/img/`:

| Archivo | Tamaño | Uso |
|---|---|---|
| `og-home.png` | 1200×630 | `og:image` y `twitter:image` |
| `apple-touch-icon.png` | 180×180 | Icono en iOS |
| `favicon.png` | 64×64 | Favicon raster de respaldo |

Se regenera, en lugar de versionarse como un binario opaco, porque es un
artefacto derivado de la paleta de marca. **Ejecutarlo de nuevo si cambia el
color, el nombre o el teléfono del negocio.**

### Comandos de gestión

| Comando | Función |
|---|---|
| `build_og_image` | Genera la imagen social y los iconos |

## Herramientas de calidad

Las tres herramientas cubren la capa **sintáctica y estructural**. Ninguna sustituye la
revisión manual en navegador.

### Ruff — Python

Linter y formatter único (reemplaza a flake8, black, isort y mypy).

```bash
ruff check .            # lint
ruff check --fix .      # autofix
ruff format .           # formatear
ruff format --check .   # verificar formato sin escribir
```

Configuración en `pyproject.toml` bajo `[tool.ruff]`: `line-length = 100`,
`target-version = "py312"`, y las categorías de reglas `E`, `W`, `F`, `I`, `B`, `UP`,
`SIM`, `RUF`, `DJ`. Excluye `.venv`, `migrations`, `media` y `staticfiles`.

### djLint — templates Django

Linter y formatter para los `.html` de `templates/`.

```bash
djlint templates/ --check      # lint
djlint templates/ --reformat   # formatear
```

Configuración en `pyproject.toml` bajo `[tool.djlint]`: `profile = "django"`, `indent = 2`.

### `python manage.py check`

Validación propia de Django: URLs, tags y filtros de template, settings, modelos y admin.
Es la **única** capa que detecta errores de template que djLint no ve — por ejemplo un
`{% block %}` desbalanceado o una variable de template mal escrita. Tarda menos de un
segundo.

```bash
python manage.py check
```

### Decisiones explícitas: lo que NO se usa

- **Sin tests automatizados.** No hay suite en el repo (ni unitarios, ni de integración,
  ni E2E). No se instala pytest, unittest, Playwright ni ningún framework de testing. El
  archivo generado `landing/tests.py` se eliminó por ser boilerplate vacío y contrario a
  esta decisión.
- **Sin Node/npm.** Ver la sección de principios.
- **Sin mypy, black, isort, flake8 por separado.** Ruff los cubre todos.
- **Sin pre-commit hooks.** La ejecución de las herramientas es manual.
- **Sin CI.** No se configura GitHub Actions ni equivalente.

## Problemas conocidos y pendientes

1. **`ALLOWED_HOSTS = ["*"]`** — aceptable en desarrollo, **debe restringirse en
   producción** al dominio real.
2. **`SECRET_KEY` insegura por defecto** — si no se define `DJANGO_SECRET_KEY` en `.secret`
   (o en el entorno de producción), Django usa una clave insegura que es pública en el
   repositorio.
3. **Sin modelos de negocio** — el contenido vive en `landing/content.py`. No hay entidades
   para clientes, solicitudes ni historial de servicios. Diseño pendiente.
4. **`ALLOWED_HOSTS = ["*"]` y `STATIC_ASSET_VERSION` manual** — ambos requieren atención en
   producción (ver arriba).
5. **Sin página de contacto propia** — todo el contacto es por WhatsApp. Si en el futuro se
   añade un formulario, necesitará protección contra spam y su propia ruta en el sitemap.
6. **Sin página de servicios en detalle** — los seis servicios son tarjetas en la portada con
   enlace directo a WhatsApp. Una URL por servicio (`/servicios/instalacion-windows/`) sería la
   siguiente mejora de SEO, porque cada una sería una página indexable con su propia keyword.

## Seguridad

- **Nunca** commitear `.secret` ni `db.sqlite3` (ya están en `.gitignore`).
- **Nunca** loguear ni hardcodear la `SECRET_KEY` en el código.
- En producción: `DEBUG=False`, `ALLOWED_HOSTS` restringido, y `DJANGO_SITE_URL` con el
  dominio real.

## Licencia

GNU General Public License v3.0. Ver [`LICENSE`](../LICENSE).