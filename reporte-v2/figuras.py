"""Figuras del reporte v2: compone las capturas de Fusion y dibuja los esquemas a escala."""
import ast, json, math, os, re, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Circle, Rectangle, FancyArrowPatch
from PIL import Image
from shapely.geometry import Point, Polygon, box
from shapely import affinity
from shapely.ops import unary_union

GEN, FRASE, CAP, OUT = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
T = "/tmp/claude-tool-results/84f37f2d-5fc7-555c-be7b-5a3d9d2e20b9/mcp-remote-devices-blob-"
R = {"funda": "1795119540714-o19vsd-ecadb84c", "aguja12": "1795119446625-6qagjr-7dd22b66", "abre": "1795119456766-fzzwe2-3febe255",
     "expo": "1795119462924-c9phc5-467057f0", "frontal": "1795119464752-zt1i2q-b203332d", "explo": "1795119489422-9x946r-a6769cc2",
     "meca": "1795119497433-ey5x1c-b40331bf", "corte": "1795119515030-9c8ca8-7f4fb3a3", "soporte": "1795119529450-k6hyir-432f1bfb",
     "aparcado": "1795119533526-w2j2pf-92c44639", "aguja": "1795119543953-evsbam-cef1ca7a"}
FONDO = (246, 245, 241)
AZUL, PAPEL, TINTA, GRIS = "#1F3FA8", "#F7F6F2", "#15171C", "#555A64"
ROJO, NARANJA, VERDE = "#D9655F", "#E8A33D", "#4E9A62"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": "#BBBBBB"})

def cap(nombre, recorte=True):
    im = Image.open(T + R[nombre] + ".png").convert("RGBA")
    if recorte:
        a = np.array(im)[:, :, 3]
        ys, xs = np.where(a > 8)
        m = 30
        im = im.crop((max(xs.min() - m, 0), max(ys.min() - m, 0), min(xs.max() + m, im.width), min(ys.max() + m, im.height)))
    bg = Image.new("RGBA", im.size, FONDO + (255,))
    bg.alpha_composite(im)
    return bg.convert("RGB")

def guardar(fig, nombre, dpi=150):
    p = os.path.join(OUT, nombre)
    fig.savefig(p, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print(nombre, Image.open(p).size)

def lienzo(w, h):
    fig = plt.figure(figsize=(w, h))
    fig.patch.set_facecolor(np.array(FONDO) / 255)
    return fig

def etiqueta(ax, txt, xy, xytext, color=TINTA, ha="center", fs=11):
    ax.annotate(txt, xy=xy, xytext=xytext, ha=ha, va="center", fontsize=fs, color=color, zorder=30,
                arrowprops=dict(arrowstyle="-", color=color, lw=1.0, shrinkA=2, shrinkB=2),
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#CCCCCC", lw=0.6))

def cota(ax, p0, p1, txt, off=(0, 0), color=TINTA, fs=10):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="<->", mutation_scale=9, color=color, lw=1.0, shrinkA=0, shrinkB=0, zorder=28))
    ax.text((p0[0] + p1[0]) / 2 + off[0], (p0[1] + p1[1]) / 2 + off[1], txt, ha="center", va="center", fontsize=fs, color=color, zorder=31,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))

# ---------- parametros ----------
mod = ast.parse(open(GEN, encoding="utf-8").read())
P_DEF = next(ast.literal_eval(n.value) for n in mod.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "P_DEF")
P = {}
for n, u, e, c in P_DEF:
    P[n] = eval(re.sub(r"\b(mm|deg)\b", "", e), {"__builtins__": {}}, P)
L, Do, Ho = P["caja_ancho"], P["caja_fondo"], P["caja_alto"]
cl, ch = P["nicho_ancho"], P["nicho_alto"]
t = math.radians(P["soporte_inclinacion"]); Rr = P["soporte_alto"] / 2; st = (P["soporte_largo"] - P["soporte_alto"]) / 2
yF, yB, zf, zp = -Do / 2 + P["tapa_alto"], Do / 2 - P["pared"], P["pared_techo"], Ho / 2
z0 = zf - P["soporte_rebaje"]; zc = z0 + P["soporte_pie"] + st * math.cos(t) + Rr
yc = yF + P["aire_frente"] + (Rr + P["reloj_grosor"]) * math.cos(t) + P["reloj_asa_asa"] / 2 * math.sin(t)
rm = P["rotor_radio_iman"]; mx, my = cl / 2 - 4.5, ch / 2 - 4.5
xs_, ym = P["soporte_ancho"] / 2 + P["patin_ancho"] / 2, yc + (P["patin_detras"] - P["patin_frente"]) / 2
h, pf = P["holg_desliza"], P["pared_funda"]
fx0, fx1 = -L / 2 - h - P["funda_fondo"], L / 2
fy = Do / 2 + h + pf; fz0, fz1 = -h - pf, Ho + h + pf

