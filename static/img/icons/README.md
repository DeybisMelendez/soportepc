# Iconos de marca

Logotipos de aplicaciones y sistemas. Son **archivos `.svg` reales**, cargados con
`<img>`, no SVG en línea: por eso los trazados son los oficiales de cada marca.

## Por qué archivo y no inline

Los iconos de interfaz (Material Symbols) van en línea en
`partials/icon.html` porque son genéricos y cambian de color según el contexto.

Los de marca son distintos: su forma **es** la identidad. Un logotipo no puede
alterarse, así que va en su propio archivo. Además, tenerlos separados permite
verificarlos de un vistazo y sustituirlos sin tocar código.

## Licencia y origen

| Archivo | Origen | Licencia |
| --- | --- | --- |
| `whatsapp`, `vlcmediaplayer`, `firefox`, `googlechrome`, `opera`, `ubuntu`, `linux`, `libreoffice`, `android`, `apple` | [Simple Icons](https://simpleicons.org) | CC0-1.0 |
| `windows` | Geometría dibujada en este repositorio | **Sin licencia de Microsoft** |

> ⚠️ **`windows.svg` es el único archivo sin licencia clara.** Simple Icons retiró el
> logotipo de Windows por litigio de marca (Microsoft lo reclama como logotipo
> propietario), y los demás sets tampoco lo ofrecen. El archivo reproduce su
> geometría con el color oficial `#0078D4`, pero Microsoft no lo distribuye ni
> licencia. Sustituirlo en cuanto exista un SVG oficial con licencia clara para
> terceros.

## Modificaciones aplicadas

A todos los archivos de Simple Icons se les cambió `fill="#RRGGBB"` por
`fill="currentColor"` y se eliminó el `<title>` generado. Sin ese cambio cada
icono tendría su color fijo y no serviría sobre fondo oscuro.

Para recuperar el color oficial de una marca, quita `currentColor` y pon el hex:

| Marca | Color |
| --- | --- |
| WhatsApp | `#25D366` |
| Chrome | `#4285F4` |
| Firefox | `#FF7139` |
| Opera | `#FF1B2D` |
| VLC | `#FF8800` |
| Ubuntu | `#E95420` |
| Linux | `#FCC624` |
| LibreOffice | `#18A303` |

## Uso

Desde una plantilla:

```html
{% load static %}
<img src="{% static 'img/icons/whatsapp.svg' %}" alt="" width="24" height="24">
```

`alt=""` es correcto aquí: el icono es decorativo y el texto del enlace ya dice
qué hace. Solo lleva `alt` con contenido si el icono es el único contenido
significativo de un enlace.

`width`/`height` evitan el desplazamiento de layout (CLS) mientras carga.