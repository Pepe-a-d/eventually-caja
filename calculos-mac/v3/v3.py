import math, numpy as np
rad=math.radians; deg=math.degrees
# ---------- parametros v3 ----------
R=15.0; pl=43.0; cont=180.0; cont_lib=200.0; t=rad(10)
pie=5; bz=3.5; aire_arr=3; reloj_g=11; reloj_d=40; asa=44
carril_alto=0.9+0.8; aire_fr=3; hueco=8; aire_det=1
st_nom=(cont-2*math.pi*R)/2; st_lib=(cont_lib-2*math.pi*R)/2
nicho_alto=pie+2*R+st_nom*math.cos(t)+bz+aire_arr
nicho_fondo=carril_alto+aire_fr+reloj_d/2*math.sin(t)+reloj_g*math.cos(t)+2*R*math.cos(t)+(st_nom-pl/2)*math.sin(t)+hueco+aire_det
tapa_alto=1.4+3+0.3+1.2+0.1
print(f"st_nom {st_nom:.1f} st_lib {st_lib:.1f} | nicho alto {nicho_alto:.1f} fondo {nicho_fondo:.1f} | caja {88+6:.1f} x {3+nicho_fondo+tapa_alto:.1f} x {nicho_alto+8:.1f}")
# ---------- 1. resbalon ----------
ch=nicho_alto; hy=ch/2-0.2; hw=4.0; eng=2.0; zA=ch/2+eng
lo,hi=0,rad(45)
for _ in range(60):
    m=(lo+hi)/2
    if hy+hw*math.sin(m)<zA*math.cos(m): lo=m
    else: hi=m
ts=(lo+hi)/2; rA=math.hypot(hw,zA); phiA=math.atan2(hw,zA); tk=phiA+math.acos(hy/rA)
print(f"\nRESBALON: giro {deg(ts):.1f} grados, pico a radio {rA:.1f}, apertura con aguja {deg(tk):.1f}")
brazo_normal=rA*math.sin(phiA+ts)/math.sqrt(2)      # palanca de la fuerza normal del chaflan (45 grados), por N
desl_lat=rA*ts; print(f"  el pico recorre {desl_lat:.1f} mm de lado para bajar {eng:.1f} mm; el panel solo avanza ~2 mm")
k_lat=desl_lat/2.0   # mm de deslizamiento lateral por mm de avance axial (tabla del report: 13 grados en ~2 mm)
f_lat=k_lat/math.hypot(k_lat,1)
print(f"  palanca que hace girar: {brazo_normal:.1f} mm por N de contacto | palanca del rozamiento en el pico: {f_lat*rA:.1f} mm por (mu N)")
mu_crit=brazo_normal/(f_lat*rA)
print(f"  solo el pico: gira si mu < {mu_crit:.2f}")
r_cara=40.0   # el empuje axial aprieta el brazo contra la piel cerca del extremo
mu_crit2=brazo_normal/(f_lat*rA+r_cara/math.sqrt(2))
print(f"  contando el roce del brazo contra la piel (reaccion axial N/raiz2 a ~{r_cara:.0f} mm): gira si mu < {mu_crit2:.2f}")
for mu in (0.15,0.2,0.3,0.4):
    print(f"   mu={mu}: par motor {brazo_normal:.1f} N·mm/N frente a resistente {mu*(f_lat*rA+r_cara/math.sqrt(2)):.1f} -> {'pasa' if brazo_normal>mu*(f_lat*rA+r_cara/math.sqrt(2)) else 'SE ACUNA'}")
# que angulo de presion haria falta
for alpha in (20,30,40,45):
    a=rad(alpha); rr=hy/math.cos(a)+2
    d_rot=eng/(rr*math.sin(a)); lat=eng/math.tan(a)
    print(f"   pico a {alpha} grados de la vertical: baja 2 mm con {deg(d_rot):.1f} grados y {lat:.1f} mm de lado; gira si mu < {math.tan(a)/math.sqrt(2)/ (1+0.3):.2f} aprox.")
