# Eventually, la caja: generador del prototipo v3 para Autodesk Fusion.
# Responde al contra-reporte de la v2 (contra-reporte-v2.md). Se ejecuta dentro de Fusion
# (API de Python). Crea los parametros de usuario y reconstruye todo desde cero.
# Todas las medidas salen de P_DEF. Necesita frase-v3.json en la misma carpeta.
#
# Ejes del modelo: X = ancho (+X es la derecha mirando la caja de frente), Y = fondo
# (el frente es -Y), Z = alto (la mesa esta en Z = 0).
# La caja se modela primero tumbada, en un sistema local "L": x = ancho, yL = alto,
# zL = del fondo (0) al frente (caja_fondo). M_L() la pone de pie.
# El reloj y la pinza usan un sistema inclinado (a, n): a sube por la cara plana de la
# pinza, n entra hacia atras. an() lo pasa a (Y, Z).
import adsk.core as C, adsk.fusion as F, math, json, os

CARPETA = os.path.dirname(os.path.abspath(globals().get('__file__', '.')))
K = 0.1          # mm -> cm (unidad interna de Fusion)
EPS = 0.01       # solape minimo para que los cortes no dejen caras coincidentes
GRANDE = 600.0   # tamano de los semiespacios de corte
PASO = 3.0       # grados entre puntos de los arcos poligonales
P = {}
P_DEF = [
# --- reloj: ficha del vendedor y supuestos a medir ---
('reloj_diametro','mm','40 mm','Caja del reloj sin corona (ficha del vendedor)'),
('reloj_grosor','mm','11 mm','Del cristal a la tapa trasera (ficha del vendedor)'),
('reloj_asa_asa','mm','44 mm','De asa a asa (ficha del vendedor)'),
('reloj_ancho_asas','mm','27 mm','SUPUESTO: ancho exterior de las asas. Medir'),
('reloj_corona_d','mm','6.5 mm','SUPUESTO: diametro de la corona. Medir'),
('reloj_corona_l','mm','3.5 mm','SUPUESTO: cuanto sobresale la corona. Medir'),
('brazalete_ancho','mm','22 mm','SUPUESTO: ancho del brazalete. Medir'),
('brazalete_grosor','mm','3.5 mm','SUPUESTO: grosor del brazalete. Medir'),
('brazalete_contorno','mm','180 mm','SUPUESTO: contorno interior del brazalete cerrado. MANDA en el tamano de la caja. Medir'),
('cierre_largo','mm','40 mm','SUPUESTO: largo del cierre plegado (solo reloj de referencia)'),
('cierre_ancho','mm','18 mm','SUPUESTO: ancho del cierre (solo reloj de referencia)'),
('cierre_grosor','mm','7 mm','SUPUESTO: grosor del cierre plegado (solo reloj de referencia)'),
# --- tarjeta, imanes, NFC ---
('tarjeta_largo','mm','85 mm','Tarjeta de autenticidad'),
('tarjeta_ancho','mm','55 mm','Tarjeta de autenticidad'),
('tarjeta_grosor','mm','0.5 mm','Cartulina de 300-350 g'),
('iman_d','mm','5 mm','Diametro del iman'),
('iman_h','mm','1.6 mm','Altura del iman'),
('iman_aloj_d','mm','iman_d + 0.15 mm','Alojamiento a presion. Ajustar con la probeta P0'),
('iman_aloj_h','mm','iman_h + 0.2 mm','Alto del alojamiento (9 capas de 0.2)'),
('iman_cubierta','mm','0.8 mm','Plastico que tapa los imanes de esquina (embutidos con pausa). Entre los dos dan 2 N de sujecion'),
('iman_central_retiro','mm','0.4 mm','I5: retiro del iman central respecto a la piel'),
('nfc_d','mm','25 mm','Etiqueta NFC'),
('nfc_aloj_d','mm','nfc_d + 0.6 mm','Rebaje del NFC bajo el techo de la funda'),
('nfc_aloj_h','mm','0.5 mm','Fondo del rebaje del NFC'),
# --- holguras (se confirman con la probeta P0) ---
('holg_desliza','mm','0.3 mm','Holgura por lado entre funda y caja (colchon de aire)'),
('holg_tapa','mm','0.2 mm','Holgura por lado del panel en la boca, y de la peana en su rebaje'),
('holg_presion','mm','0.15 mm','Holgura para encajes a presion (tapeta, ancla del muelle)'),
('holg_giro','mm','0.3 mm','Holgura lateral del rotor en su camara y en las ranuras'),
('holg_corte','mm','0.15 mm','Margen de las ranuras del pestillo hacia delante y hacia atras'),
('rotor_holg_eje','mm','0.15 mm','I10: juego radial del rotor en su eje'),
('rotor_holg_axial','mm','0.3 mm','Juego del rotor entre piel y tapeta'),
# --- paredes y redondeos ---
('pared','mm','3 mm','Paredes laterales y trasera de la caja'),
('pared_techo','mm','4 mm','Techo y suelo: ranura del pestillo, rebaje de la aguja y rebaje de la peana'),
('pared_funda','mm','2 mm','Pared de la funda de campana'),
('funda_techo','mm','2.4 mm','Techo de la funda: frase por fuera y NFC por dentro'),
('redondeo_ext','mm','1 mm','Punto 18: redondeo de las aristas exteriores'),
('redondeo_boca','mm','0.5 mm','Punto 18: canto matado de la boca (chaflan)'),
# --- pinza en C y peana (G1) ---
('soporte_inclinacion','deg','10 deg','Cuanto se recuesta la esfera hacia atras'),
('soporte_pie','mm','5 mm','Altura libre bajo la pinza para el brazalete'),
('pinza_radio','mm','15 mm','Radio exterior de los extremos de la pinza (pinza aplanada: 30 mm de grueso)'),
('pinza_cara','mm','43 mm','Largo de la cara plana rigida donde apoya la tapa trasera del reloj'),
('pinza_contorno_libre','mm','200 mm','Contorno de la pinza sin reloj. Vale para brazaletes de 160 a 200'),
('pinza_pared','mm','1.6 mm','Grosor del brazo elastico (PETG). Ajustar con la probeta P3'),
('pinza_pared_rigida','mm','3.2 mm','Grosor de la zona rigida: cara plana, base y talon'),
('pinza_talon','mm','8 mm','Largo del talon rigido por detras'),
('pinza_transicion','mm','6 mm','Tramo en que el grosor baja de rigido a elastico'),
('pinza_remeter','mm','5 mm','Cuanto se mete la punta del brazo por detras de la cara plana'),
('cuna_luz','mm','reloj_ancho_asas + 2 mm','Paso libre entre las dos cunas de la peana (brazalete y asas)'),
('cuna_apoyo','mm','3.5 mm','Lo que la pinza apoya en cada cuna'),
('pinza_ancho','mm','cuna_luz + 2 * cuna_apoyo','Ancho de la pinza (extrusion pura)'),
('cuna_pared','mm','2.2 mm','Pared exterior de cada cuna, que centra la pinza'),
('cuna_holgura','mm','0.3 mm','Holgura de la pinza en su cuna'),
('cuna_grosor','mm','3 mm','Grosor de la cuna alrededor de la pinza'),
('cuna_frente','mm','7 mm','Altura de la una delantera de la cuna (por debajo de la caja del reloj)'),
('cuna_detras','mm','8 mm','Altura de la una trasera de la cuna'),
('bandeja_ala','mm','4 mm','Ala de la peana a cada lado de las cunas'),
('bandeja_ancho','mm','pinza_ancho + 2 * cuna_holgura + 2 * cuna_pared + 2 * bandeja_ala','Ancho de la base de la peana'),
('bandeja_grosor','mm','2.4 mm','Grosor de la base de la peana, encastrada en el suelo'),
('bandeja_margen','mm','2 mm','Lo que la base sobresale por delante y por detras de las cunas'),
('bandeja_dientes','','4','Dientes del frente de la peana (la fijan sin imanes y se imprimen sin soportes)'),
('aire_frente','mm','3 mm','Aire entre los carriles de la tarjeta y el cristal del reloj'),
('aire_arriba','mm','3 mm','Aire entre el brazalete y el techo'),
('hueco_cierre','mm','8 mm','G1: hueco libre para el cierre detras de la pinza'),
('aire_detras','mm','1 mm','Aire entre el cierre y la pared trasera'),
# --- carriles de la tarjeta en el interior del panel (G5) ---
('carril_hueco','mm','tarjeta_grosor + 0.4 mm','Paso libre para la tarjeta'),
('carril_labio','mm','0.8 mm','Grosor del labio del carril'),
('carril_alto','mm','carril_hueco + carril_labio','Lo que sobresalen los carriles por detras del panel'),
('carril_solape','mm','1.2 mm','Lo que el labio pisa la tarjeta por cada lado'),
('carril_holgura','mm','0.3 mm','Holgura lateral de la tarjeta'),
('carril_largo','mm','46 mm','Largo de cada carril (la tarjeta asoma por arriba para cogerla)'),
('carril_tope','mm','1 mm','Tope recto bajo la tarjeta'),
('carril_tope_ancho','mm','6 mm','Ancho de cada tope'),
# --- interior y exterior de la caja ---
('nicho_ancho','mm','tarjeta_largo + 3 mm','Ancho interior: lo fija la tarjeta'),
('nicho_alto','mm','soporte_pie + 2 * pinza_radio + (brazalete_contorno - 2 * PI * pinza_radio) / 2 * cos(soporte_inclinacion) + brazalete_grosor + aire_arriba','Alto interior: lo fija el brazalete'),
('nicho_fondo','mm','carril_alto + aire_frente + reloj_diametro / 2 * sin(soporte_inclinacion) + reloj_grosor * cos(soporte_inclinacion) + 2 * pinza_radio * cos(soporte_inclinacion) + ((brazalete_contorno - 2 * PI * pinza_radio) / 2 - pinza_cara / 2) * sin(soporte_inclinacion) + hueco_cierre + aire_detras','Fondo interior, del panel a la pared trasera'),
# --- panel frontal y mecanismo (G2, G3, G4, I5, I10, I11) ---
('tapa_piel','mm','1.4 mm','I5: piel sobre el mecanismo, con relleno opaco'),
('rotor_grosor','mm','3 mm','Grosor del rotor'),
('tapeta_grosor','mm','1.2 mm','Grosor de la tapeta'),
('tapa_holg_tapeta','mm','0.1 mm','Lo que la tapeta queda hundida respecto a la cara trasera del panel'),
('tapa_alto','mm','tapa_piel + rotor_grosor + rotor_holg_axial + tapeta_grosor + tapa_holg_tapeta','Grosor del panel frontal'),
('rotor_ancho','mm','8 mm','Ancho de la barra del rotor'),
('rotor_giro','deg','50 deg','I10: giro de la aguja entre cerrado y abierto'),
('rotor_enganche','mm','2 mm','I10: cuanto entra cada pestillo en techo y suelo'),
('rotor_radio_iman','mm','16 mm','Del eje al iman de arrastre (y a la pala de la aguja)'),
('rotor_chaflan','mm','2.2 mm','G2: chaflan de resbalon en la cara de entrada de cada pestillo'),
('rotor_margen_tope','deg','1.5 deg','Giro de mas que deja la camara despues del resbalon'),
('eje_radio','mm','4 mm','Radio del eje del panel (hueco, con el iman central dentro)'),
('cubo_radio','mm','6 mm','Radio exterior del cubo del rotor'),
('muelle_grosor','mm','0.6 mm','G3: grosor de la espiral. Ajustar con la probeta P2 (0.45 / 0.6 / 0.8)'),
('muelle_alto','mm','1.6 mm','G3: alto de la espiral'),
('muelle_vueltas','','1.5','G3: vueltas de la espiral'),
('muelle_radio_ext','mm','11.6 mm','G3: radio exterior de la espiral'),
('muelle_holgura','mm','0.6 mm','Hueco entre la espiral y el alma del rotor (puente de impresion)'),
('rotor_alma','mm','rotor_grosor - muelle_alto - muelle_holgura','Grosor del alma que une cubo y brazos por encima de la espiral'),
('muelle_ancla_largo','mm','3.2 mm','Largo del taco que ancla la espiral al panel'),
('muelle_ancla_ancho','mm','3 mm','Ancho del taco de anclaje'),
('camara_muelle','mm','muelle_radio_ext + 0.8 mm','Radio de la camara de la espiral'),
('rotor_radio_brazo','mm','camara_muelle + 0.6 mm','Radio desde el que los brazos tienen todo el grosor'),
('tapeta_ancho','mm','40 mm','Ancho de la tapeta desmontable (cola de milano)'),
('tapeta_tope','mm','2 mm','Tope inferior de la tapeta'),
('refuerzo_esq','mm','8 mm','Refuerzos de esquina donde asienta el panel'),
('iman_esq_dist','mm','4.5 mm','Distancia de los imanes de esquina a las paredes'),
('tapa_chaflan','mm','6 mm','I11: esquina achaflanada del panel y de la boca'),
('labio_ancho','mm','34 mm','Zona central del suelo sin bisel, donde engancha el pestillo'),
('bisel','mm','3 mm','I1: bisel de apertura bajo el panel'),
('una_fondo','mm','1.2 mm','Ranura para la una en el canto inferior del panel'),
('una_ancho','mm','1.5 mm','Ancho de la ranura para la una'),
('una_dist','mm','2 mm','Distancia de la ranura al frente del panel'),
('emergencia_d','mm','1.5 mm','G4: taladro de emergencia en el techo'),
('emergencia_x','mm','3 mm','Posicion del taladro a la izquierda del eje, sobre el pico del pestillo'),
('caja_ancho','mm','nicho_ancho + 2 * pared','Exterior de la caja'),
('caja_alto','mm','nicho_alto + 2 * pared_techo','Exterior de la caja'),
('caja_fondo','mm','pared + nicho_fondo + tapa_alto','Exterior de la caja, panel incluido'),
# --- aguja-llave (G6, I6) ---
('aguja_punta','mm','34 mm','Del centro a la punta'),
('aguja_suelo','mm','0.4 mm','I6: plastico bajo los imanes de la aguja'),
('aguja_techo','mm','0.4 mm','I6: plastico sobre los imanes de la aguja'),
('aguja_grosor','mm','aguja_suelo + iman_aloj_h + aguja_techo','Grosor de la aguja'),
('aguja_cubo_d','mm','9 mm','Diametro del cubo'),
('aguja_pala_ancho','mm','8 mm','I6: ancho de la pala de la cola, con el iman dentro'),
('aguja_pala_cuello','mm','3.2 mm','I6: ancho de la pala junto al cubo'),
('aguja_varilla','mm','2.2 mm','Ancho de la varilla junto al cubo'),
('aguja_varilla_punta','mm','1.6 mm','I6: ancho minimo de la varilla'),
('aguja_flecha_largo','mm','10 mm','Largo de la punta de flecha calada'),
('aguja_flecha_ancho','mm','6.5 mm','Ancho de la punta de flecha'),
('aguja_flecha_pared','mm','1.2 mm','Grosor del contorno de la flecha'),
('aguja_rebaje_holg','mm','0.3 mm','G6: holgura del rebaje de la aguja en el techo de la caja'),
('aguja_rebaje_extra','mm','0.2 mm','G6: lo que la aguja queda bajo la superficie'),
('aguja_rebaje_x','mm','17 mm','G6: distancia del eje de la aguja guardada a la arista derecha de la caja'),
('aguja_una_d','mm','12 mm','G6: rebaje redondo para pellizcar la aguja'),
('aguja_una_u','mm','14 mm','G6: posicion del rebaje redondo a lo largo de la varilla'),
# --- funda de campana y frase (I3, I9) ---
('funda_ancho','mm','caja_ancho + 2 * holg_desliza + 2 * pared_funda','Exterior de la funda'),
('funda_fondo','mm','caja_fondo + 2 * holg_desliza + 2 * pared_funda','Exterior de la funda'),
('funda_alto','mm','caja_alto + holg_desliza + funda_techo','Exterior de la funda (abierta por abajo)'),
('frase_fondo','mm','0.6 mm','Profundidad de la frase: 3 capas de 0.2'),
('frase_margen','mm','14 mm','Del borde delantero del techo de la funda a la frase'),
]

