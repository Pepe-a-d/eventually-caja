import zipfile, re, sys, numpy as np
def carga(fn):
    z = zipfile.ZipFile(fn)
    name = [n for n in z.namelist() if n.endswith('.model')][0]
    s = z.read(name).decode('utf-8', 'replace')
    unit = re.search(r'unit="(\w+)"', s)
    V = np.array([[float(a), float(b), float(c)] for a, b, c in re.findall(r'<vertex x="([-\d.eE+]+)" y="([-\d.eE+]+)" z="([-\d.eE+]+)"', s)])
    Tt = np.array([[int(a), int(b), int(c)] for a, b, c in re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', s)])
    tr = re.findall(r'transform="([^"]+)"', s)
    return V, Tt, (unit.group(1) if unit else '?'), tr
def rayo(V, Tt, o, d):
    """Devuelve los parametros t donde el rayo o + t d corta la malla."""
    o = np.array(o, float); d = np.array(d, float)
    a, b, c = V[Tt[:, 0]], V[Tt[:, 1]], V[Tt[:, 2]]
    e1, e2 = b - a, c - a
    p = np.cross(d, e2); det = (e1 * p).sum(1)
    ok = np.abs(det) > 1e-12
    inv = np.where(ok, 1 / np.where(ok, det, 1), 0)
    s = o - a; u = (s * p).sum(1) * inv
    q = np.cross(s, e1); v = (q @ d) * inv
    t = (e2 * q).sum(1) * inv
    m = ok & (u >= -1e-9) & (v >= -1e-9) & (u + v <= 1 + 1e-9)
    ts = np.sort(t[m]); out = []
    for x in ts:
        if not out or abs(x - out[-1]) > 1e-4: out.append(float(x))
    return out
if __name__ == '__main__':
    V, Tt, unit, tr = carga(sys.argv[1])
    print(len(V), 'vertices', len(Tt), 'triangulos', 'unidad', unit, 'transform', tr[:2])
    print('min', V.min(0).round(2), 'max', V.max(0).round(2))
