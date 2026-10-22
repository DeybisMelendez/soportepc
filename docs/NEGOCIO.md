# Contexto del negocio — Soporte PC Managua

Este documento describe **qué hacemos y para quién**, sin entrar en detalles técnicos.
Está pensado tanto para desarrolladores humanos como para asistentes de IA que
necesitan entender el propósito del proyecto antes de tocar el código.

Para lo técnico ver [`ARQUITECTURA.md`](ARQUITECTURA.md) y
[`ESTILOS.md`](ESTILOS.md).

## Descripción general

**Soporte PC Managua** es un servicio de soporte técnico especializado en la
**instalación y configuración de programas profesionales para computadoras**.

La diferencia central del negocio no es reparar fallas de hardware cualesquiera, sino
**instalar y dejar funcionando correctamente el software que el cliente necesita para
trabajar**: sistemas de contabilidad, programas de diseño, suite ofimática, herramientas
de arquitectura y CAD, plataformas de facturación, entre otros.

Esto implica que el cliente no siempre sabe *en abstracto* qué le pasa. Sabe que "el
programa no le abre", que "el sistema no le guarda la información" o que "necesito esto
para empezar a facturar". El trabajo del técnico es diagnosticar e instalar la
herramienta correcta, no solo resolver el síntoma.

## Modalidades de servicio

Ofrecemos dos modalidades. La diferencia entre ambas es la **presencia física**: el
resultado para el cliente es el mismo (software instalado y funcionando), pero el
proceso y los costos cambian.

### 1. Servicio presencial — visita al cliente

Un técnico se desplaza físicamente hasta el domicilio u oficina del cliente.

**Cobertura:** toda **Managua**.

**Se usa cuando:**

- Hay un problema físico: disco duro, RAM, fuente, motherboard, pantalla.
- Se requiere formatear o reinstalar el sistema operativo.
- Se instalan redes, impresoras o equipos compartidos en una oficina.
- El cliente no tiene acceso a internet estable, o no se siente cómodo dando acceso
  remoto a su equipo.

**Ventaja para el cliente:** un técnico en el lugar, sin depender de la conexión.

### 2. Servicio remoto — soporte a distancia

El técnico se conecta al equipo del cliente mediante software de acceso remoto y
resuelve el problema sin salir de su taller.

**Cobertura:** toda **Nicaragua**, sin restricción de zona.

**Se usa cuando:**

- Se instala o configura un programa de trabajo.
- Se corrigen errores, lentitud o conflictos de software.
- Se configura correo electrónico, navegadores, impresoras en red.
- El cliente está en una ciudad fuera de Managua (León, Masaya, Granada, Chinandega,
  Estelí, Rivas, la Costa Sur, etc.).

**Ventaja para el cliente:** servicio disponible en cualquier punto del país, y
generalmente más rápido y económico que una visita, porque no hay deslocamiento.

## Cobertura geográfica

| Modalidad | Cobertura |
|---|---|
| Presencial (visita) | Toda **Managua** |
| Remoto (acceso a distancia) | Toda **Nicaragua** |

Esta cobertura es una decisión de posicionamiento, no una limitación técnica. El servicio
remoto permite atender a clientes de todo el país sin desplazamientos, lo que
reduce el costo operativo y amplía el mercado alcanzable.

## Público objetivo

### Cliente individual (hogar o freelancer)

- Instala por primera vez un programa de facturación, diseño o contabilidad.
- Necesita un programa configurado para trabajar desde casa.
- No tiene un técnico de confianza ni quiere Llevar su computadora a una tienda y
  esperar días.

### Pequeña y mediana empresa

- Varios usuarios que necesitan el mismo software instalado y estandarizado.
- Equipos en distintas ciudades o sucursales: se atienden en remoto.
- No cuentan con personal de soporte técnico interno.

### Empresa con sistemas existentes

- Necesita migrar, actualizar o integrar software en equipos ya instalados.
- Prefiere que el trabajo se documente y no quede en manos de un tercero sin respaldo.

