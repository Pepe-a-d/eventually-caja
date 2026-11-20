import numpy as np, math
from malla import carga, rayo
P=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','probetas-v4','')
D=np.array((0.123,0.957,0.262)); D/=np.linalg.norm(D)
def dentro(M, p):
    return len([t for t in rayo(M[0],M[1],p,D) if t>1e-6])%2==1
Do2,Ho2=35.69,46.34
cb,ct,zs=66.68,69.98,64.78
# panel y rotor: malla = (xL, -(yL+Ho2), Do2 - zL) ; tapa trasera y aro: malla = (xL, yL+Ho2, zL-Do2)
def pA(x,y,z): return (x, -(y+Ho2), Do2-z)      # frente abajo
def pB(x,y,z): return (x, y+Ho2, z-Do2)         # frente arriba
pan=carga(P+'p1-panel.3mf')[:2]; tap=carga(P+'p1-tapa-trasera.3mf')[:2]; rot=carga(P+'p1-rotor-muelle-medio.3mf')[:2]
pol=lambda r,g:(r*math.cos(math.radians(g)), r*math.sin(math.radians(g)))
print("C1) PANEL: mapa del canal del taco a zL=68.9 (#=plastico, .=hueco); filas r=17..10.5, columnas angulo 108..204 cada 2")
for r in np.arange(17,10.4,-0.5):
    print(f"  r={r:4.1f} "+''.join('#' if dentro(pan,pA(*pol(r,g),68.9)) else '.' for g in range(108,206,2)))
def borde(f, a, b):
    fa=f(a)
    for _ in range(40):
        m=(a+b)/2
        if f(m)==fa: a=m
        else: b=m
    return (a+b)/2
for r in (12.0,13.6,15.6):
    g0=borde(lambda g: dentro(pan,pA(*pol(r,g),68.9)), 105,125); g1=borde(lambda g: dentro(pan,pA(*pol(r,g),68.9)), 215,190)
    print(f"  r={r}: el canal va de {g0:.2f} a {g1:.2f} grados")
print("  pared exterior del canal en 189 y 150 grados:", [round(borde(lambda r: dentro(pan,pA(*pol(r,g),68.9)), 14,18),3) for g in (189,150,171)])
print("C2) PANEL: teton. Corte a zL=69.5 alrededor de (13.6,189):")
xt,yt=pol(13.6,189)
for dz in (68.4,68.6,68.7,69.0,69.9):
    rr=[borde(lambda r: dentro(pan,pA(xt+r*math.cos(a),yt+r*math.sin(a),dz)),0.0,1.6) if dentro(pan,pA(xt,yt,dz)) else None for a in (0,1.57,3.14,4.71)]
    print(f"   zL={dz}: centro dentro={dentro(pan,pA(xt,yt,dz))} radios={rr}")
print("C3) ROTOR impreso (relajado): taco y ojo a zL=68.9. centro esperado del ojo:", [round(v,2) for v in pol(13.6,171)])
xo,yo=pol(13.6,171)
print("   ojo: centro hueco=", not dentro(rot,pA(xo,yo,68.9)), " radios del ojo:", [round(borde(lambda r: dentro(rot,pA(xo+r*math.cos(a),yo+r*math.sin(a),68.9)),0.0,1.8),2) for a in (0,1.57,3.14,4.71)])
for r in (11.2,12,13,14,15,15.5):
    g0=borde(lambda g: dentro(rot,pA(*pol(r,g),68.9)), 155,171 if r<12.4 or r>14.8 else 165.9); g1=borde(lambda g: dentro(rot,pA(*pol(r,g),68.9)), 190,171 if r<12.4 or r>14.8 else 176.5)
    print(f"   r={r}: taco de {g0:.2f} a {g1:.2f} grados")
print("   radio exterior del taco a 171:", round(borde(lambda r: dentro(rot,pA(*pol(r,171),68.9)), 15.0,17),3), " grosor del rotor en la punta (x=0,yL=40) y en el brazo (yL=25):")
for y in (40,36,34.5,33.5,25,-40):
    ts=rayo(rot[0],rot[1],pA(0.5,y,60),(0,0,-1)); print(f"     yL={y}: zL de {[round(60+t,2) for t in ts]}")
print("D) TAPA TRASERA: resalte sobre el taco, pestana y clip")
ts=rayo(tap[0],tap[1],pB(xt,yt,60),(0,0,1)); print("   en el teton (13.6,189): zL", [round(60+t,2) for t in ts], " cb=",cb)
for x,y in ((-19,35.0),(-19,36.0),(-19,37.3),(-19,37.6),(-9.5,36.5),(-29,36.5)):
    ts=rayo(tap[0],tap[1],pB(x,y,60),(0,0,1)); print(f"   pestana x={x} yL={y}: zL {[round(60+t,2) for t in ts]}")
for x in (9,11,16,20,21,22.5):
    ts=rayo(tap[0],tap[1],pB(x,-30,62),(0,-1,0)); print(f"   clip x={x}: cortes en yL bajando a zL=66: ", end='')
    ts=rayo(tap[0],tap[1],pB(x,-30,66.0),(0,-1,0)); print([round(-30-t,2) for t in ts])
print("   resalte del clip: a x=21, yL=-35.8 (fuera del borde -35.49), cortes a lo largo de z:", [round(60+t,2) for t in rayo(tap[0],tap[1],pB(21,-35.8,60),(0,0,1))])
print("C4) PANEL: muesca del clip. a x=21, yL=-35.8: cortes a lo largo de z (de atras adelante):", [round(60+t,2) for t in rayo(pan[0],pan[1],pA(21,-35.8,60),(0,0,-1)) ] if False else '')
ts=rayo(pan[0],pan[1],(21,-(-35.8+Ho2),Do2-60),(0,0,-1)); print("   panel a x=21,yL=-35.8: zL", [round(60+t,2) for t in ts], " (cara trasera zs=64.78, cb=66.68)")
ts=rayo(pan[0],pan[1],(21,-(-36.3+Ho2),Do2-60),(0,0,-1)); print("   panel a x=21,yL=-36.3: zL", [round(60+t,2) for t in ts])
ts=rayo(pan[0],pan[1],(15,-(-35.8+Ho2),Do2-60),(0,0,-1)); print("   panel a x=15,yL=-35.8: zL", [round(60+t,2) for t in ts])
print("   panel, ranura de la pestana: x=-19, yL=36.5 y 37.5 y 38.2:")
for y in (35.8,36.5,37.5,37.9,38.2):
    ts=rayo(pan[0],pan[1],(-19,-(y+Ho2),Do2-60),(0,0,-1)); print(f"     yL={y}: zL {[round(60+t,2) for t in ts]}")