# Probeta P0: valores que se prueban (no son parametros del modelo)
P0_ALOJAMIENTOS = (5.05, 5.10, 5.15, 5.20, 5.25, 5.30)
P0_HOLGURAS = (0.10, 0.15, 0.20, 0.25, 0.30, 0.35)
P0_PIELES = (0.8, 1.0, 1.2, 1.4)
P0_LLAVE = 6.0
P2_MUELLES = (('fino', 0.45), ('medio', 0.6), ('grueso', 0.8))

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
        P[name] = math.degrees(v) if unit == 'deg' else (v if unit == '' else v * 10.0)
    return P

# ---------------------------------------------------------------- primitivas
def box(x0, x1, y0, y1, z0, z1):
    o = C.OrientedBoundingBox3D.create(pt((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), vec(1, 0, 0), vec(0, 1, 0), abs(x1 - x0) * K, abs(y1 - y0) * K, abs(z1 - z0) * K)
    return T().createBox(o)

def cyl(a, b, r): return T().createCylinderOrCone(pt(*a), r * K, pt(*b), r * K)
def sph(c, r): return T().createSphere(pt(*c), r * K)

def half(p0, n, S=GRANDE):
    """Semiespacio: todo lo que queda del lado +n a partir del punto p0."""
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
def mover(body, dx, dy, dz):
    m = C.Matrix3D.create()
    m.translation = C.Vector3D.create(dx * K, dy * K, dz * K)
    T().transform(body, m)
    return body

def rbox(x0, x1, y0, y1, z0, z1, r):
    """Caja con las doce aristas redondeadas a radio r."""
    if r <= 0:
        return box(x0, x1, y0, y1, z0, z1)
    b = box(x0 + r, x1 - r, y0 + r, y1 - r, z0, z1)
    join(b, box(x0 + r, x1 - r, y0, y1, z0 + r, z1 - r))
    join(b, box(x0, x1, y0 + r, y1 - r, z0 + r, z1 - r))
    for x in (x0 + r, x1 - r):
        for y in (y0 + r, y1 - r):
            join(b, cyl((x, y, z0 + r), (x, y, z1 - r), r))
    for x in (x0 + r, x1 - r):
        for z in (z0 + r, z1 - r):
            join(b, cyl((x, y0 + r, z), (x, y1 - r, z), r))
    for y in (y0 + r, y1 - r):
        for z in (z0 + r, z1 - r):
            join(b, cyl((x0 + r, y, z), (x1 - r, y, z), r))
    for x in (x0 + r, x1 - r):
        for y in (y0 + r, y1 - r):
            for z in (z0 + r, z1 - r):
                join(b, sph((x, y, z), r))
    return b

def prisma(polys, eje, c0, c1):
    """Extruye poligonos planos. polys = [(contorno, [agujeros])] con puntos 2D.
    eje 'x': puntos (y, z); eje 'y': puntos (x, z); eje 'z': puntos (x, y). De c0 a c1 en ese eje."""
    cm = (c0 + c1) / 2.0
    def p3(a, b):
        if eje == 'x':
            return C.Point3D.create(cm * K, a * K, b * K)
        if eje == 'y':
            return C.Point3D.create(a * K, cm * K, b * K)
        return C.Point3D.create(a * K, b * K, cm * K)
    def wire(ring):
        pts = []
        for a, b in ring:
            q = (round(a, 4), round(b, 4))
            if not pts or q != pts[-1]:
                pts.append(q)
        if pts[0] == pts[-1]:
            pts.pop()
        q3 = [p3(a, b) for a, b in pts]
        return T().createWireFromCurves([C.Line3D.create(q3[i], q3[(i + 1) % len(q3)]) for i in range(len(q3))], False)[0]
    root = des().rootComponent
    occ = root.occurrences.addNewComponent(C.Matrix3D.create())
    comp = occ.component
    comp.name = '_aux'
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    for outer, holes in polys:
        comp.bRepBodies.add(T().createFaceFromPlanarWires([wire(outer)] + [wire(h) for h in holes]), bf)
    bf.finishEdit()
    caras = C.ObjectCollection.create()
    for b in comp.bRepBodies:
        caras.add(b.faces.item(0))
    inp = comp.features.extrudeFeatures.createInput(caras, F.FeatureOperations.NewBodyFeatureOperation)
    inp.setSymmetricExtent(C.ValueInput.createByReal(abs(c1 - c0) * K), True)
    feat = comp.features.extrudeFeatures.add(inp)
    out = None
    for b in feat.bodies:
        c = T().copy(b)
        out = c if out is None else join(out, c)
    occ.deleteMe()
    return out

def arco(ca, cb_, r, g0, g1):
    """Puntos de un arco. Angulo g medido desde el segundo eje hacia el primero:
    punto = (ca + r sen g, cb_ + r cos g)."""
    n = max(2, int(abs(g1 - g0) / PASO) + 1)
    return [(ca + r * math.sin(math.radians(g0 + (g1 - g0) * i / n)), cb_ + r * math.cos(math.radians(g0 + (g1 - g0) * i / n))) for i in range(n + 1)]

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

# ---------------------------------------------------------------- medidas derivadas
def D():
    p = P
    d = {}
    d['L'], d['Do'], d['Ho'] = p['caja_ancho'], p['caja_fondo'], p['caja_alto']
    d['cl'], d['ch'] = p['nicho_ancho'], p['nicho_alto']
    # sistema L (caja tumbada)
    d['zs'] = d['Do'] - p['tapa_alto']                       # cara trasera del panel
    d['ct'] = d['Do'] - p['tapa_piel']                       # cara interior de la piel
    d['cb'] = d['ct'] - p['rotor_grosor'] - p['rotor_holg_axial']   # fondo de la camara (cara de la tapeta)
    d['hx'] = d['cl'] / 2 - p['holg_tapa']
    d['hy'] = d['ch'] / 2 - p['holg_tapa']
    d['mx'] = d['cl'] / 2 - p['iman_esq_dist']
    d['my'] = d['ch'] / 2 - p['iman_esq_dist']
    # pestillo de resbalon: el pico del pestillo es la esquina izquierda de la barra
    hw = p['rotor_ancho'] / 2
    zA = d['ch'] / 2 + p['rotor_enganche']
    lo, hi = 0.0, math.radians(45)
    for _ in range(60):                                      # giro de resbalon: canto del pestillo a ras del panel
        mid = (lo + hi) / 2
        if d['hy'] + hw * math.sin(mid) < zA * math.cos(mid):
            lo = mid
        else:
            hi = mid
    d['hw'] = hw
    d['ts'] = (lo + hi) / 2                                  # giro de resbalon (rad), a izquierdas
    d['rA'] = math.hypot(hw, zA)                             # radio del pico
    d['phiA'] = math.atan2(hw, zA)
    d['tk'] = d['phiA'] + math.acos(d['hy'] / d['rA'])       # giro de apertura con la aguja (rad), a derechas
    d['Rc'] = d['rA'] + p['holg_giro']                       # radio de camara y ranuras
    d['lente'] = math.sqrt(max(d['Rc'] ** 2 - (d['ch'] / 2) ** 2, 0.0))
    d['a1'] = -(math.degrees(d['ts']) + p['rotor_margen_tope'])   # tope del lado del resbalon (grados)
    d['a2'] = p['rotor_giro']                                     # tope del lado de la aguja (grados)
    # mundo
    d['yF'] = -d['Do'] / 2 + p['tapa_alto']
    d['yB'] = d['Do'] / 2 - p['pared']
    d['zf'] = p['pared_techo']
    d['zp'] = d['Ho'] / 2
    # pinza: sistema (a, n) con origen O en el centro de la cara plana
    t = math.radians(p['soporte_inclinacion'])
    R, pl = p['pinza_radio'], p['pinza_cara']
    d['t'], d['R'], d['pl'] = t, R, pl
    d['st_nom'] = (p['brazalete_contorno'] - 2 * math.pi * R) / 2
    d['st_lib'] = (p['pinza_contorno_libre'] - 2 * math.pi * R) / 2
    d['ab'] = -pl / 2                                        # centro del arco inferior
    d['zO'] = d['zf'] + p['soporte_pie'] + R + pl / 2 * math.cos(t) + R * math.sin(t)
    d['yO'] = d['yF'] + p['carril_alto'] + p['aire_frente'] + p['reloj_diametro'] / 2 * math.sin(t) + p['reloj_grosor'] * math.cos(t)
    # peana
    yc, zc = an(d, d['ab'], R)
    d['ycu'], d['zcu'] = yc, zc                              # centro del arco de la cuna
    ro = R + p['cuna_holgura'] + p['cuna_grosor']
    d['ro'] = ro
    d['yt0'] = yc - ro - p['bandeja_margen']                 # frente de la base (sin dientes)
    d['yt1'] = yc + ro + p['bandeja_margen']                 # trasera de la base (arriba)
    d['xin'] = p['cuna_luz'] / 2
    d['xpz'] = p['pinza_ancho'] / 2 + p['cuna_holgura']
    d['xout'] = d['xpz'] + p['cuna_pared']
    # aguja guardada
    d['pala_fin'] = p['rotor_radio_iman'] + p['aguja_pala_ancho'] / 2
    d['xn'] = d['L'] / 2 - p['aguja_rebaje_x']               # la aguja va de atras adelante, con la punta hacia el frente
    d['yh'] = (p['aguja_punta'] - d['pala_fin']) / 2
    d['zr'] = d['Ho'] - p['aguja_grosor'] - p['aguja_rebaje_extra']
    # funda
    h, pf = p['holg_desliza'], p['pared_funda']
    d['Xi'], d['Yi'] = d['L'] / 2 + h, d['Do'] / 2 + h
    d['Xo'], d['Yo'] = d['Xi'] + pf, d['Yi'] + pf
    d['Zi'] = d['Ho'] + h
    d['Zo'] = d['Zi'] + p['funda_techo']
    return d

def an(d, a, n):
    """Del sistema inclinado de la pinza (a, n) a (Y, Z) del modelo."""
    t = d['t']
    return (d['yO'] + a * math.sin(t) + n * math.cos(t), d['zO'] + a * math.cos(t) - n * math.sin(t))

def M_L():
    d = D()
    m = C.Matrix3D.create()
    m.setWithCoordinateSystem(pt(0, d['Do'] / 2, d['Ho'] / 2), vec(1, 0, 0), vec(0, 0, 1), vec(0, -1, 0))
    return m

def al_mundo(body):
    T().transform(body, M_L())
    return body

# ---------------------------------------------------------------- caja
def build_base():
    p = P
    d = D()
    L, Do, Ho, cl, ch, zs = d['L'], d['Do'], d['Ho'], d['cl'], d['ch'], d['zs']
    re = p['redondeo_ext']
    b = rbox(-L / 2, L / 2, -Ho / 2 - 2 * re, Ho / 2, 0, Do, re)
    inter(b, half((0, -Ho / 2, 0), (0, 1, 0)))               # la arista de apoyo en la mesa queda viva
    cut(b, box(-cl / 2, cl / 2, -ch / 2, ch / 2, p['pared'], Do + 5))
    r = p['refuerzo_esq']
    hb = p['iman_cubierta'] + p['iman_aloj_h'] + 1.2
    for sx in (1, -1):
        for sy in (1, -1):
            xa, xb = sorted((sx * (cl / 2 - r), sx * (cl / 2 + 0.5)))
            ya, yb = sorted((sy * (ch / 2 - r), sy * (ch / 2 + 0.5)))
            bo = box(xa, xb, ya, yb, zs - hb - 1.5 * r - 1, zs)
            inter(bo, half((sx * (cl / 2 - r), sy * (ch / 2 - r), zs - hb), (sx, sy, math.sqrt(2))))
            join(b, bo)
    for sx, sy in ((-1, 1), (1, -1)):                        # imanes embutidos: arriba-izquierda y abajo-derecha
        z1 = zs - p['iman_cubierta']
        cut(b, cyl((sx * d['mx'], sy * d['my'], z1 - p['iman_aloj_h']), (sx * d['mx'], sy * d['my'], z1), p['iman_aloj_d'] / 2))
    # esquina achaflanada de la boca (arriba a la derecha): el panel solo entra al derecho
    c = p['tapa_chaflan']
    fill = box(cl / 2 - c - 1, cl / 2 + 0.5, ch / 2 - c - 1, ch / 2 + 0.5, zs, Do)
    k2 = d['hx'] + d['hy'] - c + p['holg_tapa'] * math.sqrt(2)
    inter(fill, half((k2 - ch / 2, ch / 2, 0), (1, 1, 0)))
    join(b, fill)
    # ranuras del pestillo en techo y suelo
    hc = p['holg_corte']
    ran = cyl((0, 0, d['cb'] - hc), (0, 0, d['ct'] + hc), d['Rc'])
    inter(ran, box(-d['lente'] - 0.5, d['lente'] + 0.5, -Ho, Ho, 0, Do))
    cut(b, ran)
    # canto matado de la boca
    rb = p['redondeo_boca']
    for sy in (1, -1):
        cu = box(-cl / 2, cl / 2, sy * ch / 2 - rb, sy * ch / 2 + rb, Do - rb, Do + EPS)
        inter(cu, half((0, sy * ch / 2, Do - rb), (0, -sy, 1)))
        cut(b, cu)
    for sx in (1, -1):
        cu = box(sx * cl / 2 - rb, sx * cl / 2 + rb, -ch / 2, ch / 2, Do - rb, Do + EPS)
        inter(cu, half((sx * cl / 2, 0, Do - rb), (-sx, 0, 1)))
        cut(b, cu)
    al_mundo(b)
    # --- a partir de aqui, en coordenadas del modelo (caja de pie) ---
    zf, zp = d['zf'], d['zp']
    # rebaje de la aguja en el techo, a ras, y rebaje redondo para pellizcarla
    rec = needle(p['aguja_rebaje_holg'], Ho, False)
    T().transform(rec, m_guardada())
    cut(b, rec)
    cut(b, cyl((d['xn'], d['yh'] - p['aguja_una_u'], d['zr']), (d['xn'], d['yh'] - p['aguja_una_u'], Ho + 1), p['aguja_una_d'] / 2))
    # taladro de emergencia sobre el pico del pestillo de arriba
    ye = Do / 2 - (d['cb'] + p['rotor_grosor'] / 2)
    cut(b, cyl((-p['emergencia_x'], ye, zf + ch - 1), (-p['emergencia_x'], ye, Ho + 1), p['emergencia_d'] / 2))
    # bisel de apertura bajo el panel, a los dos lados de la zona del pestillo
    bi = p['bisel']
    for sx in (1, -1):
        xa, xb = sorted((sx * p['labio_ancho'] / 2, sx * cl / 2))
        cu = box(xa, xb, -Do / 2 - 1, -Do / 2 + bi, zf - bi, zf + EPS)
        inter(cu, half((0, -Do / 2, zf - bi), (0, -1, 1)))
        cut(b, cu)
    cut(b, rebaje_peana())
    return b

def planta_peana(extra):
    """Planta (x, y) de la base de la peana: rectangulo con el frente en dientes de sierra.
    extra = holgura (0 para la pieza, holg_tapa para el rebaje del suelo)."""
    p = P
    d = D()
    w = p['bandeja_ancho'] / 2
    n = int(round(p['bandeja_dientes']))
    paso = 2 * w / n
    yv = d['yt0'] - extra * math.sqrt(2)
    yb = d['yt1'] + p['bandeja_grosor'] + 2 + extra
    pts = [(w + extra, yb), (w + extra, yv)]
    for i in range(n):
        x0 = w - i * paso
        pts.append((x0, yv))
        pts.append((x0 - paso / 2, yv - paso / 2))
    pts += [(-w, yv), (-w - extra, yv), (-w - extra, yb)]
    return pts

def rebaje_peana():
    p = P
    d = D()
    h, g = p['holg_tapa'], p['bandeja_grosor'] + p['holg_tapa']
    c = prisma([(planta_peana(h), [])], 'z', d['zf'] - g, d['zf'] + 1)
    # el fondo trasero entra a 45 grados por debajo del suelo: ahi se mete el talon de la base
    inter(c, half((0, d['yt1'] + h, d['zf']), (0, -1, -1)))
    return c

# ---------------------------------------------------------------- panel frontal
def camara(z0, z1):
    """Hueco del rotor dentro del panel (sistema L): barrido de los brazos, espiral y ancla."""
    p = P
    d = D()
    hwc = d['hw'] + p['holg_giro']
    def lados(a):
        g = math.radians(a)
        return (-math.cos(g), math.sin(g)), (math.cos(g), -math.sin(g))    # normal izquierda, normal derecha
    l1, _ = lados(d['a1'])
    _, r2 = lados(d['a2'])
    wp = half((hwc * l1[0], hwc * l1[1], 0), (-l1[0], -l1[1], 0))
    inter(wp, half((hwc * r2[0], hwc * r2[1], 0), (-r2[0], -r2[1], 0)))
    wn = half((-hwc * l1[0], -hwc * l1[1], 0), (l1[0], l1[1], 0))
    inter(wn, half((-hwc * r2[0], -hwc * r2[1], 0), (r2[0], r2[1], 0)))
    join(wp, wn)
    c = cyl((0, 0, z0), (0, 0, z1), d['Rc'])
    inter(c, wp)
    join(c, cyl((0, 0, z0), (0, 0, z1), p['camara_muelle']))
    xa = p['muelle_radio_ext'] + p['muelle_ancla_largo'] + p['holg_giro']
    ya = p['muelle_ancla_ancho'] / 2 + p['holg_presion']
    join(c, box(-xa, -p['camara_muelle'] + 1, -ya, ya, z0, z1))
    cut(c, cyl((0, 0, z0 - 1), (0, 0, z1 + 1), p['eje_radio']))
    return c

def tapa_L():
    p = P
    d = D()
    hx, hy, Do, zs, cb, ct = d['hx'], d['hy'], d['Do'], d['zs'], d['cb'], d['ct']
    t = box(-hx, hx, -hy, hy, zs, Do)
    inter(t, half((hx + hy - p['tapa_chaflan'] - hy, hy, 0), (-1, -1, 0)))       # esquina achaflanada
    cut(t, camara(zs - 1, ct))                               # abierta por detras: la cubren la tapeta y la tarjeta
    # iman central, dentro del eje, retirado de la piel
    cut(t, cyl((0, 0, cb - EPS), (0, 0, ct - p['iman_central_retiro']), p['iman_aloj_d'] / 2))
    # rebaje en cola de milano para la tapeta: entra por arriba y hace tope abajo
    tw, hp = p['tapeta_ancho'] / 2 + p['holg_presion'], cb - zs
    cut(t, prisma([([(-tw, zs - EPS), (tw, zs - EPS), (tw + hp, cb), (-tw - hp, cb)], [])], 'y', -hy + p['tapeta_tope'], hy + 1))
    # imanes de esquina embutidos
    for sx, sy in ((-1, 1), (1, -1)):
        z0 = zs + p['iman_cubierta']
        cut(t, cyl((sx * d['mx'], sy * d['my'], z0), (sx * d['mx'], sy * d['my'], z0 + p['iman_aloj_h']), p['iman_aloj_d'] / 2))
    # carriles en U para la tarjeta, con tope recto
    tl, ta = p['tarjeta_largo'] / 2, p['tarjeta_ancho'] / 2
    y0, y1 = -ta - p['carril_tope'], -ta + p['carril_largo']
    for sx in (1, -1):
        xa, xb = sorted((sx * (tl + p['carril_holgura']), sx * hx))
        join(t, box(xa, xb, y0, y1, zs - p['carril_alto'], zs + EPS))
        xa, xb = sorted((sx * (tl - p['carril_solape']), sx * hx))
        join(t, box(xa, xb, y0, y1, zs - p['carril_alto'], zs - p['carril_hueco']))
        xa, xb = sorted((sx * (tl - p['carril_tope_ancho']), sx * hx))
        join(t, box(xa, xb, y0, -ta, zs - p['carril_alto'], zs + EPS))
    # ranura para la una en el canto inferior
    cut(t, box(-hx - 1, hx + 1, -hy - 1, -hy + p['una_fondo'], Do - p['una_dist'] - p['una_ancho'], Do - p['una_dist']))
    return t

def tapeta_L():
    p = P
    d = D()
    hy, cb = d['hy'], d['cb']
    tw, g = p['tapeta_ancho'] / 2, p['tapeta_grosor']
    e = p['tapa_holg_tapeta']
    return prisma([([(-tw - e, cb - g), (tw + e, cb - g), (tw + e + g, cb), (-tw - e - g, cb)], [])], 'y', -hy + p['tapeta_tope'] + p['holg_tapa'], hy)

def espiral(grosor):
    """Contorno de la espiral del muelle (sistema L, plano del rotor). Acaba apuntando a -x."""
    p = P
    r0, r1 = p['cubo_radio'] - 0.4, p['muelle_radio_ext'] - grosor / 2
    tot = 360.0 * p['muelle_vueltas']
    n = int(tot / 4) + 1
    ext, itr = [], []
    for i in range(n + 1):
        f = i / n
        g = math.radians(180.0 - tot + tot * f)
        r = r0 + (r1 - r0) * f
        dr = (r1 - r0) / math.radians(tot)
        tx, ty = dr * math.cos(g) - r * math.sin(g), dr * math.sin(g) + r * math.cos(g)
        lt = math.hypot(tx, ty)
        nx, ny = ty / lt, -tx / lt                           # normal hacia fuera
        x, y = r * math.cos(g), r * math.sin(g)
        ext.append((x + nx * grosor / 2, y + ny * grosor / 2))
        itr.append((x - nx * grosor / 2, y - ny * grosor / 2))
    return ext + itr[::-1]

def rotor_L(ang=0.0, muelle=True, grosor=None):
    """Rotor en el sistema L. ang > 0 = giro a derechas visto de frente (el de la aguja)."""
    p = P
    d = D()
    zb = d['cb']
    zt = zb + p['rotor_grosor']
    hw, hy, rbz = d['hw'], d['hy'], p['rotor_radio_brazo']
    s, c = math.sin(d['ts']), math.cos(d['ts'])
    r = box(-hw, hw, rbz, d['rA'] + 3, zb, zt)
    join(r, box(-hw, hw, -d['rA'] - 3, -rbz, zb, zt))
    join(r, box(-hw, hw, -rbz - EPS, rbz + EPS, zb, zb + p['rotor_alma']))        # alma: puente sobre la espiral
    join(r, cyl((0, 0, zb), (0, 0, zt), p['cubo_radio']))
    cut(r, cyl((0, 0, zb - 1), (0, 0, zt + 1), p['eje_radio'] + p['rotor_holg_eje']))
    # pestillos: canto inclinado (queda a ras del panel al girar ts a izquierdas) y chaflan de resbalon
    ch = p['rotor_chaflan']
    inter(r, half((0, hy / c, 0), (-s, -c, 0)))
    inter(r, half((0, hy / c, zb + ch), (-s, -c, 1)))
    inter(r, half((0, -hy / c, 0), (s, c, 0)))
    inter(r, half((0, -hy / c, zb + ch), (s, c, 1)))
    # iman de arrastre en el brazo de abajo, abierto hacia la piel
    rm = p['rotor_radio_iman']
    cut(r, cyl((0, -rm, zt - p['iman_aloj_h']), (0, -rm, zt + 1), p['iman_aloj_d'] / 2))
    if muelle:
        g = grosor or p['muelle_grosor']
        join(r, prisma([(espiral(g), [])], 'z', zt - p['muelle_alto'], zt))
        x1 = p['muelle_radio_ext'] + p['muelle_ancla_largo']
        join(r, box(-x1, -p['muelle_radio_ext'] + g, -p['muelle_ancla_ancho'] / 2, p['muelle_ancla_ancho'] / 2, zt - p['muelle_alto'], zt))
    if ang:
        rotz(r, -ang)
    return r

def build_tapa(): return al_mundo(tapa_L())
def build_tapeta(): return al_mundo(tapeta_L())
def build_rotor(): return al_mundo(rotor_L())

# ---------------------------------------------------------------- aguja
def flecha(u0, off, t, zb=0.0):
    p = P
    pu, fl, fw = p['aguja_punta'], p['aguja_flecha_largo'], p['aguja_flecha_ancho']
    b = box(u0, pu + 8, -fw / 2 - 3, fw / 2 + 3, zb, zb + t)
    for s in (1, -1):
        nx, ny = fw / 2, s * fl
        ln = math.hypot(nx, ny)
        inter(b, half((pu + nx / ln * off, ny / ln * off, 0), (-nx, -ny, 0)))
    return b

def needle(off=0.0, t=None, real=True, prueba=False):
    """Aguja en local: u = eje (punta hacia +u), v = ancho, w = grosor. La cara w = 0 es la que toca el panel."""
    p = P
    t = t or p['aguja_grosor']
    pu, co = p['aguja_punta'], p['rotor_radio_iman']
    va, vp = p['aguja_varilla'], p['aguja_varilla_punta']
    pa, pc = p['aguja_pala_ancho'], p['aguja_pala_cuello']
    fb = pu - p['aguja_flecha_largo']
    n = cyl((0, 0, 0), (0, 0, t), p['aguja_cubo_d'] / 2 + off)
    # pala de la cola: se ensancha del cuello a la punta redonda, con el iman dentro
    join(n, cyl((-co, 0, 0), (-co, 0, t), pa / 2 + off))
    pal = box(-co, 0, -pa / 2 - off - 1, pa / 2 + off + 1, 0, t)
    for s in (1, -1):
        nx, ny = (pa - pc) / 2, s * co                       # el borde va de (0, s pc/2) a (-co, s pa/2)
        inter(pal, half((0, s * (pc / 2 + off), 0), (-nx, -ny, 0)))
    join(n, pal)
    # varilla: se afina del cubo a la flecha
    sh = box(0, fb + 0.6, -va / 2 - off, va / 2 + off, 0, t)
    for s in (1, -1):
        nx, ny = (va - vp) / 2, s * fb
        ln = math.hypot(nx, ny)
        inter(sh, half((nx / ln * off, s * va / 2 + ny / ln * off, 0), (-nx, -ny, 0)))
    join(n, sh)
    join(n, flecha(fb - off, off, t))
    if real:
        cut(n, flecha(fb + p['aguja_flecha_pared'], -p['aguja_flecha_pared'], t + 2, -1.0))
        z0 = p['aguja_suelo']
        for u in (0.0, -co):
            if prueba:                                       # probeta: imanes recuperables
                cut(n, cyl((u, 0, z0), (u, 0, t + 1), p['iman_aloj_d'] / 2))
                cut(n, cyl((u, 0, -1), (u, 0, z0 + EPS), p['emergencia_d'] / 2))
            else:                                            # definitiva: imanes embutidos con pausa
                cut(n, cyl((u, 0, z0), (u, 0, z0 + p['iman_aloj_h']), p['iman_aloj_d'] / 2))
    return n

def m_guardada():
    """Aguja guardada en el techo de la caja: tumbada de atras adelante, con la punta hacia el frente."""
    d = D()
    m = C.Matrix3D.create()
    m.setWithCoordinateSystem(pt(d['xn'], d['yh'], d['zr']), vec(0, -1, 0), vec(1, 0, 0), vec(0, 0, 1))
    return m

def build_aguja():
    n = needle()
    T().transform(n, m_guardada())
    return n

# ---------------------------------------------------------------- funda de campana y frase
def build_frase():
    p = P
    d = D()
    data = json.load(open(os.path.join(CARPETA, 'frase-v3.json'), encoding='utf-8'))
    x0 = -data['ancho_mm'] / 2
    y0 = -d['Yo'] + p['frase_margen'] + data['alto_mm']
    polys = [([(x0 + x, y0 + y) for x, y in pol['outer']], [[(x0 + x, y0 + y) for x, y in h] for h in pol['holes']]) for pol in data['poligonos']]
    return prisma(polys, 'z', d['Zo'] - p['frase_fondo'], d['Zo']), (0.0, y0 - data['alto_mm'] / 2)

def build_funda(ink=None, centro=(0.0, 0.0)):
    p = P
    d = D()
    re = p['redondeo_ext']
    f = rbox(-d['Xo'], d['Xo'], -d['Yo'], d['Yo'], -2 * re, d['Zo'], re)
    inter(f, half((0, 0, 0), (0, 0, 1)))
    cut(f, box(-d['Xi'], d['Xi'], -d['Yi'], d['Yi'], -1, d['Zi']))
    cut(f, cyl((centro[0], centro[1], d['Zi'] - EPS), (centro[0], centro[1], d['Zi'] + p['nfc_aloj_h']), p['nfc_aloj_d'] / 2))
    if ink is not None:
        cut(f, T().copy(ink))
    return f

# ---------------------------------------------------------------- pinza en C, peana y reloj de referencia
def pinza_perfil(st):
    """Contorno (a, n) de la pinza. st = tramo recto del lado del brazo: st_lib sin reloj, st_nom con el reloj nominal."""
    p = P
    d = D()
    R, pl, ab = d['R'], d['pl'], d['ab']
    tr, tf = p['pinza_pared_rigida'], p['pinza_pared']
    at = ab + st
    ext, itr = [], []
    def add(a, n, ia, inn, t):
        ext.append((a, n))
        itr.append((a + ia * t, n + inn * t))
    add(pl / 2, 0.0, 0, 1, tr)
    add(ab, 0.0, 0, 1, tr)
    for a, n in arco(ab, R, R, 180.0, 360.0)[1:]:
        add(a, n, (ab - a) / R, (R - n) / R, tr)
    a1 = ab + p['pinza_talon']
    a2 = min(a1 + p['pinza_transicion'], at - 0.5)
    add(a1, 2 * R, 0, -1, tr)
    add(a2, 2 * R, 0, -1, tf)
    add(at, 2 * R, 0, -1, tf)
    gfin = math.degrees(math.acos((p['pinza_remeter'] - R) / R))
    for a, n in arco(at, R, R, 0.0, gfin)[1:]:
        add(a, n, (at - a) / R, (R - n) / R, tf)
    return ext + itr[::-1], ext

def contorno(pts):
    """Perimetro de la envolvente convexa: lo que rodea un brazalete tenso."""
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in pts))
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    h = lo[:-1] + up[:-1]
    return sum(math.hypot(h[i][0] - h[i - 1][0], h[i][1] - h[i - 1][1]) for i in range(len(h)))

