# Eventually, la caja: generador del prototipo v4 para Autodesk Fusion. PARCHE v4.1 (20-nov-2026):
# corrige lo que senala contra-reporte-v4.md (ranura de emergencia, taco del muelle, puntas del rotor,
# tapa trasera, retenes de peana y funda).
# Responde al contra-reporte de la v3 (contra-reporte-v3.md): rotor de un solo sentido con tope y muelle
# precargado, puentes tras los pestillos, peana corredera, pinza a medida, reten de la funda. Se ejecuta dentro de Fusion
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
('brazalete_contorno','mm','180 mm','SUPUESTO: contorno interior del brazalete cerrado. MANDA en pinza y caja. MEDIR antes de imprimir la caja'),
('pinza_extra','mm','6 mm','G2: lo que la pinza libre mide de mas que el brazalete (trabaja al 0.3-0.4 %)'),
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
('iman_cubierta','mm','1.8 mm','v4.1 (I3): plastico sobre los imanes de esquina. Entre los dos dan 0.7 N: la aguja saca el panel tirando del centro'),
('iman_central_retiro','mm','0.4 mm','I5: retiro del iman central respecto a la piel'),
('nfc_d','mm','25 mm','Etiqueta NFC'),
('nfc_aloj_d','mm','nfc_d + 0.6 mm','Rebaje del NFC bajo el techo de la funda'),
('nfc_aloj_h','mm','0.5 mm','Fondo del rebaje del NFC'),
# --- holguras (se confirman con la probeta P0) ---
('holg_desliza','mm','0.3 mm','Holgura por lado entre funda y caja (colchon de aire)'),
('holg_tapa','mm','0.2 mm','Holgura por lado del panel en la boca, y de la peana en su rebaje'),
('holg_presion','mm','0.15 mm','Holgura para encajes a presion (tapeta, ancla del muelle)'),
('holg_giro','mm','0.3 mm','Holgura lateral del rotor en su camara y en las ranuras'),
('holg_corte','mm','0.35 mm','v4.1 (I4): margen de las ranuras del pestillo; el labio de la caja es un puente y descuelga'),
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
('soporte_pie','mm','4.5 mm','Altura libre entre el suelo y la pinza, para el brazalete'),
('pinza_radio','mm','15 mm','Radio exterior de los extremos de la pinza (pinza aplanada: 30 mm de grueso)'),
('pinza_cara','mm','43 mm','Largo de la cara plana rigida donde apoya la tapa trasera del reloj'),
('pinza_contorno_libre','mm','brazalete_contorno + pinza_extra','G2: contorno de la pinza sin reloj. Pinza a medida, no universal'),
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
('bandeja_oreja','mm','4 mm','G3: largo de las orejas de la base que pasan el reten'),
('guia_pared','mm','2 mm','G3: pared de cada guia de la peana corredera'),
('guia_labio','mm','1.2 mm','G3: grosor del labio que impide que la peana se levante'),
('guia_solape','mm','2 mm','G3: lo que el labio pisa la base'),
('guia_holg','mm','0.25 mm','G3: holgura entre la base y el labio'),
('guia_frente','mm','3 mm','G3: lo que las guias sobresalen por delante de la peana'),
('guia_chaflan','mm','1.5 mm','v4.1 (I8): chaflan de entrada de las guias'),
('lengueta_largo','mm','12 mm','v4.1 (I1): lengueta elastica de la base de la peana, a cada lado'),
('lengueta_grosor','mm','1.2 mm','v4.1 (I1): grosor de la lengueta'),
('lengueta_ranura','mm','0.8 mm','v4.1 (I1): ranura que libera la lengueta'),
('lengueta_resalte','mm','0.6 mm','v4.1 (I1): resalte redondo en la punta, que cae en una muesca de la guia'),
('aire_frente','mm','3 mm','Aire entre los carriles de la tarjeta y el cristal del reloj'),
('aire_arriba','mm','1.5 mm','Punto 15: aire entre el brazalete y el techo (la peana ya no se levanta)'),
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
('carril_resalte','mm','carril_hueco - tarjeta_grosor + 0.1 mm','I10: resalte bajo el labio que pellizca la tarjeta'),
# --- interior y exterior de la caja ---
('nicho_ancho','mm','tarjeta_largo + 3 mm','Ancho interior: lo fija la tarjeta'),
('nicho_alto','mm','soporte_pie + 2 * pinza_radio + (pinza_contorno_libre - 2 * PI * pinza_radio) / 2 * cos(soporte_inclinacion) + brazalete_grosor + aire_arriba','Alto interior: lo fija la pinza en su forma libre'),
('nicho_fondo','mm','carril_alto + aire_frente + reloj_diametro / 2 * sin(soporte_inclinacion) + reloj_grosor * cos(soporte_inclinacion) + 2 * pinza_radio * cos(soporte_inclinacion) + ((pinza_contorno_libre - 2 * PI * pinza_radio) / 2 - pinza_cara / 2) * sin(soporte_inclinacion) + hueco_cierre + aire_detras','Fondo interior, del panel a la pared trasera'),
# --- panel frontal y mecanismo (G2, G3, G4, I5, I10, I11) ---
('tapa_piel','mm','1.4 mm','I5: piel sobre el mecanismo, con relleno opaco'),
('rotor_grosor','mm','3 mm','Grosor del rotor'),
('tapeta_grosor','mm','1.8 mm','I2: grosor de la tapa trasera y de los puentes que respaldan los pestillos'),
('tapeta_x','mm','38.5 mm','I3: semiancho de la tapa trasera, que cubre toda la camara'),
('tapeta_corte','mm','8.5 mm','I3: esquinas cortadas de la tapa trasera, para librar los imanes'),
('puente','mm','6.5 mm','I2: alto de la banda maciza que queda detras de cada pestillo'),
('tapeta_pestana','mm','2 mm','v4.1 (I5): pestana de la tapa trasera que entra bajo la banda de arriba'),
('tapeta_pestana_ancho','mm','18 mm','v4.1 (I5): ancho de la pestana'),
('tapeta_pestana_x','mm','-19 mm','v4.1 (I5): posicion de la pestana'),
('tapeta_clip_largo','mm','12 mm','v4.1 (I5): lengueta-clip del borde de abajo de la tapa trasera'),
('tapeta_clip_ancho','mm','1.5 mm','v4.1 (I5): ancho de esa lengueta'),
('tapeta_clip_resalte','mm','0.5 mm','v4.1 (I5): resalte del clip'),
('tapeta_clip_x','mm','10 mm','v4.1 (I5): posicion del clip'),
('llave_d','mm','4 mm','I7: resalte por detras del panel para que solo entre al derecho'),
('llave_h','mm','1.6 mm','I7: alto de ese resalte'),
('tapa_holg_tapeta','mm','0.1 mm','Lo que la tapeta queda hundida respecto a la cara trasera del panel'),
('tapa_alto','mm','tapa_piel + rotor_grosor + rotor_holg_axial + tapeta_grosor + tapa_holg_tapeta','Grosor del panel frontal'),
('rotor_ancho','mm','8 mm','Ancho de la barra del rotor'),
('rotor_giro','deg','50 deg','I10: giro de la aguja entre cerrado y abierto'),
('rotor_enganche','mm','2 mm','I10: cuanto entra cada pestillo en techo y suelo'),
('rotor_radio_iman','mm','16 mm','Del eje al iman de arrastre (y a la pala de la aguja)'),
('rotor_chaflan','mm','2.2 mm','Solo rotor articulado: chaflan de entrada del pico'),
('eje_radio','mm','4 mm','Radio del eje del panel (hueco, con el iman central dentro)'),
('cubo_radio','mm','6 mm','Radio exterior del cubo del rotor'),
('muelle_grosor','mm','0.6 mm','G3: grosor de la espiral. Ajustar con la probeta P2 (0.45 / 0.6 / 0.8)'),
('muelle_alto','mm','1.6 mm','G3: alto de la espiral'),
('muelle_vueltas','','1.5','G3: vueltas de la espiral'),
('muelle_radio_ext','mm','11.6 mm','G3: radio exterior de la espiral'),
('muelle_holgura','mm','0.6 mm','Hueco entre la espiral y el alma del rotor (puente de impresion)'),
('rotor_alma','mm','rotor_grosor - muelle_alto - muelle_holgura','Grosor del alma que une cubo y brazos por encima de la espiral'),
('muelle_ancla_largo','mm','4 mm','Largo del taco que ancla la espiral al panel'),
('muelle_ancla_ancho','mm','4.4 mm','Ancho del taco de anclaje'),
('muelle_precarga','deg','18 deg','I1: giro con que la espiral queda cargada contra el tope'),
('muelle_ancla_ang','deg','9 deg','Posicion de la muesca del taco, por debajo de la horizontal izquierda'),
('muelle_montaje','deg','45 deg','I2: giro al que se mete el rotor, donde no hay puente'),
('ancla_teton_d','mm','1.8 mm','v4.1 (G2): teton del panel en el que entra el ojo del taco; lo sujeta en todas direcciones'),
('ancla_teton_h','mm','1 mm','v4.1 (G2): lo que el teton entra en el taco (hay que levantar el taco para montarlo)'),
('ancla_ojo_d','mm','2.2 mm','v4.1 (G2): ojo del taco'),
('rotor_rebaje','mm','0.4 mm','v4.1 (I4): rebaje de las puntas del rotor por detras, bajo los puentes del panel'),
('art_barra','mm','27.5 mm','Rotor articulado: radio donde acaba la barra rigida'),
('art_codo','mm','7.5 mm','Rotor articulado: largo del codo lateral'),
('art_codo_alto','mm','4 mm','Rotor articulado: alto del codo'),
('lamina_grosor','mm','0.6 mm','Rotor articulado: grosor de la lamina que hace de bisagra'),
('lamina_largo','mm','6 mm','Rotor articulado: largo de la lamina'),
('art_brazo','mm','3 mm','Rotor articulado: ancho del bracito'),
('pico_ancho','mm','3 mm','Rotor articulado: ancho del pico'),
('pico_alto','mm','3.5 mm','Rotor articulado: alto de la cabeza del pico'),
('art_alivio','mm','3.4 mm','Hueco de la camara para que el pico se aparte al bascular'),
('art_barrido','deg','28 deg','Angulo de mas de la camara para el codo del rotor articulado'),
('art_barrido_r','mm','35 mm','Radio de esa zona de la camara'),
('camara_muelle','mm','muelle_radio_ext + 0.8 mm','Radio de la camara de la espiral'),
('rotor_radio_brazo','mm','camara_muelle + 0.6 mm','Radio desde el que los brazos tienen todo el grosor'),
('refuerzo_esq','mm','8 mm','Refuerzos de esquina donde asienta el panel'),
('iman_esq_dist','mm','4.5 mm','Distancia de los imanes de esquina a las paredes'),
('labio_ancho','mm','34 mm','Zona central del suelo sin bisel, donde engancha el pestillo'),
('bisel','mm','3 mm','I1: bisel de apertura bajo el panel'),
('una_fondo','mm','1.2 mm','Ranura para la una en el canto inferior del panel'),
('una_ancho','mm','1.5 mm','Ancho de la ranura para la una'),
('una_dist','mm','2 mm','Distancia de la ranura al frente del panel'),
('emergencia_d','mm','1.6 mm','G4: ancho de la ranura de emergencia de la base (y taladros para sacar imanes de las probetas)'),
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
('aguja_roce','mm','0.33 mm','I10: dos puntos de roce que retienen la aguja en su rebaje'),
# --- funda de campana y frase (I3, I9) ---
('funda_ancho','mm','caja_ancho + 2 * holg_desliza + 2 * pared_funda','Exterior de la funda'),
('funda_fondo','mm','caja_fondo + 2 * holg_desliza + 2 * pared_funda','Exterior de la funda'),
('funda_alto','mm','caja_alto + holg_desliza + funda_techo','Exterior de la funda (abierta por abajo)'),
('frase_fondo','mm','0.6 mm','Profundidad de la frase: 3 capas de 0.2'),
('frase_margen','mm','14 mm','Del borde delantero del techo de la funda a la frase'),
('reten_funda_r','mm','1.5 mm','I4: radio de los dos nervios de la caja que retienen la funda'),
('reten_funda_sale','mm','0.8 mm','v4.1 (I2): lo que sobresale cada nervio (aprieto de 0.2 mm ya asentada)'),
('reten_funda_rebaje','mm','0.3 mm','I4: fondo del rebaje de la funda donde descansa el nervio'),
('reten_funda_z','mm','6 mm','I4: altura de los nervios sobre la mesa'),
('reten_funda_largo','mm','30 mm','I4: largo de cada nervio'),
]

