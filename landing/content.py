"""
Contenido editorial de las paginas publicas.

Este modulo es la fuente de verdad del copy del sitio: titulares, servicios,
proceso, preguntas frecuentes y textos de SEO. Se eligio esta via en lugar de
modelos de base de datos porque:

- El contenido es estatico y solo lo edita el desarrollador.
- Evita migraciones y fixtures para un sitio que aun no tiene CMS.
- Mantiene el copy en Python, separado del markup, y por lo tanto versionable
  y revisable en un solo lugar.

Si en el futuro el contenido debe editarlo un cliente sin tocar codigo, el
salto natural es convertir estas constantes en modelos de Django. La forma de
los diccionarios ya esta pensada para que esa migracion sea mecanica.

Convenciones:
- Los nombres de claves y variables van en ingles (regla del repositorio).
- Los textos visibles al usuario van en espanol.
- Cada servicio lleva un `icon` cuyo valor es una clave de `ICONS` en
  `templates/landing/_icons.html`, para mantener los SVG fuera del copy.
"""

from typing import Any, Final

# ---------------------------------------------------------------------------
# SEO
# ---------------------------------------------------------------------------

# Título de la página.
#
# Dos reglas de SEO que condicionan este valor:
#   - Google recorta a unos 60 caracteres. Superarlo hace que el título
#     aparezca cortado en los resultados, y lo que se pierde es justo la
#     keyword ("...para PC en Nic"), que es lo que el usuario busca.
#   - La keyword principal va al principio. El peso de Google se concentra en
#     el inicio del título.
#
# La marca y la ubicación van al final, tras un separador: identifican al
# buscador sin robarle sitio a las keywords, que ocupan el inicio y el peso
# principal. Con el sufijo son 60 caracteres, el límite exacto.
SEO_TITLE: Final = "Instalación de Programas para PC | Soporte Técnico Nicaragua"

# Descripcion de la pagina. El limite recomendado por Google es de 160
# caracteres; esta en 158, con la keyword principal al principio.
SEO_DESCRIPTION: Final = (
    "Instalamos y configuramos programas en tu PC o laptop. Soporte remoto en "
    "toda Nicaragua y visitas a domicilio en Managua. Cotización por WhatsApp."
)


# ---------------------------------------------------------------------------
# Seccion principal (hero)
# ---------------------------------------------------------------------------

HERO: Final[dict[str, Any]] = {
    # Texto pequeno sobre el H1. Aporta contexto sin competir por el titular.
    "eyebrow": "Soporte técnico en Nicaragua",
    "title": "Instalamos tus programas y dejamos tu computadora funcionando",
    "description": (
        "¿Necesitas instalar Windows, configurar un programa de trabajo o "
        "solucionar un problema con tu computadora? Te ayudamos a instalar y "
        "configurar software en tu PC o laptop, con asistencia remota en "
        "Nicaragua y visita a domicilio en Managua."
    ),
    # Etiquetas de cobertura. Refuerzan las dos modalidades del negocio.
    "badges": [
        {
            "title": "Remoto",
            "detail": "Toda Nicaragua",
            "icon": "public",
        },
        {
            "title": "A domicilio",
            "detail": "Toda Managua",
            "icon": "home",
        },
    ],
    # Llamado a la accion principal. Abre WhatsApp con un mensaje prellenado.
    "cta": {
        "label": "Solicitar cotización por WhatsApp",
        "message": (
            "Hola, necesito una cotización para instalar/configurar software en mi computadora."
        ),
    },
    # Llamado a la accion secundario: baja a la seccion de servicios.
    "cta_secondary": {
        "label": "Ver servicios",
        "href": "#servicios",
    },
    # Mensaje de confianza bajo los botones. Refuerza la ausencia de compromiso
    # economico antes de cotizar, tal como recomienda docs/NEGOCIO.md.
    "cta_note": "Cotización sin compromiso. Cuéntanos qué necesitas y te explicamos el precio.",
}

