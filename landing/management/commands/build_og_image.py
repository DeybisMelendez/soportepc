"""Generador de la imagen para vistas previas en redes sociales.

Genera tres archivos a partir de la paleta de marca:

    static/img/og-home.png         1200x630, imagen Open Graph y Twitter Card
    static/img/apple-touch-icon.png  180x180, icono para iOS
    static/img/favicon.png          64x64, favicon raster de respaldo

Por qué un comando y no imágenes versionadas:
    - El PNG resultante pesa pocos KB y es un artefacto derivado: se regenera
      con un comando cuando cambia la marca, en lugar de versionar un binario opaco
      en el repositorio.
    - Los colores salen de `settings.BUSINESS`, así que la imagen no puede
      desincronizarse del tema del sitio.

Sin dependencias: solo Pillow, que ya está en `requirements.txt`.

Uso:
    python manage.py build_og_image
"""

from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

# Lienzo de Open Graph. Las dimensiones son obligatorias: Facebook, WhatsApp y
# X recortan o estiran la imagen si no coincide con una proporción conocida.
OG_SIZE = (1200, 630)
APPLE_TOUCH_SIZE = (180, 180)
FAVICON_SIZE = (64, 64)

# Escala tipográfica sobre el ancho del lienzo. Se expresan en fracciones para
# que el diseño se mantenga si algún día se cambia `OG_SIZE`.
#
# El título es el elemento que más condiciona el resultado: a 1200 px de ancho
# el área útil es de 1020 px (1200 menos dos márgenes del 7.5 %), y una fuente
# en negrita ocupa del orden del 55 % de su tamaño en ancho por carácter. Con
# un 5.2 % el título ocupa cuatro líneas cómodas; por encima del 5.5 % las
# palabras largas ("computadora") se desbordan.
TITLE_SIZE = 0.052  # ~62 px a 1200 de ancho
SUBTITLE_SIZE = 0.027  # ~32 px
BRAND_SIZE = 0.024  # ~29 px
PHONE_SIZE = 0.024  # ~29 px

# Candidatos de fuente, en orden de preferencia. Pillow no conoce las fuentes
# del sistema por nombre: hay que pasar la ruta al archivo.
FONT_CANDIDATES_BOLD = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
)
FONT_CANDIDATES_REGULAR = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
)