# Probeta P0: valores que se prueban (no son parametros del modelo)
P0_ALOJAMIENTOS = (5.05, 5.10, 5.15, 5.20, 5.25, 5.30)
P0_HOLGURAS = (0.10, 0.15, 0.20, 0.25, 0.30, 0.35)
P0_PIELES = (0.8, 1.0, 1.2, 1.4)
P0_LLAVE = 6.0
MUELLES = (('fino', 0.45), ('medio', 0.6), ('grueso', 0.8))

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

def pol(r, g):
    """Punto en polares; g = angulo matematico en grados (0 = +x, antihorario)."""
    return (r * math.cos(math.radians(g)), r * math.sin(math.radians(g)))

def arco_pol(r, g0, g1):
    n = max(2, int(abs(g1 - g0) / PASO) + 1)
    return [pol(r, g0 + (g1 - g0) * i / n) for i in range(n + 1)]

def obox(c, dx, dy, largo, ancho, z0, z1):
    """Caja orientada en el plano: centro c, direccion (dx, dy) del largo."""
    o = C.OrientedBoundingBox3D.create(pt(c[0], c[1], (z0 + z1) / 2), vec(dx, dy, 0), vec(-dy, dx, 0), largo * K, ancho * K, abs(z1 - z0) * K)
    return T().createBox(o)

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
    # pestillo: rotor de un solo sentido (a derechas, con la aguja) y tope en cerrado
    hw = p['rotor_ancho'] / 2
    Rt = d['ch'] / 2 + p['rotor_enganche']
    d['hw'], d['Rt'] = hw, Rt
    d['rA'] = math.hypot(hw, Rt)
    d['tk'] = math.asin(hw / Rt) + math.acos(d['hy'] / Rt)   # giro de apertura (rad)
    d['Rc'] = d['rA'] + p['holg_giro']
    d['lente'] = math.sqrt(max(d['Rc'] ** 2 - (d['ch'] / 2) ** 2, 0.0))
    d['a1'], d['a2'] = 0.0, p['rotor_giro']
    d['gn'] = 180.0 + p['muelle_ancla_ang']                  # angulo del teton del taco
    d['rojo'] = p['muelle_radio_ext'] + p['muelle_ancla_largo'] - p['ancla_ojo_d'] / 2 - 0.9     # radio del ojo del taco
    # mundo
    d['yF'] = -d['Do'] / 2 + p['tapa_alto']
    d['yB'] = d['Do'] / 2 - p['pared']
    d['zf'] = p['pared_techo']
    d['zp'] = d['Ho'] / 2
    # pinza: sistema (a, n) con origen O en el centro de la cara plana
    t = math.radians(p['soporte_inclinacion'])
    R, pl = p['pinza_radio'], p['pinza_cara']
    d['t'], d['R'], d['pl'] = t, R, pl
    d['st_lib'] = (p['pinza_contorno_libre'] - 2 * math.pi * R) / 2
    d['ab'] = -pl / 2                                        # centro del arco inferior
    d['zt'] = d['zf'] + p['bandeja_grosor']                 # cara de arriba de la base de la peana
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
    # I7: el panel solo entra al derecho por un resalte trasero; su agujero, en el refuerzo de abajo a la izquierda
    cut(b, cyl((-d['mx'], -d['my'], zs - p['llave_h'] - 0.4), (-d['mx'], -d['my'], zs + EPS), p['llave_d'] / 2 + p['holg_tapa']))
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
    # rebaje de la aguja en el techo, a ras, rebaje redondo para pellizcarla y dos puntos de roce
    rec = needle(p['aguja_rebaje_holg'], Ho, False)
    T().transform(rec, m_guardada())
    cut(b, rec)
    cut(b, cyl((d['xn'], d['yh'] - p['aguja_una_u'], d['zr']), (d['xn'], d['yh'] - p['aguja_una_u'], Ho + 1), p['aguja_una_d'] / 2))
    rc = p['aguja_cubo_d'] / 2 + p['aguja_rebaje_holg']
    for s in (1, -1):
        xa, xb = sorted((d['xn'] + s * (rc - p['aguja_roce']), d['xn'] + s * (rc + 0.5)))
        join(b, box(xa, xb, d['yh'] - 1, d['yh'] + 1, d['zr'], Ho - 0.4))
    # G4: ranura de emergencia en la base, sobre el recorrido del pestillo de abajo (se arrastra de lado con un clip)
    ye = Do / 2 - (d['cb'] + p['rotor_grosor'] / 2)
    xa = -(d['rA'] * math.sin(d['tk']) + d['hw'] + 1)
    cut(b, box(xa, d['hw'] + 2.5, ye - p['emergencia_d'] / 2, ye + p['emergencia_d'] / 2, -1, zf + EPS))                    # v4.1: pasante hasta la cara de arriba del suelo
    # bisel de apertura bajo el panel, a los dos lados de la zona del pestillo
    bi = p['bisel']
    for sx in (1, -1):
        xa, xb = sorted((sx * p['labio_ancho'] / 2, sx * cl / 2))
        cu = box(xa, xb, -Do / 2 - 1, -Do / 2 + bi, zf - bi, zf + EPS)
        inter(cu, half((0, -Do / 2, zf - bi), (0, -1, 1)))
        cut(b, cu)
    # G3: guias con labio para la peana corredera, de delante atras, con tope al fondo y reten delante
    bw, bg, h = p['bandeja_ancho'] / 2, p['bandeja_grosor'], p['holg_tapa']
    zl = zf + bg + p['guia_holg']
    yg = d['yt0'] - p['guia_frente']
    for sx in (1, -1):
        xa, xb = sorted((sx * (bw + h), sx * (bw + h + p['guia_pared'])))
        join(b, box(xa, xb, yg, d['yB'] + EPS, zf - EPS, zl + p['guia_labio']))
        xa, xb = sorted((sx * (bw - p['guia_solape']), sx * (bw + h + p['guia_pared'])))
        join(b, box(xa, xb, yg, d['yB'] + EPS, zl, zl + p['guia_labio']))
        xa, xb = sorted((sx * (bw - 5), sx * (bw + h + EPS)))
        join(b, box(xa, xb, d['yt1'] + h, d['yB'] + EPS, zf - EPS, zl))
        cut(b, cyl((sx * (bw - 1.0 + p['lengueta_resalte']), d['yt0'] + 3.2, zf), (sx * (bw - 1.0 + p['lengueta_resalte']), d['yt0'] + 3.2, zl), 1.2))    # muesca del reten
        gc = p['guia_chaflan']
        xa, xb = sorted((sx * (bw + h - EPS), sx * (bw + h + gc)))
        cu = box(xa, xb, yg - EPS, yg + gc, zf, zl + p['guia_labio'] + 1)
        inter(cu, half((sx * (bw + h + gc), yg, 0), (-sx, -1, 0)))
        cut(b, cu)
    # I4: dos nervios cerca de la base que retienen la funda
    for sx in (1, -1):
        xc = sx * (L / 2 - (p['reten_funda_r'] - p['reten_funda_sale']))
        join(b, cyl((xc, -p['reten_funda_largo'] / 2, p['reten_funda_z']), (xc, p['reten_funda_largo'] / 2, p['reten_funda_z']), p['reten_funda_r']))
    return b