def build_pinza(libre=False):
    p = P
    d = D()
    pol, _ = pinza_perfil(d['st_lib'] if libre else d['st_nom'])
    return prisma([([an(d, a, n) for a, n in pol], [])], 'x', -p['pinza_ancho'] / 2, p['pinza_ancho'] / 2)

def build_peana():
    p = P
    d = D()
    R, ab, h, w = d['R'], d['ab'], p['cuna_holgura'], p['cuna_grosor']
    zf, bg = d['zf'], p['bandeja_grosor']
    af, ar = ab + p['cuna_frente'], ab + p['cuna_detras']
    # base encastrada: frente en dientes, talon trasero a 45 grados
    b = prisma([(planta_peana(0.0), [])], 'z', zf - bg, zf)
    inter(b, half((0, d['yt1'], zf), (0, -1, -1)))
    # cunas: macizo en U alrededor del arco inferior de la pinza, con su pedestal
    lleno = [(af, -h - w), (ab, -h - w)] + arco(ab, R, R + h + w, 180.0, 360.0)[1:] + [(ar, 2 * R + h + w)]
    u = prisma([([an(d, a, n) for a, n in lleno], [])], 'x', -d['xout'], d['xout'])
    ped = box(-d['xout'], d['xout'], d['ycu'] - d['ro'], d['ycu'] + d['ro'], zf - EPS, d['zcu'])
    join(u, ped)
    cut(u, box(-d['xin'], d['xin'], -GRANDE / 4, GRANDE / 4, zf, zf + GRANDE / 4))           # paso del brazalete
    alto = d['pl'] + 2 * R
    hueco = [(alto, -h), (ab, -h)] + arco(ab, R, R + h, 180.0, 360.0)[1:] + [(alto, 2 * R + h)]
    cut(u, prisma([([an(d, a, n) for a, n in hueco], [])], 'x', -d['xpz'], d['xpz']))
    join(b, u)
    return b

