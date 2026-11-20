import math
rad=math.radians; deg=math.degrees
ch=83.72; hy=ch/2-0.2; hw=4.0; zA=ch/2+2; rA=math.hypot(hw,zA); phiA=math.atan2(hw,zA); ts=rad(13.7)
# --- apertura de emergencia: clip fijo en x=-3 empujando el canto del pestillo ---
r_der=math.hypot(hw, zA-2*hw*math.tan(ts)); phi_der=math.atan2(hw, zA-2*hw*math.tan(ts))   # extremo derecho del canto
fi=math.asin(3.0/r_der)+phi_der
print(f"emergencia: el clip (x=-3) se sale del canto cuando el rotor ha girado {deg(fi):.1f} grados de los 13.7 que hacen falta")
print(f"  en ese punto el pico sigue entrando {rA*math.cos(phiA+fi)-hy:.2f} mm")
print(f"  rozamiento: gira si mu(acero-plastico) < {rA*math.sin(phiA+ts)/(rA*math.cos(ts)):.2f}")
# --- sacar la pinza de las cunas: recorrido necesario frente a altura libre ---
R=15; print(f"cunas: la pinza tiene que subir {R+7:.0f} mm (una delantera) / {R+8:.0f} mm (trasera) para salir; altura libre sobre el brazalete: 3 mm")
print(f"peana: base de 2.4 mm en un rebaje de 2.6; el frente puede subir ~3 mm antes de tocar techo -> margen {3-2.6:.1f} mm")
# --- funda de campana: cuanto tarda en salirse la caja ---
m=0.26; A=0.094*0.0703; per=2*(0.094+0.0703); h=3e-4; mu=1.8e-5; L0=0.0917
dp=m*9.81/A
c=per*h**3*dp/(12*mu)/A      # v = c / L (flujo laminar en la rendija, L = solape)
print(f"funda: presion que sostiene la caja {dp:.0f} Pa; velocidad inicial {c/L0*100:.1f} cm/s; la caja sale entera en ~{L0**2/(2*c):.1f} s (holgura 0.30)")
for hh in (2e-4,2.5e-4,3.5e-4):
    cc=per*hh**3*dp/(12*mu)/A; print(f"   con {hh*1e3:.2f} mm: ~{L0**2/(2*cc):.1f} s")
# --- carga del pestillo sobre la tapeta ---
E=3000; F=5.0; Lspan=40.0; t=1.2; bef=15.0; I=bef*t**3/12
print(f"tapeta: tirando del panel con 10 N (5 N por pestillo), flecha ~{F*Lspan**3/(48*E*I):.1f} mm y tension ~{F*Lspan/4/(bef*t*t/6):.0f} MPa (ancho eficaz {bef:.0f} mm)")
# --- imanes y calor: coeficiente de permeancia de un disco fino ---
print(f"iman 5x1.6: relacion alto/diametro {1.6/5:.2f} (disco fino: es la forma que peor aguanta el calor)")
