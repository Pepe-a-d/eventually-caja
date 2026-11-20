import numpy as np, math
rad=math.radians; deg=math.degrees
def modelo(g=0.6, E=3000.0, alto=1.6, N=1500):
    r0, r1 = 5.6, 11.6-g/2
    gs = np.linspace(rad(-360), rad(180), N+1)
    rs = r0 + (r1-r0)*(gs-gs[0])/(gs[-1]-gs[0])
    P0 = np.c_[rs*np.cos(gs), rs*np.sin(gs)]
    seg = np.diff(P0, axis=0); ds = np.hypot(seg[:,0], seg[:,1]); psi0 = np.unwrap(np.arctan2(seg[:,1], seg[:,0]))
    k0 = np.gradient(psi0)/ds
    return P0, ds, psi0, k0, E*alto*g**3/12, r1
def integra(mod, F, M0, off):
    P0, ds, psi0, k0, EI, r1 = mod
    N=len(ds); psi=np.empty(N); P=np.empty((N+1,2)); P[0]=P0[0]; M=M0; Ms=np.empty(N)
    # psi[i] = angulo del segmento i. psi[0]=psi0[0] (empotrado en el cubo)
    a=psi0[0]
    for i in range(N):
        psi[i]=a; Ms[i]=M
        c,s=math.cos(a),math.sin(a)
        P[i+1,0]=P[i,0]+ds[i]*c; P[i+1,1]=P[i,1]+ds[i]*s
        Mn = M - (c*F[1]-s*F[0])*ds[i]
        if i<N-1: a = a + (psi0[i+1]-psi0[i]) + 0.5*(M+Mn)/EI*0.5*(ds[i]+ds[i+1])
        M=Mn
    t=np.array([math.cos(psi[-1]),math.sin(psi[-1])]); n=np.array([t[1],-t[0]])
    X=P[-1]+off*n
    return P, psi, Ms, M, X, t, n
def newton(fun, x, n=60):
    x=np.array(x,float)
    for _ in range(n):
        g0=fun(x)
        if np.abs(g0).max()<1e-9: break
        J=np.zeros((len(g0),len(x)))
        for k in range(len(x)):
            xx=x.copy(); h=1e-7; xx[k]+=h; J[:,k]=(fun(xx)-g0)/h
        dx=np.linalg.solve(J,-g0); x=x+dx
    return x, np.abs(g0).max()
def barrido(g, modo, giros, E=3000.0, holgura=None):
    """modo: 'art' (taco libre de girar en el teton), 'emp' (taco gira con el panel),
    'mix' (libre hasta que el taco gira 'holgura' grados respecto al panel; a partir de ahi, sujeto)."""
    mod=modelo(g,E); P0,ds,psi0,k0,EI,r1=mod; off=13.6-r1
    x=np.zeros(3); out=[]
    for giro in np.arange(1,max(giros)+0.5,1.0):
        T=13.6*np.array([math.cos(rad(180+giro)), math.sin(rad(180+giro))])
        def f_art(x):
            P,psi,Ms,Mend,X,t,n=integra(mod,x[:2],x[2],off)
            return np.r_[X-T, Mend-((X[0]-P[-1,0])*x[1]-(X[1]-P[-1,1])*x[0])]
        def f_emp(x, rel=0.0):
            P,psi,Ms,Mend,X,t,n=integra(mod,x[:2],x[2],off)
            return np.r_[X-T, (psi[-1]-psi0[-1])-rad(giro-rel)]
        if modo=='art': x,err=newton(f_art,x)
        elif modo=='emp': x,err=newton(f_emp,x)
        else:
            xa,err=newton(f_art,x); P,psi,Ms,Mend,X,t,n=integra(mod,xa[:2],xa[2],off)
            if giro-deg(psi[-1]-psi0[-1])>holgura: x,err=newton(lambda x:f_emp(x,holgura),x)
            else: x=xa
        if giro in giros:
            P,psi,Ms,Mend,X,t,n=integra(mod,x[:2],x[2],off)
            par=-(x[2] + (P0[0,0]*x[1]-P0[0,1]*x[0]))      # momento en el centro = momento en el arranque + r x F
            rr=np.hypot(P[:,0],P[:,1]); ang=np.unwrap(np.arctan2(P[:,1],P[:,0])); N=len(rr); hue=9
            for i in range(0,N,10):
                j=np.searchsorted(ang, ang[i]+2*math.pi)
                if j<N: hue=min(hue, rr[j]-rr[i]-g)
            # roce con el cubo (radio 6): radio minimo de la tira pasados 60 grados del arranque
            i60=np.searchsorted(ang, ang[0]+rad(60))
            out.append(dict(giro=giro, par=abs(par)*1000, F=np.hypot(x[0],x[1])*1000, rel=giro-deg(psi[-1]-psi0[-1]), eps=np.abs(Ms).max()/EI*g/2*100,
                            rmax=rr.max()+g/2, hueco=hue, cubo=rr[i60:].min()-g/2-6.0, err=err))
    return out
if __name__=='__main__':
    print("ESPIRAL v4.1. par en uN·m; 'rel' = lo que el taco gira sobre el teton respecto al panel")
    for g in (0.45,0.6,0.8):
        for modo,h in (('emp',None),('art',None),('mix',5.0)):
            for r in barrido(g,modo,(0.0,18.0,43.0,68.0) if False else (18.0,43.0,68.0),holgura=h):
                print(f" g={g:4.2f} {modo:3s} giro {r['giro']:4.0f}: par {r['par']:6.0f} | F teton {r['F']:6.1f} mN | rel {r['rel']:5.1f} | deform {r['eps']:.2f} % | r max {r['rmax']:.2f} | hueco entre vueltas {r['hueco']:.2f} | hueco al cubo {r['cubo']:.2f} | err {r['err']:.0e}")
    print("sensibilidad al modulo (g=0.6, mix): E=2300 y 3500")
    for E in (2300.0,3500.0):
        for r in barrido(0.6,'mix',(18.0,68.0),E,5.0): print(f"   E={E:.0f} giro {r['giro']:.0f}: par {r['par']:.0f}")
