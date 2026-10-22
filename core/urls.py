"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from django.views.generic import TemplateView
    2. Add a URL to urlpatterns:  path('', TemplateView.as_view())
Including a URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from landing import views as landing_views

urlpatterns = [
    # La página de inicio se monta en la raiz: `include` conserva los nombres
    # de `landing.urls`, asi que las plantillas usan `{% url 'landing:home' %}`.
    path("", include("landing.urls")),
    # SEO técnico. Se sirven como vistas en vez de archivos estaticos para que
    # la URL del sitemap se derive de `DJANGO_SITE_URL` y no se desincronice.
    path("robots.txt", landing_views.robots_txt, name="robots"),
    path("sitemap.xml", landing_views.sitemap_xml, name="sitemap"),
    path("admin/", admin.site.urls),
]

# 404 con el diseño del sitio. Debe ir despues de `urlpatterns` para que solo
# se use como fallback: si una ruta no coincide con ninguna de las anteriores,
# Django aplica este handler.
handler404 = "landing.views.handler_404"
