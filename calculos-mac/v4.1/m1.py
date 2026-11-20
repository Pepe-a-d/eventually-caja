import numpy as np, math
from malla import carga, rayo
P=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','probetas-v4','')
def dentro(M, p, d=(0.123,0.957,0.262)):
    V,T=M; d=np.array(d)/np.linalg.norm(d)
    return len([t for t in rayo(V,T,p,d) if t>1e-6])%2==1
aro=carga(P+'p2-aro-de-la-boca.3mf')[:2]
print("A) ARO: rayo vertical desde debajo, plano medio del rotor (z_malla=32.49)")
for x in (8,7,6.6,6.4,5,4,2,0,-5,-10,-14,-15,-20,-22.4,-22.8,-24):
    ts=rayo(aro[0],aro[1],(x,-1.0,32.49),(0,1,0)); print(f"  x={x:6.1f}: {[round(t-1,2) for t in ts if t-1<9]}")
print("   ancho de la ranura (rayo de delante atras a y=0.8):")
for x in (0,-10,-20):
    ts=rayo(aro[0],aro[1],(x,0.8,37),(0,0,-1)); print(f"  x={x}: {[round(37-t,2) for t in ts]}  (z_malla; frente=35.69)")
print("   labio y ranura del pestillo (rayo de delante atras a y=3.0 y 3.8, x=0; y a x=10):")
for x,y in ((0,3.0),(0,3.8),(10,3.8),(-18,3.8),(-18,2.0),(0,1.0),(0,90.0),(0,89.5)):
    ts=rayo(aro[0],aro[1],(x,y,37),(0,0,-1)); print(f"  x={x} y={y}: {[round(35.69-(37-t),2) for t in ts]}  (mm desde el frente)")
print("   bisel del suelo: perfil a x=-18 y x=-20 (rayo vertical, a distintas profundidades desde el frente)")
for dz in (0.2,1.0,2.0,2.3,3.2,4.1,5.0):
    for x in (-16,-19):
        ts=rayo(aro[0],aro[1],(x,-1.0,35.69-dz),(0,1,0)); print(f"  x={x} a {dz} del frente: {[round(t-1,2) for t in ts if t-1<9]}")