def caja_inclinada(a0, a1, n0, n1, x0, x1):
    d = D()
    t = d['t']
    yc, zc = an(d, (a0 + a1) / 2, (n0 + n1) / 2)
    o = C.OrientedBoundingBox3D.create(pt((x0 + x1) / 2, yc, zc), vec(0, math.sin(t), math.cos(t)), vec(0, math.cos(t), -math.sin(t)), abs(a1 - a0) * K, abs(n1 - n0) * K, abs(x1 - x0) * K)
    return T().createBox(o)

def build_reloj():
    """Reloj de referencia completo: cabeza, corona, brazalete y cierre (punto 10)."""
    p = P
    d = D()
    R, ab, st, g = d['R'], d['ab'], d['st_nom'], p['reloj_grosor']
    bz, bw = p['brazalete_grosor'], p['brazalete_ancho'] / 2
    y0, z0 = an(d, 0, 0)
    y1, z1 = an(d, 0, -g)
    r = cyl((0, y0, z0), (0, y1, z1), p['reloj_diametro'] / 2)
    yk, zk = an(d, 0, -g / 2)
    join(r, cyl((p['reloj_diametro'] / 2 - 1, yk, zk), (p['reloj_diametro'] / 2 + p['reloj_corona_l'], yk, zk), p['reloj_corona_d'] / 2))
    at = ab + st
    def estadio(e):
        return [(at, -e), (ab, -e)] + arco(ab, R, R + e, 180.0, 360.0)[1:] + arco(at, R, R + e, 0.0, 180.0)
    fuera = [an(d, a, n) for a, n in estadio(bz)]
    dentro = [an(d, a, n) for a, n in estadio(0.0)]
    join(r, prisma([(fuera, [dentro])], 'x', -bw, bw))
    am = (ab + at) / 2
    join(r, caja_inclinada(am - p['cierre_largo'] / 2, am + p['cierre_largo'] / 2, 2 * R, 2 * R + p['cierre_grosor'], -p['cierre_ancho'] / 2, p['cierre_ancho'] / 2))
    return r

