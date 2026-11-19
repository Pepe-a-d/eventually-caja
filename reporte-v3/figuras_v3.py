"""Figuras y calculos del reporte de la v3. Lee las medidas del generador (sin Fusion)."""
import math, re, os, sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP, Circle, Rectangle, Arc
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from imanes import fuerza
GEN = os.path.join(AQUI, '..', 'generador_caja_v3.py')
src = open(GEN, encoding='utf-8').read().replace('import adsk.core as C, adsk.fusion as F, math, json, os', 'import math, json, os')
g = {'__file__': GEN}; exec(compile(src, 'gen', 'exec'), g)
P = g['P']; env = {'PI': math.pi, 'cos': lambda x: math.cos(math.radians(x)), 'sin': lambda x: math.sin(math.radians(x))}
for name, unit, expr, com in g['P_DEF']:
    P[name] = eval(re.sub(r'\s*(mm|deg)\b', '', expr), env, P)
d = g['D'](); an = lambda a, n: g['an'](d, a, n)
AZ, PAPEL, TINTA, GRIS, ROJO = '#1F3FA8', '#F7F6F2', '#22252B', '#9AA0A6', '#C8553D'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'figure.facecolor': PAPEL, 'axes.facecolor': PAPEL, 'savefig.facecolor': PAPEL})

def rot(pts, ang):
    a = math.radians(ang)       # a derechas visto de frente
    return [(x * math.cos(a) + y * math.sin(a), -x * math.sin(a) + y * math.cos(a)) for x, y in pts]
def rotor_pts():
    hw, hy, s, c = d['hw'], d['hy'], math.sin(d['ts']), math.cos(d['ts'])
    top = lambda x: (hy - x * s) / c
    return [(-hw, top(-hw)), (hw, top(hw)), (hw, -top(-hw)), (-hw, -top(hw))]
def enganche(ang):
    return max(0.0, max(y for x, y in rot(rotor_pts(), ang)) - d['ch'] / 2)

# ------------------------------------------------ figura 8: mecanismo
fig, axs = plt.subplots(1, 4, figsize=(15, 5.4), gridspec_kw={'width_ratios': [1, 1, 1, 1.25]})
estados = [(-math.degrees(d['ts']), 'Resbalón: al empujar el panel,\nla boca gira el rotor %.1f° a izquierdas' % math.degrees(d['ts'])),
           (0, 'Cerrado: la espiral lo deja en 0°\ny cada pestillo entra %.1f mm' % P['rotor_enganche']),
           (P['rotor_giro'], 'Abierto: la aguja lo gira %d° a derechas.\nSe libera a los %.1f°' % (P['rotor_giro'], math.degrees(d['tk'])))]
for ax, (ang, tit) in zip(axs[:3], estados):
    cl, ch, hx, hy = d['cl'], d['ch'], d['hx'], d['hy']
    ax.add_patch(Rectangle((-cl / 2 - 3, -ch / 2 - 4), cl + 6, ch + 8, fc='#E4E2DC', ec=TINTA, lw=1))
    c = P['tapa_chaflan']
    ax.add_patch(MP([(-hx, -hy), (hx, -hy), (hx, hy - c), (hx - c, hy), (-hx, hy)], fc='white', ec=TINTA, lw=1))
    for sg in (1, -1):      # ranuras del pestillo
        th = np.linspace(-math.asin(d['lente'] / d['Rc']), math.asin(d['lente'] / d['Rc']), 40)
        ax.add_patch(MP([(d['Rc'] * math.sin(t), sg * d['Rc'] * math.cos(t)) for t in th], fc=PAPEL, ec=TINTA, lw=.8))
    ax.add_patch(MP(rot(rotor_pts(), ang), fc='#C9CED6', ec=TINTA, lw=1))
    ax.add_patch(Circle((0, 0), P['cubo_radio'], fc='#C9CED6', ec=TINTA, lw=1)); ax.add_patch(Circle((0, 0), P['eje_radio'], fc='white', ec=TINTA, lw=.8))
    tt = np.radians(np.linspace(180 - 360 * P['muelle_vueltas'], 180, 200)); rr = np.linspace(P['cubo_radio'], P['muelle_radio_ext'], 200)
    ax.plot(rr * np.cos(tt), rr * np.sin(tt), color=TINTA, lw=.9)
    mx, my = rot([(0, -P['rotor_radio_iman'])], ang)[0]
    ax.add_patch(Circle((mx, my), P['iman_d'] / 2, fc=ROJO, ec=TINTA, lw=.6))
    ax.add_patch(Circle((0, 0), P['iman_d'] / 2, fc=ROJO, ec=TINTA, lw=.6))
    if ang >= 0:            # la aguja, por fuera
        pu, co = P['aguja_punta'], P['rotor_radio_iman']
        ag = [(-1.1, 0), (-0.8, pu - 10), (-3.2, pu - 10), (0, pu), (3.2, pu - 10), (0.8, pu - 10), (1.1, 0), (1.6, -2), (4, -co), (3, -co - 3.4), (0, -co - 4), (-3, -co - 3.4), (-4, -co), (-1.6, -2)]
        ax.add_patch(MP(rot(ag, ang), fc=AZ, ec=AZ, alpha=.55, lw=1))
    ax.set_xlim(-cl / 2 - 5, cl / 2 + 5); ax.set_ylim(-ch / 2 - 6, ch / 2 + 6); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(tit, fontsize=9.5, color=TINTA)
