# Eventually, la caja: generador del prototipo v2 (caja-expositor) para Autodesk Fusion.
# Se ejecuta dentro de Fusion (API de Python). Crea los parametros de usuario y
# reconstruye todos los componentes desde cero. Todas las medidas salen de P_DEF.
# Necesita frase.json en la misma carpeta (contornos de la frase en Reenie Beanie).
#
# Ejes del modelo: X = ancho (la funda abre por +X), Y = fondo (el frente es -Y),
# Z = alto (el suelo de la caja esta en Z = 0).
# La caja se modela primero tumbada, en un sistema local ("L") igual al de la v1:
# x = ancho, yL = alto, zL = del fondo (0) al frente. M_L() la pone de pie.
import adsk.core as C, adsk.fusion as F, math, json, os

CARPETA = os.path.dirname(os.path.abspath(globals().get('__file__', '.')))
K = 0.1
P = {}
P_DEF = [
('reloj_diametro','mm','40 mm','Caja del reloj sin corona (ficha del vendedor)'),
('reloj_grosor','mm','11 mm','Del cristal a la tapa trasera (ficha del vendedor)'),
('reloj_asa_asa','mm','44 mm','De asa a asa (ficha del vendedor)'),
('reloj_ancho_corona','mm','43.5 mm','SUPUESTO: ancho total con corona. Medir'),
('brazalete_ancho','mm','27 mm','SUPUESTO: ancho del brazalete junto a la caja. Medir'),
('brazalete_grosor','mm','3.5 mm','SUPUESTO: grosor del brazalete. Medir'),
('tarjeta_largo','mm','85 mm','Tarjeta de autenticidad'),
('tarjeta_ancho','mm','55 mm','Tarjeta de autenticidad'),
('tarjeta_grosor','mm','0.5 mm','Cartulina de 300-350 g'),
('iman_d','mm','5 mm','Diametro del iman'),
('iman_h','mm','1.6 mm','Altura del iman'),
('iman_aloj_d','mm','iman_d + 0.15 mm','Alojamiento a presion'),
('iman_aloj_h','mm','iman_h + 0.2 mm','Fondo del alojamiento'),
('iman_retiro','mm','0.5 mm','Retiro extra de los imanes de esquina para suavizar el clic'),
('nfc_d','mm','25 mm','Etiqueta NFC'),
('nfc_aloj_d','mm','nfc_d + 0.6 mm','Rebaje del NFC en el techo de la funda'),
('nfc_aloj_h','mm','0.5 mm','Fondo del rebaje del NFC'),
('nfc_y','mm','27 mm','v2: NFC hacia el fondo de la caja, lejos del reloj y de los imanes'),
('holg_desliza','mm','0.3 mm','Holgura por lado entre funda y caja'),
('holg_tapa','mm','0.2 mm','Holgura por lado entre tapa y caja'),
('holg_presion','mm','0.15 mm','Holgura para encajes a presion'),
('pared','mm','3 mm','Paredes laterales y fondo de la caja'),
('pared_techo','mm','3.4 mm','v2: techo y suelo de la caja: ranura del pestillo, rebaje e imanes del soporte'),
('pared_funda','mm','2 mm','Pared de la funda'),
('funda_fondo','mm','3.8 mm','v2: fondo cerrado de la funda: rebaje de aguja + imanes'),
('soporte_largo','mm','60 mm','SUPUESTO: eje largo del ovalo del soporte. Ajustar al brazalete'),
('soporte_alto','mm','46 mm','SUPUESTO: eje corto del ovalo del soporte'),
('soporte_ancho','mm','30 mm','Ancho del soporte (sentido de la muneca)'),
('soporte_inclinacion','deg','25 deg','v2: cuanto se recuesta la esfera hacia atras respecto a la vertical'),
('soporte_pared','mm','4 mm','Grosor del anillo del soporte'),
('soporte_pie','mm','4.5 mm','Altura libre bajo el anillo para el brazalete'),
('soporte_rebaje','mm','1.2 mm','v2: rebaje del suelo donde encajan los patines'),
('soporte_iman_retiro','mm','1.2 mm','v2: retiro de los imanes del soporte para que salga sin arrastrar la caja'),
('patin_ancho','mm','8 mm','Ancho de cada patin lateral del soporte'),
('patin_alto','mm','14 mm','Altura de los patines'),
('patin_frente','mm','34 mm','v2: del centro del anillo al frente del patin (bajo el reloj, para que no vuelque)'),
('patin_detras','mm','22 mm','v2: del centro del anillo a la trasera del patin'),
('aire_frente','mm','5 mm','v2: aire entre la tapa y el punto mas adelantado del reloj'),
('guia_tarjeta','mm','2.5 mm','v2: saliente de las guias en cuna que sujetan la tarjeta al fondo'),
('guia_alto','mm','45 mm','v2: altura de las guias de la tarjeta'),
('nicho_ancho','mm','tarjeta_largo + 3 mm','v2: ancho interior de la caja'),
('nicho_alto','mm','72 mm','v2: alto interior de la caja'),
('nicho_fondo','mm','80 mm','v2: fondo interior de la caja, de la tapa a la pared trasera'),
('tapa_piel','mm','1 mm','Piel sobre el mecanismo. Bajar a 0.8 si el iman no arrastra'),
('rotor_grosor','mm','2.2 mm','Grosor del rotor'),
('rotor_holg_axial','mm','0.3 mm','Juego del rotor'),
('rotor_ancho','mm','9 mm','Ancho de la barra del rotor'),
('rotor_giro','deg','40 deg','v2: giro entre cerrado y abierto'),
('rotor_radio_iman','mm','13.5 mm','v2: del centro al iman de arrastre (va en la cola de la aguja)'),
('rotor_enganche','mm','1.3 mm','Cuanto entra cada pestillo del rotor en techo y suelo'),
('rotor_radio','mm','nicho_alto / 2 + rotor_enganche','Radio del rotor, extremos redondeados'),
('pestillo_grosor','mm','1.2 mm','Grosor del pestillo en cada extremo del rotor'),
('tapeta_grosor','mm','1 mm','Grosor de la tapeta'),
('tapeta_largo','mm','62 mm','Largo de la tapeta'),
('tapa_alto','mm','tapa_piel + rotor_grosor + rotor_holg_axial + tapeta_grosor + 0.1 mm','Grosor de la tapa frontal, encastrada a ras'),
('refuerzo_esq','mm','8.5 mm','Refuerzo de esquina para los imanes de la tapa'),
('caja_ancho','mm','nicho_ancho + 2 * pared','v2: exterior de la caja'),
('caja_alto','mm','nicho_alto + 2 * pared_techo','v2: exterior de la caja'),
('caja_fondo','mm','pared + nicho_fondo + tapa_alto','v2: exterior de la caja, tapa incluida'),
('aguja_punta','mm','34 mm','v2: del centro a la punta'),
('aguja_grosor','mm','2.4 mm','v2: grosor de la aguja-llave (era 3.2)'),
('aguja_cubo_d','mm','9 mm','v2: diametro del cubo (era 12)'),
('aguja_pala_d','mm','8.6 mm','v2: diametro del disco de la cola, aloja el iman de arrastre'),
('aguja_varilla','mm','2 mm','v2: ancho de la varilla junto al cubo'),
('aguja_varilla_punta','mm','1.2 mm','v2: ancho de la varilla junto a la flecha'),
('aguja_flecha_largo','mm','10 mm','v2: largo de la punta de flecha calada'),
('aguja_flecha_ancho','mm','6.5 mm','v2: ancho de la punta de flecha'),
('aguja_flecha_pared','mm','1 mm','v2: grosor del contorno de la flecha'),
('aguja_rebaje','mm','1.4 mm','v2: profundidad del rebaje de la aguja en la funda'),
('funda_largo','mm','caja_ancho + holg_desliza + funda_fondo','Exterior de la funda (un extremo abierto)'),
('funda_ancho','mm','caja_fondo + 2 * holg_desliza + 2 * pared_funda','Exterior de la funda'),
('funda_alto','mm','caja_alto + 2 * holg_desliza + 2 * pared_funda','Exterior de la funda'),
('frase_fondo','mm','0.6 mm','Profundidad de la frase incrustada'),
('frase_trazo_min','mm','0.8 mm','Trazo minimo imprimible de la letra'),
('frase_margen','mm','11 mm','v2: margen de la frase desde la esquina superior izquierda del frente de la funda'),
]

