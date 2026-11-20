import numpy as np, math, sys
from malla import carga, rayo
sys.path.insert(0,__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','reporte-v3'))
P=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','probetas-v4','')
Do2,Ho2=35.69,46.34
pan=carga(P+'p1-panel.3mf')[:2]
print("PANEL por el canto de abajo, plano medio del rotor (zL=68.18): primer plastico subiendo desde yL=-44 (canto del panel en -42.14)")
for x in (9,8,7.5,7,6,5,4.5,4,0,-5,-10,-14,-15,-16):
    ts=rayo(pan[0],pan[1],(x,-(-44+Ho2),Do2-68.18),(0,-1,0)); print(f"  x={x:5.1f}: {[round(-44+t,2) for t in ts][:4]}")
# viga del frente del suelo tras abrir la ranura pasante
print("\nTIRA DELANTERA DEL SUELO (entre el frente y la ranura de emergencia): viga biempotrada de x=-22,6 a 6,5")
E=3000.0; ch2=42.34; Rc=44.82
xs=np.linspace(-22.6,6.5,583); dx=xs[1]-xs[0]
def seccion(x):
    """Inercia (flexion hacia el frente) y fibra extrema de la tira: fondo 2,4 mm (0..2,4 desde el frente)."""
    dep = math.sqrt(Rc*Rc-x*x)-ch2 if abs(x)<14.70 else 0.0     # hondo de la ranura del pestillo
    piezas=[]      # (y0, y1, alto)
    if abs(x)>17.0:      # bisel: alto de 1 a 3,4
        n=24
        for i in range(n):
            y0=2.4*i/n; y1=2.4*(i+1)/n; piezas.append((y0,y1,1.0+(y0+y1)/2))
    else:
        piezas.append((0,2.4,4.0-dep)); 
        if dep>0: piezas.append((0,1.05,dep))
    A=sum((b-a)*h for a,b,h in piezas); yc=sum((b-a)*h*(a+b)/2 for a,b,h in piezas)/A
    I=sum(h*(b-a)**3/12+(b-a)*h*((a+b)/2-yc)**2 for a,b,h in piezas)
    return I, max(yc,2.4-yc), A
Is=np.array([seccion(x)[0] for x in xs]); cs=np.array([seccion(x)[1] for x in xs])
print("  inercia: en el bisel %.2f mm4, zona maciza %.2f, bajo el pestillo (x=0) %.2f" % (seccion(-20)[0], seccion(-16)[0], seccion(0)[0]))
# biempotrada con carga repartida de -4 a 4: metodo de flexibilidad (2 hiperestaticas: R_A, M_A)
def resolver(P_total):
    q=np.where(np.abs(xs)<=4.0, P_total/8.0, 0.0)
    def M_de(RA,MA):
        s=xs-xs[0]
        Mq=np.array([np.sum(q[:i+1]*(xs[i]-xs[:i+1]))*dx for i in range(len(xs))])
        return MA+RA*s-Mq
    def extremo(RA,MA):
        M=M_de(RA,MA); k=M/(E*Is); th=np.cumsum(k)*dx; w=np.cumsum(th)*dx
        return np.array([th[-1], w[-1]])
    b=extremo(0,0); A=np.c_[extremo(1,0)-b, extremo(0,1)-b]; RA,MA=np.linalg.solve(A,-b)
    M=M_de(RA,MA); k=M/(E*Is); th=np.cumsum(k)*dx; w=np.cumsum(th)*dx
    sig=np.abs(M)*cs/Is
    return w, sig
for Pn in (10.0,30.0):
    w,sig=resolver(Pn)
    i=np.argmax(np.abs(w)); j=np.argmax(sig)
    print(f"  tiron de {Pn:.0f} N en el pestillo de abajo: cede {abs(w[i]):.3f} mm (en x={xs[i]:.1f}); tension max {sig[j]:.0f} MPa en x={xs[j]:.1f}")
# comparacion: antes del parche el labio estaba unido al suelo a todo lo largo (voladizo de 2,5 mm de alto y 1,25 de grueso)
print("  antes del parche: labio en voladizo unido al suelo; 10 N repartidos en 8 mm -> tension ~%.0f MPa" % (6*10*1.25/(8*1.25**2)))
# rozamiento del rotor frente al par del muelle
print("\nROTOR: lo que frena frente a lo que empuja el muelle (0,31 mN·m contra el tope; 0,6 mm)")
vol = 2*8*31.3*3 + math.pi*(6**2-4.15**2)*3 + 8*26*0.8 + 80*0.6*1.6     # brazos, cubo, alma, espiral (mm3)
m = vol*1.24e-3 + 0.24                                                    # g, con el iman
print(f"  masa del rotor ~{m:.1f} g ({m*9.81e-3*1000:.0f} mN)")
W=m*9.81e-3
for mu in (0.2,0.3,0.4):
    print(f"  mu={mu}: de pie, roce en el eje {W*mu*4.15*1000:.0f} uN·m | tumbado, apoyado en las puntas (r~40) {W*mu*40*1000:.0f} uN·m, apoyado en el cubo (r~5) {W*mu*5*1000:.0f} uN·m")
print(f"  desequilibrio del iman (0,24 g a 16 mm): hasta {0.24e-3*9.81*16*1000:.0f} uN·m; de pie ayuda a cerrar")
# lengueta de la peana
print("\nLENGUETA DE LA PEANA (12 x 1,2 x 2,4; resalte de radio 1,0 que sale 0,6; holgura 0,2 -> flexa 0,4)")
def lengueta(t, sale, E, mu, L=10.8, alto=2.4, r=1.0, holg=0.2):
    k=3*E*(alto*t**3/12)/L**3; dmax=sale-holg; best=0
    for i in range(1,400):
        d=dmax*i/400; c=(r-sale)+holg+d      # distancia horizontal del centro del resalte a la arista de la muesca... (centro a 0,4 por dentro del canto; pared a 0,2)
        c=(r-sale+holg)+d; s=math.sqrt(max(r*r-c*c,0)); be=math.atan2(s,c)
        best=max(best,k*d*math.tan(be+math.atan(mu)))
    return k, k*dmax, 2*best, 100*3*t*dmax/(2*L*L), 2*k*dmax*mu
for t,sale in ((1.2,0.6),(1.5,0.6),(1.6,0.6),(1.2,0.8)):
    a=lengueta(t,sale,2500,0.2); b=lengueta(t,sale,3300,0.4)
    print(f"  grosor {t}, resalte {sale}: rigidez {a[0]:.1f} a {b[0]:.1f} N/mm; fuerza al flexar del todo {a[1]:.2f} a {b[1]:.2f} N; RETENCION con las dos {a[2]:.1f} a {b[2]:.1f} N; deformacion {a[3]:.2f} %; roce al meterla {a[4]:.1f} a {b[4]:.1f} N")
print("  peso que carga: reloj ~150 g + pinza ~14 g + peana ~12 g = ~1,7 N")
