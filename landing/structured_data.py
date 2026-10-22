"""Construcción de los datos estructurados (JSON-LD) de las páginas públicas.

Se separa en su propio módulo por dos motivos:

- El JSON-LD tiene una forma lógica que no cabe bien en una plantilla y que sí
  conviene leer como Python, especialmente la lista de servicios.
- Al generarse con `json.dumps`, las comillas y los acentos se escapan
  correctamente. Hacerlo en la plantilla con `{{ valor }}` produciría
  `&quot;` dentro del JSON y los buscadores no podrían parsearlo.

Regla de oro: el JSON-LD debe repetir exactamente lo que el usuario ve. Un dato
estructurado que contradice la página es una penalización manual de Google.
"""

import json
from typing import Any

from django.conf import settings
from django.urls import reverse

from landing import content


def _business_url() -> str:
    """URL absoluta de la página de inicio, usada como `@id` del negocio."""
    return f"{settings.SITE_URL}/"


def _image_url() -> str:
    """URL absoluta de la imagen social."""
    return f"{settings.SITE_URL}{settings.STATIC_URL}{settings.BUSINESS['og_image']}"


def _business_node() -> dict[str, Any]:
    """Nodo `ProfessionalService` con los datos del negocio y su catálogo.

    `ProfessionalService` es una subclase de `LocalBusiness` y encaja con este
    negocio: no se vende un producto en un local, se presta un servicio técnico.
    """
    business = settings.BUSINESS

    node: dict[str, Any] = {
        "@type": "ProfessionalService",
        "@id": f"{_business_url()}#negocio",
        "name": business["name"],
        "description": content.SEO_DESCRIPTION,
        "url": _business_url(),
        "image": _image_url(),
        "telephone": business["phone_display"],
        "availableLanguage": business["language"],
        # Sin dirección pública: el negocio opera a domicilio. Declarar
        # `address` sin dato real sería información incorrecta.
        "areaServed": [
            {
                "@type": "City",
                "name": "Managua",
            },
            {
                "@type": "Country",
                "name": "Nicaragua",
            },
        ],
        # El catálogo permite que Google entienda qué ofrece el negocio y
        # puede generar enlaces de servicio en lugar de solo texto azul.
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Servicios de soporte técnico",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": service["title"],
                        "description": service["description"],
                        "url": f"{_business_url()}#{service['id']}",
                        "provider": {"@id": f"{_business_url()}#negocio"},
                    },
                }
                for service in content.SERVICES
            ],
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "telephone": business["phone_display"],
            "areaServed": business["coverage_remote"],
            "availableLanguage": business["language"],
            "url": f"https://wa.me/{business['whatsapp_number']}",
        },
    }

    # Coordenadas aproximadas para el panel local de resultados. Se omiten si
    # no hay dato configurado en `settings.BUSINESS`.
    geo = business.get("geo")
    if geo:
        node["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": geo["latitude"],
            "longitude": geo["longitude"],
        }

    return node


def _faq_node() -> dict[str, Any]:
    """Nodo `FAQPage` con las preguntas frecuentes visibles."""
    return {
        "@type": "FAQPage",
        "@id": f"{_business_url()}#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["answer"],
                },
            }
            for item in content.FAQ_ITEMS
        ],
    }


def _breadcrumb_node(crumbs: list[tuple[str, str]]) -> dict[str, Any]:
    """Nodo `BreadcrumbList`.

    `crumbs` es una lista de pares `(nombre visible, URL absoluta)`.
    """
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": name,
                "item": url,
            }
            for index, (name, url) in enumerate(crumbs, start=1)
        ],
    }


def build_structured_data(crumbs: list[tuple[str, str]] | None = None) -> str:
    """Devuelve el grafo JSON-LD listo para incrustar en el `<head>`.

    Siempre incluye el nodo del negocio, para que todas las páginas del sitio
    declaren la misma entidad. En la página de inicio añade el catálogo de
    servicios y la FAQ; el resto de páginas reciben solo la ruta de navegación.
    """
    home_url = f"{settings.SITE_URL}{reverse('landing:home')}"

    graph: list[dict[str, Any]] = [_business_node()]

    # El catálogo y la FAQ solo existen en la página de inicio: repetir el mismo
    # `FAQPage` en la 404 sería describir contenido que allí no está visible.
    if crumbs is None:
        graph.append(_faq_node())

    breadcrumb_crumbs = crumbs or [("Inicio", home_url)]
    graph.append(_breadcrumb_node(breadcrumb_crumbs))

    payload = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
