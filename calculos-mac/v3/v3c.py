import math, sys
sys.path.insert(0,'.')
from imanes import force
rad=math.radians; deg=math.degrees
ch=83.72; hy=ch/2-0.2; hw=4.0; zA=ch/2+2; rA=math.hypot(hw,zA); phiA=math.atan2(hw,zA); ts=rad(13.7)
print("RESBALON, contacto real: la boca es una arista horizontal -> empuja el pico en vertical")
print(" giro | pico x,y | mm de lado por mm de avance | gira si mu < (solo pico) | (con roce contra la piel)")
for th in (0,2,4.5,8,11,13.7):
    a=phiA+rad(th); x=rA*math.sin(a); y=rA*math.cos(a)
    lat=y/x
    mu1=x*math.sqrt(y*y+2*x*x)/(math.sqrt(2)*rA*rA)
    mu2=(x/math.sqrt(2))/(rA*rA/math.sqrt(y*y+2*x*x)+40/math.sqrt(2))
    print(f" {th:4.1f} | {-x:5.1f},{y:5.1f} | {lat:4.1f} | {mu1:.3f} | {mu2:.3f}")
print("\nPICO BASCULANTE (propuesta): brazo corto a 45 grados, articulado en una lamina")
for (x,y) in ((8,8),(11,11),(14,10)):
    r=math.hypot(x,y); mu1=x*math.sqrt(y*y+2*x*x)/(math.sqrt(2)*r*r)
    dth=2.2/x; 
    for l in (4,6):
        eps=0.6*dth/(2*l)
        print(f" brazo ({x},{y}) mm: gira si mu < {mu1:.2f}; baja 2,2 mm con {deg(dth):.0f} grados; lamina 0,6 x {l} mm -> deformacion {eps*100:.1f} %")
print("\nIMANES: fuerza entre dos discos 5x1.6 enfrentados (N35)")
for g in (1.6,2.0,2.2,2.6,3.0,3.6):
    fx,fz=force(gap=g*1e-3); print(f"  {g:.1f} mm -> {abs(fz):.2f} N")
print("\nMUELLE con tope y precarga (rotor en un solo sentido)")
E=3000; b=1.6; r0=5.6
for g in (0.6,0.7,0.8):
    r1=11.6-g/2; L=0.5*(r0+r1)*rad(540); k=E*b*g**3/12/L*rad(1)*1000  # uN·m/grado
    for pre in (0,10,20):
        print(f"  {g} mm, precarga {pre:2d} grados: par en reposo {k*pre:4.0f} uN·m (rozamiento 40 de pie / 193 tumbado) | par a 50 grados {k*(50+pre)/1000:.2f} mN·m | deformacion {g/2*rad(50+pre)/L*100:.2f} %")
# golpe lateral que abre el pestillo hacia el lado del resbalon
k06=E*b*0.6**3/12/(0.5*(5.6+11.3)*rad(540))   # N·mm/rad
En=0.5*k06*1e-3*ts**2; I=0.0033*0.088**2/12; mr=0.24e-3*0.016
dv=math.sqrt(2*En*I)/mr
print(f"\ngolpe: energia para girar 13.7 grados {En*1e6:.0f} uJ -> cambio brusco de velocidad lateral de {dv:.1f} m/s (caida de {dv*dv/19.6*100:.0f} cm de canto)")