# ---------- 01 portada ----------
cap("funda").save(os.path.join(OUT, "01-funda-con-frase-y-aguja.png")); print("01 ok")

# ---------- 02 secuencia ----------
fig = lienzo(15, 11.2)
pasos = [("funda", "1 · La funda: la frase al frente, la aguja en el lateral"), ("aguja12", "2 y 3 · Fuera de la funda: la aguja se coloca sola a las 12"),
         ("abre", "4 y 5 · Se gira 40° y el panel sale"), ("expo", "6 · El reloj a la vista, con la tarjeta de fondo")]
for i, (k, tit) in enumerate(pasos):
    ax = fig.add_subplot(2, 2, i + 1); ax.imshow(cap(k)); ax.axis("off")
    ax.set_title(tit, fontsize=13, color=TINTA, loc="left", pad=8, fontweight="bold")
fig.subplots_adjust(wspace=0.04, hspace=0.12)
guardar(fig, "02-secuencia-de-apertura.png", 120)

# ---------- 03 expositor ----------
cap("expo").save(os.path.join(OUT, "03-expositor-abierto.png")); print("03 ok")

# ---------- 04 frontal + aparcado ----------
fig = lienzo(15, 6.4)
for i, (k, tit) in enumerate([("frontal", "Vista de frente, sin panel"), ("aparcado", "Por detrás, con el panel aparcado en la trasera")]):
    ax = fig.add_subplot(1, 2, i + 1); ax.imshow(cap(k)); ax.axis("off"); ax.set_title(tit, fontsize=13, loc="left", fontweight="bold", color=TINTA)
guardar(fig, "04-vista-frontal-y-panel-aparcado.png", 120)

# ---------- 05 explosionada ----------
im = cap("explo", recorte=False)
fig = lienzo(15, 10); ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(im); ax.axis("off")
for txt, xy, xt in [("funda", (330, 300), (300, 130)), ("frase", (470, 445), (560, 620)), ("aguja", (168, 520), (95, 700)),
                    ("rebaje de la aguja", (248, 480), (300, 760)), ("base (la caja)", (620, 170), (560, 50)), ("soporte", (840, 470), (800, 620)),
                    ("reloj (referencia)", (930, 340), (1010, 215)), ("tapeta", (1190, 470), (1120, 300)), ("rotor", (1272, 425), (1290, 290)),
                    ("tapa (panel frontal)", (1380, 560), (1380, 760))]:
    etiqueta(ax, txt, xy, xt, fs=13)
ax.set_xlim(0, im.width); ax.set_ylim(im.height - 140, 0)
guardar(fig, "05-vista-explosionada.png", 110)

# ---------- 06 mecanismo en tres estados ----------
def hp(p, n, S=400):
    nx, ny = n; ln = math.hypot(nx, ny); nx, ny = nx / ln, ny / ln; tx, ty = -ny, nx
    return Polygon([(p[0] + tx * S, p[1] + ty * S), (p[0] - tx * S, p[1] - ty * S), (p[0] - tx * S + nx * S, p[1] - ty * S + ny * S), (p[0] + tx * S + nx * S, p[1] + ty * S + ny * S)])
def disco(r, c=(0, 0)): return Point(c).buffer(r, 96)
Rc, Rrot, hw = P["rotor_radio"] + 0.3, P["rotor_radio"], P["rotor_ancho"] / 2
g = math.radians(P["rotor_giro"]); lat = (math.cos(g), -math.sin(g)); hw2 = hw + 0.3
wp = hp((-hw2, 0), (1, 0)).intersection(hp((hw2 * lat[0], hw2 * lat[1]), (-lat[0], -lat[1])))
wn = hp((hw2, 0), (-1, 0)).intersection(hp((-hw2 * lat[0], -hw2 * lat[1]), lat))
camara = disco(Rc).intersection(wp.union(wn)).union(disco(7.3)).difference(disco(4.0))
panel = box(-cl / 2 + 0.2, -ch / 2 + 0.2, cl / 2 - 0.2, ch / 2 - 0.2)
hueco = box(-cl / 2, -ch / 2, cl / 2, ch / 2)
caja = box(-L / 2, -Ho / 2, L / 2, Ho / 2)
ranuras = disco(Rc).intersection(caja).difference(hueco)
def rotor(ang):
    r = box(-hw, -Rrot - 2, hw, Rrot + 2).intersection(disco(Rrot)).union(disco(7.0)).difference(disco(4.3))
    return affinity.rotate(r, -ang, origin=(0, 0))
