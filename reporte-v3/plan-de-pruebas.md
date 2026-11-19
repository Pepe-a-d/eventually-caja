# Eventually, la caja v3: plan de pruebas

Cinco probetas, en este orden. Cada una dice qué resultado vale y qué parámetro tocar si no vale. Los ficheros están en `probetas-v3/` y vienen ya orientados para la cama.

**En las probetas los imanes no se pegan ni se embuten.** Entran a presión y se recuperan empujando con un clip por el taladro de detrás. Hacen falta 4 como mucho a la vez.

Los parámetros se cambian en `generador_caja_v3.py`, en la lista `P_DEF`, y se vuelve a generar el modelo. Si no quieres tocarlo tú, dime el resultado de la probeta y lo cambio yo.

## P0. Tolerancias

**Qué se imprime.** `p0-tolerancias.3mf` y `p0-llave.3mf`, en PLA blanco.

La tira tiene una esquina cortada: esa es la izquierda. Los valores crecen hacia la derecha.

| Fila | Qué tiene | Valores |
| --- | --- | --- |
| De arriba | 6 alojamientos de imán | 5,05 · 5,10 · 5,15 · 5,20 · 5,25 · 5,30 mm |
| Del medio | 6 ventanas cuadradas para la llave de 6 mm | holgura por lado 0,10 · 0,15 · 0,20 · 0,25 · 0,30 · 0,35 mm |
| De abajo | 4 alojamientos con el fondo cada vez más grueso | piel de 0,8 · 1,0 · 1,2 · 1,4 mm |

**Vale si** eliges:

- el alojamiento donde el imán entra apretando con el dedo y no se cae al dar la vuelta a la tira → `iman_aloj_d`;
- la ventana más justa por la que la llave pasa sin forzar → `holg_tapa` (y `holg_desliza` una más);
- la piel más fina que, con un imán detrás y mirada por la cara de la cama, no deja ver una sombra → `tapa_piel`.

El modelo está hecho con 5,15 mm, 0,20 mm y 1,4 mm. Si eliges otros, hay que regenerar antes de seguir.

## P1. La llave

**Qué se imprime.** `p1-panel.3mf`, `p1-tapeta.3mf`, `p1-rotor.3mf` (PLA blanco) y `p1-aguja-de-prueba.3mf` (cualquier color). 4 imanes: central, rotor y los dos de la aguja. Los de esquina no hacen falta.

Se monta como dice la guía, apartado 4.

**Vale si:**

- la aguja arrastra el rotor 10 de 10 veces, con el panel de pie, tumbado y boca abajo;
- el rotor va menos de 10° por detrás de la aguja;
- al soltar la aguja girada, se queda;
- al quitarla, el rotor vuelve solo;
- la tarjeta entra en los carriles y no se sale al sacudir el panel.

**Si falla:**

| Qué pasa | Qué tocar |
| --- | --- |
| El rotor no gira ni con el dedo | La espiral se ha pegado al alma: subir `muelle_holgura` de 0,6 a 0,8 |
| La aguja no arrastra | Bajar `tapa_piel` (lo que permita P0) o alargar `rotor_radio_iman` |
| La aguja no se queda girada | Muelle más fino: `muelle_grosor` |
| El rotor no vuelve | Muelle más grueso: `muelle_grosor` |
| El labio de los carriles sale caído | Bajar `carril_solape` de 1,2 a 0,9 |

Si la aguja no arrastra de ninguna manera, se pasa al plan C del contra-reporte (eje pasante). El cálculo no lo espera.

## P2. El resbalón

**Qué se imprime.** `p2-aro-de-la-boca.3mf` (los 15 mm delanteros de la caja) y los tres rotores `p2-rotor-muelle-fino`, `-medio` y `-grueso` (espiral de 0,45, 0,6 y 0,8 mm). Se usa el panel de P1.

**Vale si,** con alguno de los tres rotores:

- el panel cierra de un empujón 20 de 20 veces;
- cerrado, no sale tirando de él sin aguja;
- agitado un minuto, sigue cerrado;
- con la aguja, abre;
- un clip por el taladro del techo también lo abre.

Quédate con el muelle **más fino** que cumpla todo.

**Si falla:**

| Qué pasa | Qué tocar |
| --- | --- |
| Hay que empujar mucho o se atasca a medio entrar | Subir `rotor_chaflan`; lijar el canto de la boca |
| Entra pero el pestillo no salta | Subir `holg_corte` |
| Cerrado, el panel baila hacia fuera | Bajar `holg_corte` |
| Se abre solo al agitar | Muelle más grueso |

## P3. El soporte

**Qué se imprime.** `p3-pinza.3mf` en **PETG**, `p3-peana.3mf` y `p3-suelo.3mf` en PLA.

**Vale si,** con el reloj de verdad:

- el brazalete cerrado entra en la pinza apretándola con una mano;
- suelta, la pinza tensa el brazalete y la cabeza no baila;
- la pinza cae en las cunas sin tocar el reloj;
- no gira y no vuelca con un golpe en la mesa;
- la peana entra en el suelo con el talón por delante y no se mueve.

**Si falla:**

| Qué pasa | Qué tocar |
| --- | --- |
| La pinza está dura de apretar | Bajar `pinza_pared` de 1,6 a 1,2 |
| El brazalete queda flojo | La pinza es pequeña para ese brazalete: subir `pinza_contorno_libre` |
| Las asas tocan las cunas | Subir `reloj_ancho_asas` con la medida real |
| La cabeza toca la uña delantera de la cuna | Bajar `cuna_frente` |

Aprovecha para medir el contorno del brazalete: es el dato que fija el tamaño de la caja.

## P4. La funda

**Qué se imprime.** `p4-funda-tramo.3mf` con `p4-frase.3mf` (mármol y azul, como dice la guía en 3.1) y `p4-caja-tramo.3mf` en blanco. Son los 40 mm de arriba de la funda y los 45 de arriba de la caja.

**Vale si:**

- la frase se lee fina y entera;
- la funda, puesta sobre el tramo de caja y sujeta en el aire, baja sola y despacio;
- con el NFC pegado dentro, el móvil lo lee a través del techo.

La lectura con el reloj dentro solo se puede probar con la caja completa.

**Si falla:**

| Qué pasa | Qué tocar |
| --- | --- |
| Se pierden trazos de la frase | Regenerar `frase-v3.json` con 0,05 mm de engorde |
| La funda cae de golpe | Bajar `holg_desliza` de 0,30 a 0,25 |
| La funda no baja | Subir `holg_desliza` |

## Después

Con las cinco en verde y el reloj medido: regenerar el modelo con los valores elegidos e imprimir la caja entera.