def planta_peana():
    """Planta (x, y) de la base de la peana corredera: recta, con orejas delante y detras que pasan el reten."""
    p = P
    d = D()
    w = p['bandeja_ancho'] / 2
    return [(w, d['yt0']), (w, d['yt1']), (-w, d['yt1']), (-w, d['yt0'])]



# ---------------------------------------------------------------- panel frontal
def camara(z0, z1):
    """Hueco del rotor dentro del panel (sistema L): barrido de los brazos, espiral, canal del taco y alivios."""
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
    ya = d['hy'] - p['puente'] - 3                           # alivios para el pico articulado
    join(wp, box(-hwc - p['art_alivio'], -hwc + 1, ya, d['Rc'] + 1, z0 - 1, z1 + 1))
    join(wp, box(hwc - 1, hwc + p['art_alivio'], -d['Rc'] - 1, -ya, z0 - 1, z1 + 1))
    c = cyl((0, 0, z0), (0, 0, z1), d['Rc'])
    inter(c, wp)
    # barrido del codo y de la lamina del rotor articulado, que van por fuera de la barra
    _, r3 = lados(d['a2'] + p['art_barrido'])
    ws = half((hwc * l1[0], hwc * l1[1], 0), (-l1[0], -l1[1], 0))
    inter(ws, half((hwc * r3[0], hwc * r3[1], 0), (-r3[0], -r3[1], 0)))
    wt = half((-hwc * l1[0], -hwc * l1[1], 0), (l1[0], l1[1], 0))
    inter(wt, half((-hwc * r3[0], -hwc * r3[1], 0), (r3[0], r3[1], 0)))
    join(ws, wt)
    cs = cyl((0, 0, z0), (0, 0, z1), p['art_barrido_r'])
    inter(cs, ws)
    join(c, cs)
    join(c, cyl((0, 0, z0), (0, 0, z1), p['camara_muelle']))
    # canal por el que el taco de la espiral llega a su muesca al montar
    r0, r1 = p['camara_muelle'] - 1, p['muelle_radio_ext'] + p['muelle_ancla_largo'] + p['holg_giro']
    g0, g1 = d['gn'] - p['muelle_precarga'] - p['muelle_montaje'] - 10, d['gn'] + 8
    join(c, prisma([(arco_pol(r1, g0, g1) + arco_pol(r0, g1, g0), [])], 'z', z0, z1))
    cut(c, cyl((0, 0, z0 - 1), (0, 0, z1 + 1), p['eje_radio']))
    return c