def aguja_poly():
    pu, fl, fw, va, vp = P["aguja_punta"], P["aguja_flecha_largo"], P["aguja_flecha_ancho"], P["aguja_varilla"], P["aguja_varilla_punta"]
    fb = pu - fl
    tri = Polygon([(-fw / 2, fb), (fw / 2, fb), (0, pu)])
    cuerpo = unary_union([disco(P["aguja_cubo_d"] / 2), disco(P["aguja_pala_d"] / 2, (0, -rm)), box(-va / 2, -rm, va / 2, 0),
                          Polygon([(-va / 2, 0), (va / 2, 0), (vp / 2, fb + 0.5), (-vp / 2, fb + 0.5)]), tri])
    return cuerpo.difference(tri.buffer(-P["aguja_flecha_pared"], join_style=2))
AG = aguja_poly()
def pinta(ax, geom, hole="white", **kw):
    for gg in (geom.geoms if hasattr(geom, "geoms") else [geom]):
        if gg.is_empty or gg.geom_type != "Polygon": continue
        ax.add_patch(MPoly(np.array(gg.exterior.coords), closed=True, **kw))
        for i in gg.interiors:
            ax.add_patch(MPoly(np.array(i.coords), closed=True, fc=hole, ec=kw.get("ec", "none"), lw=kw.get("lw", 0.8), zorder=kw.get("zorder", 1) + 0.01))
fig = lienzo(16.5, 5.9)
estados = [(0, "0° · BLOQUEADO", "Los extremos del rotor están dentro\nde las ranuras del techo y del suelo.", ROJO),
           (20, "20° · AÚN BLOQUEADO", "Los extremos siguen asomando\nmás allá del borde del panel.", ROJO),
           (40, "40° · LIBRE", "El rotor queda entero dentro del panel.\nSe libera a partir de unos 25°.", VERDE)]
for i, (ang, tit, sub, col) in enumerate(estados):
    ax = fig.add_subplot(1, 3, i + 1); ax.set_aspect("equal"); ax.axis("off")
    pinta(ax, caja.difference(hueco), fc="#DDD8C8", ec="#8A8676", lw=1.0, zorder=1)
    pinta(ax, ranuras, fc="white", ec="#8A8676", lw=0.8, zorder=2)
    pinta(ax, panel, fc="#F4F1E8", ec="#8A8676", lw=1.0, zorder=3)
    pinta(ax, camara, fc="#E2DCCB", ec="#B5AE9A", lw=0.8, zorder=4, hole="#F4F1E8")
    r = rotor(ang)
    pinta(ax, r, fc=ROJO, ec="#8E3B36", lw=1.0, zorder=5, hole="#F4F1E8")
    fuera = r.difference(panel)
    if not fuera.is_empty: pinta(ax, fuera, fc="#8E1F1A", ec="#5A0F0C", lw=1.0, zorder=6)
    a = math.radians(-ang)
    for cx, cy, fc in [(0, 0, "#3A3A3A"), (rm * math.sin(a), -rm * math.cos(a), NARANJA)]:
        ax.add_patch(Circle((cx, cy), 2.5, fc=fc, ec="black", lw=0.8, zorder=7))
    pinta(ax, affinity.rotate(AG, -ang, origin=(0, 0)), fc=AZUL, ec="#0E1F5C", lw=0.8, zorder=8, alpha=0.55, hole="none")
    for sx in (1, -1):
        for sz in (1, -1): ax.add_patch(Circle((sx * mx, sz * my), 2.5, fc="#BDBDBD", ec="#777", lw=0.6, zorder=4))
    ax.set_xlim(-L / 2 - 3, L / 2 + 3); ax.set_ylim(-Ho / 2 - 15, Ho / 2 + 9)
    ax.text(0, Ho / 2 + 5, tit, ha="center", va="center", fontsize=15, fontweight="bold", color=col)
    ax.text(0, -Ho / 2 - 8.5, sub, ha="center", va="center", fontsize=10.5, color=GRIS)
    if i == 0:
        etiqueta(ax, "pestillo en\nla ranura", (0, ch / 2 + 0.6), (-27, 27), fs=9.5)
        etiqueta(ax, "imán del rotor", (0, -rm), (27, -22), fs=9.5)
        etiqueta(ax, "imán central\nfijo", (0, 0), (28, 2), fs=9.5)
        etiqueta(ax, "cámara:\ndos cuñas", (-14, -22), (-30, -6), fs=9.5)
        etiqueta(ax, "aguja\n(por fuera)", (0.5, 16), (-27, 8), color=AZUL, fs=9.5)
    if i == 1:
        ax.add_patch(FancyArrowPatch((6, 30), (20, 22), connectionstyle="arc3,rad=-0.25", arrowstyle="-|>", mutation_scale=14, color=AZUL, lw=1.8, zorder=9))
        ax.text(30, 14, "giro\nhorario", ha="center", va="center", color=AZUL, fontsize=10, fontweight="bold", zorder=30)
    if i == 2:
        ax.add_patch(FancyArrowPatch((-8.7, -10.3), (-8.7, -22), arrowstyle="-|>", mutation_scale=12, color=NARANJA, lw=1.6, zorder=9))
        ax.text(22, -22, "el peso del imán\ntira hacia cerrado", ha="center", va="center", color="#9A6410", fontsize=9.5, fontweight="bold", zorder=30)
