import numpy as np, math, sys
sys.path.insert(0,__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','reporte-v3'))
# --- elemento de placa ACM (12 gdl), rigidez por integracion numerica
def kel(a, b, D, nu):
    def base(x,y): return np.array([1,x,y,x*x,x*y,y*y,x**3,x*x*y,x*y*y,y**3,x**3*y,x*y**3])
    def dx(x,y): return np.array([0,1,0,2*x,y,0,3*x*x,2*x*y,y*y,0,3*x*x*y,y**3])
    def dy(x,y): return np.array([0,0,1,0,x,2*y,0,x*x,2*x*y,3*y*y,x**3,3*x*y*y])
    C=[]
    for (x,y) in ((0,0),(a,0),(a,b),(0,b)):
        C += [base(x,y), dx(x,y), dy(x,y)]
    Ci=np.linalg.inv(np.array(C))
    def B(x,y):
        return np.array([[0,0,0,2,0,0,6*x,2*y,0,0,6*x*y,0],[0,0,0,0,0,2,0,0,2*x,6*y,0,6*x*y],[0,0,0,0,2,0,0,4*x,4*y,0,6*x*x,6*y*y]])
    Dm=D*np.array([[1,nu,0],[nu,1,0],[0,0,(1-nu)/2]])
    gp,gw=np.polynomial.legendre.leggauss(4)
    K=np.zeros((12,12))
    for i,xi in enumerate(gp):
        for j,et in enumerate(gp):
            x=a*(xi+1)/2; y=b*(et+1)/2; Bm=B(x,y)@Ci
            K+=gw[i]*gw[j]*a*b/4*Bm.T@Dm@Bm
    return K
def placa(Lx, Lz, t, E, bordes_lat, techo, zr=6.0, largo=30.0, nx=38, nz=48, nu=0.35):
    """Pared lateral de la funda: Lx (fondo) x Lz (alto). z=0 borde libre de abajo; z=Lz techo.
    bordes_lat/techo: 'apoyado' o 'empotrado'. Carga repartida en 'largo' a la altura zr. Devuelve N/mm."""
    D=E*t**3/(12*(1-nu*nu)); a=Lx/nx; b=Lz/nz
    Ke=kel(a,b,D,nu); nn=(nx+1)*(nz+1); K=np.zeros((3*nn,3*nn))
    nid=lambda i,j: j*(nx+1)+i
    for j in range(nz):
        for i in range(nx):
            ns=[nid(i,j),nid(i+1,j),nid(i+1,j+1),nid(i,j+1)]
            dof=np.array([[3*n,3*n+1,3*n+2] for n in ns]).ravel()
            K[np.ix_(dof,dof)]+=Ke
    fijo=set()
    for j in range(nz+1):
        for i in (0,nx):
            n=nid(i,j); fijo.add(3*n); fijo.add(3*n+2)           # w=0 y giro dw/dz=0 a lo largo del borde vertical
            if bordes_lat=='empotrado': fijo.add(3*n+1)
    for i in range(nx+1):
        n=nid(i,nz); fijo.add(3*n); fijo.add(3*n+1)
        if techo=='empotrado': fijo.add(3*n+2)
    libres=np.array(sorted(set(range(3*nn))-fijo))
    f=np.zeros(3*nn); jr=int(round(zr/b)); cargados=[nid(i,jr) for i in range(nx+1) if abs(i*a-Lx/2)<=largo/2+1e-9]
    for n in cargados: f[3*n]=1.0/len(cargados)
    u=np.zeros(3*nn); u[libres]=np.linalg.solve(K[np.ix_(libres,libres)], f[libres])
    w=np.mean([u[3*n] for n in cargados])
    return 1.0/w
print("RIGIDEZ DE LA PARED DE LA FUNDA frente a un nervio de 30 mm a 6 mm del borde (elementos finitos de placa, pared de 2 mm)")
res={}
for nombre,Lz,nz in (("funda entera",95.4-2.4,48),("funda corta P4",40-2.4,20)):
    for E in (2500.0,3300.0):
        for lat in ('apoyado','empotrado'):
            k=placa(76.0, Lz, 2.0, E, lat, 'empotrado', nz=nz); res[(nombre,E,lat)]=k
            print(f"  {nombre:14s} E={E:.0f} bordes verticales {lat:9s}: {k:5.1f} N/mm")
def reten(k, sale, rebaje, holg=0.3, r=1.5, mu=0.3):
    """Nervio de radio r que sale 'sale'; rebaje de radio r+0.1 y fondo 'rebaje'. Devuelve (aprieto asentada, fuerza normal asentada por lado,
    retencion maxima con los dos nervios, aprieto al pasar, fuerza para bajar la funda el ultimo tramo)."""
    d0 = r - sale + holg                 # distancia del centro del nervio a la cara interior de la pared sin deformar
    rr = r + 0.1; cg = rr - rebaje       # centro del rebaje, por dentro de la pared
    asent = max(0.0, (r - d0) - rebaje)  # aprieto ya asentada
    # borde del rebaje: a +-sqrt(rr^2-cg^2) del centro. La pared se abre w: centro del nervio a d0+w de la cara.
    best=0
    for i in range(1,400):
        w = asent + (r-d0-asent)*i/400.0
        d = d0 + w
        s = math.sqrt(max(r*r-d*d,0)); be=math.atan2(s,d)
        best=max(best, k*w*math.tan(be+math.atan(mu)))
    paso = r-d0
    return asent, k*asent, 2*best, paso, 2*k*paso*mu
print("\nRETEN DE LA FUNDA (dos nervios). Peso a sostener ~2,6 N")
for et,sale,reb in (("v4   (0,5 / 0,3)",0.5,0.3),("v4.1 (0,8 / 0,3)",0.8,0.3),("alt. (0,8 / 0,55) sin aprieto",0.8,0.55),("alt. (0,6 / 0,35)",0.6,0.35)):
    for nombre in ("funda entera","funda corta P4"):
        ks=[res[(nombre,E,lat)] for E in (2500.0,3300.0) for lat in ('apoyado','empotrado')]
        lo=[reten(min(ks),sale,reb,mu=0.2), reten(max(ks),sale,reb,mu=0.4)]
        print(f"  {et:30s} {nombre:14s}: aprieto asentada {lo[0][0]:.2f} mm ({lo[0][1]:.1f} a {lo[1][1]:.1f} N por lado, permanente) | retencion {lo[0][2]:.1f} a {lo[1][2]:.1f} N | al pasar abre {lo[0][3]:.2f} mm por lado, roce {lo[0][4]:.1f} a {lo[1][4]:.1f} N")
# tension en la pared con el aprieto permanente
print("\nIMANES (N35, 1,2 T)")
from imanes import fuerza
for g in (2.6,3.6,3.6+0.65,3.2,4.0):
    print(f"  esquina, separacion {g:.2f} mm: {fuerza(g)[0]:.3f} N cada uno, {2*fuerza(g)[0]:.2f} N los dos")
print("  aguja: central (0,4+1,4+0,4=2,2):", round(fuerza(2.2)[0],2), " rotor (0,4+1,4+0,3):", round(fuerza(2.1)[0],2), " rotor con el rotor pegado a la piel (1,8):", round(fuerza(1.8)[0],2))