def poligono_tapeta(e=0.0):
    """Contorno (x, yL) de la tapa trasera: cubre toda la camara menos las dos bandas de los puentes."""
    p = P
    d = D()
    X, Z, c = p['tapeta_x'] - e, d['hy'] - p['puente'] - e, p['tapeta_corte']
    return [(-X + c, Z), (X, Z), (X, -Z + c), (X - c, -Z), (-X, -Z), (-X, Z - c)]

def tapa_L():
    p = P
    d = D()
    hx, hy, Do, zs, cb, ct = d['hx'], d['hy'], d['Do'], d['zs'], d['cb'], d['ct']
    t = box(-hx, hx, -hy, hy, zs, Do)
    cut(t, camara(cb, ct))
    # v4.1 (G2): teton en el que entra el ojo del taco de la espiral
    xt, yt_ = pol(d['rojo'], d['gn'])
    join(t, cyl((xt, yt_, ct - p['ancla_teton_h'] - p['rotor_holg_axial']), (xt, yt_, ct + EPS), p['ancla_teton_d'] / 2))
    # iman central, dentro del eje, retirado de la piel
    cut(t, cyl((0, 0, cb - EPS), (0, 0, ct - p['iman_central_retiro']), p['iman_aloj_d'] / 2))
    # hueco de la tapa trasera. Fuera de el, arriba y abajo, queda la banda maciza que respalda cada pestillo
    cut(t, prisma([(poligono_tapeta(), [])], 'z', zs - 1, cb))
    # v4.1 (I5): ranura bajo la banda de arriba para la pestana de la tapa trasera, y muesca para su clip
    Z, tg, pe = hy - p['puente'], p['tapeta_grosor'], p['tapeta_pestana']
    c1 = cb - tg / 2 - 0.15
    px0, px1 = p['tapeta_pestana_x'] - p['tapeta_pestana_ancho'] / 2 - 0.3, p['tapeta_pestana_x'] + p['tapeta_pestana_ancho'] / 2 + 0.3
    cut(t, prisma([([(Z - EPS, cb + EPS), (Z + pe + 0.3, cb + EPS), (Z + pe + 0.3, c1), (Z + tg / 2, c1), (Z - EPS, c1 - tg / 2 - EPS)], [])], 'x', px0, px1))
    xk = p['tapeta_clip_x'] + p['tapeta_clip_largo'] - 1.0
    yk = -(Z - p['holg_presion']) + 0.7 - p['tapeta_clip_resalte']
    cut(t, cyl((xk, yk, zs - 1), (xk, yk, cb), 0.9))
    # imanes de esquina embutidos
    for sx, sy in ((-1, 1), (1, -1)):
        z0 = zs + p['iman_cubierta']
        cut(t, cyl((sx * d['mx'], sy * d['my'], z0), (sx * d['mx'], sy * d['my'], z0 + p['iman_aloj_h']), p['iman_aloj_d'] / 2))
    # I7: resalte trasero (abajo a la izquierda) para que el panel solo entre al derecho. El frente queda liso
    join(t, cyl((-d['mx'], -d['my'], zs - p['llave_h']), (-d['mx'], -d['my'], zs + EPS), p['llave_d'] / 2))
    # carriles en U para la tarjeta, con tope recto y un resalte que la pellizca
    tl, ta = p['tarjeta_largo'] / 2, p['tarjeta_ancho'] / 2
    y0, y1 = -ta - p['carril_tope'], -ta + p['carril_largo']
    for sx in (1, -1):
        xa, xb = sorted((sx * (tl + p['carril_holgura']), sx * hx))
        join(t, box(xa, xb, y0, y1, zs - p['carril_alto'], zs + EPS))
        xa, xb = sorted((sx * (tl - p['carril_solape']), sx * hx))
        join(t, box(xa, xb, y0, y1, zs - p['carril_alto'], zs - p['carril_hueco']))
        xa, xb = sorted((sx * (tl - p['carril_tope_ancho']), sx * hx))
        join(t, box(xa, xb, y0, -ta, zs - p['carril_alto'], zs + EPS))
        xa, xb = sorted((sx * (tl - p['carril_solape']), sx * tl))
        join(t, box(xa, xb, y1 - 3, y1 - 1, zs - p['carril_resalte'], zs + EPS))
    # ranura para la una en el canto inferior
    cut(t, box(-hx - 1, hx + 1, -hy - 1, -hy + p['una_fondo'], Do - p['una_dist'] - p['una_ancho'], Do - p['una_dist']))
    return t