fig.suptitle("El panel visto de frente, con el interior al descubierto", fontsize=14, color=TINTA, y=0.93)
guardar(fig, "06-mecanismo-tres-estados.png", 130)

# ---------- 07 seccion de la tapa ----------
EX = 7.0  # ampliacion de los espesores
fig = lienzo(13, 7.2); ax = fig.add_axes([0.02, 0.03, 0.96, 0.88]); ax.set_aspect("equal"); ax.axis("off")
def capa(d0, d1, a0, a1, **kw): ax.add_patch(Rectangle((d0 * EX, a0), (d1 - d0) * EX, a1 - a0, **kw))
piel, rg, ha_, tg, ta = P["tapa_piel"], P["rotor_grosor"], P["rotor_holg_axial"], P["tapeta_grosor"], P["tapa_alto"]
cb = piel + rg + ha_; alt = ch / 2
for s in (1, -1):  # techo y suelo de la caja
    capa(0, ta + 4.5, s * alt, s * (alt + P["pared_techo"]), fc="#DDD8C8", ec="#8A8676", lw=1.0, zorder=1)
    capa(cb - rg - 0.5, cb + 0.2, s * alt, s * (alt + 1.6), fc="white", ec="#8A8676", lw=0.8, zorder=2)
capa(0, piel, -alt + 0.2, alt - 0.2, fc="#F2C98A", ec="#9A6B1E", lw=1.0, zorder=3)           # piel
capa(piel, cb, -alt + 0.2, alt - 0.2, fc="#FBF8EF", ec="#C9C2AC", lw=0.6, zorder=3)           # camara
capa(cb, cb + tg, -alt + 0.2, alt - 0.2, fc="#B7D7B0", ec="#4E7C47", lw=1.0, zorder=3)        # tapeta
capa(piel, cb, -4, 4, fc="#F2C98A", ec="#9A6B1E", lw=1.0, zorder=4)                            # poste
capa(cb - rg, cb, -P["rotor_radio"] + 1.5, P["rotor_radio"] - 1.5, fc=ROJO, ec="#8E3B36", lw=1.0, zorder=5)
for s in (1, -1):
    capa(cb - P["pestillo_grosor"], cb, s * (P["rotor_radio"] - 1.5), s * P["rotor_radio"], fc="#8E1F1A", ec="#5A0F0C", lw=1.0, zorder=6)
capa(cb - rg, cb, -4.3, 4.3, fc="#FBF8EF", ec="#8E3B36", lw=0.8, zorder=6)                     # hueco del rotor alrededor del poste
capa(piel, cb, -4, 4, fc="#F2C98A", ec="#9A6B1E", lw=1.0, zorder=7)
ag = P["aguja_grosor"]
capa(-ag - 0.15, -0.15, -rm - 4.3, P["aguja_punta"] - 2, fc=AZUL, ec="#0E1F5C", lw=1.0, zorder=5, alpha=0.9)
ims = [(-1.75, 0, "#3A3A3A"), (-1.75, -rm, "#3A3A3A"), (piel, 0, "#3A3A3A"), (cb - rg, -rm, NARANJA)]
for d0, a, fc in ims: capa(d0, d0 + P["iman_h"], a - 2.5, a + 2.5, fc=fc, ec="black", lw=0.9, zorder=8)
for a in (0, -rm):
    ax.add_patch(FancyArrowPatch((-0.1 * EX, a), ((piel if a == 0 else cb - rg) * EX, a), arrowstyle="<->", mutation_scale=10, color="#C0392B", lw=1.6, zorder=9))
