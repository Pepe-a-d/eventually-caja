import math, numpy as np
t=math.radians(25); R=23.0; st=7.0; reloj_g=11; asa=44; D=40
pared=3; techo=3.4; nicho_f=80; nicho_h=72; tapa=4.6
Do=pared+nicho_f+tapa; Ho=nicho_h+2*techo
yF=-Do/2+tapa; yB=Do/2-pared; zf=techo; z0=zf-1.2; zp=Ho/2
zc=z0+4.5+st*math.cos(t)+R
yc=yF+5+(R+reloj_g)*math.cos(t)+asa/2*math.sin(t)
a=np.array([math.sin(t), math.cos(t)]); n=np.array([-math.cos(t), math.sin(t)])
C=np.array([yc,zc])
print(f"centro del anillo: y={yc:.1f} z={zc:.1f} | frente interior yF={yF:.1f} | fondo yB={yB:.1f} | suelo zf={zf} techo {zf+nicho_h}")
# contorno del anillo (estadio)
pts=[]
for k in range(360):
    th=math.radians(k)
    c=C+ (st if math.cos(th)>=0 else -st)*a
    pts.append(c+R*(math.cos(th)*a+math.sin(th)*n))
ring=np.array(pts)
per_ring=2*(2*st)+2*math.pi*R
print(f"perimetro del anillo: {per_ring:.1f} mm  (ovalo {2*(R+st):.0f} x {2*R:.0f})")
pat=np.array([[yc-34,z0],[yc+22,z0],[yc+22,z0+14],[yc-34,z0+14]])
allp=np.vstack([ring,pat])
def hull(P):
    P=sorted(map(tuple,P)); 
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[]
    for p in P:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    up=[]
    for p in reversed(P):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return np.array(lo[:-1]+up[:-1])
h=hull(allp); per=sum(np.linalg.norm(h[i]-h[(i+1)%len(h)]) for i in range(len(h)))
print(f"contorno minimo que rodea anillo + patin (lo que tiene que saltar el brazalete): {per:.1f} mm")
for muneca in (165,175,185):
    print(f"  brazalete ajustado a muneca de {muneca} mm: cerrado {'NO cierra' if muneca<per_ring else 'holgura %.0f mm'%(muneca-per_ring)} sobre el anillo")
# reloj
s=R+reloj_g
head=C+ (R+reloj_g/2)*n
low=C+s*n-asa/2*a; top=C+s*n+asa/2*a
print(f"reloj: punto bajo-delantero y={low[0]:.1f} z={low[1]:.1f} | alto z={top[1]:.1f} (techo {zf+nicho_h:.1f}) | frente del patin y={yc-34:.1f}")
print(f"  el reloj vuela {(yc-34)-low[0]:.1f} mm por delante del patin; cdg de la cabeza a {head[0]-(yc-34):.1f} mm por detras del frente del patin")
# imanes y movimiento
def Bz(z,Rm=2.5,h=1.6,Br=1.2): return Br/2*((z+h)/math.hypot(z+h,Rm)-z/math.hypot(z,Rm))*1000
yiman=-Do/2+1+0.8
d_c=math.hypot(head[0]-yiman, head[1]-zp); d_r=math.hypot(head[0]-yiman, head[1]-(zp-13.5))
print(f"iman central -> centro del movimiento {d_c:.1f} mm ; del rotor {d_r:.1f} mm")
for z in (4,8,11,15,24,31,52):
    print(f"  campo en el eje de un iman 5x1.6 a {z:2d} mm: {Bz(z):6.2f} mT = {Bz(z)*1e-3/(4e-7*math.pi):6.0f} A/m (ISO 764: 4800 A/m)")
pm=np.array([19.0, yc-6, z0+2.2]); mov=np.array([0, head[0], head[1]])
print(f"iman de patin -> centro del movimiento: {np.linalg.norm(pm-mov):.1f} mm")
# pestillo
Rr=37.3; hw=4.5; half=math.degrees(math.asin(hw/Rr))
free=half+math.degrees(math.acos(36/Rr))
print(f"rotor: queda libre a partir de {free:.1f} grados (extremo redondeado, semiancho angular {half:.1f})")
for th in (0,4,10,15,20):
    e=Rr*math.cos(math.radians(max(th-half,0)))-36
    print(f"  enganche a {th:2d} grados: {e:.2f} mm")
# gravedad
m_iman=math.pi*2.5**2*1.6*7.5e-6; m_rotor=1.4*1.24e-3+m_iman
for th in (40,20,10,5):
    print(f"  par de gravedad a {th:2d} grados: {m_iman*9.81*0.0135*math.sin(math.radians(th))*1e6:5.1f} uN·m")
print(f"  par de rozamiento del rotor sobre su eje (mu=0.3, peso {m_rotor*1000:.1f} g, radio 4.3 mm): {0.3*m_rotor*9.81*0.0043*1e6:.1f} uN·m")
print(f"par de arrastre maximo de la aguja (0.59 N a 13.5 mm): {0.59*13.5:.1f} mN·m = {0.59*13.5*1000:.0f} uN·m")
# tarjeta
print(f"tarjeta: hueco entre guias {88-2*2.5} mm para tarjeta de 85 -> solape {(85-83)/2:.1f} mm por lado; zona tapada por el soporte (46 mm): se ven {(85-46)/2:.1f} mm a cada lado")
# cierre del brazalete
print(f"brazalete tras el anillo: pared trasera a {yB-(yc+st*math.sin(t)+R):.1f} mm del anillo; con brazalete 3.5 quedan {yB-(yc+st*math.sin(t)+R)-3.5:.1f}; con cierre de 7 mm quedan {yB-(yc+st*math.sin(t)+R)-7:.1f}")
print(f"bajo el anillo: {4.5} mm libres (brazalete 3.5)")