def tapeta_L():
    p = P
    d = D()
    cb, tg, hp = d['cb'], p['tapeta_grosor'], p['holg_presion']
    Ze = d['hy'] - p['puente'] - hp
    t = prisma([(poligono_tapeta(hp), [])], 'z', cb - tg, cb)
    # v4.1 (I5): pestana que entra bajo la banda de arriba (con apoyo a 45 grados para imprimirla sin soportes)
    pe = p['tapeta_pestana']
    px0, px1 = p['tapeta_pestana_x'] - p['tapeta_pestana_ancho'] / 2, p['tapeta_pestana_x'] + p['tapeta_pestana_ancho'] / 2
    join(t, prisma([([(Ze - 0.5, cb), (Ze + pe, cb), (Ze + pe, cb - tg / 2), (Ze + tg / 2, cb - tg / 2), (Ze, cb - tg), (Ze - 0.5, cb - tg)], [])], 'x', px0, px1))
    # clip: lengueta en el borde de abajo, con un resalte que cae en una muesca del panel
    x0, x1, ca = p['tapeta_clip_x'], p['tapeta_clip_x'] + p['tapeta_clip_largo'], p['tapeta_clip_ancho']
    cut(t, box(x0, x1 + 0.8, -Ze + ca, -Ze + ca + 0.8, cb - tg - 1, cb + 1))
    cut(t, box(x1, x1 + 0.8, -Ze - 1, -Ze + ca + 0.8, cb - tg - 1, cb + 1))
    join(t, cyl((x1 - 1.0, -Ze + 0.7 - p['tapeta_clip_resalte'], cb - tg), (x1 - 1.0, -Ze + 0.7 - p['tapeta_clip_resalte'], cb), 0.7))
    # v4.1 (G2): resalte sobre el taco de la espiral, para que no pueda levantarse y salirse del teton
    xt, yt_ = pol(d['rojo'], d['gn'])
    join(t, cyl((xt, yt_, cb - EPS), (xt, yt_, cb + p['rotor_grosor'] - p['muelle_alto'] - 0.25), 2.0))
    return t

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

def pico_articulado(zb, zt):
    """Extremo de arriba del rotor articulado (nivel 1): codo, lamina-bisagra, bracito y pico. Sin probar."""
    p = P
    d = D()
    hw, Rt = d['hw'], d['Rt']
    k = math.sqrt(0.5)
    b = box(hw - EPS, hw + p['art_codo'], p['art_barra'] - p['art_codo_alto'], p['art_barra'], zb, zt)
    A = (hw + p['art_codo'] - 0.7, p['art_barra'])
    H = (A[0] - k * p['lamina_largo'], A[1] + k * p['lamina_largo'])
    join(b, obox(((A[0] + H[0]) / 2, (A[1] + H[1]) / 2), -k, k, p['lamina_largo'] + 0.8, p['lamina_grosor'], zb, zt))
    P2 = (-hw + p['pico_ancho'] / 2, Rt - p['pico_alto'] + 0.5)
    L = math.hypot(P2[0] - H[0], P2[1] - H[1])
    join(b, obox(((H[0] + P2[0]) / 2, (H[1] + P2[1]) / 2), (P2[0] - H[0]) / L, (P2[1] - H[1]) / L, L + 1.2, p['art_brazo'], zb, zt))
    pico = box(-hw, -hw + p['pico_ancho'], Rt - p['pico_alto'], Rt, zb, zt)
    inter(pico, half((0, Rt, zb + p['rotor_chaflan']), (0, -1, 1)))
    join(b, pico)
    return b