def app(): return C.Application.get()
def des(): return F.Design.cast(app().activeProduct)
def T(): return F.TemporaryBRepManager.get()
def pt(x, y, z): return C.Point3D.create(x * K, y * K, z * K)
def vec(x, y, z): return C.Vector3D.create(x, y, z)

def load_params():
    ups = des().userParameters
    for name, unit, expr, com in P_DEF:
        u = ups.itemByName(name)
        if u is None:
            ups.add(name, C.ValueInput.createByString(expr), unit, com)
        else:
            u.expression = expr
            u.comment = com
    vivos = set(n for n, _, _, _ in P_DEF)
    for u in [u for u in ups if u.name not in vivos]:
        u.deleteMe()
    for name, unit, expr, com in P_DEF:
        v = ups.itemByName(name).value
        P[name] = math.degrees(v) if unit == 'deg' else v * 10.0
    return P

def box(x0, x1, y0, y1, z0, z1):
    o = C.OrientedBoundingBox3D.create(pt((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), vec(1, 0, 0), vec(0, 1, 0), abs(x1 - x0) * K, abs(y1 - y0) * K, abs(z1 - z0) * K)
    return T().createBox(o)

def cyl(a, b, r): return T().createCylinderOrCone(pt(*a), r * K, pt(*b), r * K)

def half(p0, n, S=600.0):
    L = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
    n = [c / L for c in n]
    a = [0.0, 0.0, 1.0] if abs(n[2]) < 0.9 else [1.0, 0.0, 0.0]
    w = [n[1] * a[2] - n[2] * a[1], n[2] * a[0] - n[0] * a[2], n[0] * a[1] - n[1] * a[0]]
    Lw = math.sqrt(w[0] ** 2 + w[1] ** 2 + w[2] ** 2)
    w = [c / Lw for c in w]
    c = [p0[i] + n[i] * S / 2 for i in range(3)]
    o = C.OrientedBoundingBox3D.create(pt(*c), vec(*n), vec(*w), S * K, S * K, S * K)
    return T().createBox(o)

def cut(a, b):
    T().booleanOperation(a, b, F.BooleanTypes.DifferenceBooleanType)
    return a
def join(a, b):
    T().booleanOperation(a, b, F.BooleanTypes.UnionBooleanType)
    return a
def inter(a, b):
    T().booleanOperation(a, b, F.BooleanTypes.IntersectionBooleanType)
    return a
def rotz(body, deg):
    m = C.Matrix3D.create()
    m.setToRotation(math.radians(deg), vec(0, 0, 1), pt(0, 0, 0))
    T().transform(body, m)
    return body
def pocket(x, y, z, dz): return cyl((x, y, z), (x, y, z + dz), P['iman_aloj_d'] / 2)

def put(name, body):
    root = des().rootComponent
    for o in [o for o in root.occurrences if o.component.name == name]:
        o.deleteMe()
    occ = root.occurrences.addNewComponent(C.Matrix3D.create())
    comp = occ.component
    comp.name = name
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    comp.bRepBodies.add(body, bf)
    bf.finishEdit()
    b = comp.bRepBodies.item(0)
    b.name = name
    return b

def D():
    p = P
    d = {}
    d['L'], d['Do'], d['Ho'] = p['caja_ancho'], p['caja_fondo'], p['caja_alto']
    d['cl'], d['ch'] = p['nicho_ancho'], p['nicho_alto']
    # sistema L (caja tumbada): zL = 0 en la cara exterior del fondo, zL = Do en el frente
    d['zs'] = d['Do'] - p['tapa_alto']
    d['ct'] = d['Do'] - p['tapa_piel']
    d['cb'] = d['ct'] - p['rotor_grosor'] - p['rotor_holg_axial']
    d['Rc'] = p['rotor_radio'] + 0.3
    d['mx'] = d['cl'] / 2 - 4.5
    d['my'] = d['ch'] / 2 - 4.5
    # mundo
    d['yF'] = -d['Do'] / 2 + p['tapa_alto']
    d['yB'] = d['Do'] / 2 - p['pared']
    d['zf'] = p['pared_techo']
    d['zp'] = d['Ho'] / 2
    t = math.radians(p['soporte_inclinacion'])
    R = p['soporte_alto'] / 2
    st = (p['soporte_largo'] - p['soporte_alto']) / 2
    d['t'], d['R'], d['st'] = t, R, st
    d['z0'] = d['zf'] - p['soporte_rebaje']
    d['zc'] = d['z0'] + p['soporte_pie'] + st * math.cos(t) + R
    d['yc'] = d['yF'] + p['aire_frente'] + (R + p['reloj_grosor']) * math.cos(t) + p['reloj_asa_asa'] / 2 * math.sin(t)
    d['xs'] = p['soporte_ancho'] / 2 + p['patin_ancho'] / 2
    d['ym'] = d['yc'] + (p['patin_detras'] - p['patin_frente']) / 2
    return d

def M_L():
    d = D()
    m = C.Matrix3D.create()
    m.setWithCoordinateSystem(pt(0, d['Do'] / 2, d['Ho'] / 2), vec(1, 0, 0), vec(0, 0, 1), vec(0, -1, 0))
    return m

def build_base():
    p = P
    d = D()
    L, Do, Ho, cl, ch = d['L'], d['Do'], d['Ho'], d['cl'], d['ch']
    b = box(-L / 2, L / 2, -Ho / 2, Ho / 2, 0, Do)
    cut(b, box(-cl / 2, cl / 2, -ch / 2, ch / 2, p['pared'], Do + 5))
    r = p['refuerzo_esq']
    dep = p['iman_aloj_h'] + p['iman_retiro']
    hb = dep + 1.2
    zs = d['zs']
    for sx in (1, -1):
        for sy in (1, -1):
            xa, xb = sorted((sx * (cl / 2 - r), sx * (cl / 2 + 0.5)))
            ya, yb = sorted((sy * (ch / 2 - r), sy * (ch / 2 + 0.5)))
            bo = box(xa, xb, ya, yb, zs - hb - 1.5 * r - 1, zs)
            inter(bo, half((sx * (cl / 2 - r), sy * (ch / 2 - r), zs - hb), (sx, sy, math.sqrt(2))))
            join(b, bo)
            cut(b, pocket(sx * d['mx'], sy * d['my'], zs + 0.01, -dep))
    zb = d['cb']
    cut(b, cyl((0, 0, zb - 0.2), (0, 0, zb + p['pestillo_grosor'] + p['rotor_holg_axial'] + 0.2), d['Rc']))
    T().transform(b, M_L())
    # --- a partir de aqui, en coordenadas del modelo (caja de pie) ---
    zf, yc, yB, zp = d['zf'], d['yc'], d['yB'], d['zp']
    sw, pw = p['soporte_ancho'] / 2, p['patin_ancho']
    rm = p['iman_aloj_d'] / 2
    for sx in (1, -1):
        xa, xb = sorted((sx * (sw - 0.3), sx * (sw + pw + 0.3)))
        cut(b, box(xa, xb, yc - p['patin_frente'] - 0.3, yc + p['patin_detras'] + 0.3, d['z0'], zf + 1))
        cut(b, cyl((sx * d['xs'], d['ym'], d['z0'] + 0.01), (sx * d['xs'], d['ym'], d['z0'] - p['iman_aloj_h']), rm))
    g = p['guia_tarjeta']
    for sx in (1, -1):
        xw = sx * cl / 2
        xa, xb = sorted((xw - sx * g, xw + sx * 0.5))
        gu = box(xa, xb, yB - 2 * g - 0.6, yB - 0.6, zf - 0.5, zf + p['guia_alto'])
        inter(gu, half((xw, yB - 0.6, 0), (sx, -1, 0)))
        inter(gu, half((xw - sx * g, yB - 0.6 - g, 0), (sx, 1, 0)))
        join(b, gu)
    for sx in (1, -1):
        for sz in (1, -1):
            cut(b, cyl((sx * d['mx'], Do / 2 + 0.01, zp + sz * d['my']), (sx * d['mx'], Do / 2 - p['iman_aloj_h'], zp + sz * d['my']), rm))
    for dz in (0.0, -p['rotor_radio_iman']):
        cut(b, cyl((-L / 2 - 0.01, 0, zp + dz), (-L / 2 + p['iman_aloj_h'] + 0.3, 0, zp + dz), rm))
    cut(b, cyl((-L / 2 - 1, -Do / 2 - 2.5, zp), (-cl / 2 + 0.01, -Do / 2 - 2.5, zp), 9))
    return b

def chamber(z0, z1):
    p = P
    d = D()
    hw = p['rotor_ancho'] / 2 + 0.3
    g = math.radians(p['rotor_giro'])
    lx, ly = math.cos(g), -math.sin(g)
    wp = half((-hw, 0, 0), (1, 0, 0))
    inter(wp, half((hw * lx, hw * ly, 0), (-lx, -ly, 0)))
    wn = half((hw, 0, 0), (-1, 0, 0))
    inter(wn, half((-hw * lx, -hw * ly, 0), (lx, ly, 0)))
    join(wp, wn)
    c = cyl((0, 0, z0), (0, 0, z1), d['Rc'])
    inter(c, wp)
    join(c, cyl((0, 0, z0), (0, 0, z1), 7.3))
    cut(c, cyl((0, 0, z0 - 1), (0, 0, z1 + 1), 4.0))
    return c

def tapa_L():
    p = P
    d = D()
    hx = d['cl'] / 2 - p['holg_tapa']
    hy = d['ch'] / 2 - p['holg_tapa']
    Do, zs = d['Do'], d['zs']
    t = box(-hx, hx, -hy, hy, zs, Do)
    cut(t, chamber(d['cb'], d['ct']))
    cut(t, cyl((0, 0, d['cb'] - 0.01), (0, 0, d['ct']), p['iman_aloj_d'] / 2))
    tl = p['tapeta_largo'] / 2 + p['holg_presion']
    cut(t, box(-tl, tl, -hy - 1, hy + 1, zs - 1, d['cb']))
    for sx in (1, -1):
        for sy in (1, -1):
            cut(t, pocket(sx * d['mx'], sy * d['my'], zs - 0.01, p['iman_aloj_h'] + p['iman_retiro']))
    return t

def tapeta_L():
    p = P
    d = D()
    hy = d['ch'] / 2 - p['holg_tapa']
    tl = p['tapeta_largo'] / 2
    return box(-tl, tl, -hy, hy, d['cb'] - p['tapeta_grosor'], d['cb'])

def rotor_L(ang=0.0):
    p = P
    d = D()
    zb = d['cb']
    zt = zb + p['rotor_grosor']
    R = p['rotor_radio']
    hw = p['rotor_ancho'] / 2
    r = box(-hw, hw, -R - 2, R + 2, zb, zt)
    inter(r, cyl((0, 0, zb - 1), (0, 0, zt + 1), R))
    join(r, cyl((0, 0, zb), (0, 0, zt), 7.0))
    cut(r, cyl((0, 0, zb - 1), (0, 0, zt + 1), 4.3))
    ring = box(-R - 5, R + 5, -R - 5, R + 5, zb + p['pestillo_grosor'], zt + 1)
    cut(ring, cyl((0, 0, zb - 1), (0, 0, zt + 2), d['ch'] / 2 - 0.7))
    cut(r, ring)
    rm = p['rotor_radio_iman']
    cut(r, cyl((0, -rm, zt - p['iman_aloj_h']), (0, -rm, zt + 1), p['iman_aloj_d'] / 2))
    if ang:
        rotz(r, -ang)
    return r

def al_mundo(body):
    T().transform(body, M_L())
    return body
def build_tapa(): return al_mundo(tapa_L())
def build_tapeta(): return al_mundo(tapeta_L())
def build_rotor(): return al_mundo(rotor_L())

def flecha(u0, off, t, zb=0.0):
    p = P
    pu, fl, fw = p['aguja_punta'], p['aguja_flecha_largo'], p['aguja_flecha_ancho']
    b = box(u0, pu + 8, -fw / 2 - 3, fw / 2 + 3, zb, zb + t)
    for s in (1, -1):
        nx, ny = fw / 2, s * fl
        ln = math.hypot(nx, ny)
        inter(b, half((pu + nx / ln * off, ny / ln * off, 0), (-nx, -ny, 0)))
    return b

def needle(off=0.0, t=None, real=True):
    # Local: u = eje de la aguja (punta hacia +u), v = ancho, w = grosor (imanes en w = 0)
    p = P
    t = t or p['aguja_grosor']
    pu, co = p['aguja_punta'], p['rotor_radio_iman']
    va, vp = p['aguja_varilla'], p['aguja_varilla_punta']
    fb = pu - p['aguja_flecha_largo']
    n = cyl((0, 0, 0), (0, 0, t), p['aguja_cubo_d'] / 2 + off)
    join(n, cyl((-co, 0, 0), (-co, 0, t), p['aguja_pala_d'] / 2 + off))
    join(n, box(-co, 0, -va / 2 - off, va / 2 + off, 0, t))
    sh = box(0, fb + 0.6, -va / 2 - off, va / 2 + off, 0, t)
    for s in (1, -1):
        nx, ny = (va - vp) / 2, s * fb
        ln = math.hypot(nx, ny)
        inter(sh, half((nx / ln * off, s * va / 2 + ny / ln * off, 0), (-nx, -ny, 0)))
    join(n, sh)
    join(n, flecha(fb - off, off, t))
    if real:
        cut(n, flecha(fb + p['aguja_flecha_pared'], -p['aguja_flecha_pared'], t + 2, -1.0))
        cut(n, cyl((0, 0, -0.01), (0, 0, p['iman_aloj_h']), p['iman_aloj_d'] / 2))
        cut(n, cyl((-co, 0, -0.01), (-co, 0, p['iman_aloj_h']), p['iman_aloj_d'] / 2))
    return n

def m_store():
    # Aguja guardada en el fondo cerrado de la funda, con la punta hacia arriba
    p = P
    d = D()
    xo = -d['L'] / 2 - p['holg_desliza'] - p['funda_fondo']
    m = C.Matrix3D.create()
    m.setWithCoordinateSystem(pt(xo + p['aguja_rebaje'], 0, d['zp']), vec(0, 0, 1), vec(0, 1, 0), vec(-1, 0, 0))
    return m

def build_aguja():
    n = needle()
    T().transform(n, m_store())
    return n

def build_frase():
    # Devuelve un cuerpo con la frase, incrustada frase_fondo en la cara frontal de la funda
    p = P
    d = D()
    data = json.load(open(os.path.join(CARPETA, 'frase.json'), encoding='utf-8'))
    yo = d['Do'] / 2 + p['holg_desliza'] + p['pared_funda']
    xo = -d['L'] / 2 - p['holg_desliza'] - p['funda_fondo']
    ztop = d['Ho'] + p['holg_desliza'] + p['pared_funda']
    x0, z0 = xo + p['frase_margen'], ztop - p['frase_margen']
    ym = -yo + p['frase_fondo'] / 2
    root = des().rootComponent
    for o in [o for o in root.occurrences if o.component.name == '_frase_aux']:
        o.deleteMe()
    occ = root.occurrences.addNewComponent(C.Matrix3D.create())
    comp = occ.component
    comp.name = '_frase_aux'
    def wire(ring):
        pts = []
        for x, z in ring:
            q = (round(x0 + x, 4), round(z0 + z, 4))
            if not pts or q != pts[-1]:
                pts.append(q)
        if pts[0] == pts[-1]:
            pts.pop()
        p3 = [C.Point3D.create(x * K, ym * K, z * K) for x, z in pts]
        curves = [C.Line3D.create(p3[i], p3[(i + 1) % len(p3)]) for i in range(len(p3))]
        return T().createWireFromCurves(curves, False)[0]
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    for pol in data['poligonos']:
        comp.bRepBodies.add(T().createFaceFromPlanarWires([wire(pol['outer'])] + [wire(h) for h in pol['holes']]), bf)
    bf.finishEdit()
    caras = C.ObjectCollection.create()
    for b in comp.bRepBodies:
        caras.add(b.faces.item(0))
    inp = comp.features.extrudeFeatures.createInput(caras, F.FeatureOperations.NewBodyFeatureOperation)
    inp.setSymmetricExtent(C.ValueInput.createByReal(p['frase_fondo'] * K), True)
    feat = comp.features.extrudeFeatures.add(inp)
    ink = None
    for b in feat.bodies:
        c = T().copy(b)
        ink = c if ink is None else join(ink, c)
    occ.deleteMe()
    return ink

def build_funda(ink=None):
    p = P
    d = D()
    h, pf = p['holg_desliza'], p['pared_funda']
    L, Do, Ho, zp = d['L'], d['Do'], d['Ho'], d['zp']
    xi = -L / 2 - h
    xo = xi - p['funda_fondo']
    xa = L / 2
    yi = Do / 2 + h
    yo = yi + pf
    z0, z1 = -h, Ho + h
    rm = p['iman_aloj_d'] / 2
    f = box(xo, xa, -yo, yo, z0 - pf, z1 + pf)
    cut(f, box(xi, xa + 5, -yi, yi, z0, z1))
    for dz in (0.0, -p['rotor_radio_iman']):
        cut(f, cyl((xi + 0.01, 0, zp + dz), (xi - p['iman_aloj_h'], 0, zp + dz), rm))
    rec = needle(0.3, p['aguja_rebaje'] + 2, False)
    T().transform(rec, m_store())
    cut(f, rec)
    cut(f, cyl((xo - 1, 0, zp), (xo + p['aguja_rebaje'], 0, zp), 8.5))
    cut(f, cyl((0, p['nfc_y'], z1 - 0.01), (0, p['nfc_y'], z1 + p['nfc_aloj_h']), p['nfc_aloj_d'] / 2))
    cut(f, cyl((xa, 0, z0 - pf - 1), (xa, 0, z1 + pf + 1), 12))
    if ink is not None:
        cut(f, T().copy(ink))
    return f

def stadium(Rr, x0, x1):
    d = D()
    t, st, yc, zc = d['t'], d['st'], d['yc'], d['zc']
    a = (0.0, math.sin(t), math.cos(t))
    n = (0.0, -math.cos(t), math.sin(t))
    o = C.OrientedBoundingBox3D.create(pt((x0 + x1) / 2, yc, zc), vec(*a), vec(*n), 2 * st * K, 2 * Rr * K, abs(x1 - x0) * K)
    s = T().createBox(o)
    for sg in (1, -1):
        cy, cz = yc + sg * st * a[1], zc + sg * st * a[2]
        join(s, cyl((x0, cy, cz), (x1, cy, cz), Rr))
    return s

def build_soporte():
    p = P
    d = D()
    sw, pw, z0, yc = p['soporte_ancho'] / 2, p['patin_ancho'], d['z0'], d['yc']
    c = stadium(d['R'], -sw, sw)
    for sx in (1, -1):
        xa, xb = sorted((sx * (sw - 0.05), sx * (sw + pw)))
        pl = box(xa, xb, yc - p['patin_frente'], yc + p['patin_detras'], z0, z0 + p['patin_alto'])
        cut(pl, cyl((sx * d['xs'], d['ym'], z0 - 0.01), (sx * d['xs'], d['ym'], z0 + p['iman_aloj_h'] + p['soporte_iman_retiro']), p['iman_aloj_d'] / 2))
        join(c, pl)
    cut(c, stadium(d['R'] - p['soporte_pared'], -60, 60))
    return c

def build_reloj():
    p = P
    d = D()
    t, R, yc, zc = d['t'], d['R'], d['yc'], d['zc']
    n = (0.0, -math.cos(t), math.sin(t))
    a = (yc + R * n[1], zc + R * n[2])
    b = (yc + (R + p['reloj_grosor']) * n[1], zc + (R + p['reloj_grosor']) * n[2])
    return cyl((0, a[0], a[1]), (0, b[0], b[1]), p['reloj_diametro'] / 2)

def build_tarjeta():
    p = P
    d = D()
    return box(-p['tarjeta_largo'] / 2, p['tarjeta_largo'] / 2, d['yB'] - 0.6 - p['tarjeta_grosor'], d['yB'] - 0.6, d['zf'], d['zf'] + p['tarjeta_ancho'])

IMPRIMIBLES = ('base', 'tapa', 'tapeta', 'rotor', 'aguja', 'soporte', 'funda', 'frase')

def build_all():
    out = []
    ink = build_frase()
    partes = (('base', build_base()), ('tapa', build_tapa()), ('tapeta', build_tapeta()), ('rotor', build_rotor()),
              ('aguja', build_aguja()), ('soporte', build_soporte()), ('funda', build_funda(ink)), ('frase', ink),
              ('reloj_referencia', build_reloj()), ('tarjeta_referencia', build_tarjeta()))
    nombres = [n for n, _ in partes]
    root = des().rootComponent
    for o in [o for o in root.occurrences if o.component.name not in nombres]:
        o.deleteMe()
    for name, body in partes:
        b = put(name, body)
        bb = b.boundingBox
        out.append('%s: %.1f x %.1f x %.1f mm, %.1f cm3' % (name, (bb.maxPoint.x - bb.minPoint.x) * 10, (bb.maxPoint.y - bb.minPoint.y) * 10, (bb.maxPoint.z - bb.minPoint.z) * 10, b.volume))
    return out

def check():
    d = des()
    col = C.ObjectCollection.create()
    out = []
    for o in d.rootComponent.occurrences:
        col.add(o.bRepBodies.item(0))
    res = d.analyzeInterference(d.createInterferenceInput(col))
    for i in range(res.count):
        r = res.item(i)
        out.append('INTERFERENCIA %s / %s: %.2f mm3' % (r.entityOne.name, r.entityTwo.name, r.interferenceBody.volume * 1000))
    if not out:
        out.append('sin interferencias entre los %d cuerpos' % col.count)
    return out

def vol_inter(a, b):
    a = T().copy(a)
    try:
        T().booleanOperation(a, b, F.BooleanTypes.IntersectionBooleanType)
        return a.volume * 1000
    except Exception:
        return 0.0

def check_pestillo():
    # Tira de la tapa 3 mm hacia fuera con el rotor a varios angulos: > 0 significa bloqueada
    out = ['giro | rotor-tapa | rotor-caja | tirando 3 mm de la tapa (>0 = bloqueada)']
    base, tapa = build_base(), build_tapa()
    tira = C.Matrix3D.create()
    tira.translation = C.Vector3D.create(0, -0.3, 0)
    g = int(P['rotor_giro'])
    for ang in (-3, 0, 5, 10, 15, 20, 25, 30, g, g + 3):
        r = al_mundo(rotor_L(ang))
        r2 = T().copy(r)
        T().transform(r2, tira)
        out.append('%3d | %.3f | %.3f | %.2f' % (ang, vol_inter(r, tapa), vol_inter(r, base), vol_inter(r2, base)))
    return out

def colores():
    d = des()
    lib = app().materialLibraries.itemById('BA5EE55E-9982-449B-9D66-9F036540E140')
    def mk(pid, name, rgb):
        a = d.appearances.itemByName(name)
        if a is None:
            a = d.appearances.addByCopy(lib.appearances.itemById(pid), name)
        if rgb:
            for k in range(a.appearanceProperties.count):
                pr = a.appearanceProperties.item(k)
                if pr.objectType == C.ColorProperty.classType():
                    C.ColorProperty.cast(pr).value = C.Color.create(rgb[0], rgb[1], rgb[2], 255)
                    break
        return a
    papel = mk('Prism-127', 'Eventually - papel', (247, 246, 242))
    marmol = mk('Prism-127', 'Eventually - marmol blanco', (236, 235, 231))
    azul = mk('Prism-115', 'Eventually - tinta azul', (31, 63, 168))
    acero = mk('Prism-073', 'Eventually - acero (referencia)', None)
    mapa = {'funda': marmol, 'aguja': azul, 'frase': azul, 'reloj_referencia': acero}
    for o in d.rootComponent.occurrences:
        o.component.bRepBodies.item(0).appearance = mapa.get(o.component.name, papel)

def distancias():
    p = P
    d = D()
    t, R, yc, zc = d['t'], d['R'], d['yc'], d['zc']
    out = []
    # punto mas adelantado y mas alto del reloj (con asas)
    s, u = R + p['reloj_grosor'], p['reloj_asa_asa'] / 2
    y_front = yc - s * math.cos(t) - u * math.sin(t)
    z_top = zc + s * math.sin(t) + u * math.cos(t)
    y_back = yc + d['st'] * math.sin(t) + R + p['brazalete_grosor']
    out.append('reloj: frente a %.1f mm de la tapa | arriba a %.1f mm del techo | brazalete a %.1f mm de la pared trasera' % (y_front - d['yF'], d['zf'] + d['ch'] - z_top, d['yB'] - y_back))
    # centro del movimiento (a media altura de la caja del reloj) frente a los imanes de la tapa
    sm = R + p['reloj_grosor'] / 2
    ymov, zmov = yc - sm * math.cos(t), zc + sm * math.sin(t)
    yiman = -d['Do'] / 2 + p['tapa_piel'] + p['iman_h'] / 2
    for nombre, zi in (('central', d['zp']), ('del rotor', d['zp'] - p['rotor_radio_iman'])):
        out.append('iman %s de la tapa -> centro del movimiento: %.1f mm' % (nombre, math.hypot(ymov - yiman, zmov - zi)))
    out.append('iman central -> punto mas cercano del reloj (borde inferior del bisel): %.1f mm' % math.hypot((yc - s * math.cos(t) - p['reloj_diametro'] / 2 * math.sin(t)) - yiman, (zc + s * math.sin(t) - p['reloj_diametro'] / 2 * math.cos(t)) - d['zp']))
    out.append('rotor: radio %.1f, se libera al superar la mitad del alto de la tapa %.1f' % (p['rotor_radio'], d['ch'] / 2 - p['holg_tapa']))
    return out

def exportar(carpeta, sufijo):
    d = des()
    em = d.exportManager
    out = []
    f3d = os.path.join(carpeta, 'Eventually-caja-%s.f3d' % sufijo)
    em.execute(em.createFusionArchiveExportOptions(f3d))
    out.append(f3d)
    stp = os.path.join(carpeta, 'Eventually-caja-%s.step' % sufijo)
    em.execute(em.createSTEPExportOptions(stp))
    out.append(stp)
    sub = os.path.join(carpeta, 'imprimir-%s' % sufijo)
    if not os.path.isdir(sub):
        os.makedirs(sub)
    for o in d.rootComponent.occurrences:
        if o.component.name in IMPRIMIBLES:
            fn = os.path.join(sub, o.component.name + '.3mf')
            em.execute(em.createC3MFExportOptions(o, fn))
            out.append(fn)
    return out

def main():
    d = des()
    d.designIntent = F.DesignIntentTypes.HybridDesignIntentType
    p = load_params()
    out = ['parametros: %d' % len(p)]
    out += build_all()
    colores()
    out += check()
    out += check_pestillo()
    out += distancias()
    app().activeViewport.fit()
    return out
