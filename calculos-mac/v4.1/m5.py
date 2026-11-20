import numpy as np, math
from malla import carga, rayo
P=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','probetas-v4','')
D=np.array((0.123,0.957,0.262)); D/=np.linalg.norm(D)
dentro=lambda M,p: len([t for t in rayo(M[0],M[1],p,D) if t>1e-6])%2==1
Do2,Ho2=35.69,46.34
pA=lambda x,y,z:(x, -(y+Ho2), Do2-z)
pan=carga(P+'p1-panel.3mf')[:2]; rot=carga(P+'p1-rotor-muelle-medio.3mf')[:2]
pol=lambda r,g:(r*math.cos(math.radians(g)), r*math.sin(math.radians(g)))
def borde(f,a,b):
    fa=f(a)
    for _ in range(40):
        m=(a+b)/2
        if f(m)==fa: a=m
        else: b=m
    return (a+b)/2
print("arranque del canal (panel) y borde del taco relajado (rotor), por radios:")
for r in (12.6,13.0,13.6,14.5,15.5):
    g0=borde(lambda g: dentro(pan,pA(*pol(r,g),68.9)), 114.0, 122.0)
    t0=borde(lambda g: dentro(rot,pA(*pol(r,g),68.9)), 156.0, 166.0)
    print(f"  r={r}: canal desde {g0:.2f}; taco desde {t0:.2f} -> el rotor puede entrar girado como mucho {t0-g0:.2f} grados")
# solape en volumen: puntos del taco girados phi dentro del plastico del panel
for phi in (42,44,45,46,48,50):
    n=0; tot=0
    for r in np.arange(11.2,15.61,0.2):
        for g in np.arange(160,182.01,0.4):
            if dentro(rot,pA(*pol(r,g),68.9)):
                tot+=1
                if dentro(pan,pA(*pol(r,g-phi),68.9)): n+=1
    print(f"  rotor a {phi} grados: {100*n/tot:.1f} % de la planta del taco cae sobre plastico del panel")