def articulado_datos():
    """Brazo de palanca, giro, deformacion y fuerza del pico articulado (calculo, no ensayo)."""
    p = P
    d = D()
    k = math.sqrt(0.5)
    F = (d['hw'] + p['art_codo'] - 0.7 - k * p['lamina_largo'] / 2, p['art_barra'] + k * p['lamina_largo'] / 2)
    bx, bz = F[0] - (-d['hw'] + p['pico_ancho'] / 2), d['Rt'] - F[1]
    baja = p['rotor_enganche'] + p['holg_tapa']
    giro = baja / bx
    EI = 3000.0 * p['rotor_grosor'] * p['lamina_grosor'] ** 3 / 12
    return {'bx': bx, 'bz': bz, 'giro': math.degrees(giro), 'eps': 100 * p['lamina_grosor'] * giro / (2 * p['lamina_largo']),
            'lado': bz * giro, 'F': EI * giro / p['lamina_largo'] / bx, 'mu': bx / bz}

def rotor_L(ang=0.0, muelle=True, grosor=None, montado=True, articulado=False):
    """Rotor en el sistema L. ang > 0 = giro a derechas visto de frente (el de la aguja).
    montado=False dibuja la espiral relajada, como se imprime; True, con el taco ya en su muesca."""
    p = P
    d = D()
    zb = d['cb']
    zt = zb + p['rotor_grosor']
    hw, rbz, Rt = d['hw'], p['rotor_radio_brazo'], d['Rt']
    fin = p['art_barra'] if articulado else Rt + 3
    r = box(-hw, hw, rbz, fin, zb, zt)
    join(r, box(-hw, hw, -fin, -rbz, zb, zt))
    if articulado:
        pa = pico_articulado(zb, zt)
        join(r, T().copy(pa))
        join(r, rotz(pa, 180))
    inter(r, cyl((0, 0, zb - 1), (0, 0, zt + 1), d['rA'] if articulado else Rt))
    yr = d['hy'] - p['puente'] - 1.5                         # v4.1 (I4): puntas rebajadas por la cara de atras
    for sg in (1, -1):
        ya, yb = sorted((sg * yr, sg * (d['rA'] + 2)))
        cut(r, box(-d['rA'], d['rA'], ya, yb, zb - 1, zb + p['rotor_rebaje']))
    join(r, box(-hw, hw, -rbz - EPS, rbz + EPS, zb, zb + p['rotor_alma']))        # alma: puente sobre la espiral
    join(r, cyl((0, 0, zb), (0, 0, zt), p['cubo_radio']))
    cut(r, cyl((0, 0, zb - 1), (0, 0, zt + 1), p['eje_radio'] + p['rotor_holg_eje']))
    rm = p['rotor_radio_iman']
    cut(r, cyl((0, -rm, zt - p['iman_aloj_h']), (0, -rm, zt + 1), p['iman_aloj_d'] / 2))
    if muelle:
        g = grosor or p['muelle_grosor']
        sp = prisma([(espiral(g), [])], 'z', zt - p['muelle_alto'], zt)
        x1 = p['muelle_radio_ext'] + p['muelle_ancla_largo']
        join(sp, box(-x1, -p['muelle_radio_ext'] + g, -p['muelle_ancla_ancho'] / 2, p['muelle_ancla_ancho'] / 2, zt - p['muelle_alto'], zt))
        cut(sp, cyl((-d['rojo'], 0, zb - 1), (-d['rojo'], 0, zt + 1), p['ancla_ojo_d'] / 2))       # ojo del taco
        rotz(sp, p['muelle_ancla_ang'] - (0.0 if montado else p['muelle_precarga']))
        join(r, sp)
    if ang:
        rotz(r, -ang)
    return r

def build_tapa(): return al_mundo(tapa_L())
def build_tapeta(): return al_mundo(tapeta_L())
def build_rotor(): return al_mundo(rotor_L())               # en el montaje, con el taco ya en su muesca

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
    rr = p['reten_funda_r'] + 0.1                            # I4: rebajes donde descansan los nervios de la caja
    for sx in (1, -1):
        xc = sx * (d['Xi'] + p['reten_funda_rebaje'] - rr)
        cut(f, cyl((xc, -p['reten_funda_largo'] / 2 - 1, p['reten_funda_z']), (xc, p['reten_funda_largo'] / 2 + 1, p['reten_funda_z']), rr))
    if ink is not None:
        cut(f, T().copy(ink))
    return f

# ---------------------------------------------------------------- pinza en C, peana y reloj de referencia
def pinza_perfil(st):
    """Contorno (a, n) de la pinza. st = tramo recto del lado del brazo: en la v4 siempre st_lib, la forma libre."""
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

def build_pinza():
    """Pinza en su forma libre, que es la que se imprime. Con 6 mm de mas que el brazalete, montada apenas cambia."""
    p = P
    d = D()
    pol_, _ = pinza_perfil(d['st_lib'])
    return prisma([([an(d, a, n) for a, n in pol_], [])], 'x', -p['pinza_ancho'] / 2, p['pinza_ancho'] / 2)

