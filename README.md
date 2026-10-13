# Airú — 3 propuestas de sitio web (demo)

**Qué es:** tres propuestas de diseño (HTML estático, bilingüe ES/EN) para el nuevo sitio de Airú (achachairu.com.bo, Angirú S.R.L.), para que el cliente elija. Página de entrada: `index.html`.

- `a-fruta-viva/` — naranja editorial, mascota como guía que sigue el scroll.
- `b-tienda/` — tienda premium blanca/verde, carrito "Mi pedido", mapa Leaflet, mascota como sello.
- `c-amazonia/` — selva nocturna cinematográfica por capítulos, mascota narradora.
- `assets/` — logos, mascota y fotos del cliente.

**Cómo se trabaja:** sin build. `python3 -m http.server` en esta carpeta, o abrir los HTML. Se publica con GitHub Pages. Todas llevan `noindex`.

**Zonas frágiles:** el muñeco NO debe seguir mouse ni dedo (regla del cliente): no agregar `mousemove/pointermove/touchmove` para moverlo. Nada de WhatsApp. Fuentes por Google Fonts; B usa Leaflet (unpkg) y tiles de OpenStreetMap.

**Pendiente:** son demos. Faltan datos reales del cliente: precios B2C/B2B, certificaciones, distribuidores (mapa), videos de comunidades, fotos de acerola y polvo. Las versión final (Next.js, panel `/administrador`, alertas por correo, SEO/GEO) se planea en `airu-web` (repo interno, no público).
