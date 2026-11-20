import numpy as np, math
rad=math.radians; deg=math.degrees
def modelo(g=0.6, E=3000.0, alto=1.6, N=600):
    r0, r1 = 5.6, 11.6-g/2
    gs = np.linspace(rad(180-540), rad(180), N+1)
    rs = r0 + (r1-r0)*(gs-gs[0])/(gs[-1]-gs[0])
    P0 = np.c_[rs*np.cos(gs), rs*np.sin(gs)]
    seg = np.diff(P0, axis=0); ds = np.hypot(seg[:,0], seg[:,1]); psi0 = np.arctan2(seg[:,1], seg[:,0]); psi0 = np.unwrap(psi0)
    EI = E*alto*g**3/12
    return P0, ds, psi0, EI
def forma(P0, ds, psi0, EI, F, lam, it=200):
    """Elastica: fuerza F (en la direccion tangente del extremo, sentido antihorario) aplicada en el punto de la cara
    horaria del taco a distancia lam del extremo de la espiral."""
    psi = psi0.copy()
    for _ in range(it):
        seg = np.c_[ds*np.cos(psi), ds*np.sin(psi)]
        P = np.vstack([P0[0], P0[0]+np.cumsum(seg, axis=0)])
        t = np.array([math.cos(psi[-1]), math.sin(psi[-1])]); a = np.array([t[1], -t[0]])
        X = P[-1] - 1.5*t + lam*a
        Fv = F*t
        mid = (P[:-1]+P[1:])/2
        M = (X[0]-mid[:,0])*Fv[1] - (X[1]-mid[:,1])*Fv[0]
        dk = M/EI
        # psi(s) = psi0(s) + integral de dk
        new = psi0 + np.cumsum(dk*ds) - dk*ds/2
        if np.abs(new-psi).max() < 1e-10: psi = new; break
        psi = 0.5*psi + 0.5*new
    seg = np.c_[ds*np.cos(psi), ds*np.sin(psi)]
    P = np.vstack([P0[0], P0[0]+np.cumsum(seg, axis=0)])
    t = np.array([math.cos(psi[-1]), math.sin(psi[-1])]); a = np.array([t[1], -t[0]])
    X = P[-1] - 1.5*t + lam*a
    return P, t, a, X, (psi-psi0)
def resuelve(g, giro, Rdiente=14.4):
    P0, ds, psi0, EI = modelo(g)
    ang0 = math.pi - math.asin(1.5/Rdiente)
    T = Rdiente*np.array([math.cos(ang0+rad(giro)), math.sin(ang0+rad(giro))])
    x = np.array([EI*rad(giro)/ds.sum()/12.0, 3.1])       # F inicial ~ par/radio
    for _ in range(60):
        def G(x):
            return forma(P0, ds, psi0, EI, x[0], x[1])[3] - T
        g0 = G(x); J = np.zeros((2,2))
        for k, h in enumerate((1e-5, 1e-4)):
            xx = x.copy(); xx[k] += h; J[:,k] = (G(xx)-g0)/h
        dx = np.linalg.solve(J, -g0); x = x + np.clip(dx, -0.5, 0.5)
        if np.abs(g0).max() < 1e-7: break
    P, t, a, X, dpsi = forma(P0, ds, psi0, EI, x[0], x[1])
    rext = np.hypot(*(P[-1] + 3.5*a - 1.5*t))             # esquina exterior horaria del taco
    par = abs(X[0]*x[0]*t[1] - X[1]*x[0]*t[0])
    eps = np.abs(np.gradient(dpsi)/ds).max()*g/2*100
    return x[0], x[1], np.hypot(*P[-1]), rext, par, eps, abs(g0).max()
print("ESPIRAL CON EL TACO RETENIDO SOLO POR EL DIENTE (elastica, sin rozamiento)")
print("grosor | giro | fuerza en el diente | la cara del taco pasa a ... del extremo (el taco mide 3,5) | radio del final de la espiral | par | deform. | error")
for g in (0.45, 0.6, 0.8):
    for giro in (18, 40, 68):
        try:
            F, lam, rE, rext, par, eps, err = resuelve(g, giro)
            est = 'RETENIDO' if lam < 3.5 else 'SE ESCAPA DEL DIENTE'
            print(f" {g:4.2f} | {giro:3d} | {F*1000:6.1f} mN | lam {lam:5.2f} mm ({est}, sobra {3.5-lam:+.2f}) | {rE:5.2f} (impreso {11.6-g/2:.2f}) | {par*1000:5.0f} uN·m | {eps:.2f} % | {err:.1e}")
        except Exception as e:
            print(g, giro, 'no converge', e)
print("\nreferencia: extremo libre con momento puro (curvatura uniforme): el radio exterior pasa de 11,3 a",
      [round(11.3/(1+rad(a)/(rad(540))),2) for a in (18,68)])
