import numpy as np, math
rad=math.radians; deg=math.degrees
# Espiral: extremo interior empotrado en el cubo (fijo); el panel (teton) gira +giro respecto al cubo.
# Extremo exterior unido rigido al taco; el taco tiene el ojo a 2,3 mm hacia fuera del eje de la tira.
def modelo(g=0.6, E=3000.0, alto=1.6, N=800):
    r0, r1 = 5.6, 11.6-g/2
    gs = np.linspace(rad(-360), rad(180), N+1)
    rs = r0 + (r1-r0)*(gs-gs[0])/(gs[-1]-gs[0])
    P0 = np.c_[rs*np.cos(gs), rs*np.sin(gs)]
    seg = np.diff(P0, axis=0); ds = np.hypot(seg[:,0], seg[:,1]); psi0 = np.unwrap(np.arctan2(seg[:,1], seg[:,0]))
    return P0, ds, psi0, E*alto*g**3/12, r1
def forma(P0, ds, psi0, EI, F, off, Mext=0.0, it=400):
    """F = fuerza (2) que el teton hace sobre el ojo. off = distancia del ojo al final de la tira, hacia fuera.
    Mext = momento adicional sobre el taco (contacto con paredes). Devuelve puntos, posicion del ojo, giro del taco."""
    psi = psi0.copy(); F=np.array(F,float)
    for _ in range(it):
        seg = np.c_[ds*np.cos(psi), ds*np.sin(psi)]
        Pm = np.vstack([P0[0], P0[0]+np.cumsum(seg, axis=0)])
        t = np.array([math.cos(psi[-1]), math.sin(psi[-1])]); n = np.array([t[1], -t[0]])   # n: hacia fuera (a la derecha de la marcha antihoraria)
        X = Pm[-1] + off*n
        mid = (Pm[:-1]+Pm[1:])/2
        M = (X[0]-mid[:,0])*F[1] - (X[1]-mid[:,1])*F[0] + Mext
        new = psi0 + np.cumsum(M/EI*ds) - M/EI*ds/2
        d = np.abs(new-psi).max(); psi = 0.5*psi+0.5*new
        if d < 1e-11: break
    seg = np.c_[ds*np.cos(psi), ds*np.sin(psi)]
    Pm = np.vstack([P0[0], P0[0]+np.cumsum(seg, axis=0)])
    t = np.array([math.cos(psi[-1]), math.sin(psi[-1])]); n = np.array([t[1], -t[0]])
    X = Pm[-1] + off*n
    mid = (Pm[:-1]+Pm[1:])/2
    M = (X[0]-mid[:,0])*F[1] - (X[1]-mid[:,1])*F[0] + Mext
    return Pm, X, psi[-1]-psi0[-1], M, t, n
def newton(fun, x, n=80):
    x=np.array(x,float)
    for _ in range(n):
        g0=fun(x); 
        if np.abs(g0).max()<1e-9: break
        J=np.zeros((len(g0),len(x)))
        for k in range(len(x)):
            xx=x.copy(); h=1e-6*(1+abs(x[k])); xx[k]+=h; J[:,k]=(fun(xx)-g0)/h
        x=x+np.clip(np.linalg.solve(J,-g0),-0.3,0.3)
    return x, np.abs(g0).max()
def caso(g, giro, modo, E=3000.0):
    P0, ds, psi0, EI, r1 = modelo(g, E)
    off = 13.6 - r1
    # posicion del teton respecto al cubo: el ojo relajado esta en angulo 180 (marco de la espiral); el panel gira +giro
    T = 13.6*np.array([math.cos(rad(180+giro)), math.sin(rad(180+giro))])
    if modo=='articulado':
        x,err = newton(lambda x: forma(P0,ds,psi0,EI,x,off)[1]-T, [0.0,0.0])
        Pm,X,rot,M,t,n = forma(P0,ds,psi0,EI,x,off); Mext=0.0
    else:   # empotrado: el taco gira con el panel (giro exacto = giro)
        def f(x):
            Pm,X,rot,M,t,n = forma(P0,ds,psi0,EI,x[:2],off,x[2]); return np.r_[X-T, rot-rad(giro)]
        x,err = newton(f, [0.0,0.0,0.0]); Pm,X,rot,M,t,n = forma(P0,ds,psi0,EI,x[:2],off,x[2]); Mext=x[2]
    F=x[:2]
    par = T[0]*F[1]-T[1]*F[0] + Mext            # par del teton sobre la espiral, respecto al centro
    eps = np.abs(M).max()/EI*g/2*100
    rr = np.hypot(Pm[:,0],Pm[:,1]); N=len(rr)
    # hueco minimo entre vueltas (aprox: diferencia de radio entre puntos a una vuelta de distancia en angulo)
    ang = np.unwrap(np.arctan2(Pm[:,1],Pm[:,0]))
    hueco=1e9
    for i in range(0,N,8):
        j=np.searchsorted(ang, ang[i]+2*math.pi)
        if j<N: hueco=min(hueco, rr[j]-rr[i]-g)
    return dict(F=np.hypot(*F), par=par, rot=deg(rot), eps=eps, rmax=rr.max()+g/2, rmin_ext=rr[N*2//3:].min(), hueco=hueco, err=err)
print("ESPIRAL v4.1: taco con ojo en un teton (articulado) frente a taco empotrado (lo que suponia el contra-reporte v3)")
print("grosor | giro | modo        | par (uN·m) | fuerza en el teton (mN) | el taco gira (grados; 'giro' si empotrado) | deform. % | radio max de la tira | hueco min entre vueltas")
for g in (0.45,0.6,0.8):
    for giro in (18,43,68):
        for modo in ('articulado','empotrado'):
            r=caso(g,giro,modo)
            print(f" {g:4.2f} | {giro:3d} | {modo:10s} | {r['par']*1000:7.0f} | {r['F']*1000:6.1f} | {r['rot']:6.1f} | {r['eps']:.2f} | {r['rmax']:.2f} | {r['hueco']:.2f} | err {r['err']:.0e}")