ax.text(-ag * EX - 18, -alt - 9, "←  FUERA", ha="right", va="center", fontsize=11, color=GRIS, fontweight="bold")
ax.text((ta + 2.2) * EX + 4, -alt - 9, "DENTRO DE LA CAJA  →", ha="left", va="center", fontsize=11, color=GRIS, fontweight="bold")
izq = -ag * EX - 6
etiqueta(ax, "aguja", (-ag / 2 * EX, 14), (izq - 12, 12), color=AZUL, ha="right")
etiqueta(ax, "imán del cubo", (-0.95 * EX, 0), (izq - 12, 2), ha="right")
etiqueta(ax, "imán de la cola", (-0.95 * EX, -rm), (izq - 12, -rm - 3), ha="right")
der = (ta + 2.2) * EX
etiqueta(ax, "piel del panel · 1,0 mm", (piel / 2 * EX, 26), (der + 4, 25), ha="left")
etiqueta(ax, "rotor · 2,2 mm en una cámara de 2,5", ((cb - rg / 2) * EX, 12), (der + 4, 12), ha="left")
etiqueta(ax, "imán central, fijo en un poste", ((piel + 0.8) * EX, 1.2), (der + 4, 3), ha="left")
etiqueta(ax, "imán del rotor", ((cb - rg + 0.8) * EX, -rm - 1), (der + 4, -rm - 1), ha="left")
etiqueta(ax, "tapeta · 1,0 mm", ((cb + tg / 2) * EX, -24), (der + 4, -24), ha="left")
etiqueta(ax, "pestillo: entra 1,3 mm\nen la ranura del techo", ((cb - 0.6) * EX, alt + 0.7), (der + 4, alt + 3), ha="left")
etiqueta(ax, "ranura del suelo", ((cb - 0.6) * EX, -alt - 0.7), (der + 4, -alt - 1), ha="left")
etiqueta(ax, "techo de la caja", (1.5 * EX, alt + 2.2), (izq - 12, alt + 2.2), ha="right")
cota(ax, (0, -alt - 7.5), (ta * EX, -alt - 7.5), "panel: 4,6 mm", off=(0, -3))
cota(ax, (izq - 2, -rm), (izq - 2, 0), "13,5", off=(-6, 0))
ax.set_xlim(izq - 62, der + 92); ax.set_ylim(-alt - 14, alt + 10)
ax.set_title("Corte del panel por su eje vertical (espesores ampliados ×7; alturas a escala)", fontsize=12.5, color=TINTA)
guardar(fig, "07-corte-del-panel.png", 130)

# ---------- 08 render del mecanismo ----------
im = cap("meca", recorte=False)
fig = lienzo(12, 9); ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(im); ax.axis("off")
for txt, xy, xt in [("rotor", (600, 250), (760, 160)), ("extremo del rotor: el pestillo", (600, 78), (900, 30)), ("cámara en dos cuñas:\nhace de tope a 0° y a 40°", (430, 220), (300, 420)),
                    ("poste con el imán central", (600, 455), (860, 400)), ("alojamiento de un imán de esquina", (208, 150), (330, 50)),
                    ("rebaje donde encaja la tapeta", (800, 300), (930, 250))]:
    etiqueta(ax, txt, xy, xt, fs=12)
guardar(fig, "08-panel-por-detras.png", 110)

# ---------- 09 aguja ----------
fig = lienzo(14, 9.2)
ax = fig.add_axes([0.02, 0.5, 0.96, 0.47]); ax.imshow(cap("aguja")); ax.axis("off")
ax = fig.add_axes([0.04, 0.02, 0.92, 0.46]); ax.set_aspect("equal"); ax.axis("off")
H = affinity.rotate(AG, -90, origin=(0, 0))   # punta hacia la derecha
pinta(ax, H, fc=AZUL, ec="#0E1F5C", lw=1.2, zorder=3, hole=np.array(FONDO) / 255)
for cx in (0, -rm): ax.add_patch(Circle((cx, 0), P["iman_d"] / 2, fc="none", ec="white", lw=1.4, ls="--", zorder=4))
pu = P["aguja_punta"]; fb = pu - P["aguja_flecha_largo"]; cola = rm + P["aguja_pala_d"] / 2
cota(ax, (-cola, -9.5), (pu, -9.5), "51,8 mm", off=(0, -2))
cota(ax, (0, 9), (pu, 9), "34", off=(0, 1.8)); cota(ax, (-rm, 9), (0, 9), "13,5", off=(0, 1.8))
cota(ax, (fb, -6.3), (pu, -6.3), "10", off=(0, -1.8))
cota(ax, (pu + 2.5, -3.25), (pu + 2.5, 3.25), "6,5", off=(3.2, 0))
etiqueta(ax, "cubo Ø 9", (2.5, 3.6), (9, 6.2), fs=10); etiqueta(ax, "disco Ø 8,6", (-rm - 2.5, -3.4), (-rm - 3, -6.4), fs=10)
etiqueta(ax, "varilla: de 2,0 a 1,2 mm", (16, 0.8), (22, 4.6), fs=10)
etiqueta(ax, "imanes de 5 × 1,6 mm (por debajo)", (0, -2.6), (10, -5.4), fs=10)
ax.text(-cola, 13.5, "Planta a escala · grosor 2,4 mm", fontsize=11, color=GRIS, ha="left")
ax.set_xlim(-cola - 4, pu + 8); ax.set_ylim(-12.5, 15)
guardar(fig, "09-aguja.png", 120)

