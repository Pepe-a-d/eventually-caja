"""Fuerza entre dos imanes de disco (modelo de cargas superficiales), eje comun o desplazado."""
import numpy as np
MU0 = 4e-7 * np.pi
def disco(R, n=26):
    pts, w = [], []
    for i in range(n):
        r0, r1 = R * i / n, R * (i + 1) / n
        m = max(6, int(round(2 * np.pi * (r0 + r1) / 2 / (R / n))))
        for j in range(m):
            a = 2 * np.pi * (j + 0.5) / m
            rc = (r0 + r1) / 2
            pts.append((rc * np.cos(a), rc * np.sin(a))); w.append(np.pi * (r1 * r1 - r0 * r0) / m)
    return np.array(pts), np.array(w)
def fuerza(gap, dx=0.0, d=5.0, h=1.6, Br=1.2):
    """gap y dx en mm. Devuelve (F_axial de atraccion, F_lateral de centrado) en N."""
    R = d / 2 * 1e-3; H = h * 1e-3; g = gap * 1e-3; x = dx * 1e-3
    P, W = disco(R)
    sig = Br / MU0
    # iman A: caras en z=-H (carga -) y z=0 (carga +); iman B: caras en z=g (-) y z=g+H (+)  -> se atraen
    F = np.zeros(3)
    for za, qa in ((-H, -1), (0.0, 1)):
        for zb, qb in ((g, -1), (g + H, 1)):
            dxm = (P[:, 0][None, :] + x) - P[:, 0][:, None]
            dym = P[:, 1][None, :] - P[:, 1][:, None]
            dz = zb - za
            r3 = (dxm ** 2 + dym ** 2 + dz ** 2) ** 1.5
            k = MU0 / (4 * np.pi) * sig * sig * qa * qb * (W[:, None] * W[None, :]) / r3
            F += np.array([(k * dxm).sum(), (k * dym).sum(), (k * dz).sum()])   # fuerza sobre B
    return -F[2], -F[0]
if __name__ == '__main__':
    print('comprobacion contra el contra-reporte (N35, 1.2 T):')
    for g, ref in ((0.8, 2.1), (1.2, 1.55), (1.4, 1.34), (1.5, 1.25), (2.0, 0.89), (3.0, 0.48)):
        print('  gap %.1f -> %.2f N (contra-reporte %.2f)' % (g, fuerza(g)[0], ref))
    print('arrastre lateral a gap 1.5: ', ['%.1f mm: lat %.2f ax %.2f coc %.2f' % ((dx,) + (lambda a, l: (l, a, l / a))(*fuerza(1.5, dx))) for dx in (0.5, 1.5, 2.5)])
    for g in (1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4):
        ax = fuerza(g)[0]
        lat = max((fuerza(g, dx)[1], dx) for dx in np.arange(0.5, 5.01, 0.25))
        a2, l2 = fuerza(g, lat[1])
        print('gap %.1f: axial %.2f N | lateral max %.2f N con desfase %.2f mm (axial ahi %.2f, cociente %.2f)' % (g, ax, lat[0], lat[1], a2, l2 / a2))
