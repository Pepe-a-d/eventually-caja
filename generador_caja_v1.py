# Eventually, la caja: generador del prototipo v1 para Autodesk Fusion.
# Se ejecuta dentro de Fusion (API de Python). Crea los parametros de usuario y
# reconstruye los ocho componentes desde cero. Todas las medidas salen de P_DEF.
# Unidades del script: milimetros y grados. Ejes: X = largo, Y = ancho, Z = alto.
# La funda abre por +X. El suelo de la base esta en Z = 0.
import adsk.core, adsk.fusion, sys, types

SRC = '''
import adsk.core as C, adsk.fusion as F, math
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
('iman_retiro','mm','0.5 mm','v1: retiro extra de los imanes de esquina para suavizar el clic'),
('nfc_d','mm','25 mm','Etiqueta NFC'),
('nfc_aloj_d','mm','nfc_d + 0.6 mm','Rebaje del NFC en el techo de la funda'),
('nfc_aloj_h','mm','0.5 mm','Fondo del rebaje del NFC'),
('nfc_desplaz','mm','22 mm','v1: NFC desplazado del centro para alejarlo del iman central (H7)'),
('holg_desliza','mm','0.3 mm','Holgura por lado entre funda y base'),
('holg_tapa','mm','0.2 mm','Holgura por lado entre tapa y base'),
('holg_presion','mm','0.15 mm','Holgura para encajes a presion'),
('pared','mm','3 mm','v1: pared de la base (era 2.4) para alojar la ranura del pestillo'),
('suelo','mm','3.4 mm','v1: suelo de la base (era 2.4): ranura de tarjeta + imanes del soporte'),
('pared_funda','mm','2 mm','Pared de la funda'),
('funda_fondo','mm','4.2 mm','v1: fondo cerrado de la funda: rebaje de aguja + iman (H4)'),
('soporte_largo','mm','60 mm','SUPUESTO: eje largo del ovalo del soporte. Ajustar al brazalete'),
('soporte_alto','mm','46 mm','SUPUESTO: eje corto del ovalo del soporte'),
('soporte_ancho','mm','30 mm','Ancho del soporte (sentido de la muneca)'),
('soporte_inclinacion','deg','25 deg','Inclinacion de la cara de apoyo para la mesilla'),
('soporte_pared','mm','4 mm','v1: grosor del anillo del soporte'),
('soporte_pie','mm','4.5 mm','v1: altura libre bajo el ovalo para el cierre del brazalete'),
('patin_ancho','mm','8 mm','v1: ancho de cada patin lateral del soporte'),
('patin_alto','mm','12 mm','v1: altura de los patines'),
('patin_atras','mm','22 mm','v1: del centro al extremo trasero del patin'),
('patin_delante','mm','30 mm','v1: del centro al extremo delantero del patin'),
('patin_quiebro','mm','8 mm','v1: donde empieza la cara inclinada'),
('aire_reloj','mm','12 mm','v1: aire entre cristal y tapa (era 7.5) para alejar imanes y NFC (H7, H8)'),
('cav_largo','mm','tarjeta_largo + 3 mm','Cavidad interior de la base'),
('cav_ancho','mm','tarjeta_ancho + 3 mm','Cavidad interior de la base'),
('cav_alto','mm','soporte_pie + soporte_alto + reloj_grosor + aire_reloj','v1: altura libre bajo la tapa'),
('ranura_tarjeta_h','mm','1.2 mm','Fondo de la ranura de la tarjeta'),
('tapa_piel','mm','1 mm','Piel sobre el mecanismo. Bajar a 0.8 si el iman no arrastra'),
('rotor_grosor','mm','2.2 mm','Grosor del rotor'),
('rotor_holg_axial','mm','0.3 mm','Juego vertical del rotor'),
('rotor_ancho','mm','9 mm','Ancho de la barra del rotor'),
('rotor_giro','deg','60 deg','Giro entre cerrado y abierto'),
('rotor_radio_iman','mm','20 mm','Distancia del centro al iman de arrastre'),
('rotor_enganche','mm','1.3 mm','v1: cuanto entra cada pestillo del rotor en la pared'),
('rotor_radio','mm','cav_ancho / 2 + rotor_enganche','v1: radio del rotor, extremos redondeados (H10)'),
('pestillo_grosor','mm','1.2 mm','v1: grosor del pestillo en cada extremo del rotor'),
('tapeta_grosor','mm','1 mm','v1: grosor de la tapeta'),
('tapeta_largo','mm','62 mm','v1: largo de la tapeta'),
('tapa_alto','mm','tapa_piel + rotor_grosor + rotor_holg_axial + tapeta_grosor + 0.1 mm','v1: tapa encastrada a ras del borde (H6)'),
('refuerzo_esq','mm','8.5 mm','v1: refuerzo de esquina para los imanes de la tapa (H3)'),
('base_largo','mm','cav_largo + 2 * pared','Exterior de la base'),
('base_ancho','mm','cav_ancho + 2 * pared','Exterior de la base'),
('base_alto','mm','suelo + cav_alto + tapa_alto','v1: exterior de la base, tapa incluida'),
('aguja_punta','mm','30 mm','Del centro a la punta'),
('aguja_cola','mm','14 mm','Del centro al final del contrapeso'),
('aguja_grosor','mm','3.2 mm','Grosor de la aguja-llave'),
('aguja_cubo_d','mm','12 mm','Diametro del cubo'),
('aguja_varilla','mm','2.4 mm','Ancho de la varilla'),
('aguja_flecha_ini','mm','13 mm','v1: del centro al inicio de la punta de flecha (H5)'),
('aguja_flecha_ancho','mm','13 mm','v1: ancho de la base de la flecha, aloja el iman de arrastre (H5)'),
('aguja_rebaje','mm','2 mm','v1: profundidad del rebaje de la aguja en la funda'),
('funda_largo','mm','base_largo + holg_desliza + funda_fondo','Exterior de la funda (un extremo abierto)'),
('funda_ancho','mm','base_ancho + 2 * holg_desliza + 2 * pared_funda','Exterior de la funda'),
('funda_alto','mm','base_alto + 2 * holg_desliza + 2 * pared_funda','Exterior de la funda'),
('frase_fondo','mm','0.6 mm','Profundidad de la frase incrustada'),
('frase_trazo_min','mm','0.8 mm','Trazo minimo imprimible de la letra'),
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
    for name, unit, expr, com in P_DEF:
        v = ups.itemByName(name).value
        P[name] = math.degrees(v) if unit == 'deg' else v * 10.0
    return P

def box(x0, x1, y0, y1, z0, z1):
    o = C.OrientedBoundingBox3D.create(pt((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), vec(1, 0, 0), vec(0, 1, 0), abs(x1 - x0) * K, abs(y1 - y0) * K, abs(z1 - z0) * K)
    return T().createBox(o)

def cyl(a, b, r): return T().createCylinderOrCone(pt(*a), r * K, pt(*b), r * K)

def half(p0, n, S=500.0):
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
    d['L'], d['W'], d['H'] = p['base_largo'], p['base_ancho'], p['base_alto']
    d['cl'], d['cw'] = p['cav_largo'], p['cav_ancho']
    d['zs'] = p['base_alto'] - p['tapa_alto']
    d['ct'] = p['base_alto'] - p['tapa_piel']
    d['cb'] = d['ct'] - p['rotor_grosor'] - p['rotor_holg_axial']
    d['Rc'] = p['rotor_radio'] + 0.3
    d['mx'] = p['cav_largo'] / 2 - 4.5
    d['my'] = p['cav_ancho'] / 2 - 4.5
    d['z0s'] = p['suelo'] - p['ranura_tarjeta_h'] + p['tarjeta_grosor']
    d['sy'] = p['soporte_ancho'] / 2 + p['patin_ancho'] / 2
    d['sx'] = (p['patin_quiebro'] - p['patin_atras']) / 2
    d['zc'] = p['base_alto'] / 2
    return d

def build_base():
    p = P
    d = D()
    L, W, H, cl, cw, s = d['L'], d['W'], d['H'], d['cl'], d['cw'], p['suelo']
    b = box(-L / 2, L / 2, -W / 2, W / 2, 0, H)
    cut(b, box(-cl / 2, cl / 2, -cw / 2, cw / 2, s, H + 5))
    tl, tw = p['tarjeta_largo'] + 1, p['tarjeta_ancho'] + 1
    zr = s - p['ranura_tarjeta_h']
    cut(b, box(-tl / 2, tl / 2, -tw / 2, tw / 2, zr, s + 1))
    sc = cyl((30, cw / 2, 1.0), (30, cw / 2, s + 1), 9)
    inter(sc, box(-cl / 2, cl / 2, -cw / 2, cw / 2, 0, H))
    cut(b, sc)
    for sy in (1, -1):
        cut(b, pocket(d['sx'], sy * d['sy'], zr + 0.01, -p['iman_aloj_h']))
    r = p['refuerzo_esq']
    dep = p['iman_aloj_h'] + p['iman_retiro']
    hb = dep + 1.2
    zs = d['zs']
    for sx in (1, -1):
        for sy in (1, -1):
            xa, xb = sorted((sx * (cl / 2 - r), sx * (cl / 2 + 0.5)))
            ya, yb = sorted((sy * (cw / 2 - r), sy * (cw / 2 + 0.5)))
            bo = box(xa, xb, ya, yb, zs - hb - 1.5 * r - 1, zs)
            inter(bo, half((sx * (cl / 2 - r), sy * (cw / 2 - r), zs - hb), (sx, sy, math.sqrt(2))))
            join(b, bo)
            cut(b, pocket(sx * d['mx'], sy * d['my'], zs + 0.01, -dep))
    zb = d['cb']
    cut(b, cyl((0, 0, zb - 0.2), (0, 0, zb + p['pestillo_grosor'] + p['rotor_holg_axial'] + 0.2), d['Rc']))
    cut(b, cyl((-L / 2 - 0.01, 0, d['zc']), (-L / 2 + p['iman_aloj_h'] + 0.3, 0, d['zc']), p['iman_aloj_d'] / 2))
    cut(b, cyl((-L / 2 - 1, 0, H + 2.5), (-cl / 2 + 0.01, 0, H + 2.5), 9))
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

def build_tapa():
    p = P
    d = D()
    hx = d['cl'] / 2 - p['holg_tapa']
    hy = d['cw'] / 2 - p['holg_tapa']
    H, zs = d['H'], d['zs']
    t = box(-hx, hx, -hy, hy, zs, H)
    cut(t, chamber(d['cb'], d['ct']))
    cut(t, cyl((0, 0, d['cb'] - 0.01), (0, 0, d['ct']), p['iman_aloj_d'] / 2))
    tl = p['tapeta_largo'] / 2 + p['holg_presion']
    cut(t, box(-tl, tl, -hy - 1, hy + 1, zs - 1, d['cb']))
    for sx in (1, -1):
        for sy in (1, -1):
            cut(t, pocket(sx * d['mx'], sy * d['my'], zs - 0.01, p['iman_aloj_h'] + p['iman_retiro']))
    return t

def build_tapeta():
    p = P
    d = D()
    hy = d['cw'] / 2 - p['holg_tapa']
    tl = p['tapeta_largo'] / 2
    return box(-tl, tl, -hy, hy, d['cb'] - p['tapeta_grosor'], d['cb'])

def build_rotor(ang=0.0):
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
    cut(ring, cyl((0, 0, zb - 1), (0, 0, zt + 2), d['cw'] / 2 - 0.7))
    cut(r, ring)
    rm = p['rotor_radio_iman']
    cut(r, cyl((0, rm, zt - p['iman_aloj_h']), (0, rm, zt + 1), p['iman_aloj_d'] / 2))
    if ang:
        rotz(r, -ang)
    return r

def needle(off=0.0, t=None, pockets=True):
    p = P
    t = t or p['aguja_grosor']
    pu, co, fi, fw, va = p['aguja_punta'], p['aguja_cola'], p['aguja_flecha_ini'], p['aguja_flecha_ancho'], p['aguja_varilla']
    n = cyl((0, 0, 0), (0, 0, t), p['aguja_cubo_d'] / 2 + off)
    join(n, box(-(co - 5.5), fi + 1, -va / 2 - off, va / 2 + off, 0, t))
    join(n, box(-co - off, -(co - 5.5) + 0.5, -2.5 - off, 2.5 + off, 0, t))
    tri = box(fi - off, pu + 6, -fw / 2 - 3, fw / 2 + 3, 0, t)
    for s in (1, -1):
        nx, ny = fw / 2, s * (pu - fi)
        ln = math.hypot(nx, ny)
        inter(tri, half((pu + nx / ln * off, ny / ln * off, 0), (-nx, -ny, 0)))
    join(n, tri)
    if pockets:
        cut(n, cyl((0, 0, -0.01), (0, 0, p['iman_aloj_h']), p['iman_aloj_d'] / 2))
        cut(n, cyl((p['rotor_radio_iman'], 0, -0.01), (p['rotor_radio_iman'], 0, p['iman_aloj_h']), p['iman_aloj_d'] / 2))
    return n

def m_store():
    p = P
    d = D()
    xo = -d['L'] / 2 - p['holg_desliza'] - p['funda_fondo']
    m = C.Matrix3D.create()
    m.setWithCoordinateSystem(pt(xo + p['aguja_rebaje'], 0, d['zc']), vec(0, 0, 1), vec(0, 1, 0), vec(-1, 0, 0))
    return m

def build_aguja():
    n = needle()
    T().transform(n, m_store())
    return n

def build_funda():
    p = P
    d = D()
    h, pf = p['holg_desliza'], p['pared_funda']
    L, W, H = d['L'], d['W'], d['H']
    xi = -L / 2 - h
    xo = xi - p['funda_fondo']
    xa = L / 2
    yi = W / 2 + h
    yo = yi + pf
    z0, z1 = -h, H + h
    f = box(xo, xa, -yo, yo, z0 - pf, z1 + pf)
    cut(f, box(xi, xa + 5, -yi, yi, z0, z1))
    cut(f, cyl((xi + 0.01, 0, d['zc']), (xi - p['iman_aloj_h'], 0, d['zc']), p['iman_aloj_d'] / 2))
    rec = needle(0.3, p['aguja_rebaje'] + 2, False)
    T().transform(rec, m_store())
    cut(f, rec)
    cut(f, cyl((-p['nfc_desplaz'], 0, z1 - 0.01), (-p['nfc_desplaz'], 0, z1 + p['nfc_aloj_h']), p['nfc_aloj_d'] / 2))
    cut(f, cyl((xa, -yo - 1, d['zc']), (xa, yo + 1, d['zc']), 10))
    return f

def build_soporte():
    p = P
    d = D()
    z0 = d['z0s']
    R = p['soporte_alto'] / 2
    st = (p['soporte_largo'] - p['soporte_alto']) / 2
    sw = p['soporte_ancho'] / 2
    zc = z0 + p['soporte_pie'] + R
    a = math.radians(p['soporte_inclinacion'])
    c = box(-st, st, -sw, sw, zc - R, zc + R)
    for sx in (1, -1):
        join(c, cyl((sx * st, -sw, zc), (sx * st, sw, zc), R))
    for sy in (1, -1):
        ya, yb = sorted((sy * (sw - 0.05), sy * (sw + p['patin_ancho'])))
        pl = box(-p['patin_atras'], p['patin_delante'], ya, yb, z0, z0 + p['patin_alto'])
        inter(pl, half((p['patin_quiebro'], 0, z0), (-math.sin(a), 0, math.cos(a))))
        cut(pl, pocket(d['sx'], sy * d['sy'], z0 - 0.01, p['iman_aloj_h']))
        join(c, pl)
    Ri = R - p['soporte_pared']
    hole = box(-st, st, -60, 60, zc - Ri, zc + Ri)
    for sx in (1, -1):
        join(hole, cyl((sx * st, -60, zc), (sx * st, 60, zc), Ri))
    cut(c, hole)
    return c

def build_reloj():
    p = P
    d = D()
    z = d['z0s'] + p['soporte_pie'] + p['soporte_alto']
    w = cyl((0, 0, z), (0, 0, z + p['reloj_grosor']), p['reloj_diametro'] / 2)
    join(w, box(-2.5, 2.5, p['reloj_diametro'] / 2 - 1, p['reloj_ancho_corona'] - p['reloj_diametro'] / 2, z + 3.5, z + 7.5))
    return w

PARTS = (('base', build_base), ('tapa', build_tapa), ('tapeta', build_tapeta), ('rotor', build_rotor), ('aguja', build_aguja), ('soporte', build_soporte), ('funda', build_funda), ('reloj_referencia', build_reloj))

def build_all():
    out = []
    for name, fn in PARTS:
        b = put(name, fn())
        bb = b.boundingBox
        out.append('%s: %.1f x %.1f x %.1f mm, %.1f cm3' % (name, (bb.maxPoint.x - bb.minPoint.x) * 10, (bb.maxPoint.y - bb.minPoint.y) * 10, (bb.maxPoint.z - bb.minPoint.z) * 10, b.volume))
    return out

def check():
    d = des()
    root = d.rootComponent
    col = C.ObjectCollection.create()
    out = []
    for o in root.occurrences:
        col.add(o.bRepBodies.item(0))
    res = d.analyzeInterference(d.createInterferenceInput(col))
    for i in range(res.count):
        r = res.item(i)
        out.append('INTERFERENCIA %s / %s: %.2f mm3' % (r.entityOne.name, r.entityTwo.name, r.interferenceBody.volume * 1000))
    if not out:
        out.append('sin interferencias entre los %d cuerpos' % col.count)
    return out
'''

def run(_context: str):
    m = types.ModuleType('ev')
    exec(SRC, m.__dict__)
    sys.modules['ev'] = m
    design = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    # Un documento de pieza solo admite un componente: pasar a hibrido antes de crear nada.
    design.designIntent = adsk.fusion.DesignIntentTypes.HybridDesignIntentType
    p = m.load_params()
    print('parametros:', len(p))
    for line in m.build_all():
        print(line)
    for line in m.check():
        print(line)