# ---------- 2. muelle ----------
E=3000; b=1.6; r0=5.6
for g in (0.45,0.6,0.8):
    r1=11.6-g/2; L=0.5*(r0+r1)*rad(540); I=b*g**3/12
    k=E*I/L*rad(1)   # N·mm por grado
    print(f"\nMUELLE {g} mm: largo {L:.0f} mm, rigidez {k*1000:.1f} uN·m/grado, a 50 grados {k*50:.2f} mN·m, a -13.7 {k*13.7:.2f}")
    m_rotor=(8*3*88+math.pi*36*3)*1.24e-6+0.24e-3  # kg aprox
    W=m_rotor*9.81
    for nombre,par in (("de pie (roza en el eje, r 4.15)",0.3*W*4.15),("tumbado (apoya de plano, r~20)",0.3*W*20)):
        print(f"   rozamiento {nombre}: {par*1000:.0f} uN·m -> zona muerta ±{par/k:.1f} grados")
print(f"  masa del rotor ~{m_rotor*1000:.1f} g")
def enganche(th):
    a=phiA+rad(th)
    # altura del pico (lado aguja, +) o del pico girado a izquierdas (-)
    if th>=0: y=rA*math.cos(a)
    else: y=rA*math.cos(phiA-rad(th))  # hacia el resbalon el pico baja
    # el otro extremo del canto inclinado sube al girar a derechas hasta ts
    return y-hy
for th in (-10,-8,-5,-2,0,2,5):
    yv=max(rA*math.cos(phiA+rad(abs(th)) if th<0 else phiA+rad(th)), 0)
print("  (enganche del report: 2.0 a 0 grados, >1 mm entre -8 y +18.5, maximo 2.2 a +5)")
# ---------- 3. pinza: forma real con el brazalete puesto ----------
ab=-pl/2
def arco(ca,cb,r,g0,g1,n=60):
    return [(ca+r*math.sin(rad(g0+(g1-g0)*i/n)), cb+r*math.cos(rad(g0+(g1-g0)*i/n))) for i in range(n+1)]
def ext(st):
    at=ab+st
    pts=[(pl/2,0.0),(ab,0.0)]+arco(ab,R,R,180,360)[1:]
    a1=ab+8; a2=min(a1+6,at-0.5)
    pts+= [(a1,2*R),(a2,2*R)]
    arm=[(at,2*R)]+arco(at,R,R,0,deg(math.acos((5-R)/R)))[1:]
    return pts, arm, (a2,2*R)
def hull_per(P):
    P=sorted(set((round(x,3),round(y,3)) for x,y in P))
    cr=lambda o,a,b:(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for q in P:
        while len(lo)>=2 and cr(lo[-2],lo[-1],q)<=0: lo.pop()
        lo.append(q)
    for q in reversed(P):
        while len(up)>=2 and cr(up[-2],up[-1],q)<=0: up.pop()
        up.append(q)
    h=lo[:-1]+up[:-1]
    return sum(math.hypot(h[i][0]-h[i-1][0],h[i][1]-h[i-1][1]) for i in range(len(h)))
fijo, brazo, piv = ext(st_lib)
print(f"\nPINZA impresa (libre): contorno {hull_per(fijo+brazo):.1f} mm, alto {max(a for a,n in fijo+brazo)-min(a for a,n in fijo+brazo):.1f} mm")
mod_f, mod_b, _ = ext(st_nom)
print(f"PINZA tal como esta en el montaje de Fusion (st_nom): contorno {hull_per(mod_f+mod_b):.1f} mm, alto {max(a for a,n in mod_f+mod_b)-min(a for a,n in mod_f+mod_b):.1f} mm")
def girado(beta):
    c,s=math.cos(beta),math.sin(beta); out=[]
    for a,n in brazo:
        da,dn=a-piv[0],n-piv[1]
        out.append((piv[0]+da*c+dn*s, piv[1]-da*s+dn*c))   # gira el brazo hacia la cara plana (n decrece)
    return out
for objetivo in (190,180,170,160):
    lo,hi=0.0,rad(80)
    for _ in range(60):
        m=(lo+hi)/2
        if hull_per(fijo+girado(m))>objetivo: lo=m
        else: hi=m
    beta=(lo+hi)/2; G=girado(beta)
    alto=max(a for a,n in fijo+G)-min(a for a,n in fijo+G)
    nmin=min(n for a,n in G); larm=st_lib-14
    print(f"  brazalete {objetivo}: el brazo gira {deg(beta):.0f} grados; alto real {alto:.1f} mm; la punta llega a n={nmin:.1f} (n<0 = por delante de la cara plana); deformacion del PETG ~{0.8*beta/larm*100:.1f} %")
alto_mod=2*R+st_nom
print(f"  el nicho se calculo para una pinza de {alto_mod:.1f} mm de alto + {bz} de brazalete + {aire_arr} de aire")
