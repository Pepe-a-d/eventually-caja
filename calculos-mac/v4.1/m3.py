import numpy as np, math
from malla import carga, rayo
P=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','probetas-v4','')
pe=carga(P+'p3-peana.3mf')[:2]; rb=carga(P+'p3-rebanada-de-caja.3mf')[:2]
print("PEANA: min/max", pe[0].min(0).round(2), pe[0].max(0).round(2))
# peana en coordenadas del modelo (x, y fondo, z alto). Base de z=4 a 6.4
y0=pe[0][:,1].min()
print("frente de la base yt0 =", y0)
for dy in (0.3,1.0,1.5,2.5,3.2,5,10,13.5,14.5,20):
    ts=rayo(pe[0],pe[1],(0.0,y0+dy,5.2),(1,0,0)); print(f"  a {dy:4.1f} del frente, corte en x (z=5.2): {[round(t,2) for t in ts]}")
print("  resalte: x max a lo largo de y (z=5.2):")
for dy in np.arange(2.0,4.6,0.2):
    ts=rayo(pe[0],pe[1],(30.0,y0+dy,5.2),(-1,0,0)); print(f"    dy={dy:.1f}: x={30-ts[0]:.3f}" if ts else f"    dy={dy:.1f}: nada")
print("REBANADA (frente arriba): malla=(x, zw, -yw). min/max", rb[0].min(0).round(2), rb[0].max(0).round(2))
# guia: pared interior a x=24.7; muesca centrada en yw = yt0+3.2
for dy in (-4,-3.2,-2.5,-1.6,-1,0,1.0,2.0,2.2,2.6,3.2,3.8,4.2,4.4,5,8):
    yw=y0+dy
    ts=rayo(rb[0],rb[1],(0.0,5.2,-yw),(1,0,0)); print(f"  a {dy:5.1f} del frente de la peana: paredes en x (zw=5.2): {[round(t,2) for t in ts]}")
print("  labio de la guia (zw=7.3), a 5 mm:", [round(t,2) for t in rayo(rb[0],rb[1],(0.0,7.3,-(y0+5)),(1,0,0))])
print("  alturas de la guia a x=25.5, 5 mm:", [round(t-1,2) for t in rayo(rb[0],rb[1],(25.5,-1,-(y0+5)),(0,1,0))][:6], " y a x=23.5:", [round(t-1,2) for t in rayo(rb[0],rb[1],(23.5,-1,-(y0+5)),(0,1,0))][:6])
print("  tope del fondo: rayo a lo largo de y, x=22, zw=5.2:", [round(-(40-t),2) for t in rayo(rb[0],rb[1],(22,5.2,40),(0,0,-1))])
print("  yt1 esperado =", pe[0][:,1].max(), " frente caja yw=-35.69; panel hasta -29.09; carriles hasta -27.39")