ax = axs[3]
xs = np.arange(-16, 50.01, 0.25); ys = [enganche(a) for a in xs]
ax.plot(xs, ys, color=AZ, lw=2); ax.axhline(0.5, color=GRIS, lw=.8, ls='--'); ax.text(49, 0.56, 'juegos sumados ≈ 0,5 mm', ha='right', fontsize=8, color=GRIS)
ax.axvline(0, color=TINTA, lw=.8); ax.set_xlabel('giro del rotor (°): negativo = resbalón, positivo = aguja'); ax.set_ylabel('cuánto entra el pestillo (mm)')
ax.set_title('Enganche según el giro (del modelo)', fontsize=9.5); ax.grid(alpha=.3); ax.set_ylim(0, 2.6)
fig.tight_layout(); fig.savefig(os.path.join(AQUI, '08-mecanismo-tres-estados.png'), dpi=130); plt.close(fig)
fiable = [a for a in xs if enganche(a) >= 1.0]

# ------------------------------------------------ figura 9: corte lateral
fig, ax = plt.subplots(figsize=(12, 7.6))
Do, Ho, zf, ch, yF, yB = d['Do'], d['Ho'], d['zf'], d['ch'], d['yF'], d['yB']
ax.add_patch(MP([(-d['Yo'], 0), (-d['Yo'], d['Zo']), (d['Yo'], d['Zo']), (d['Yo'], 0), (d['Yi'], 0), (d['Yi'], d['Zi']), (-d['Yi'], d['Zi']), (-d['Yi'], 0)], fc='#ECEBE7', ec=TINTA, lw=1))
ax.add_patch(MP([(-Do / 2, 0), (Do / 2, 0), (Do / 2, Ho), (-Do / 2, Ho), (-Do / 2, zf + ch), (yB, zf + ch), (yB, zf), (-Do / 2 + P['bisel'], zf), (-Do / 2, zf - P['bisel']), (-Do / 2, 0)], fc='white', ec=TINTA, lw=1))
ax.add_patch(Rectangle((-Do / 2, zf + P['holg_tapa']), P['tapa_alto'], ch - 2 * P['holg_tapa'], fc='#DADDE2', ec=TINTA, lw=1))
ax.add_patch(Rectangle((-Do / 2 + P['tapa_piel'], d['zp'] - d['rA']), P['rotor_grosor'], 2 * d['rA'], fc='#AEB6C2', ec=TINTA, lw=.6))
ax.add_patch(Rectangle((yF, d['zp'] - P['tarjeta_ancho'] / 2), P['carril_alto'], P['tarjeta_ancho'], fc=AZ, ec=AZ, alpha=.5))
pol, ext = g['pinza_perfil'](d['st_nom'])
ax.add_patch(MP([an(a, n) for a, n in pol], fc='#9FB3C8', ec=TINTA, lw=.8))
R, ab, at, bz = d['R'], d['ab'], d['ab'] + d['st_nom'], P['brazalete_grosor']
est = lambda e: [(at, -e), (ab, -e)] + g['arco'](ab, R, R + e, 180, 360)[1:] + g['arco'](at, R, R + e, 0, 180)
ax.add_patch(MP([an(a, n) for a, n in est(bz)] + [an(a, n) for a, n in est(0)][::-1], fc='#6E7379', ec=TINTA, lw=.5, alpha=.8))
gr, dia = P['reloj_grosor'], P['reloj_diametro']
ax.add_patch(MP([an(-dia / 2, 0), an(dia / 2, 0), an(dia / 2, -gr), an(-dia / 2, -gr)], fc='#4A4E55', ec=TINTA, lw=.8))
am = (ab + at) / 2; cl2 = P['cierre_largo'] / 2
ax.add_patch(MP([an(am - cl2, 2 * R), an(am + cl2, 2 * R), an(am + cl2, 2 * R + P['cierre_grosor']), an(am - cl2, 2 * R + P['cierre_grosor'])], fc='#4A4E55', ec=TINTA, lw=.8))
h, w = P['cuna_holgura'], P['cuna_grosor']
cu = [(ab + P['cuna_frente'], -h - w), (ab, -h - w)] + g['arco'](ab, R, R + h + w, 180, 360)[1:] + [(ab + P['cuna_detras'], 2 * R + h + w)]
ax.add_patch(MP([an(a, n) for a, n in cu], fc='white', ec=TINTA, lw=.8, alpha=.75, hatch='//'))
ax.add_patch(Rectangle((d['ycu'] - d['ro'], zf), 2 * d['ro'], d['zcu'] - zf, fc='white', ec=TINTA, lw=.8, alpha=.6, hatch='//'))
bg = P['bandeja_grosor']; t0 = d['yt0'] - P['bandeja_ancho'] / P['bandeja_dientes'] / 2
ax.add_patch(MP([(t0, zf), (t0, zf - bg), (d['yt1'] + bg, zf - bg), (d['yt1'], zf)], fc='#F2D9A0', ec=TINTA, lw=.8))
ax.add_patch(Rectangle((d['yh'] - P['aguja_punta'], d['zr']), P['aguja_punta'] + d['pala_fin'], P['aguja_grosor'], fc=AZ, ec=AZ, alpha=.85))
def cota(p, q, txt, off=(0, 0), ha='center'):
    ax.annotate('', p, q, arrowprops=dict(arrowstyle='<->', color=ROJO, lw=1)); ax.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1], txt, color=ROJO, fontsize=8.5, ha=ha, va='center', bbox=dict(fc=PAPEL, ec='none', pad=1))
