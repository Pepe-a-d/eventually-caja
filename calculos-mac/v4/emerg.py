import numpy as np, math
from malla import carga, rayo
P=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','probetas-v4','')
V,T,_,_=carga(P+'p2-aro-de-la-boca.3mf')
zrot=35.69-3.2
print("ARO DE LA BOCA: rayo vertical desde debajo de la base, en el plano medio del rotor")
print("  x   | cortes (altura en mm sobre la mesa) -> tramos macizos entre pares")
for x in (6.0,5.0,4.5,2.0,0.3,0.0,-2.0,-5.0,-8.0,-10.0,-13.0,-14.0,-20.0,-24.0):
    ts=rayo(V,T,(x,-1.0,zrot),(0,1,0)); hs=[round(t-1.0,2) for t in ts if t-1.0<8]
    print(f" {x:5.1f} | {hs}")
# perfil del fondo de la ranura del pestillo y techo de la ranura de emergencia, teorico
ch=84.68; hw=4; Rt=ch/2+2; rA=math.hypot(hw,Rt); Rc=rA+0.3; zf=4
print(f"teorico: techo de la ranura de emergencia a {zf-(Rc-ch/2)+0.01:.2f} mm; fondo de la ranura del pestillo:")
for x in (0,2,4,5,6,8,10,13,14):
    print(f"   x=±{x}: fondo a {zf-(math.sqrt(Rc*Rc-x*x)-ch/2):.2f} -> plastico entre las dos ranuras {max(0,(Rc-math.sqrt(Rc*Rc-x*x))-0.01):.2f} mm")
tk=math.asin(hw/Rt)+math.acos((ch/2-0.2)/Rt)
print(f"apertura a {math.degrees(tk):.1f} grados; la esquina de arrastre del pestillo acaba en x = {hw*math.cos(tk)-Rt*math.sin(tk):.1f}")
for xc in (-3,-5,-6,-8):
    # angulo del rotor cuando la esquina derecha del pestillo de abajo esta en xc-0.5
    lo,hi=0,tk
    for _ in range(50):
        m=(lo+hi)/2
        if hw*math.cos(m)-Rt*math.sin(m) > xc-0.5: lo=m
        else: hi=m
    th=lo; top=Rt*math.cos(max(0,th-math.asin(hw/Rt)))
    print(f"   clip parado en x={xc}: rotor a {math.degrees(th):.1f} grados, enganche que queda {top-(ch/2):.2f} mm")
# labio que retiene el pestillo
print(f"labio delante de la ranura del pestillo: {1.4-0.15:.2f} mm de grueso; cuerda de la ranura {2*math.sqrt(Rc*Rc-(ch/2)**2):.1f} mm; fondo {Rc-ch/2:.2f} mm")
