/**
 * Soporte PC Managua — Comportamiento del sitio.
 *
 * JavaScript vanilla, sin dependencias, sin framework, sin build. Un solo
 * archivo que se carga con `defer`, por lo que no bloquea el render.
 *
 * PRINCIPIO RECTOR
 * ----------------
 * El sitio funciona completo sin este archivo. El JavaScript solo mejora la
 * experiencia; nunca es la única vía para alcanzar un contenido o una acción.
 * Por eso cada módulo degrada con elegancia:
 *
 *   - Menú móvil: el HTML ya tiene `hidden` en el panel. Sin JS, no hay menú
 *     desplegable, pero los enlaces del pie y del contenido siguen ahí.
 *   - Scrollspy: sin JS, los enlaces navegan a su ancla normalmente.
 *   - Animaciones: el CSS solo oculta el contenido cuando la clase `.js` está
 *     en `<html>` (la añade `base.html`). Sin JS, todo es visible.
 *
 * MÓDULOS
 * -------
 *   1. setupMobileNav()   Menú desplegable accesible en móvil.
 *   2. setupScrollSpy()    Resalta el enlace de la sección visible.
 *   3. setupReveal()       Anima la entrada de los bloques al hacer scroll.
 *   4. setupFloatingCta()  Muestra el botón flotante de WhatsApp al bajar.
 *
 * Cada módulo se registra con su propio guard (`if (!elemento) return`) para
 * que añadir uno nuevo no rompa los demás, y todo se envuelve en un
 * `DOMContentLoaded` implícito gracias a `defer`.
 */

