"""Rutas de la app `landing`.

Cada vista tiene un `name` para que las plantillas usen `{% url %}` en lugar de
rutas escritas a mano: si una URL cambia, el enlace se actualiza solo.
"""

from django.urls import path

from landing import views

app_name = "landing"

urlpatterns = [
    # Página de inicio. Es la raiz del sitio, montada con `include` en el raiz
    # de `core/urls.py`, asi que su ruta final es "" y no "/".
    path("", views.home, name="home"),
    # Confirmación de contacto. Es una pantalla intermedia: lleva `noindex` y
    # no aparece en el sitemap.
    path("gracias/", views.thanks, name="thanks"),
]