# Diferenciadores que venta confianza. Extraidos de los puntos de venta de
# docs/NEGOCIO.md: espanol, especialidad en software profesional, cobertura.
TRUST_POINTS: Final[list[dict[str, Any]]] = [
    {
        "title": "Atención en español",
        "description": "Te explicamos el problema y la solución sin tecnicismos.",
        "icon": "chat",
    },
    {
        "title": "Especialistas en software",
        "description": "Instalamos y configuramos programas profesionales, no solo hardware.",
        "icon": "apps",
    },
    {
        "title": "Cobertura nacional",
        "description": "Asistencia remota desde cualquier departamento de Nicaragua.",
        "icon": "map",
    },
]


# ---------------------------------------------------------------------------
# Servicios
# ---------------------------------------------------------------------------
# El `id` se usa como ancla en la URL y como clave del JSON-LD.
# El `icon` es una clave de `templates/partials/icon.html` (Material Symbols).
# El `message` es el texto que llega prellenado en WhatsApp, para que el
# cliente ya diga qué servicio necesita al escribirnos.

SERVICES: Final[list[dict[str, Any]]] = [
    {
        "id": "instalacion-windows",
        "title": "Instalación de Windows",
        "description": (
            "Instalación o reinstalación de Windows, configuración inicial y "
            "preparación de tu computadora para trabajar o estudiar."
        ),
        "icon": "desktop_windows",
        "message": "Hola, quiero cotizar la instalación de Windows en mi computadora.",
    },
    {
        "id": "instalacion-programas",
        "title": "Instalación de programas para PC",
        "description": (
            "Instalación y configuración de aplicaciones compatibles con tu "
            "equipo, de acuerdo con tus necesidades y las licencias "
            "correspondientes."
        ),
        "icon": "apps",
        "message": "Hola, quiero cotizar la instalación de un programa en mi computadora.",
    },
    {
        "id": "configuracion",
        "title": "Configuración de computadoras",
        "description": (
            "Ayuda para configurar una computadora nueva, instalar los "
            "controladores disponibles y preparar el sistema para su uso."
        ),
        "icon": "tune",
        "message": "Hola, necesito ayuda para configurar mi computadora.",
    },
    {
        "id": "solucion-problemas",
        "title": "Solución de problemas de software",
        "description": (
            "Asistencia para diagnosticar problemas de Windows, errores de "
            "aplicaciones y dificultades de configuración."
        ),
        "icon": "build",
        "message": "Hola, tengo un problema de software en mi computadora y necesito ayuda.",
    },
    {
        "id": "soporte-remoto",
        "title": "Soporte técnico remoto",
        "description": (
            "Recibe asistencia por internet cuando el problema pueda "
            "resolverse a distancia. La modalidad depende del trabajo "
            "requerido y de las condiciones del equipo."
        ),
        "icon": "support_agent",
        "message": "Hola, quiero consultar por soporte técnico remoto.",
    },
    {
        "id": "visita-domicilio",
        "title": "Servicio técnico a domicilio en Managua",
        "description": (
            "Consulta la disponibilidad de visitas presenciales para "
            "instalación de software y configuración de computadoras en "
            "Managua."
        ),
        "icon": "local_shipping",
        "message": "Hola, quiero consultar por una visita a domicilio en Managua.",
    },
]


# ---------------------------------------------------------------------------
# Proceso
# ---------------------------------------------------------------------------

PROCESS_TITLE: Final = "¿Cómo funciona?"
PROCESS_INTRO: Final = "Tres pasos, sin sorpresas. Cotizamos antes de empezar."
PROCESS_STEPS: Final[list[dict[str, Any]]] = [
    {
        "title": "Cuéntanos tu problema",
        "description": (
            "Indica qué computadora tienes y qué necesitas instalar o "
            "solucionar. Por WhatsApp basta."
        ),
    },
    {
        "title": "Recibe una cotización",
        "description": ("Te explicamos el servicio, el precio y la modalidad de atención."),
    },
    {
        "title": "Coordina el trabajo",
        "description": (
            "Si aceptas la cotización, acordamos la asistencia remota o la "
            "visita presencial, según corresponda."
        ),
    },
]


