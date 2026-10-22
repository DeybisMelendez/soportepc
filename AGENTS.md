# AGENTS.md

Guía del repositorio para sesiones de OpenCode que trabajen en **Soporte PC Managua**, un
sitio web de soporte técnico en instalación y configuración de programas profesionales
para computadoras.

> Lee primero [`README.md`](README.md) (contexto + setup),
> [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) (arquitectura y decisiones técnicas) y
> [`docs/ESTILOS.md`](docs/ESTILOS.md) (sistema de diseño). El contexto del negocio está en
> [`docs/NEGOCIO.md`](docs/NEGOCIO.md).

## Qué es el proyecto

Soporte PC Managua ofrece dos modalidades de servicio:

- **Presencial (visita al cliente)** en **toda Managua**.
- **Remoto (acceso a distancia)** en **toda Nicaragua**.

El sitio web presenta el servicio, genera confianza y capta clientes.

## Filosofía de desarrollo

- **KISS**: código simple y legible, sin complicaciones innecesarias.
- **Código siempre en inglés, documentación siempre en español** (nombres de variables,
  funciones, clases y mensajes de commit en inglés; comentarios, docstrings, README y
  archivos de `/docs/` en español).
- **Claridad sobre ingeniosidad**: el código debe ser legible por otro desarrollador.
- **Cada cambio debe ir acompañado de su actualización en la documentación** correspondiente.
- `/docs/` es el lugar reservado para documentación y contexto, tanto para desarrolladores
  humanos como para agentes.
- **Sin Node.js**: no introducir `package.json`, Prettier, ESLint ni Stylelint.
- **Frontend sin framework ni librería**: CSS puro y JavaScript vanilla. Nada de Bootstrap,
  Tailwind, React o jQuery. Un solo archivo de CSS y uno de JS, sin build.
- **Iconos sin CDN ni fuente de iconos**: los iconos de interfaz son trazados de Google
  Material Symbols copiados en `partials/icon.html`; los logotipos de marca son archivos
  `.svg` reales en `static/img/icons/`. Ni Font Awesome, ni Material Icons por CDN, ni
  `bootstrap-icons`. Cada icono debe pesar lo mínimo y servirse desde el propio dominio.

## Estado actual del proyecto

La página de inicio **ya está implementada**. Esto es lo que existe hoy:

- Paquete `core/` con la configuración del proyecto (`settings.py`, `urls.py`, `asgi.py`,
  `wsgi.py`), incluyendo el diccionario `BUSINESS` con los datos de contacto.
- App `landing/` con la página de inicio y sus rutas en `core/urls.py`:
  - `landing/content.py` — todo el copy del sitio en constantes Python.
  - `landing/structured_data.py` — genera el JSON-LD.
  - `landing/views.py` — vistas públicas, `robots.txt`, `sitemap.xml` y el 404.
  - `landing/templatetags/landing_tags.py` — filtro `whatsapp_link`.
  - `landing/management/commands/build_og_image.py` — imagen social e iconos.
- `templates/base.html` con el `head` SEO completo, más `404.html`,
  `landing/home.html`, `landing/thanks.html` y los parciales compartidos.
- `static/css/main.css` (sistema de diseño completo, ~40 KB) y `static/js/main.js`
  (4 módulos vanilla, ~10 KB).
- Sin modelos de negocio: el contenido vive en `content.py`, no en la base de datos.

**Al añadir una página nueva**: extiende `base.html`, expone sus datos en la vista,
compón con los componentes existentes de `main.css` y añade la ruta en
`landing/urls.py` con el namespace `landing:`. Consulta
[`docs/ESTILOS.md`](docs/ESTILOS.md) antes de escribir CSS.

## Entorno

- El venv de Python vive en `.venv/` (no en `.env/`). Activar con `source .venv/bin/activate`.
- Dependencias en `requirements.txt`: Django 6.1.2, `python-dotenv` 1.2.4, Pillow 11.3.0,
  y el stack de calidad (Ruff 0.14.1, djLint 1.36.4). Configuración de herramientas en
  `pyproject.toml`.
- `core/settings.py` carga variables de entorno desde un archivo `.secret` en la raíz del
  proyecto mediante `load_dotenv(BASE_DIR / ".secret")`. El archivo está en `.gitignore`.
  Variables esperadas:
  - `DJANGO_SECRET_KEY` — sin default seguro. Definir siempre en producción.
  - `DJANGO_DEBUG` — string exacto `"True"` para habilitar. Nunca en producción.
  - `DJANGO_SITE_URL` — URL pública del sitio **sin barra final**, con esquema incluido
    (ej. `https://tudominio.com.ni`). Fuente de verdad para `<link rel="canonical">`,
    `og:url`, `sitemap.xml` y `robots.txt`. Default `http://localhost:8000`.
    `settings.py` aplica `.rstrip("/")`, así que la barra final se normaliza sola.
    **Sin esto en producción, el sitemap y los canonicals emitirán URLs de `localhost`.**
  - `DJANGO_WHATSAPP_NUMBER` — número internacional **solo dígitos** (ej. `50555025301`).
    Destino de todos los enlaces `wa.me`.
  - `DJANGO_PHONE_DISPLAY` — número como se muestra al usuario (ej. `5502-5301`).
  - `DJANGO_OG_IMAGE` — ruta relativa a `STATIC_URL` de la imagen social.