cota((-d['Yo'], -6), (d['Yo'], -6), 'fondo con funda %.1f' % (2 * d['Yo']))
cota((d['Yo'] + 6, 0), (d['Yo'] + 6, d['Zo']), 'alto con funda %.1f' % d['Zo'], off=(16, 22))
yfr = d['yO'] - dia / 2 * math.sin(d['t']) - gr * math.cos(d['t']); zfr = an(-dia / 2, -gr)[1]
cota((yF + P['carril_alto'], zfr), (yfr, zfr), '%.0f' % (yfr - yF - P['carril_alto']), off=(0, -4))
ztop = an(at, R)[1] + R + bz
cota((an(at, R)[0], ztop), (an(at, R)[0], zf + ch), '%.0f' % (zf + ch - ztop), off=(6, 0))
yb = an(at, 2 * R)[0]
cota((yb, an(at, 2 * R)[1]), (yB, an(at, 2 * R)[1]), 'hueco %.0f' % (yB - yb), off=(0, 5))
for txt, xy, xt in (('frase (0,6 mm) y NFC debajo', (-10, d['Zo']), (-40, d['Zo'] + 9)), ('aguja guardada a ras\n(en el techo de la caja)', (d['yh'] + 10, Ho), (16, Ho + 12)),
                    ('panel: piel 1,4 + rotor 3 + tapeta 1,2', (-Do / 2 + 3, 70), (-98, 76)), ('tarjeta en carriles', (yF + 1, 30), (-98, 40)),
                    ('bisel de apertura', (-Do / 2 + 1.2, zf - 1.2), (-98, 6)), ('peana encastrada,\ntalón a 45° por detrás', (d['yt1'] + 1, zf - 1.2), (50, 14)),
                    ('pinza en C (PETG)', an(at - 6, 2 * R - 0.8), (50, 66)), ('cuna de la peana', an(ab + 2, -2), (-98, 22)), ('cierre', an(am, 2 * R + 5), (50, 50))):
    ax.annotate(txt, xy, xt, fontsize=8.5, color=TINTA, arrowprops=dict(arrowstyle='-', color=TINTA, lw=.6), va='center')