# ---------- 10 corte lateral acotado ----------
im = Image.open(T + R["corte"] + ".png").convert("RGBA")
bg = Image.new("RGBA", im.size, FONDO + (255,)); bg.alpha_composite(im); im = bg.convert("RGB")
s = (1212 - 88) / (2 * fy)                      # px por mm, medido sobre la funda
y_izq = -fy - 88 / s; y_der = y_izq + im.width / s
z_sup = fz1 + 42 / s; z_inf = z_sup - im.height / s
fig = lienzo(14, 11.5); ax = fig.add_axes([0.03, 0.03, 0.94, 0.92]); ax.set_aspect("equal"); ax.axis("off")
ax.imshow(im, extent=[y_izq, y_der, z_inf, z_sup])
n = (-math.cos(t), math.sin(t)); a_ = (math.sin(t), math.cos(t))
sw = Rr + P["reloj_grosor"]
p_frente = (yc + sw * n[0] - 22 * a_[0], zc + sw * n[1] - 22 * a_[1])
p_arriba = (yc + sw * n[0] + 22 * a_[0], zc + sw * n[1] + 22 * a_[1])
y_braz = yc + st * math.sin(t) + Rr + P["brazalete_grosor"]; z_braz = zc + st * math.cos(t)
cota(ax, (yF, p_frente[1]), (p_frente[0], p_frente[1]), "5,0", off=(0, 3.2), color="#B03A2E")
cota(ax, (p_arriba[0], p_arriba[1]), (p_arriba[0], zf + ch), "5,0", off=(-4.5, 0), color="#B03A2E")
cota(ax, (y_braz, z_braz), (yB, z_braz), ("%.1f" % (yB - y_braz)).replace(".", ","), off=(0, 3.2), color="#B03A2E")
cota(ax, (yF, zf + ch - 2.4), (yB, zf + ch - 2.4), "fondo interior: 80 mm", off=(20, -2.8))
cota(ax, (yB - 9.5, zf), (yB - 9.5, zf + ch), "alto interior: 72 mm", off=(-13.5, -16))
cota(ax, (-fy, fz0 - 5), (fy, fz0 - 5), "fondo con funda: 92,2 mm", off=(0, -3))
cota(ax, (fy + 5, fz0), (fy + 5, fz1), "83,4 mm", off=(8, 0))
# angulo
base = (yc + Rr * n[0] - 34 * a_[0], zc + Rr * n[1] - 34 * a_[1])
ax.plot([base[0], base[0]], [base[1], base[1] + 22], color=AZUL, lw=1.2, ls="--")
ax.plot([base[0], base[0] + 22 * a_[0]], [base[1], base[1] + 22 * a_[1]], color=AZUL, lw=1.2, ls="--")
ax.text(base[0] + 3.2, base[1] + 16.5, "25°", color=AZUL, fontsize=12, fontweight="bold")
izq, der = -fy - 6, fy + 16
etiqueta(ax, "funda", (-fy + 1, 62), (izq - 8, 62), ha="right")
etiqueta(ax, "panel frontal", (-Do / 2 + 0.5, 50), (izq - 8, 50), ha="right")
etiqueta(ax, "rotor", (-Do / 2 + 2.4, 60), (izq - 8, 70), ha="right")
etiqueta(ax, "tapeta", (-Do / 2 + 4.0, 20), (izq - 8, 20), ha="right")
etiqueta(ax, "pestillo en la\nranura del techo", (-Do / 2 + 2.9, zf + ch + 0.8), (izq - 8, fz1 + 3), ha="right")
etiqueta(ax, "pestillo en la\nranura del suelo", (-Do / 2 + 2.9, zf - 0.8), (izq - 8, fz0 - 2), ha="right")
etiqueta(ax, "imán central", (-Do / 2 + 1.8, zp), (izq - 8, zp - 4), ha="right")
etiqueta(ax, "reloj (referencia,\nsin corona ni brazalete)", (yc + (Rr + 5) * n[0] + 6 * a_[0], zc + (Rr + 5) * n[1] + 6 * a_[1]), (-12, fz1 + 5))
etiqueta(ax, "anillo del soporte", (yc + (Rr - 2) * math.sin(0.6), zc + st + (Rr - 2) * math.cos(0.6)), (22, fz1 + 5))
etiqueta(ax, "patín (detrás del corte)", (yc + 22, z0 + 5), (der + 2, z0 + 5), ha="left")
etiqueta(ax, "tarjeta", (yB - 0.85, zf + 40), (der + 2, zf + 40), ha="left")
etiqueta(ax, "guía en cuña", (yB - 3.2, zf + 20), (der + 2, zf + 20), ha="left")
etiqueta(ax, "rebaje del NFC", (P["nfc_y"], zf + ch + P["pared_techo"] + h + 0.2), (der + 2, fz1 + 3), ha="left")
etiqueta(ax, "pared de la caja", (Do / 2 - 1.5, 62), (der + 2, 62), ha="left")
ax.set_xlim(izq - 42, der + 34); ax.set_ylim(fz0 - 14, fz1 + 10)
ax.set_title("Corte por el centro de la caja, visto desde la derecha (el frente queda a la izquierda)", fontsize=12.5, color=TINTA)
guardar(fig, "10-corte-lateral-acotado.png", 125)

