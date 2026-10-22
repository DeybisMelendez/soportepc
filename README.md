# Soporte PC Managua

Sitio web de **Soporte PC Managua**, un servicio de soporte técnico especializado en la
**instalación y configuración de programas profesionales para computadoras**.

El objetivo del sitio es presentar el servicio, generar confianza y captar clientes que
necesitan ayuda técnica en su equipo.

## Qué ofrecemos

Trabajamos en dos modalidades, según lo que el cliente necesite y la cercanía de la zona:

### Servicio presencial (visita al cliente)

Un técnico se desplaza hasta el domicilio u oficina del cliente en **toda la zona de
Managua** para instalar, configurar o resolver problemas directamente en su computadora.

Ideal para:

- Formateo e instalación de sistemas.
- Cambio de disco duro, RAM u otros componentes.
- Problemas de hardware que requieren presencia física.
- Instalación de redes y configuración de equipos compartidos.

### Servicio remoto (soporte a distancia)

Resolvemos el problema **conectándonos al equipo del cliente mediante acceso remoto**, sin
necesidad de visita. Disponible en **toda Nicaragua**, sin restricciones de zona.

Ideal para:

- Instalación y configuración de programas de trabajo.
- Resolución de errores y problemas de rendimiento.
- Configuración de correo, navegadores y software de oficina.
- Soporte para empresas con varias sucursales o usuarios en distintas ciudades.

> **Resumen de cobertura:** presencial en **toda Managua**, remoto en **toda Nicaragua**.

## Público objetivo

El sitio está dirigido principalmente a personas y pequeñas empresas que:

- Necesitan instalar software profesional (contabilidad, diseño, arquitectura, CAD, etc.).
- No cuentan con personal de soporte técnico propio.
- Prefieren un servicio cercano, en español y con atención personalizada.
- Quieren resolver un problema técnico de forma rápida y sin complicaciones.

---

## Stack tecnológico

- **Backend:** [Django 6.1.2](https://docs.djangoproject.com/en/6.1/) (Python 3.12)
- **Base de datos:** SQLite (mediante el módulo de Django)
- **Variables de entorno:** `python-dotenv` (archivo `.secret`)
- **Imágenes y archivos:** Pillow
- **Frontend:** CSS puro y JavaScript vanilla. **Sin framework, sin librería,
  sin build y sin Node.js.**
- **Calidad de código:** Ruff (Python) y djLint (templates Django)
- **Licencia:** GNU General Public License v3.0 (ver `LICENSE`)

El sitio carga **un HTML, un CSS, un JS y un SVG**, con la tipografía del sistema:
cero peticiones a terceros, cero webfonts y cero fuentes de iconos externas. Los
iconos de interfaz son Material Symbols en línea y los logotipos son archivos
`.svg` locales. Es completamente funcional sin JavaScript.

## Puesta en marcha (entorno local)

### Requisitos previos

- Python 3.12 o superior.

### Instalación

1. **Clonar el repositorio**

   ```bash
   git clone <url-del-repositorio>
   cd soportepc
   ```

2. **Crear y activar el entorno virtual**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # En Windows: .venv\Scripts\activate
   ```

3. **Instalar las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las variables de entorno**

   Crea un archivo `.secret` en la raíz del proyecto (ya está incluido en `.gitignore`):

   ```ini
   DJANGO_SECRET_KEY=cambia-esta-clave-por-una-segura
   DJANGO_DEBUG=True
   DJANGO_SITE_URL=http://localhost:8000
   ```

   - `DJANGO_SECRET_KEY`: clave secreta de Django.
   - `DJANGO_DEBUG`: pon `True` solo en desarrollo.
   - `DJANGO_SITE_URL`: URL pública del sitio **sin barra final**, con esquema incluido. En
     producción define aquí tu dominio real (por ejemplo `https://tudominio.com.ni`) para que
     los enlaces canónicos, `og:url`, `sitemap.xml` y `robots.txt` sean correctos.

5. **Aplicar las migraciones**

   ```bash
   python manage.py migrate
   ```

6. **Crear un usuario administrador** (para acceder a `/admin/`)

   ```bash
   python manage.py createsuperuser
   ```

7. **Levantar el servidor de desarrollo**

   ```bash
   python manage.py runserver
   ```

   El sitio queda disponible en <http://localhost:8000/> y el panel de administración en
   <http://localhost:8000/admin/>.

## Comandos útiles

### Desarrollo

```bash
python manage.py runserver                 # Servidor de desarrollo
python manage.py makemigrations            # Crear migraciones tras cambiar modelos
python manage.py migrate                   # Aplicar migraciones
python manage.py createsuperuser           # Crear usuario admin
```

### Calidad de código

```bash
ruff check .            # Analizar errores y estilo en Python
ruff format .           # Formatear el código Python
ruff check --fix .      # Corregir automáticamente lo que se pueda
djlint templates/ --check      # Analizar templates Django
djlint templates/ --reformat   # Formatear los templates
```

### Validación

```bash
python manage.py check   # Validar URLs, templates, settings y modelos
```

### Frontend

```bash
python manage.py build_og_image       # Regenera la imagen social (1200x630) e iconos
python manage.py collectstatic        # Prepara staticfiles/ para producción
```

Ejecuta `build_og_image` de nuevo si cambian el nombre, el color o el teléfono
del negocio. En producción, **sube también `STATIC_ASSET_VERSION`** en
`core/settings.py` para invalidar la caché del navegador.

## Estructura del proyecto

```
soportepc/
├── core/                 # Configuración central del proyecto Django
│   ├── settings.py       # Configuración (base de datos, apps, estáticos, seguridad)
│   ├── urls.py           # URLs raíz del proyecto
│   ├── asgi.py           # Entrada para servidores ASGI
│   └── wsgi.py           # Entrada para servidores WSGI
├── landing/              # App del sitio público
│   ├── content.py        # Copy del sitio en constantes Python
│   ├── structured_data.py # Generador de JSON-LD
│   ├── views.py          # Vistas públicas y SEO técnico
│   ├── urls.py           # Rutas (namespace "landing")
│   ├── templatetags/     # Filtro whatsapp_link
│   └── management/commands/build_og_image.py
├── templates/            # Templates HTML
│   ├── base.html         # Esqueleto común (head SEO, header, footer)
│   ├── 404.html
│   ├── partials/         # header, footer, iconos, JSON-LD
│   └── landing/          # home.html, thanks.html
├── static/               # Archivos estáticos (versionado)
│   ├── css/main.css      # Sistema de diseño completo
│   ├── js/main.js        # JS vanilla (menú, scrollspy, animaciones)
│   └── img/              # Imagen social, favicon y logos de marca (icons/)
├── docs/                 # Documentación del proyecto
├── media/                # Archivos subidos por usuarios (no versionado)
├── manage.py             # Utilidad de línea de comandos de Django
├── requirements.txt      # Dependencias del proyecto
├── pyproject.toml        # Configuración de Ruff y djLint
├── .secret               # Variables de entorno (no versionado)
└── README.md             # Este archivo
```

## Documentación

- [`docs/NEGOCIO.md`](docs/NEGOCIO.md) — Contexto del negocio, servicios, cobertura y SEO.
- [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) — Arquitectura técnica y decisiones del proyecto.
- [`docs/ESTILOS.md`](docs/ESTILOS.md) — Sistema de diseño: tokens, componentes y reutilización.
- [`AGENTS.md`](AGENTS.md) — Guía para asistentes de IA que trabajan en este repositorio.

## Licencia

Este proyecto está bajo la licencia [GNU General Public License v3.0](LICENSE).