ax.set_xlim(-102, 96); ax.set_ylim(-12, d['Zo'] + 16); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Corte lateral por el eje (frente a la izquierda). Cotas en mm, del modelo.', fontsize=10, color=TINTA)
fig.tight_layout(); fig.savefig(os.path.join(AQUI, '09-corte-lateral.png'), dpi=130); plt.close(fig)

# ------------------------------------------------ figura 10: imanes
fig, ax = plt.subplots(figsize=(8.6, 7.6))
cl, ch, hx, hy = d['cl'], d['ch'], d['hx'], d['hy']
ax.add_patch(Rectangle((-d['L'] / 2, -d['Ho'] / 2), d['L'], d['Ho'], fc='#ECEBE7', ec=TINTA, lw=1))
c = P['tapa_chaflan']
ax.add_patch(MP([(-hx, -hy), (hx, -hy), (hx, hy - c), (hx - c, hy), (-hx, hy)], fc='white', ec=TINTA, lw=1))
def iman(x, y, n, txt, dx=7, dy=0):
    ax.add_patch(Circle((x, y), 2.5, fc=ROJO, ec=TINTA, lw=.8)); ax.text(x + dx, y + dy, '%s  %s' % (n, txt), fontsize=8.5, va='center', color=TINTA)
iman(0, 0, '1+1', 'iman central del panel + cubo de la aguja', dx=7, dy=4)
iman(0, -P['rotor_radio_iman'], '1+1', 'iman del rotor + pala de la aguja')
iman(-d['mx'], d['my'], '1+1', 'esquina: panel + caja (embutidos)')
iman(d['mx'], -d['my'], '1+1', 'esquina: panel + caja (embutidos)', dx=-66, dy=7)
ax.text(0, -d['Ho'] / 2 - 7, 'Total 8 imanes de 5 × 1,6 mm. Con una aguja de repuesto, 10. Quedan 4 de los 14.', ha='center', fontsize=9.5, color=TINTA)
ax.set_xlim(-d['L'] / 2 - 4, d['L'] / 2 + 4); ax.set_ylim(-d['Ho'] / 2 - 12, d['Ho'] / 2 + 4); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Mapa de imanes (vista de frente). Ninguno queda a la vista.', fontsize=10, color=TINTA)
fig.tight_layout(); fig.savefig(os.path.join(AQUI, '10-mapa-de-imanes.png'), dpi=130); plt.close(fig)

# ------------------------------------------------ numeros para el texto
out = []
ga, gc, ge = P['aguja_suelo'] + P['tapa_piel'] + 0.2, P['aguja_suelo'] + P['tapa_piel'] + P['iman_central_retiro'], 2 * P['iman_cubierta']
fa, fc_, fe = fuerza(ga)[0], fuerza(gc)[0], fuerza(ge)[0]
lat = max((fuerza(ga, x)[1], x) for x in np.arange(0.5, 5.01, 0.25)); ax_l = fuerza(ga, lat[1])[0]
rm = P['rotor_radio_iman']
tt = np.radians(np.linspace(0, 360 * P['muelle_vueltas'], 2000)); rr = np.linspace(P['cubo_radio'], P['muelle_radio_ext'] - P['muelle_grosor'] / 2, 2000)
Lm = float(np.sum(np.hypot(np.diff(rr), rr[:-1] * np.diff(tt)))) - 6.0
def par_muelle(t, E=3000.0): return E * P['muelle_alto'] * t ** 3 / 12 * math.radians(P['rotor_giro']) / Lm
def H(dist):
    R_, h_ = P['iman_d'] / 2, P['iman_h']; z = dist - h_ / 2
    return 1.2 / 2 * ((z + h_) / math.hypot(z + h_, R_) - z / math.hypot(z, R_)) / (4e-7 * math.pi)