## Qué hace que este servicio sea confiable

Este es el argumento central de venta del sitio:

- **Atención en español.** El cliente explica su problema en su idioma y recibe
  instrucciones que puede entender.
- **Visita a domicilio.** No hay que trasladar la computadora a una tienda.
- **Cobertura nacional en remoto.** Clientes fuera de Managua también reciben soporte.
- **Trabajo profesional.** Nos especializamos en programas de uso profesional, no solo
  en reparar fallas básicas.

## Cómo se traduce esto al sitio

La página de inicio comunica, en este orden y por secciones:

| # | Sección | Idea |
|---|---|---|
| 1 | Hero | Qué hacemos y cómo pedirlo, en el primer pliegue |
| 2 | Servicios | Los seis servicios, cada uno con enlace directo a WhatsApp |
| 3 | Proceso | Tres pasos: cuéntanos, cotizamos, coordinamos |
| 4 | Cobertura | Las dos modalidades, con su alcance explícito |
| 5 | Preguntas frecuentes | Las cuatro objeciones reales del cliente |
| 6 | Contacto | Último llamado a la acción |

La secuencia tiene un orden deliberado: primero *qué* hacemos, después *cómo*
funciona el proceso (que reduce la incertidumbre de escribir), luego las
modalidades (el diferenciador) y por último las objeciones. El CTA aparece en el
hero y al final, y no en medio: interrumpir el proceso de lectura resta.

Evitar:

- Prometer tiempos de respuesta que no se pueden garantizar.
- Usar jerga técnica innecesaria (el cliente promedio no busca "configuración de
  drivers de red", busca "que mi programa abra").
- Ocultar que hay dos modalidades con alcances distintos: es mejor ser claro desde el
  inicio para evitar decepciones.

El copy vive en `landing/content.py`; esta sección es la referencia de qué debe
decir cada parte.

## Marketing y SEO

**Keywords objetivo** (por orden de intención):

1. `instalación de programas para PC` — intención comercial alta.
2. `soporte técnico Nicaragua` — intención de locality.
3. `instalación de Windows Managua` — intención específica de zona.
4. `instalación de programas[software de trabajo] en Nicaragua` — de cola larga,
   la que más convierte y la más fácil de posicionar.

**Título y descripción** están fijados en `content.py` (`SEO_TITLE`,
`SEO_DESCRIPTION`) y sus longitudes están verificadas: ≤ 60 y ≤ 160 caracteres.
Superar esos límites hace que Google recorte el texto por la mitad y pierda
justo la keyword.

**Sin formulario de contacto.** Todo el contacto ocurre por WhatsApp, con el
mensaje prellenado según el servicio. Es coherente con el negocio (el cliente
prefiere hablar por WhatsApp) y evita mantener spam, base de datos y un flujo
de formularios.

## Datos de contacto

| Dato | Valor | Dónde vive |
|---|---|---|
| Nombre comercial | Soporte PC Managua | `settings.BUSINESS["name"]` |
| WhatsApp (enlaces) | `50555025301` | `DJANGO_WHATSAPP_NUMBER` |
| Teléfono (mostrado) | `5502-5301` | `DJANGO_PHONE_DISPLAY` |
| Cobertura presencial | Toda Managua | `settings.BUSINESS["coverage_onsite"]` |
| Cobertura remota | Toda Nicaragua | `settings.BUSINESS["coverage_remote"]` |
| Idioma de atención | Español | `settings.BUSINESS["language"]` |

> **Pendiente de confirmar:** el número de WhatsApp es de **8 dígitos**
> (`5502-5301`), cuando el estándar de Nicaragua es de **8 dígitos** con prefijo
> 505. Hay que verificar el número real antes de publicar: los enlaces `wa.me`
> con un número equivocado abren una conversación que no llega a nadie.
> El valor por defecto en `settings.py` es una aproximación.

## Resumen en una frase

> Instalamos y configuramos programas profesionales para computadoras, con visita a
> domicilio en toda Managua y soporte remoto en toda Nicaragua.