def build_peana():
    p = P
    d = D()
    R, ab, h, w = d['R'], d['ab'], p['cuna_holgura'], p['cuna_grosor']
    zf, zt = d['zf'], d['zt']
    af, ar = ab + p['cuna_frente'], ab + p['cuna_detras']
    b = prisma([(planta_peana(), [])], 'z', zf, zt)          # base corredera: va sobre el suelo, entre las guias
    o = p['bandeja_oreja']                                   # es un marco: el brazalete cuelga por el hueco hasta casi el suelo
    cut(b, box(-d['xin'], d['xin'], d['yt0'] + o, d['yt1'] - o, zf - 1, zt + 1))
    # v4.1 (I1): reten con lengueta elastica a cada lado; el resalte de la punta cae en una muesca de la guia
    bw_, lg, lr, ll, yp = p['bandeja_ancho'] / 2, p['lengueta_grosor'], p['lengueta_ranura'], p['lengueta_largo'], d['yt0'] + 2.0
    for sx in (1, -1):
        xa, xb = sorted((sx * (bw_ - lg - lr), sx * (bw_ - lg)))
        cut(b, box(xa, xb, yp - lr, yp + ll, zf - 1, zt + 1))
        xa, xb = sorted((sx * (bw_ - lg - lr), sx * (bw_ + 1)))
        cut(b, box(xa, xb, yp - lr, yp, zf - 1, zt + 1))
        xc = sx * (bw_ - 1.0 + p['lengueta_resalte'])
        join(b, cyl((xc, yp + 1.2, zf), (xc, yp + 1.2, zt), 1.0))
    lleno = [(af, -h - w), (ab, -h - w)] + arco(ab, R, R + h + w, 180.0, 360.0)[1:] + [(ar, 2 * R + h + w)]
    u = prisma([([an(d, a, n) for a, n in lleno], [])], 'x', -d['xout'], d['xout'])
    join(u, box(-d['xout'], d['xout'], d['ycu'] - d['ro'], d['ycu'] + d['ro'], zt - EPS, d['zcu']))
    cut(u, box(-d['xin'], d['xin'], -GRANDE / 4, GRANDE / 4, zt, zt + GRANDE / 4))           # paso del brazalete
    cut(u, box(-d['xin'], d['xin'], d['yt0'] + p['bandeja_oreja'], d['yt1'] - p['bandeja_oreja'], zf - 1, zt + EPS))
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
    R, ab, st, g = d['R'], d['ab'], d['st_lib'], p['reloj_grosor']
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
    dentro = [an(d, a, n) for a, n in estadio(0.05)]
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
    """Grado a grado: el panel esta bloqueado si, tirando de el hacia fuera, el rotor choca con el labio de la caja."""
    d = D()
    base, tapa = build_base(), build_tapa()
    tira = C.Matrix3D.create()
    tiron = P['rotor_holg_axial'] + P['holg_corte'] + 0.3    # el panel se mueve esto antes de que el pestillo muerda
    tira.translation = C.Vector3D.create(0, -tiron * K, 0)
    bloq, choca = [], []
    a2 = int(P['rotor_giro'])
    for ang in range(0, a2 + 1):
        r = al_mundo(rotor_L(ang, False))
        if vol_inter(r, tapa) > 0.01 or vol_inter(r, base) > 0.01:
            choca.append(ang)
        r2 = T().copy(r)
        T().transform(r2, tira)
        if vol_inter(r2, base) > 0.01:
            bloq.append(ang)
    out = ['pestillo, grado a grado de 0 a %d (giro de la aguja, a derechas):' % a2]
    out.append('  bloqueado de %d a %d grados; libre desde %d (teorico %.1f)' % (min(bloq), max(bloq), max(bloq) + 1, math.degrees(d['tk'])))
    out.append('  el rotor gira sin tocar caja ni panel en %s' % ('todo el recorrido' if not choca else 'todo menos %s' % choca))
    # el rotor articulado tiene que caber en el mismo panel y la misma caja
    ra = al_mundo(rotor_L(0.0, True, None, True, True))
    out.append('  rotor articulado en reposo: choque con panel %.2f mm3, con caja %.2f mm3' % (vol_inter(ra, tapa), vol_inter(ra, base)))
    libre = [a for a in range(0, a2 + 1) if vol_inter(al_mundo(rotor_L(a, False, None, True, True)), tapa) <= 0.01]
    out.append('  rotor articulado: gira libre dentro del panel de %d a %d grados' % (min(libre), max(libre)))
    # el rotor entra al angulo de montaje sin tocar los puentes
    rm = al_mundo(rotor_L(P['muelle_montaje'], False))
    T().transform(rm, tira_atras())
    out.append('  montaje a %d grados: al meter el rotor por detras roza %.2f mm3 con el panel' % (P['muelle_montaje'], vol_inter(rm, tapa)))
    return out

def tira_atras():
    m = C.Matrix3D.create()
    m.translation = C.Vector3D.create(0, 0.25, 0)
    return m



def check_emergencia():
    """G1: un clip de 1 mm, junto al pestillo de abajo, recorre la ranura de emergencia sin tocar la caja,
    y a lo largo de ese recorrido el pestillo esta a su alcance (el clip llega por encima del fondo de la ranura del pestillo)."""
    p = P
    d = D()
    base = build_base()
    ye = d['Do'] / 2 - (d['cb'] + p['rotor_grosor'] / 2)
    x0, x1 = d['hw'] + 1.0, -(d['rA'] * math.sin(d['tk']) + d['hw'])
    n = int((x0 - x1) / 0.5)
    toca = [round(x0 - i * 0.5, 1) for i in range(n + 1) if vol_inter(cyl((x0 - i * 0.5, ye, -0.5), (x0 - i * 0.5, ye, d['zf'] + 1.5), 0.5), base) > 0.001]
    r = al_mundo(rotor_L(0.0, False))
    alcanza = vol_inter(cyl((d['hw'] - 0.3, ye, -0.5), (d['hw'] - 0.3, ye, d['zf'] + 1.5), 0.5), r) > 0.001
    return ['emergencia: el clip recorre la ranura de x = %.1f a %.1f mm %s; %s' % (x0, x1, 'sin tocar la caja' if not toca else 'y TOCA la caja en %s' % toca, 'el pestillo queda a su alcance' if alcanza else 'NO ALCANZA el pestillo')]

