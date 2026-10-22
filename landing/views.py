"""Vistas públicas del sitio.

Solo hay vistas sin estado que renderizan templates. No hay lógica de negocio
aquí: el copy vive en `landing.content` y los datos de contacto en
`settings.BUSINESS`. Las vistas se limitan a elegir qué plantilla usar y a
exponer el contexto mínimo que cada template necesita.

Las funciones auxiliares centralizan tres cosas que de otro modo se
duplicarían en cada plantilla:

- La URL absoluta, que el canonical y el Open Graph necesitan siempre basada en
  `DJANGO_SITE_URL` (nunca en el host de la petición, que en desarrollo es
  `localhost`).
- El enlace `wa.me` con mensaje prellenado.
- El contexto común del sitio.
"""

from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from landing.structured_data import build_structured_data

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------


def build_absolute_url(path: str = "/") -> str:
    """Devuelve la URL absoluta de `path` usando `SITE_URL` como base.

    Acepta tanto `/gracias/` como `gracias/` y evita duplicar la barra final.
    """
    return f"{settings.SITE_URL}/{path.lstrip('/')}"


def build_whatsapp_link(message: str) -> str:
    """Construye un enlace `wa.me` con el mensaje prellenado.

    Usa el formato oficial de WhatsApp: número internacional sin `+` ni
    espacios en la ruta y el texto en el parámetro `text`.

    El mensaje va URL-encoded: los textos del sitio llevan acentos y signos de
    apertura, y sin codificar romperían el atributo `href` en cuanto aparece un
    `&`, un `+` o un símbolo UTF-8.
    """
    number = settings.BUSINESS["whatsapp_number"]
    query = urlencode({"text": message})
    return f"https://wa.me/{number}?{query}"


def build_site_context(request: HttpRequest, **extra: object) -> dict[str, object]:
    """Arma el contexto común a todas las páginas del sitio.

    Centralizarlo aquí garantiza que la 404 y la página de gracias hereden los
    mismos datos del negocio que la página de inicio, en lugar de duplicarlos
    (y olvidarlos) en cada plantilla.
    """
    return {
        "business": settings.BUSINESS,
        "site_url": settings.SITE_URL,
        "canonical_url": build_absolute_url(request.path),
        # Función, no string: cada botón necesita su propio mensaje prellenado.
        "whatsapp": build_whatsapp_link,
        **extra,
    }


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------


def home(request: HttpRequest) -> HttpResponse:
    """Página de inicio."""
    from landing import content  # Import local: evita un ciclo en el arranque.

    context = build_site_context(
        request,
        page_title=content.SEO_TITLE,
        meta_description=content.SEO_DESCRIPTION,
        og_type="website",
        hero=content.HERO,
        trust_points=content.TRUST_POINTS,
        services=content.SERVICES,
        process_title=content.PROCESS_TITLE,
        process_intro=content.PROCESS_INTRO,
        process_steps=content.PROCESS_STEPS,
        coverage_title=content.COVERAGE_TITLE,
        coverage_intro=content.COVERAGE_INTRO,
        coverage_modes=content.COVERAGE_MODES,
        faq_title=content.FAQ_TITLE,
        faq_items=content.FAQ_ITEMS,
        contact_title=content.CONTACT_TITLE,
        contact_text=content.CONTACT_TEXT,
        contact_cta=content.CONTACT_CTA,
        footer_services_title=content.FOOTER_SERVICES_TITLE,
        footer_nav_title=content.FOOTER_NAV_TITLE,
        footer_legal=content.FOOTER_LEGAL,
        # Permite a la plantilla activar el CTA de WhatsApp en la barra de
        # navegación solo en la página de inicio.
        is_home=True,
    )
    # Sin argumentos: la página de inicio es la que lleva el catálogo de
    # servicios y la FAQ en sus datos estructurados.
    context["structured_data"] = build_structured_data()
    return render(request, "landing/home.html", context)


def thanks(request: HttpRequest) -> HttpResponse:
    """Página de confirmación.

    El sitio es estático y el contacto ocurre por WhatsApp, así que esta
    página no procesa ningún formulario: confirma que el mensaje se abrió
    correctamente y ofrece salidas alternativas de contacto.
    """
    context = build_site_context(
        request,
        page_title="Solicitud enviada",
        meta_description=(
            "Gracias por escribirnos. Te responderemos por WhatsApp con la "
            "cotización de tu servicio de soporte técnico."
        ),
        # No debe indexarse: es una página intermedia sin contenido propio.
        noindex=True,
        is_home=False,
    )
    # Con `crumbs`: la página declara su ruta de navegación, pero no el catálogo
    # ni la FAQ, porque ese contenido no existe aquí.
    context["structured_data"] = build_structured_data(
        crumbs=[("Inicio", build_absolute_url(reverse("landing:home")))]
    )
    return render(request, "landing/thanks.html", context)


# ---------------------------------------------------------------------------
# SEO técnico
# ---------------------------------------------------------------------------


def robots_txt(request: HttpRequest) -> HttpResponse:
    """Archivo `robots.txt`.

    Se permite rastreo del sitio y se anuncia la ruta del sitemap. El backend
    de administración queda fuera porque no aporta contenido público y no debe
    aparecer en resultados de búsqueda.
    """
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "\n"
        f"Sitemap: {build_absolute_url('/sitemap.xml')}\n"
    )
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


def sitemap_xml(request: HttpRequest) -> HttpResponse:
    """Sitemap XML con las URLs públicas indexables.

    Se construye a mano en lugar de usar `django.contrib.sitemaps` porque el
    sitio tiene pocas URLs y su contenido es estático: un XML explícito es más
    legible y controlable, y no obliga a registrar modelos de negocio que aún
    no existen.
    """
    # Solo se listan páginas públicas con contenido real. `/gracias/` se omite
    # a propósito: es una pantalla de confirmación con `noindex` y no aporta
    # nada al indice de busqueda.
    pages = [
        {
            "loc": build_absolute_url(reverse("landing:home")),
            "changefreq": "monthly",
            "priority": "1.0",
        },
    ]
    lastmod = timezone.now().date().isoformat()
    urls = "".join(
        "  <url>\n"
        f"    <loc>{page['loc']}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{page['changefreq']}</changefreq>\n"
        f"    <priority>{page['priority']}</priority>\n"
        "  </url>\n"
        for page in pages
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}"
        "</urlset>\n"
    )
    return HttpResponse(xml, content_type="application/xml; charset=utf-8")


def handler_404(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    """Página 404 con el diseño del sitio.

    Devolver un 404 renderizado y no la vista por defecto de Django mantiene la
    identidad visual y, sobre todo, ofrece salidas: quien llega a una URL rota
    no debe quedarse sin opciones de contacto.
    """
    context = build_site_context(
        request,
        page_title="Página no encontrada",
        meta_description="La página que buscas no existe o cambió de dirección.",
        noindex=True,
        is_home=False,
    )
    context["structured_data"] = build_structured_data(
        crumbs=[("Inicio", build_absolute_url(reverse("landing:home")))]
    )
    return render(request, "404.html", context, status=404)