# ---------------------------------------------------------------------------
# Cobertura
# ---------------------------------------------------------------------------

COVERAGE_TITLE: Final = "Dos modalidades, mismo resultado"
COVERAGE_INTRO: Final = (
    "Elegimos la forma de atención según el trabajo y la ubicación. Te "
    "decimos cuál corresponde cuando nos escribes."
)

COVERAGE_MODES: Final[list[dict[str, Any]]] = [
    {
        "id": "remoto",
        "title": "Soporte remoto",
        "scope": "Toda Nicaragua",
        "icon": "public",
        "description": (
            "Asistencia por internet desde cualquier departamento del país. "
            "Es la modalidad más rápida y económica cuando el problema puede "
            "resolverse sin tocar el equipo."
        ),
        "highlights": [
            "Instalación y configuración de programas de trabajo",
            "Diagnóstico de errores y lentitud del sistema",
            "Configuración de correo, navegadores e impresoras en red",
        ],
    },
    {
        "id": "domicilio",
        "title": "Visita a domicilio",
        "scope": "Toda Managua",
        "icon": "home",
        "description": (
            "Vamos a tu casa u oficina. Indicada para reinstalaciones de "
            "sistema, problemas físicos o equipos sin conexión estable."
        ),
        "highlights": [
            "Reinstalación de Windows con visita presencial",
            "Problemas físicos: disco, memoria, fuente o pantalla",
            "Redes, impresoras y equipos compartidos de oficina",
        ],
    },
]


# ---------------------------------------------------------------------------
# Preguntas frecuentes
# ---------------------------------------------------------------------------
# El par `question`/`answer` alimenta dos cosas: el bloque visible (con
# <details> nativo, que no necesita JavaScript) y el JSON-LD `FAQPage`.
# Las respuestas evitan prometer tiempos de respuesta o precios fijos, tal como
# indica docs/NEGOCIO.md.

FAQ_TITLE: Final = "Preguntas frecuentes"
FAQ_ITEMS: Final[list[dict[str, str]]] = [
    {
        "question": "¿Atienden fuera de Managua?",
        "answer": (
            "Sí, puedes consultar por asistencia remota desde cualquier "
            "departamento de Nicaragua. La posibilidad de resolver el problema "
            "a distancia depende del servicio solicitado."
        ),
    },
    {
        "question": "¿Cuánto cuesta instalar Windows o un programa?",
        "answer": (
            "El precio depende del trabajo, la compatibilidad del equipo y los "
            "servicios adicionales. Solicita una cotización antes de comenzar."
        ),
    },
    {
        "question": "¿Pueden instalar programas en mi laptop?",
        "answer": (
            "Sí, previa comprobación de los requisitos del programa, la "
            "compatibilidad del sistema y las condiciones de licencia."
        ),
    },
    {
        "question": "¿Qué debo hacer antes de reinstalar Windows?",
        "answer": (
            "Te recomendamos respaldar tus archivos importantes. Una instalación "
            "limpia puede borrar documentos, aplicaciones y configuraciones."
        ),
    },
]


# ---------------------------------------------------------------------------
# Cierre y contacto
# ---------------------------------------------------------------------------

CONTACT_TITLE: Final = "¿Necesitas ayuda con tu computadora?"
CONTACT_TEXT: Final = (
    "Escríbenos, explícanos qué necesitas y consulta las opciones de servicio disponibles."
)
CONTACT_CTA: Final = {
    "label": "Solicitar cotización por WhatsApp",
    "message": "Hola, quiero solicitar una cotización de soporte técnico.",
}


# ---------------------------------------------------------------------------
# Pie de pagina
# ---------------------------------------------------------------------------

FOOTER_SERVICES_TITLE: Final = "Servicios"
FOOTER_NAV_TITLE: Final = "En esta página"
FOOTER_LEGAL: Final = "Instalación de programas, configuración y soporte técnico para computadoras."