def build_tarjeta():
    p = P
    d = D()
    y0 = d['yF'] + p['carril_hueco'] / 2 - p['tarjeta_grosor'] / 2
    return box(-p['tarjeta_largo'] / 2, p['tarjeta_largo'] / 2, y0, y0 + p['tarjeta_grosor'], d['zp'] - p['tarjeta_ancho'] / 2, d['zp'] + p['tarjeta_ancho'] / 2)

# ---------------------------------------------------------------- montaje
REFERENCIAS = ('reloj_referencia', 'tarjeta_referencia')

def build_all():
    out = []
    ink, centro = build_frase()
    partes = (('base', build_base()), ('tapa', build_tapa()), ('tapeta', build_tapeta()), ('rotor', build_rotor()),
              ('aguja', build_aguja()), ('peana', build_peana()), ('pinza', build_pinza()), ('funda', build_funda(ink, centro)),
              ('frase', ink), ('reloj_referencia', build_reloj()), ('tarjeta_referencia', build_tarjeta()))
    nombres = [n for n, _ in partes]
    root = des().rootComponent
    for o in [o for o in root.occurrences if o.component.name not in nombres]:
        o.deleteMe()
    for name, body in partes:
        b = put(name, body)
        bb = b.boundingBox
        out.append('%s: %.1f x %.1f x %.1f mm, %.1f cm3' % (name, (bb.maxPoint.x - bb.minPoint.x) * 10, (bb.maxPoint.y - bb.minPoint.y) * 10, (bb.maxPoint.z - bb.minPoint.z) * 10, b.volume))
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
    petg = mk('Prism-127', 'Eventually - PETG', (214, 219, 224))
    acero = mk('Prism-073', 'Eventually - acero (referencia)', None)
    mapa = {'funda': marmol, 'aguja': azul, 'frase': azul, 'pinza': petg, 'reloj_referencia': acero}
    for o in d.rootComponent.occurrences:
        o.component.bRepBodies.item(0).appearance = mapa.get(o.component.name, papel)

