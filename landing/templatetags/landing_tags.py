"""Filtros de plantilla propios de `landing`.

Django no permite invocar funciones con argumentos desde una plantilla, así que
`{{ whatsapp mensaje }}` es sintaxis inválida. Este filtro resuelve ese caso: en
el contexto la vista expone `whatsapp`, una función, y aquí se expone además
como filtro, que es la única vía que el lenguaje de plantillas soporta.

    {% load landing_tags %}
    <a href="{{ mensaje|whatsapp_link }}">

El argumento de un filtro no puede ser una variable complexa (`hero.cta.message`
no es válido como argumento), por eso el patrón de uso es siempre el mismo: la
vista aplana los datos y expone el mensaje ya en una variable simple.
"""

from django import template
from django.utils.safestring import mark_safe

from landing.views import build_whatsapp_link

register = template.Library()


@register.filter(name="whatsapp_link")
def whatsapp_link(message: str) -> str:
    """Convierte un texto en un enlace `wa.me` con el mensaje prellenado.

    Se devuelve `mark_safe` porque la URL la genera el propio código, no el
    usuario: no hay contenido externo que pueda inyectar HTML.
    """
    return mark_safe(build_whatsapp_link(message))