def distancias():
    p = P
    d = D()
    t, R, g = d['t'], d['R'], p['reloj_grosor']
    out = []
    yfr = d['yO'] - p['reloj_diametro'] / 2 * math.sin(t) - g * math.cos(t)
    ztop = an(d, d['ab'] + d['st_lib'], R)[1] + R + p['brazalete_grosor']
    yback = an(d, d['ab'] + d['st_lib'], 2 * R)[0]
    out.append('reloj: cristal a %.1f mm de los carriles | brazalete a %.1f mm del techo | hueco tras la pinza %.1f mm' % (yfr - d['yF'] - p['carril_alto'], d['zf'] + d['ch'] - ztop, d['yB'] - yback))
    ymov, zmov = an(d, 0, -g / 2)
    yim = -d['Do'] / 2 + p['tapa_piel'] + p['iman_central_retiro'] + p['iman_h'] / 2
    out.append('imanes -> centro del movimiento: central %.1f mm | del rotor %.1f mm' % (math.hypot(ymov - yim, zmov - d['zp']), math.hypot(ymov - yim, zmov - (d['zp'] - p['rotor_radio_iman']))))
    out.append('pinza: contorno libre %.1f mm para un brazalete de %.0f | alto libre %.1f mm' % (contorno(pinza_perfil(d['st_lib'])[1]), p['brazalete_contorno'], d['st_lib'] + 2 * R))
    a = articulado_datos()
    out.append('pico articulado (calculo): brazo %.1f / %.1f mm, bascula %.1f grados, lamina al %.2f %%, se aparta %.1f mm de lado, %.2f N por pico; limite de rozamiento por palanca %.2f, pero manda el roce del pico contra la piel: 0.35 segun contra-reporte-v4' % (a['bx'], a['bz'], a['giro'], a['eps'], a['lado'], a['F'], a['mu']))
    out.append('exterior con funda: %.1f x %.1f x %.1f mm (ancho x fondo x alto) | caja interior %.1f x %.1f x %.1f | panel %.1f de grueso' % (2 * d['Xo'], 2 * d['Yo'], d['Zo'], d['L'], d['Do'], d['Ho'], p['tapa_alto']))
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
            ('tapeta', o(build_tapeta(), M_FRENTE_ARRIBA())), ('rotor', o(al_mundo(rotor_L(0.0, True, None, False)), M_FRENTE_ABAJO())),
            ('aguja', needle()), ('peana', build_peana()), ('pinza', o(build_pinza(), M_DE_LADO())),
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
    # I9: pastilla con un iman embutido con pausa, para comparar su fuerza con la de uno suelto
    pc = box(0, 14, 0, 14, 0, p['aguja_grosor'])
    cut(pc, cyl((7, 7, p['aguja_suelo']), (7, 7, p['aguja_suelo'] + p['iman_aloj_h']), p['iman_aloj_d'] / 2))
    out.append(('p0-iman-embutido', pc))
    # P1: llave. Panel, tapa trasera, tres rotores (espiral fina, media y gruesa) y aguja de prueba
    for nombre, body, m in (('p1-panel', build_tapa(), M_FRENTE_ABAJO()), ('p1-tapa-trasera', build_tapeta(), M_FRENTE_ARRIBA())):
        T().transform(body, m)
        out.append((nombre, body))
    for nombre, g in MUELLES:
        r = al_mundo(rotor_L(0.0, True, g, False))
        T().transform(r, M_FRENTE_ABAJO())
        out.append(('p1-rotor-muelle-%s' % nombre, r))
    out.append(('p1-aguja-de-prueba', needle(prueba=True)))
    # P2: aro de la boca (cierre con la aguja puesta, tiron, emergencia) y rotor articulado (cierre de un empujon)
    aro = build_base()
    inter(aro, half((0, -d['Do'] / 2 + 15, 0), (0, -1, 0)))
    T().transform(aro, M_FRENTE_ARRIBA())
    out.append(('p2-aro-de-la-boca', aro))
    ra = al_mundo(rotor_L(0.0, True, None, False, True))
    T().transform(ra, M_FRENTE_ABAJO())
    out.append(('p2-rotor-articulado', ra))
    # P3: pinza, peana y una rebanada de la caja con suelo, guias, techo y pared trasera
    pz = build_pinza()
    T().transform(pz, M_DE_LADO())
    out.append(('p3-pinza', pz))
    out.append(('p3-peana', build_peana()))
    nicho = build_base()
    w = p['bandeja_ancho'] / 2 + p['holg_tapa'] + p['guia_pared'] + 3
    inter(nicho, box(-w, w, -d['Do'], d['Do'], -1, d['Ho'] + 1))
    T().transform(nicho, M_FRENTE_ARRIBA())
    out.append(('p3-rebanada-de-caja', nicho))
    # P4: funda corta (techo con la frase y borde con los rebajes del reten) y vaso con los nervios, para lastrarlo
    alto = 40.0
    ink, centro = build_frase()
    fu = build_funda(ink, centro)
    abajo = T().copy(fu)
    inter(fu, half((0, 0, d['Zo'] - alto / 2), (0, 0, 1)))
    inter(abajo, half((0, 0, alto / 2), (0, 0, -1)))
    mover(abajo, 0, 0, d['Zo'] - alto)
    join(fu, abajo)
    T().transform(fu, M_TECHO_ABAJO())
    out.append(('p4-funda-corta', fu))
    T().transform(ink, M_TECHO_ABAJO())
    out.append(('p4-frase', ink))
    re, hv = p['redondeo_ext'], alto - p['funda_techo'] - p['holg_desliza']
    cj = rbox(-d['L'] / 2, d['L'] / 2, -d['Do'] / 2, d['Do'] / 2, -2 * re, hv + 2 * re, re)
    inter(cj, box(-d['L'], d['L'], -d['Do'], d['Do'], 0, hv))
    cut(cj, box(-d['L'] / 2 + 2, d['L'] / 2 - 2, -d['Do'] / 2 + 2, d['Do'] / 2 - 2, 2, hv + 1))
    for sx in (1, -1):
        xc = sx * (d['L'] / 2 - (p['reten_funda_r'] - p['reten_funda_sale']))
        join(cj, cyl((xc, -p['reten_funda_largo'] / 2, p['reten_funda_z']), (xc, p['reten_funda_largo'] / 2, p['reten_funda_z']), p['reten_funda_r']))
    out.append(('p4-vaso-para-lastrar', cj))
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
        out += check_emergencia()
    out += distancias()
    app().activeViewport.fit()
    return out
