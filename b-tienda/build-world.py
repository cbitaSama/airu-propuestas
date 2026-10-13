#!/usr/bin/env python3
"""Herramienta de build (no la usa el visitante): genera el mapamundi SVG estilizado
a partir de world-atlas (countries-110m.json) y lo inlinea en index.html entre los
marcadores <!--WORLD:START--> y <!--WORLD:END-->.
Uso: python3 build-world.py <countries-110m.json> <index.html>"""
import json, math, sys, re

src, html = sys.argv[1], sys.argv[2]
topo = json.load(open(src))
sc, tr = topo['transform']['scale'], topo['transform']['translate']
arcs = []
for a in topo['arcs']:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy
        pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
    arcs.append(pts)

def ring(idx):
    out = []
    for i in idx:
        p = arcs[i] if i >= 0 else arcs[~i][::-1]
        out.extend(p if not out else p[1:])
    return out

def ne(lon, lat):  # Natural Earth 1
    l, p = math.radians(lon), math.radians(lat)
    p2 = p * p; p4 = p2 * p2
    x = l * (0.8707 - 0.131979 * p2 + p4 * (-0.013791 + p4 * (0.003971 * p2 - 0.001529 * p4)))
    y = p * (1.007226 + p2 * (0.015085 + p4 * (-0.044475 + 0.028874 * p2 - 0.005916 * p4)))
    return x, -y

# bbox
allp = [ne(lo, la) for lo in (-180, 180) for la in (-58, 84)]
minx = min(p[0] for p in allp); maxx = max(p[0] for p in allp)
miny = min(p[1] for p in allp); maxy = max(p[1] for p in allp)
W = 1000.0; S = W / (maxx - minx); H = (maxy - miny) * S
def P(lon, lat):
    x, y = ne(lon, lat); return ((x - minx) * S, (y - miny) * S)

def num(v):
    t = ('%.1f' % v).rstrip('0').rstrip('.')
    if t.startswith('0.'): t = t[1:]
    elif t.startswith('-0.'): t = '-' + t[2:]
    return t or '0'

def rel(pts):
    # M absoluto + l relativos (coordenadas acumuladas redondeadas, sin deriva)
    x0, y0 = round(pts[0][0], 1), round(pts[0][1], 1)
    out = ['M' + num(x0) + ' ' + num(y0) + 'l']
    px, py = x0, y0; segs = []
    for x, y in pts[1:]:
        x, y = round(x, 1), round(y, 1)
        dx, dy = round(x - px, 1), round(y - py, 1)
        if dx == 0 and dy == 0: continue
        segs.append(num(dx) + ' ' + num(dy)); px, py = x, y
    return out[0] + ' '.join(segs).replace(' -', '-') + 'z'

def unwrap(ll):
    out = [ll[0]]
    for lo, la in ll[1:]:
        pl = out[-1][0]
        while lo - pl > 180: lo -= 360
        while lo - pl < -180: lo += 360
        out.append((lo, la))
    return out

def path_of(geom):
    polys = geom['arcs'] if geom['type'] == 'MultiPolygon' else [geom['arcs']]
    d = []
    for poly in polys:
        for r in poly:
            ll = unwrap(ring(r))
            lons = [p[0] for p in ll]
            shifts = [0]
            if max(lons) > 180: shifts.append(-360)
            if min(lons) < -180: shifts.append(360)
            for sh in shifts:
                pts = [P(lo + sh, la) for lo, la in ll]
                xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
                if (max(xs) - min(xs)) < 2.2 and (max(ys) - min(ys)) < 2.2: continue
                d.append(rel(pts))
    return ''.join(d)

land, bol = [], ''
for g in topo['objects']['countries']['geometries']:
    name = g['properties']['name']
    if name == 'Antarctica': continue
    d = path_of(g)
    if name == 'Bolivia': bol = d
    else: land.append(d)

sx, sy = P(-63.18, -17.78)
dests = [(-100, 40), (10, 48), (30, 22), (112, 33), (135, -27), (-50, -12 + 0)]
dests = [(-100, 40), (12, 48), (32, 18), (112, 32), (136, -27)]
routes = []; pins = []
for i, (lo, la) in enumerate(dests):
    ex, ey = P(lo, la)
    mx, my = (sx + ex) / 2, (sy + ey) / 2
    dist = math.hypot(ex - sx, ey - sy)
    cx, cy = mx, my - dist * 0.32
    routes.append('M%.1f %.1f Q%.1f %.1f %.1f %.1f' % (sx, sy, cx, cy, ex, ey))
    pins.append((ex, ey))

out = []
out.append('<svg class="wmap" viewBox="0 0 %d %d" role="img" aria-labelledby="wmT" data-i18n-attr="aria-label:w.aria">' % (W, round(H)))
out.append('<title id="wmT">Mapamundi estilizado: rutas desde Santa Cruz, Bolivia</title>')
out.append('<g class="land"><path d="%s"/></g>' % ''.join(land))
out.append('<path class="bol" d="%s"/>' % bol)
out.append('<g class="routes" fill="none">')
for i, r in enumerate(routes):
    out.append('<path id="rt%d" class="route" d="%s"/>' % (i, r))
for i, r in enumerate(routes):
    out.append('<path class="rfill" d="%s" pathLength="1"/>' % r)
out.append('</g>')
out.append('<path id="rtLbl" d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none"/>' % (
    sx, sy, (sx + pins[1][0]) / 2 - 10, min(sy, pins[1][1]) - 150, pins[1][0], pins[1][1]))
out.append('<text class="rumbo"><textPath href="#rtLbl" startOffset="20%" data-i18n="w.rumbo">Rumbo al mundo</textPath></text>')
for i, r in enumerate(routes):
    out.append('<g class="fly"><use href="#s-fruit" x="-9" y="-12" width="18" height="22"/><animateMotion dur="%ds" begin="%ds" repeatCount="indefinite" path="%s" keyPoints="0;1" keyTimes="0;1" calcMode="linear"/></g>' % (7 + i, i * 1.3, r))
out.append('<g class="dests">')
for i, (x, y) in enumerate(pins):
    anc = 'end' if x > 780 else 'middle'
    dx = -12 if x > 780 else 0
    dy = 34 if x > 780 else -16
    out.append('<g class="dest" transform="translate(%.1f %.1f)"><circle class="pulse" r="9"/><circle class="dot" r="7"/><text class="dq" x="%d" y="%d" text-anchor="%s" data-i18n="w.dest">Tu mercado</text></g>' % (x, y, dx, dy, anc))
out.append('</g>')
out.append('<g class="origin" transform="translate(%.1f %.1f)"><circle class="pulse o" r="12"/><circle r="9" fill="#F26B21" stroke="#fff" stroke-width="3"/><text class="oq" x="16" y="34" data-i18n="w.origin">Santa Cruz, Bolivia</text></g>' % (sx, sy))
out.append('</svg>')
block = '<!--WORLD:START-->' + ''.join(out) + '<!--WORLD:END-->'

h = open(html, encoding='utf-8').read()
h2, n = re.subn(r'<!--WORLD:START-->.*?<!--WORLD:END-->', lambda m: block, h, flags=re.S)
assert n == 1, 'marcadores no encontrados'
open(html, 'w', encoding='utf-8').write(h2)
print('ok, bytes svg:', len(block), 'viewBox', W, round(H))