(function () {
  "use strict";

  /**
   * Devuelve `true` si el usuario pidió menos animación en su sistema.
   * Se consulta en caliente (no se cachea) porque el usuario puede cambiar la
   * preferencia sin recargar la página.
   */
  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  /* ======================================================================
     1. MENÚ MÓVIL
     ======================================================================
     El botón alterna `aria-expanded` y quita el `hidden` del panel.

     Se cierra con Escape y al pulsar fuera, que son las dos conductas que se
     esperan de un menú desplegable. No se controla `focus-trap`: el panel es
     una lista de cuatro enlaces y sin él el tabulador sigue un orden lógico.
     ====================================================================== */
  function setupMobileNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var panel = document.querySelector("[data-nav-panel]");

    if (!toggle || !panel) {
      return;
    }

    /** Abre o cierra el panel y deja el botón en el estado correcto. */
    function setOpen(open) {
      panel.hidden = !open;
      toggle.setAttribute("aria-expanded", String(open));
      toggle
        .querySelector(".visually-hidden")
        .textContent = open ? "Cerrar menú de navegación" : "Abrir menú de navegación";
    }

    function isOpen() {
      return toggle.getAttribute("aria-expanded") === "true";
    }

    toggle.addEventListener("click", function () {
      setOpen(!isOpen());
    });

    // Cerrar al navegar dentro del panel: si no, el menú tapa el destino.
    panel.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        setOpen(false);
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && isOpen()) {
        setOpen(false);
        // El foco vuelve al botón para que el teclado no se quede perdido.
        toggle.focus();
      }
    });

    document.addEventListener("click", function (event) {
      if (isOpen() && !panel.contains(event.target) && !toggle.contains(event.target)) {
        setOpen(false);
      }
    });

    // Al pasar a escritorio, el panel móvil debe cerrarse: si no, queda
    // flotando sobre el contenido al volver a reducir la ventana.
    window.matchMedia("(min-width: 48rem)").addEventListener("change", function (event) {
      if (event.matches) {
        setOpen(false);
      }
    });
  }

  /* ======================================================================
     2. SCROLLSPY
     ======================================================================
     Resalta el enlace de navegación de la sección que el visitante está
     leyendo.

     Se usa `IntersectionObserver` en lugar de escuchar `scroll`: el navegador
     decide cuándo notificar y el callback no se ejecuta en cada píxel, lo que
     mantiene el desplazamiento fluido incluso en móviles de gama baja.

     La franja de detección es una línea horizontal situada cerca del tercio
     superior de la pantalla. Se eligió esa altura y no el centro porque el
     header fijo ocupa la parte superior: una sección que «está visible» pero
     sigue bajo el header no es la que el visitante está leyendo.
     ====================================================================== */
  function setupScrollSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll("[data-nav-link]"));

    if (!links.length || !("IntersectionObserver" in window)) {
      return;
    }

    // Mapa id de sección → enlace correspondiente.
    var linkById = {};
    links.forEach(function (link) {
      var id = link.getAttribute("href");
      if (id && id.charAt(0) === "#") {
        linkById[id.slice(1)] = link;
      }
    });

    var visible = Object.create(null);

    /** Aplica `aria-current` a un único enlace, para no acumular estados. */
    function markActive(id) {
      links.forEach(function (link) {
        link.removeAttribute("aria-current");
      });
      if (linkById[id]) {
        linkById[id].setAttribute("aria-current", "true");
      }
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            visible[entry.target.id] = entry.intersectionRatio;
          } else {
            delete visible[entry.target.id];
          }
        });

        // Con varias secciones visibles a la vez (las tarjetas son altas), gana
        // la que ocupa más pantalla: es la que el visitante está leyendo.
        var bestId = null;
        var bestRatio = 0;
        Object.keys(visible).forEach(function (id) {
          if (visible[id] > bestRatio) {
            bestRatio = visible[id];
            bestId = id;
          }
        });

        if (bestId) {
          markActive(bestId);
        }
      },
      {
        // Franja de observación: la franja superior, ya por debajo del header.
        rootMargin: "-20% 0px -70% 0px",
        threshold: [0, 0.25, 0.5, 0.75, 1],
      }
    );

    Object.keys(linkById).forEach(function (id) {
      var section = document.getElementById(id);
      if (section) {
        observer.observe(section);
      }
    });
  }

  /* ======================================================================
     3. ANIMACIONES DE ENTRADA
     ======================================================================
     Los bloques con `data-reveal` aparecen con un desplazamiento suave al
     entrar en pantalla.

     El CSS mantiene todo visible salvo que la clase `.js` esté presente en
     `<html>`; este módulo solo añade `is-visible`. Si el usuario pidió menos
     movimiento, se marcan todos como visibles de inmediato.
     ====================================================================== */
  function setupReveal() {
    var items = document.querySelectorAll("[data-reveal]");

    if (!items.length) {
      return;
    }

    if (prefersReducedMotion() || !("IntersectionObserver" in window)) {
      items.forEach(function (item) {
        item.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            return;
          }
          entry.target.classList.add("is-visible");
          // Deja de observar: la animación ocurre una sola vez y no se
          // repite cada vez que el usuario vuelve a hacer scroll arriba.
          observer.unobserve(entry.target);
        });
      },
      {
        // Un margen inferior negativo hace que la animación empiece antes de
        // que el bloque entre del todo en pantalla: se percibe más fluida.
        rootMargin: "0px 0px -10% 0px",
        threshold: 0.1,
      }
    );

    items.forEach(function (item) {
      observer.observe(item);
    });
  }

  /* ======================================================================
     4. BOTÓN FLOTANTE DE WHATSAPP
     ======================================================================
     El botón flotante compite con el contenido, así que solo aparece cuando
     el visitante ya ha leído una parte de la página. Se oculta de nuevo al
     llegar al final, donde el CTA grande del sitio cumple la misma función.

     El HTML lo incluye con `hidden`, de modo que no aparece nunca por defecto
     (y si el script falla, el botón simplemente no se muestra). Este módulo
     quita y pone ese atributo según la posición del scroll.
     ====================================================================== */
  function setupFloatingCta() {
    var button = document.querySelector("[data-whatsapp-float]");

    if (!button) {
      return;
    }

    var SHOW_AFTER = 600; // px de scroll antes de mostrarlo.

    /** Actualiza la visibilidad según la posición del scroll. */
    function update() {
      var scrolled = window.scrollY > SHOW_AFTER;
      var atBottom =
        window.innerHeight + window.scrollY >= document.body.scrollHeight - 120;

      if (scrolled && !atBottom) {
        button.removeAttribute("hidden");
      } else {
        button.setAttribute("hidden", "");
      }
    }

    // `passive: true` declara que el callback no llama a `preventDefault`, lo
    // que permite al navegador seguir desplazando sin esperar al JS.
    window.addEventListener("scroll", update, { passive: true });
    update();
  }

  /* ======================================================================
     ARRANQUE
     ====================================================================== */
  setupMobileNav();
  setupScrollSpy();
  setupReveal();
  setupFloatingCta();
})();