ymov, zmov = an(0, -gr / 2); yim = -Do / 2 + P['tapa_piel'] + P['iman_central_retiro'] + P['iman_h'] / 2
dc = math.hypot(ymov - yim, zmov - d['zp']); dag = dc + P['tapa_piel'] + P['iman_central_retiro'] + P['aguja_suelo'] + P['iman_h']
out += ['separacion aguja-rotor %.1f mm -> atraccion %.2f N | aguja-central %.1f mm -> %.2f N | esquinas %.1f mm -> %.2f N cada una, %.1f N las dos (hasta %.1f N si los imanes se acercan 0,2 mm en su alojamiento)' % (ga, fa, gc, fc_, ge, fe, 2 * fe, 2 * fuerza(ge - 0.4)[0]),
        'arrastre lateral maximo %.2f N con %.2f mm de desfase (atraccion ahi %.2f N) -> par %.1f mN·m en un brazo de %.0f mm; rozamiento del rotor en ese punto (mu 0,3) %.1f mN·m; quedan %.1f' % (lat[0], lat[1], ax_l, lat[0] * rm, rm, 0.3 * ax_l * rm, lat[0] * rm - 0.3 * ax_l * rm),
        'rozamiento que sujeta la aguja girada (mu 0,3): %.1f mN·m' % (0.3 * fa * rm + 0.3 * fc_ * 3.0),
        'espiral: largo util %.0f mm; par a %d grados con E = 3000 MPa: %s; deformacion maxima %.2f %%' % (Lm, P['rotor_giro'], ', '.join('%.2f mm -> %.2f mN·m' % (t, par_muelle(t)) for t in (0.45, 0.6, 0.8)), 100 * P['muelle_grosor'] * math.radians(P['rotor_giro']) / (2 * Lm)),
        'campo en el centro del movimiento: iman central a %.1f mm -> %.0f A/m (limite ISO 764: 4800, %.1f veces por debajo); con la aguja puesta %.0f A/m (%.1f veces por debajo)' % (dc, H(dc), 4800 / H(dc), H(dc) + H(dag), 4800 / (H(dc) + H(dag))),
        'enganche: %.2f mm a 0 grados; por encima de 1 mm entre %.1f y %.1f grados; resbalon %.1f, apertura %.1f' % (enganche(0), min(fiable), max(fiable), math.degrees(d['ts']), math.degrees(d['tk'])),
        'exterior con funda %.1f x %.1f x %.1f mm = %.0f cm3 (v2: 98.1 x 92.2 x 83.4 = %.0f cm3)' % (2 * d['Xo'], 2 * d['Yo'], d['Zo'], 4 * d["Xo"] * d["Yo"] * d["Zo"] / 1000, 98.1 * 92.2 * 83.4 / 1000)]
for b in (160, 170, 180, 190, 200):
    stn = (b - 2 * math.pi * R) / 2
    out.append('brazalete de %d mm: alto interior necesario %.1f mm, fondo %.1f mm -> exterior con funda %.1f x %.1f x %.1f' % (b, P['soporte_pie'] + 2 * R + stn * math.cos(d['t']) + bz + P['aire_arriba'],
        P['nicho_fondo'] + (stn - d['st_nom']) * math.sin(d['t']), 2 * d['Xo'], 2 * d['Yo'] + (stn - d['st_nom']) * math.sin(d['t']), d['Zo'] + (stn - d['st_nom']) * math.cos(d['t'])))
open(os.path.join(AQUI, 'calculos-v3.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('\n'.join(out))