# ---------- 11 soporte ----------
im = cap("soporte", recorte=False)
fig = lienzo(10, 9); ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(im); ax.axis("off")
for txt, xy, xt in [("anillo ovalado de 60 × 46 mm,\nrecostado 25°", (700, 210), (800, 90)), ("hueco para apretar\nel cierre del brazalete", (690, 440), (860, 380)),
                    ("patín: llega hasta debajo\ndel reloj para que no vuelque", (230, 700), (190, 850)), ("imán bajo cada patín", (640, 760), (800, 850)),
                    ("reloj (referencia)", (360, 400), (150, 180)), ("4,5 mm libres para\nel brazalete", (420, 640), (120, 560))]:
    etiqueta(ax, txt, xy, xt, fs=12)
guardar(fig, "11-soporte.png", 110)

# ---------- 12 frase ----------
data = json.load(open(FRASE))
fig = lienzo(11, 9.4); ax = fig.add_axes([0.05, 0.05, 0.9, 0.88]); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Rectangle((fx0, fz0), fx1 - fx0, fz1 - fz0, fc="#ECEBE7", ec="#8A8676", lw=1.4))
x0, zt = fx0 + P["frase_margen"], fz1 - P["frase_margen"]
for pol in data["poligonos"]:
    ax.add_patch(MPoly(np.array(pol["outer"]) + [x0, zt], closed=True, fc=AZUL, ec="none", zorder=3))
    for hh in pol["holes"]: ax.add_patch(MPoly(np.array(hh) + [x0, zt], closed=True, fc="#ECEBE7", ec="none", zorder=4))
W_, H_ = data["ancho_mm"], data["alto_mm"]
cota(ax, (x0, zt - H_ - 4), (x0 + W_, zt - H_ - 4), "74,4 mm", off=(0, -2.6))
cota(ax, (x0 + W_ + 4, zt - H_), (x0 + W_ + 4, zt), "22,4", off=(5, 0))
cota(ax, (fx0, zt - 7), (x0, zt - 7), "11", off=(0, 2.6)); cota(ax, (x0 + 16, zt), (x0 + 16, fz1), "11", off=(3.4, 0))
cota(ax, (fx0, fz0 - 5), (fx1, fz0 - 5), "98,1 mm", off=(0, -2.8)); cota(ax, (fx1 + 5, fz0), (fx1 + 5, fz1), "83,4 mm", off=(8, 0))
ax.text((fx0 + fx1) / 2, fz0 + 20, "Reenie Beanie · incrustada 0,6 mm · trazo engordado 0,20 mm por lado", ha="center", fontsize=10.5, color=GRIS)
ax.text(fx0 + 2, fz0 + 3, "lateral cerrado\n(aguja)", fontsize=9, color=GRIS, ha="left", va="bottom")
ax.text(fx1 - 2, fz0 + 3, "boca de\nla funda", fontsize=9, color=GRIS, ha="right", va="bottom")
ax.set_xlim(fx0 - 10, fx1 + 20); ax.set_ylim(fz0 - 11, fz1 + 8)
ax.set_title("El frente de la funda, a escala", fontsize=12.5, color=TINTA)
guardar(fig, "12-frase-en-la-funda.png", 130)

# ---------- 13 mapa de imanes ----------
COL = {"llave": "#C0392B", "panel": "#2E6FBF", "soporte": "#2E9E5B", "aparcado": "#8E5BC0", "funda": "#D68910"}
NOM = {"llave": "Llave (4)", "panel": "Clic del panel (8)", "soporte": "Soporte (4)", "aparcado": "Panel aparcado (4)", "funda": "Funda y caja (4)"}
fig = lienzo(16, 7.3)
def iman(ax, xy, k, txt=None, dx=0, dy=0):
    ax.add_patch(Circle(xy, 2.6, fc=COL[k], ec="black", lw=0.8, zorder=6))
    if txt: ax.text(xy[0] + dx, xy[1] + dy, txt, fontsize=9, ha="center", va="center", color=COL[k], fontweight="bold")
# vista de frente (x, z)
ax = fig.add_subplot(1, 2, 1); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Rectangle((fx0, fz0), fx1 - fx0, fz1 - fz0, fc="none", ec="#B9B4A4", lw=1.0, ls="--"))
ax.add_patch(Rectangle((-L / 2, 0), L, Ho, fc="#EFEBDF", ec="#8A8676", lw=1.2))
ax.add_patch(Rectangle((-cl / 2 + 0.2, zf + 0.2), cl - 0.4, ch - 0.4, fc="#F8F6EF", ec="#8A8676", lw=1.0))
for sx in (1, -1):
    for sz in (1, -1): iman(ax, (sx * mx, zp + sz * my), "panel", "×2", 0, -sz * 6)
    iman(ax, (sx * mx - sx * 7, zp + my), "aparcado"); iman(ax, (sx * mx - sx * 7, zp - my), "aparcado")
    iman(ax, (sx * xs_, 1.6), "soporte", "×2", 0, 6.5)