# ---------------------------------------------------------------- comprobaciones
def vol_inter(a, b):
    a = T().copy(a)
    try:
        T().booleanOperation(a, b, F.BooleanTypes.IntersectionBooleanType)
        return a.volume * 1000
    except Exception:
        return 0.0

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

def check_pestillo():
    """Grado a grado: el panel esta bloqueado si, tirando de el 0.6 mm hacia fuera, el rotor choca con la caja."""
    d = D()
    base, tapa = build_base(), build_tapa()
    tira = C.Matrix3D.create()
    tira.translation = C.Vector3D.create(0, -0.06, 0)
    bloq, choca = [], []
    a1, a2 = int(math.ceil(d['a1'])), int(P['rotor_giro'])
    for ang in range(a1, a2 + 1):
        r = al_mundo(rotor_L(ang, False))
        if vol_inter(r, tapa) > 0.01 or vol_inter(r, base) > 0.01:
            choca.append(ang)
        r2 = T().copy(r)
        T().transform(r2, tira)
        if vol_inter(r2, base) > 0.01:
            bloq.append(ang)
    out = ['pestillo, grado a grado de %d a %d (positivo = giro de la aguja, a derechas):' % (a1, a2)]
    out.append('  bloqueado de %d a %d grados; libre con la aguja desde %d; libre por resbalon desde %d' % (min(bloq), max(bloq), max(bloq) + 1, min(bloq) - 1))
    out.append('  el rotor gira sin tocar caja ni panel en %s' % ('todo el recorrido' if not choca else 'todo menos %s' % choca))
    out.append('  teorico: resbalon %.1f grados, apertura con aguja %.1f grados, pico del pestillo a radio %.2f' % (math.degrees(d['ts']), math.degrees(d['tk']), d['rA']))
    return out