class Command(BaseCommand):
    help = "Genera la imagen Open Graph, el icono de iOS y el favicon raster."

    def handle(self, *args: Any, **options: Any) -> None:
        static_img = Path(settings.BASE_DIR) / "static" / "img"
        static_img.mkdir(parents=True, exist_ok=True)

        self._build_og_image(static_img)
        self._build_icon(static_img, "apple-touch-icon.png", APPLE_TOUCH_SIZE)
        self._build_icon(static_img, "favicon.png", FAVICON_SIZE)

    # ------------------------------------------------------------------
    # Imagen Open Graph
    # ------------------------------------------------------------------
    def _build_og_image(self, static_img: Path) -> None:
        width, height = OG_SIZE
        image = self._background(width, height)
        draw = ImageDraw.Draw(image)

        brand = settings.BUSINESS
        margin = int(width * 0.075)  # 90 px
        content_width = width - margin * 2

        # --- Marca, arriba a la izquierda -----------------------------
        mark_size = int(width * 0.055)
        draw.rounded_rectangle(
            [margin, margin, margin + mark_size, margin + mark_size],
            radius=int(width * 0.016),
            fill="#f97316",
        )
        mark_x = margin + int(mark_size * 0.32)
        for offset in (0, int(mark_size * 0.30), int(mark_size * 0.60)):
            draw.line(
                [
                    mark_x,
                    margin + int(mark_size * 0.22) + offset,
                    margin + mark_size - int(mark_size * 0.32),
                    margin + int(mark_size * 0.22) + offset,
                ],
                fill="#ffffff",
                width=max(2, int(width * 0.005)),
            )

        draw.text(
            (margin + mark_size + int(width * 0.020), margin + int(mark_size * 0.28)),
            brand["name"],
            font=_font(FONT_CANDIDATES_BOLD, int(width * BRAND_SIZE)),
            fill="#e0e7ff",
        )

        # --- Título: el mensaje que se lee en la vista previa --------
        # El título se ajusta al ancho disponible y se coloca justo encima del
        # bloque de modalidades, de forma que el alto que ocupen los subtítulos
        # no pueda empujar el pie fuera del lienzo.
        title_font = _font(FONT_CANDIDATES_BOLD, int(width * TITLE_SIZE))
        title = "Instalamos tus programas y dejamos tu computadora funcionando"
        subtitle_font = _font(FONT_CANDIDATES_REGULAR, int(width * SUBTITLE_SIZE))
        subtitle = "Soporte remoto en Nicaragua · Visita a domicilio en Managua"

        title_lines = _wrap(draw, title, title_font, content_width)
        subtitle_lines = _wrap(draw, subtitle, subtitle_font, content_width)

        line_height = int(title_font.size * 1.24)
        subtitle_line_height = int(subtitle_font.size * 1.40)
        gap_after_title = int(height * 0.035)

        # --- Pie: llamada a la acción y teléfono --------------------
        # El botón se ancla al fondo con un margen fijo, igual que en el
        # contenido: así nunca depende de cuántas líneas ocupe el título.
        footer_font = _font(FONT_CANDIDATES_BOLD, int(width * PHONE_SIZE))
        footer_height = int(width * 0.058)
        footer_y = height - margin - footer_height

        # El bloque de texto se coloca en el espacio que queda entre la marca y
        # el pie. Calcularlo así (y no con un porcentaje fijo) garantiza que un
        # título más largo nunca invada el botón, sin importar cuántas líneas
        # ocupe.
        block_height = (
            len(title_lines) * line_height
            + gap_after_title
            + len(subtitle_lines) * subtitle_line_height
        )
        top = margin + mark_size + int(height * 0.04)  # holgura bajo la marca
        available = footer_y - int(height * 0.045) - top
        block_top = top + max(0, (available - block_height) // 2)

        y = block_top
        for line in title_lines:
            draw.text((margin, y), line, font=title_font, fill="#ffffff")
            y += line_height

        y += gap_after_title
        for line in subtitle_lines:
            draw.text((margin, y), line, font=subtitle_font, fill="#c7d2fe")
            y += subtitle_line_height

        cta_label = "Cotización por WhatsApp"
        cta_text_width = int(draw.textlength(cta_label, font=footer_font))
        cta_padding = int(width * 0.024)
        cta_width = cta_text_width + cta_padding * 2
        draw.rounded_rectangle(
            [margin, footer_y, margin + cta_width, footer_y + footer_height],
            radius=footer_height // 2,
            fill="#1da851",
        )
        draw.text(
            (margin + cta_padding, footer_y + int(footer_height * 0.28)),
            cta_label,
            font=footer_font,
            fill="#ffffff",
        )
        draw.text(
            (margin + cta_width + int(width * 0.028), footer_y + int(footer_height * 0.28)),
            brand["phone_display"],
            font=footer_font,
            fill="#fb923c",
        )

        # --- Acento gráfico: círculos translúcidos --------------------
        # Se dibujan encima de todo el texto a propósito: con opacidad baja solo
        # añaden profundidad y no estorban la lectura.
        overlay = Image.new("RGBA", OG_SIZE, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.ellipse(
            [int(width * 0.62), int(height * -0.22), int(width * 1.18), int(height * 0.55)],
            fill=(99, 102, 241, 70),
        )
        overlay_draw.ellipse(
            [int(width * 0.74), int(height * 0.52), int(width * 1.10), int(height * 1.10)],
            fill=(249, 115, 22, 60),
        )
        image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")

        output = static_img / Path(settings.BUSINESS["og_image"]).name
        image.save(output, "PNG", optimize=True)
        self.stdout.write(self.style.SUCCESS(f"Imagen Open Graph: {output}"))

    # ------------------------------------------------------------------
    # Iconos cuadrados
    # ------------------------------------------------------------------
    def _build_icon(self, static_img: Path, filename: str, size: tuple[int, int]) -> None:
        """Icono cuadrado: fondo índigo con la marca naranja centrada."""
        image = Image.new("RGB", size, "#312e81")
        draw = ImageDraw.Draw(image)

        # Todas las medidas se derivan del ancho, para que el icono se vea
        # igual de bien a 64 px (favicon) que a 180 px (iOS).
        unit = size[0] / 32
        radius = int(8 * unit)
        draw.rounded_rectangle(
            [int(6 * unit), int(6 * unit), int(26 * unit), int(26 * unit)],
            radius=radius,
            fill="#f97316",
        )
        bar_width = int(2.2 * unit)
        for offset in (12, 16.5, 21):
            draw.line(
                [int(10.5 * unit), int(offset * unit), int(21.5 * unit), int(offset * unit)],
                fill="#ffffff",
                width=bar_width,
            )

        output = static_img / filename
        image.save(output, "PNG", optimize=True)
        self.stdout.write(self.style.SUCCESS(f"Icono {size[0]}px: {output}"))

    # ------------------------------------------------------------------
    # Fondo del OG image
    # ------------------------------------------------------------------
    @staticmethod
    def _background(width: int, height: int) -> Image.Image:
        """Degradado diagonal índigo, dibujado píxel a píxel.

        Pillow no tiene un generador de degradado incorporado, y.draw_image lo
        resuelve con dos colores. Se calcula el color de cada fila, que es
        suficiente para un degradado diagonal limpio y evita el coste de
        hacerlo por píxel.
        """
        image = Image.new("RGB", OG_SIZE)
        draw = ImageDraw.Draw(image)

        # Mismos extremos que `linear-gradient(135deg, ...)` del CSS del hero.
        start = (55, 48, 163)  # índigo 800
        end = (30, 27, 75)  # índigo 950

        for y in range(height):
            ratio = y / (height - 1)
            color = tuple(
                int(start[channel] + (end[channel] - start[channel]) * ratio)
                for channel in range(3)
            )
            draw.line([(0, y), (width, y)], fill=color)

        return image


def _font(candidates: tuple[str, ...], size: int) -> ImageFont.FreeTypeFont:
    """Devuelve la primera fuente encontrada de la lista.

    Si no hay ninguna (por ejemplo, en una imagen de Docker mínima), se recurre
    a la fuente por defecto de Pillow: la imagen se genera, aunque el texto se
    verá con otro tipo de letra. Es preferible a que el comando falle.
    """
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def _wrap(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    """Parte un texto en líneas que caben en `max_width`.

    Se hace aquí y no con un salto calculado por número de caracteres porque el
    ancho real depende de la fuente cargada, que puede variar entre sistemas.
    """
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word

    if current:
        lines.append(current)

    return lines