iman(ax, (0, zp), "llave", "×2", 7, 0); iman(ax, (0, zp - rm), "llave", "×2", 7, 0)
iman(ax, (-L / 2 - 0.3, zp), "funda", "×2", -7.5, 0); iman(ax, (-L / 2 - 0.3, zp - rm), "funda", "×2", -7.5, 0)
ax.text(-mx + 11.5, zp + my, "en la cara trasera", fontsize=8.5, color=COL["aparcado"], ha="left", va="center")
ax.text(0, fz1 + 6, "DE FRENTE", ha="center", fontsize=12, fontweight="bold", color=TINTA)
ax.text(0, fz0 - 5, "«×2» = una pareja: un imán en cada pieza, enfrentados", ha="center", fontsize=9.5, color=GRIS)
ax.set_xlim(fx0 - 14, fx1 + 6); ax.set_ylim(fz0 - 9, fz1 + 8)
# vista desde arriba (x, y) con el frente abajo
ax = fig.add_subplot(1, 2, 2); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Rectangle((fx0, -fy), fx1 - fx0, 2 * fy, fc="none", ec="#B9B4A4", lw=1.0, ls="--"))
ax.add_patch(Rectangle((-L / 2, -Do / 2), L, Do, fc="#EFEBDF", ec="#8A8676", lw=1.2))
ax.add_patch(Rectangle((-cl / 2, yF), cl, yB - yF, fc="#F8F6EF", ec="#8A8676", lw=0.8))
ax.add_patch(Rectangle((-cl / 2 + 0.2, -Do / 2), cl - 0.4, P["tapa_alto"], fc="#F2C98A", ec="#9A6B1E", lw=0.9))
ax.add_patch(Rectangle((-P["soporte_ancho"] / 2, yc - Rr - 3), P["soporte_ancho"], 2 * Rr + 6, fc="#EDEDED", ec="#999", lw=0.8))
for sx in (1, -1):
    x_p = P["soporte_ancho"] / 2 if sx > 0 else -P["soporte_ancho"] / 2 - P["patin_ancho"]
    ax.add_patch(Rectangle((x_p, yc - P["patin_frente"]), P["patin_ancho"], P["patin_frente"] + P["patin_detras"], fc="#DADADA", ec="#888", lw=0.8))
ax.add_patch(Circle((0, yc - (Rr + 5.5) * math.cos(t)), 20, fc="#9A9A9A", ec="#555", lw=0.8, alpha=0.55, zorder=5))
ax.text(0, yc - (Rr + 5.5) * math.cos(t), "reloj", ha="center", va="center", fontsize=9.5, color="white", fontweight="bold", zorder=6)
for sx in (1, -1):
    iman(ax, (sx * mx, -Do / 2 + 2.3), "panel", "panel", -sx * 9.5, -0.8)
    iman(ax, (sx * mx, yF + 3.0), "panel", "caja", -sx * 9, 1.2)
    iman(ax, (sx * mx, Do / 2 - 1.0), "aparcado")
    iman(ax, (sx * xs_, ym), "soporte", "patín\n+ suelo", sx * 10.5, 0)
iman(ax, (-3.2, -Do / 2 + 1.8), "llave"); iman(ax, (3.2, -Do / 2 + 1.8), "llave")
ax.text(0, -fy - 4.5, "panel: central + rotor   ·   aguja: cubo + cola", ha="center", fontsize=9, color=COL["llave"])
iman(ax, (-L / 2 + 1.4, 0), "funda", "caja", 8, 0); iman(ax, (fx0 + 2.6, 0), "funda")
ax.text(fx0 - 2, 0, "funda", fontsize=9, color=COL["funda"], ha="right", va="center", fontweight="bold")
ax.text(0, fy + 3.5, "cara trasera de la caja", fontsize=9, color=COL["aparcado"], ha="center")
ax.text(0, fy + 10, "DESDE ARRIBA (el frente queda abajo)", ha="center", fontsize=12, fontweight="bold", color=TINTA)
ax.text(0, -Do / 2 + 2.3, "", fontsize=1)
ax.set_xlim(fx0 - 16, fx1 + 6); ax.set_ylim(-fy - 9, fy + 13)
fig.legend(handles=[plt.Line2D([], [], marker="o", ls="", ms=11, mfc=COL[k], mec="black", label=NOM[k]) for k in COL], loc="lower center", ncol=5, frameon=False, fontsize=11)
fig.subplots_adjust(bottom=0.09, top=0.98, wspace=0.05)
guardar(fig, "13-mapa-de-imanes.png", 120)
print("frente %.2f arriba %.2f detras %.2f" % (p_frente[0] - yF, zf + ch - p_arriba[1], yB - y_braz))