def check_resbalon():
    """Empuja el panel hacia dentro y busca, a cada paso, el giro minimo que deja pasar al rotor."""
    d = D()
    base = build_base()
    out = ['resbalon: panel a x mm de su sitio -> giro a izquierdas que la boca le pide al rotor']
    pasos = (P['tapa_alto'], 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0.0)
    lim = int(math.floor(-d['a1'] * 2))
    rot = [al_mundo(rotor_L(-q / 2.0, False)) for q in range(lim + 1)]
    for s in pasos:
        m = C.Matrix3D.create()
        m.translation = C.Vector3D.create(0, -s * K, 0)
        need = None
        for q in range(lim + 1):
            r = T().copy(rot[q])
            T().transform(r, m)
            if vol_inter(r, base) <= 0.01:
                need = q / 2.0
                break
        out.append('  %.1f mm -> %s' % (s, ('%.1f grados' % need) if need is not None else 'NO PASA dentro del tope'))
    return out

def distancias():
    p = P
    d = D()
    t, R, g = d['t'], d['R'], p['reloj_grosor']
    out = []
    yfr = d['yO'] - p['reloj_diametro'] / 2 * math.sin(t) - g * math.cos(t)
    ztop = an(d, d['ab'] + d['st_nom'], R)[1] + R + p['brazalete_grosor']
    yback = an(d, d['ab'] + d['st_nom'], 2 * R)[0]
    out.append('reloj: cristal a %.1f mm de los carriles de la tarjeta | brazalete a %.1f mm del techo | hueco tras la pinza %.1f mm' % (yfr - d['yF'] - p['carril_alto'], d['zf'] + d['ch'] - ztop, d['yB'] - yback))
    ymov, zmov = an(d, 0, -g / 2)
    yim = -d['Do'] / 2 + p['tapa_piel'] + p['iman_central_retiro'] + p['iman_h'] / 2
    out.append('imanes -> centro del movimiento: central %.1f mm | del rotor %.1f mm | esquinas %.1f y %.1f mm | aguja guardada %.1f mm' % (
        math.hypot(ymov - yim, zmov - d['zp']), math.hypot(ymov - yim, zmov - (d['zp'] - p['rotor_radio_iman'])),
        math.sqrt(d['mx'] ** 2 + (ymov - d['yF']) ** 2 + (zmov - d['zp'] - d['my']) ** 2), math.sqrt(d['mx'] ** 2 + (ymov - d['yF']) ** 2 + (zmov - d['zp'] + d['my']) ** 2),
        math.sqrt(d['xn'] ** 2 + (ymov - d['yh']) ** 2 + (zmov - d['zr']) ** 2)))
    out.append('pinza: contorno libre %.1f mm | con el reloj nominal %.1f mm | cara plana %.0f mm, extremos de radio %.0f' % (contorno(pinza_perfil(d['st_lib'])[1]), contorno(pinza_perfil(d['st_nom'])[1]), d['pl'], R))
    out.append('exterior con funda: %.1f x %.1f x %.1f mm (ancho x fondo x alto) | caja interior %.1f x %.1f x %.1f' % (2 * d['Xo'], 2 * d['Yo'], d['Zo'], d['L'], d['Do'], d['Ho']))
    out.append('imanes: 2 aguja + 1 central + 1 rotor + 2 panel + 2 caja = 8')
    return out