- `settings.BUSINESS` concentra nombre, teléfono, cobertura, idioma, imagen social y
  coordenadas. Cambiar esos datos **nunca** obliga a tocar vistas ni templates.

## Problemas conocidos

- `ALLOWED_HOSTS = ["*"]` — aceptable en dev, **restringir en producción**.
- `SECRET_KEY` con default inseguro y público en el repo. Si no se define
  `DJANGO_SECRET_KEY`, Django usa esa clave.
- `STATIC_ASSET_VERSION` es manual: hay que subirlo en cada despliegue que toque
  CSS, JS o imágenes, o los navegadores servirán la versión anterior 30 días.
- Número de WhatsApp por defecto sin confirmar (ver `docs/NEGOCIO.md`).
- Sin entidades de negocio (clientes, solicitudes) — diseño pendiente.
- Sin página de detalle por servicio: las seis tarjetas van a WhatsApp. Una URL
  propia por servicio sería la siguiente mejora de SEO.

## Comandos

### Desarrollo

- Levantar servidor: `python manage.py runserver` (tras activar `.venv`). Para `DEBUG=True`
  y estáticos automáticos, define `DJANGO_DEBUG=True` en `.secret`.
- Admin: `python manage.py createsuperuser`, luego visitar `/admin/`.
- Migraciones: `python manage.py makemigrations && python manage.py migrate`.
- Imagen social: `python manage.py build_og_image` — regenera `og-home.png` (1200×630)
  y los iconos. Ejecutarlo si cambia el nombre, el color o el teléfono del negocio.
- Producción: `python manage.py collectstatic` y subir `STATIC_ASSET_VERSION` en
  `core/settings.py`.

### Calidad Python (Ruff)

- `ruff check .` (lint) · `ruff check --fix .` (autofix) · `ruff format .` (formatear) ·
  `ruff format --check .` (verificar formato).

### Calidad templates (djLint)

- `djlint templates/ --check` (lint) · `djlint templates/ --reformat` (formatear).

### Validación

- `python manage.py check` — URLs, templates, settings, modelos y admin. Única capa que
  detecta errores de template que djLint no ve (un `{% block %}` desbalanceado, una
  variable mal escrita). Tarda menos de un segundo.

## Stack de calidad y validación

Tres herramientas, todas instalables vía `pip`, alineadas con la decisión de no introducir
Node:

- **Ruff** — linter + formatter de Python. Reemplaza a flake8/black/isort/mypy.
  Config en `pyproject.toml` (`[tool.ruff]`): `line-length = 100`, `target-version = "py312"`,
  reglas `E`, `W`, `F`, `I`, `B`, `UP`, `SIM`, `RUF`, `DJ`. Excluye `.venv`, `migrations`,
  `media`, `staticfiles`.
- **djLint** — linter + formatter de templates Django en `templates/`.
  Config en `pyproject.toml` (`[tool.djlint]`): `profile = "django"`, `indent = 2`,
  `max_line_length = 100`.
  Nota: expande los SVG de `templates/partials/icon.html` a varias líneas cada uno.
  Es el comportamiento esperado con esta configuración; no es un error.
- **`python manage.py check`** — validación propia de Django (ver arriba).

En conjunto cubren la capa sintáctica y estructural en ~2.5 segundos.

**Lo que NO se usa (decisión explícita):**

- **Sin tests automatizados**: no hay suite en el repo (ni unitarios, ni integración, ni
  E2E). No instalar pytest, unittest, Playwright ni ningún framework de testing.
- **Sin Node/npm** bajo ningún motivo.
- **Sin mypy, black, isort, flake8 por separado**: Ruff los cubre.
- **Sin pre-commit hooks**: la ejecución es manual.
- **Sin CI**: no configurar GitHub Actions ni equivalente.

## Alcance del agente

El agente **puede** ejecutar las herramientas de calidad al terminar cada tarea. Todas
corren en segundos y no requieren servidor, navegador ni datos de prueba:

- `ruff check .` y `ruff format --check .` para Python.
- `djlint templates/ --check` para templates (solo si hay templates).
- `python manage.py check` para URLs, templates y settings.

El agente NO debe:

- Levantar `runserver` ni dejar procesos colgados.
- Modificar la base de datos para "preparar datos de prueba".
- Escribir tests, scripts de validación throwaway ni archivos sueltos en `/tmp` o en la
  raíz. Para comprobar algo puntual, usar `manage.py shell` de forma puntual y no dejar el
  script en el repo.
- Levantar dependencias de Node.
- Commitear `.secret` o `db.sqlite3` (ya ignorados, pero verifícalo).

La **verificación última** (aceptación funcional, pruebas de flujos, revisión visual y
responsive) sigue siendo **personal y manual del desarrollador**: las herramientas cubren
únicamente la capa sintáctica y estructural, no el comportamiento en navegador.