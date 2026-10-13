# Propuesta B · Tienda premium (Airú)

`index.html` es la página completa (CSS+JS inline, sin build para el visitante).

- Posicionamiento: "Achachairú de Bolivia, para el mundo": sección de Exportación (importadores/distribuidores), formulario de consulta de exportación (demo), modo "Importadores" del carrito (cotización de exportación con país), mapa Leaflet "En Bolivia" y mapamundi SVG "En el mundo".
- El mapamundi se genera con `build-world.py` (herramienta de desarrollo) a partir de `world-atlas` (`countries-110m.json`, `npm i world-atlas` o jsDelivr) y se inlinea entre los marcadores `<!--WORLD:START-->` y `<!--WORLD:END-->`:
  `python3 build-world.py countries-110m.json index.html`
- Zonas frágiles: no mover la mascota con mousemove/pointermove/touchmove (regla del cliente); sin WhatsApp; las rutas y destinos del mundo son de ejemplo (no afirman exportaciones reales); certificaciones y fichas técnicas son casilleros rotulados.
- Pendiente: textos/datos reales del cliente (precios, certificaciones, puntos de venta, videos, presentaciones).