# ---------------------------------------------------------------- exportar
def m_ejes(xa, ya, za):
    m = C.Matrix3D.create()
    m.setWithCoordinateSystem(pt(0, 0, 0), vec(*xa), vec(*ya), vec(*za))
    m.invert()
    return m

# Orientacion de impresion: que direccion del modelo queda hacia arriba en la cama
M_FRENTE_ARRIBA = lambda: m_ejes((1, 0, 0), (0, 0, 1), (0, -1, 0))      # caja: pared trasera en la cama
M_FRENTE_ABAJO = lambda: m_ejes((1, 0, 0), (0, 0, -1), (0, 1, 0))       # panel, tapeta, rotor: cara vista en la cama
M_TECHO_ABAJO = lambda: m_ejes((1, 0, 0), (0, -1, 0), (0, 0, -1))       # funda y frase: techo en la cama
M_DE_LADO = lambda: m_ejes((0, 1, 0), (0, 0, 1), (1, 0, 0))             # pinza: de canto, sin soportes

def imprimibles():
    ink, centro = build_frase()
    def o(body, m):
        if m is not None:
            T().transform(body, m)
        return body
    return [('base', o(build_base(), M_FRENTE_ARRIBA())), ('tapa', o(build_tapa(), M_FRENTE_ABAJO())),
            ('tapeta', o(build_tapeta(), M_FRENTE_ABAJO())), ('rotor', o(build_rotor(), M_FRENTE_ABAJO())),
            ('aguja', needle()), ('peana', build_peana()), ('pinza', o(build_pinza(True), M_DE_LADO())),
            ('funda', o(build_funda(ink, centro), M_TECHO_ABAJO())), ('frase', o(T().copy(ink), M_TECHO_ABAJO()))]

def probetas():
    p = P
    d = D()
    out = []
    # P0: tira de tolerancias. De izquierda (esquina cortada) a derecha, valores crecientes.
    nA, paso = len(P0_ALOJAMIENTOS), 14.0
    largo, ancho, alto = paso * nA + 6, 40.0, 4.0
    t = box(0, largo, 0, ancho, 0, alto)
    inter(t, half((4, 0, 0), (1, 1, 0)))
    for i, dd in enumerate(P0_ALOJAMIENTOS):
        x = 3 + paso * (i + 0.5)
        cut(t, cyl((x, 33, alto - p['iman_aloj_h']), (x, 33, alto + 1), dd / 2))
        cut(t, cyl((x, 33, -1), (x, 33, alto), p['emergencia_d'] / 2))
    for i, hh in enumerate(P0_HOLGURAS):
        x = 3 + paso * (i + 0.5)
        cut(t, box(x - P0_LLAVE / 2 - hh, x + P0_LLAVE / 2 + hh, 20 - P0_LLAVE / 2 - hh, 20 + P0_LLAVE / 2 + hh, -1, alto + 1))
    for i, pi in enumerate(P0_PIELES):
        x = 3 + paso * (i + 1.5)
        cut(t, cyl((x, 7, pi), (x, 7, alto + 1), p['iman_aloj_d'] / 2))
    out.append(('p0-tolerancias', t))
    out.append(('p0-llave', box(0, P0_LLAVE, 0, P0_LLAVE, 0, 20)))
    # P1: llave. Panel, tapeta, rotor y aguja de prueba (imanes recuperables)
    for nombre, body in (('p1-panel', build_tapa()), ('p1-tapeta', build_tapeta()), ('p1-rotor', build_rotor())):
        T().transform(body, M_FRENTE_ABAJO())
        out.append((nombre, body))
    out.append(('p1-aguja-de-prueba', needle(prueba=True)))
    # P2: resbalon. Aro de la boca y tres rotores con espirales de distinto grosor
    aro = build_base()
    inter(aro, half((0, -d['Do'] / 2 + 15, 0), (0, -1, 0)))
    T().transform(aro, M_FRENTE_ARRIBA())
    out.append(('p2-aro-de-la-boca', aro))
    for nombre, g in P2_MUELLES:
        r = al_mundo(rotor_L(0.0, True, g))
        T().transform(r, M_FRENTE_ABAJO())
        out.append(('p2-rotor-muelle-%s' % nombre, r))
    # P3: soporte. Pinza libre, peana y un trozo de suelo con su rebaje
    pz = build_pinza(True)
    T().transform(pz, M_DE_LADO())
    out.append(('p3-pinza', pz))
    out.append(('p3-peana', build_peana()))
    su = build_base()
    w = p['bandeja_ancho'] / 2 + 5
    inter(su, box(-w, w, d['yt0'] - w / 2, d['yt1'] + 10, 0, d['zf']))
    out.append(('p3-suelo', su))
    # P4: funda. Tramo de 40 mm de campana con la frase, y un tramo de caja para probar el colchon de aire
    ink, centro = build_frase()
    fu = build_funda(ink, centro)
    corte = half((0, 0, d['Zo'] - 40), (0, 0, 1))
    inter(fu, corte)
    T().transform(fu, M_TECHO_ABAJO())
    out.append(('p4-funda-tramo', fu))
    T().transform(ink, M_TECHO_ABAJO())
    out.append(('p4-frase', ink))
    re = p['redondeo_ext']
    cj = rbox(-d['L'] / 2, d['L'] / 2, -d['Do'] / 2, d['Do'] / 2, d['Ho'] - 45 - 2 * re, d['Ho'], re)
    inter(cj, half((0, 0, d['Ho'] - 45), (0, 0, 1)))
    cut(cj, box(-d['L'] / 2 + 2, d['L'] / 2 - 2, -d['Do'] / 2 + 2, d['Do'] / 2 - 2, 0, d['Ho'] - 2))
    T().transform(cj, M_TECHO_ABAJO())
    out.append(('p4-caja-tramo', cj))
    return out

def _exporta_cuerpos(lista, sub):
    d = des()
    em = d.exportManager
    out = []
    if not os.path.isdir(sub):
        os.makedirs(sub)
    for nombre, body in lista:
        put('_exp', body)
        occ = [o for o in d.rootComponent.occurrences if o.component.name == '_exp'][0]
        fn = os.path.join(sub, nombre + '.3mf')
        em.execute(em.createC3MFExportOptions(occ, fn))
        occ.deleteMe()
        out.append(fn)
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
    out += _exporta_cuerpos(imprimibles(), os.path.join(carpeta, 'imprimir-%s' % sufijo))
    out += _exporta_cuerpos(probetas(), os.path.join(carpeta, 'probetas-%s' % sufijo))
    csv = os.path.join(carpeta, 'parametros-fusion-%s.csv' % sufijo)
    with open(csv, 'w', encoding='utf-8') as fh:
        fh.write('Nombre,Unidad,Expresion,Valor,Comentario\n')
        for name, unit, expr, com in P_DEF:
            fh.write('%s,%s,"%s",%.4g,"%s"\n' % (name, unit, expr, P[name], com.replace('"', "'")))
    out.append(csv)
    return out

def main(comprobar=True):
    d = des()
    d.designIntent = F.DesignIntentTypes.HybridDesignIntentType
    p = load_params()
    out = ['parametros: %d' % len(p)]
    out += build_all()
    colores()
    if comprobar:
        out += check()
        out += check_pestillo()
        out += check_resbalon()
    out += distancias()
    app().activeViewport.fit()
    return out
