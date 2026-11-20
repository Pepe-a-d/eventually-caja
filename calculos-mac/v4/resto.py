import numpy as np, math
from malla import carga, rayo
rad=math.radians; deg=math.degrees
P=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','probetas-v4','')
Do=71.38; Ho=92.68; ch=84.68; cl=88; hy=ch/2-0.2; hw=4; Rt=ch/2+2; rA=math.hypot(hw,Rt); Rc=rA+0.3
# ---- 1. puentes del panel: luz libre sobre la camara
V,T,_,_=carga(P+'p1-panel.3mf'); yc=-Ho/2; zf=-Do/2
print("PANEL (malla): banda maciza tras el pestillo y camara debajo")
for yy in (36.5, 39.0, 41.5):
    for nombre, z in (("camara", zf+1.4+1.6), ("banda ", zf+4.7+0.9)):
        for signo, eti in ((+1,"arriba"),(-1,"abajo ")):
            ts=rayo(V,T,(-60, yc+signo*yy, z),(1,0,0)); xs=[round(t-60,1) for t in ts]
            print(f"  {eti} y={yy:4.1f} {nombre}: cortes en x = {xs}")
print("  juego axial del rotor bajo la banda: 0,30 mm en total")
# ---- 2. peana corredera
t=rad(10); R=15; pl=43; st=(186-2*math.pi*R)/2; ab=-pl/2
yF=-Do/2+6.6; zO=4+4.5+R+pl/2*math.cos(t)+R*math.sin(t); yO=yF+1.7+3+20*math.sin(t)+11*math.cos(t)
an=lambda a,n:(yO+a*math.sin(t)+n*math.cos(t), zO+a*math.cos(t)-n*math.sin(t))
ycu,zcu=an(ab,R); ro=R+0.3+3; yt0=ycu-ro-2; yt1=ycu+ro+2
print(f"\nPEANA: base de {yt1-yt0:.1f} mm de largo; su frente queda a {yt0-yF:.1f} mm del panel (a {yt0-yF-1.7:.1f} de los carriles); las guias empiezan {yt0-3-yF:.1f} mm detras del panel")
print(f"  bajo de la pinza a {zcu-R-4:.1f} mm del suelo; brazalete de 3,5 -> queda a {zcu-R-4-3.5:.1f} mm del suelo (por el hueco del marco)")
print(f"  reten: resalte 0,35 en cada guia con 0,20 de holgura -> aprieto de {0.35-0.2:.2f} mm por lado entre piezas rigidas (pared de guia de 2 mm y 3,85 de alto)")
k_guia=3000*2**3/(4*1.2**3)   # N/mm por mm de largo, voladizo cargado a 1,2 mm de la raiz
print(f"  rigidez de la pared de la guia donde aprieta: ~{k_guia:.0f} N/mm por mm de largo -> para ceder 0,15 mm en 1,2 mm de largo: ~{k_guia*1.2*0.15:.0f} N por lado")
ztop=an(ab+st,R)[1]+R+3.5; print(f"  brazalete a {4+ch-ztop:.1f} mm del techo; pinza libre de {st+2*R:.1f} mm de alto")
# ---- 3. reten de la funda
print("\nFUNDA: nervio de radio 1,5 que sale 0,5; holgura 0,30; rebaje 0,30")
E=3000
for nombre,L_,bef in (("funda entera (pared de 76 x 95)",76,25),("funda corta de P4 (pared de 76 x 40)",76,45)):
    for apoyo,c in (("apoyada",48),("empotrada",192)):
        k=c*E*(bef*2**3/12)/L_**3
        best=0
        for i in range(1,200):
            dl=0.2*i/200; p=0.3+dl; s=math.sqrt(max(2.25-(1+p)**2,0)); al=math.atan2(s,1+p)
            best=max(best,k*dl*math.tan(al+math.atan(0.3)))
        print(f"  {nombre}, {apoyo}: rigidez ~{k:.0f} N/mm -> retencion maxima ~{2*best:.1f} N con los dos nervios (peso estimado 2,6 N)")
# ---- 4. la aguja como tirador
print("\nAGUJA COMO TIRADOR: imanes a u=0 (0,78 N) y u=-16 (0,89 N); panel sujeto con 1,22 N")
for u in (-16,-8,0,8,14,25):
    # se despega cuando la traccion en un iman supera su fuerza: reparto por momentos
    Fa = min(0.78/((u+16)/16), 0.89/((0-u)/16)) if -16<u<0 else (0.78*16/(u+16) if u>=0 else 0.89)
    print(f"  tirando a {u:+3d} mm del centro: la aguja se despega con {Fa:.2f} N -> {'saca el panel' if Fa>1.22 else 'se queda la aguja en la mano'}")
# ---- 5. pico articulado: empujon
print("\nPICO ARTICULADO: el rotor cede a derechas y el pico baja sin resbalar de lado")
bx,bz=11.18,14.73
phi=2.2/(bx-2.5*bz/Rt); dl=bz*phi/Rt
EI=3000*3*0.6**3/12; Fflex=EI*phi/6/bx
print(f"  la lamina dobla {deg(phi):.1f} grados; el rotor cede {deg(dl):.1f} grados; fuerza para doblar {Fflex:.2f} N por pico")
for mu in (0.2,0.3,0.35,0.4,0.45):
    r=(1+mu)/(1-mu); den=1-mu*r
    if den<=0: print(f"  mu={mu}: SE ACUNA (el roce del pico contra la piel se come el empuje)"); continue
    Fv=Fflex/den; print(f"  mu={mu}: empuje por pico {Fv*r:.1f} N -> {2*Fv*r:.1f} N en total")
print(f"  limite: mu = {math.sqrt(2)-1:.2f}")
# ---- 6. labio de la caja y ranura
print(f"\nLABIO que retiene el pestillo: 1,25 mm de grueso, vuela {Rc-ch/2:.2f} mm sobre una cuerda de {2*math.sqrt(Rc*Rc-(ch/2)**2):.1f} mm; holgura hacia el rotor 0,15 mm")
