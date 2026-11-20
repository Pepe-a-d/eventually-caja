import numpy as np
MU0 = 4e-7*np.pi
def disc_pts(R, n=40):
    # puntos en un disco, areas iguales (malla polar)
    rs = (np.arange(n)+0.5)/n*R
    pts=[]; w=[]
    for r in rs:
        m = max(6, int(round(2*np.pi*r/(R/n))))
        th = (np.arange(m)+0.5)/m*2*np.pi
        pts.append(np.c_[r*np.cos(th), r*np.sin(th)]); w.append(np.full(m, 2*np.pi*r*(R/n)/m))
    return np.vstack(pts), np.concatenate(w)
def force(R=2.5e-3, h=1.6e-3, gap=1.5e-3, dx=0.0, Br=1.2, n=34):
    """Iman A debajo (cara superior en z=0), iman B encima separado 'gap', desplazado dx. Devuelve (Fx, Fz) sobre B."""
    p, w = disc_pts(R, n)
    M = Br/MU0
    F = np.zeros(3)
    # caras de A: z=0 (+), z=-h (-). Caras de B: z=gap (-), z=gap+h (+)  -> atraccion
    for za, sa in ((0.0, +1), (-h, -1)):
        for zb, sb in ((gap, -1), (gap+h, +1)):
            A = np.c_[p, np.full(len(p), za)]
            B = np.c_[p[:,0]+dx, p[:,1], np.full(len(p), zb)]
            d = B[None,:,:]-A[:,None,:]
            r3 = (d**2).sum(-1)**1.5
            k = (w[:,None]*w[None,:])/r3
            F += sa*sb*(d*k[...,None]).sum((0,1))
    F *= MU0*M*M/(4*np.pi)
    return F[0], F[2]
print("== Fuerza axial coaxial, dos discos 5x1.6, Br=1.2 T (N35) ==")
for g in (0.0, 0.2, 0.6, 1.0, 1.2, 1.4, 1.5, 1.7, 2.0, 3.0):
    fx, fz = force(gap=g*1e-3)
    print(f" separacion {g:3.1f} mm: {abs(fz):5.2f} N  ({abs(fz)/9.81*1000:4.0f} g)")
print("== Arrastre lateral: iman de la aguja desplazado respecto al del rotor ==")
for g in (1.2, 1.5, 1.7):
    best=(0,0,0)
    rows=[]
    for dx in np.arange(0.25, 6.01, 0.25):
        fx, fz = force(gap=g*1e-3, dx=dx*1e-3)
        rows.append((dx, -fx, -fz))
        if -fx > best[1]: best=(dx, -fx, -fz)
    fz0 = -force(gap=g*1e-3)[1]
    print(f" separacion {g} mm: axial centrado {fz0:.2f} N | arrastre maximo {best[1]:.2f} N con {best[0]:.2f} mm de desfase (axial ahi {best[2]:.2f} N) | cociente arrastre/axial = {best[1]/best[2]:.2f}")
    print("   desfase->arrastre/axial:", ", ".join(f"{dx:.1f}:{fx/max(fz,1e-9):.2f}" for dx,fx,fz in rows[1::4]))
