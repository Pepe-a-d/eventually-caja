# Eventually, la caja: contra-reporte del parche v4.1

Revisión crítica del parche v4.1 y lista de lo que queda por corregir.

Escrito el 20 de noviembre de 2026 sobre el commit `8c8da45` del repositorio (el parche ya
está fusionado en `main`). He leído `reporte-v4/parche-v4.1.md`, la guía y el plan
corregidos, y todos los cambios de `generador_caja_v4.py`. He medido sobre las piezas
regeneradas de `probetas-v4/` y he rehecho los cálculos del muelle, los retenes y los imanes.
No he abierto Fusion ni he impreso nada.

Cada cifra lleva su procedencia: **del modelo** (leída en el generador), **medida en la
pieza** (sobre el `.3mf` exportado), **calculada** (por mí), **estimada** (orden de magnitud)
o **juicio** (opinión de diseño).

---

## 1. Veredicto

El parche hace lo que se le pidió. Los dos fallos graves de la v4 están arreglados, y esta
vez lo he comprobado: la ranura de emergencia llega al pestillo (medido) y el muelle
conserva la carga (calculado).

- **No encuentro fallos graves nuevos.** Quedan 5 importantes y unos cuantos detalles.
- **P0, P1 y P2 se pueden imprimir ya**, con los ficheros nuevos. Nada de lo que queda lo
  impide.
- **Lo más serio que queda:**
  - **El clip de la tapa trasera no sujeta.** Está dibujado en la dirección en que la tapa
    se sale: la tapa sigue cayéndose al sacar la tarjeta (I1).
  - **El retén de la funda sale ahora demasiado fuerte** y deja la funda apretada para
    siempre. La caja no saldría con «un tirón suave» (I3).
  - **La lengüeta de la peana retiene la mitad de lo que dice el parche**, más o menos lo
    que pesa el reloj (I4).
- **Tres de los cinco fallos importantes salen de frases mías** del contra-reporte anterior,
  copiadas al pie de la letra: «con el mismo rebaje», «rebajar las puntas» y «pasante hasta
  la cara de arriba» (6.2).
- **Sexta ronda, cero piezas impresas, reloj sin medir.** Lo que queda ya no se decide
  calculando.

### Cómo queda cada punto del contra-reporte de la v4

| | Pedía | En el parche | Mi lectura |
| --- | --- | --- | --- |
| **G1** | Ranura de emergencia pasante y comprobada | Hecho | **Resuelto** (3.1). Debilita la tira del suelo (I5) |
| **G2** | Taco sujeto también hacia dentro | Ojo en un tetón, y resalte en la tapa | **Resuelto** (3.2) |
| **I1** | Lengüeta en la peana, 2 o 3 N | Hecho | Bien de forma. Retiene 1,0 a 1,8 N, no 2,7 (I4) |
| **I2** | Nervio de 0,8 con el mismo rebaje | Hecho tal cual | Lo pedí mal: sale demasiado fuerte (I3) |
| **I3** | Un solo gesto; imanes de esquina más flojos | Hecho | Bien. Falta decidir el pomo |
| **I4** | Puntas del rotor rebajadas; holgura de 0,35 | Hecho tal cual | Lo pedí mal: el tirón pasa ahora por la tapa (I2) |
| **I5** | Tapa trasera con pestaña y clip | Hecho | La pestaña, bien. El clip no sujeta (I1) |
| **I6** | Corregir el margen del pico articulado | Corregido en el texto | Bien |
| **I7** | Nada hasta medir | Nada | Bien. **Sigue sin medirse** |
| **I8** | Chaflán en las guías | Hecho | Resuelto (medido) |
| 6.1 | `imprimir-v4/` en el repositorio | Subido, 9 piezas | Resuelto |
| 6.2 | Plan de pruebas | Corregido | Bien. Dos retoques (5) |

## 2. Lo que el parche hace bien

- **Es un parche de verdad.** Mismo generador, mismos nombres de fichero, medidas exteriores
  iguales. No ha vuelto a empezar.
- **La emergencia tiene por fin una comprobación en `main()`**, después de tres versiones
  sin ella.
- **El tetón es mejor que la muesca que pedí yo.** Sujeta el taco en todas las direcciones y
  no depende de un salto de 0,4 mm.
- **Las dos lengüetas descansan relajadas.** La de la peana cae en su muesca con 0,2 mm de
  holgura (**medido en la pieza**): no hay plástico en tensión permanente. Era el error de
  la v4.
- **El apartado 3 del parche avisa de sus efectos secundarios** sin que nadie se lo pida: el
  juego de 0,65 mm del panel y el cambio de orientación de la tapa trasera.
- **Dice lo que no ha recalculado.** «No he recalculado la forma deformada de la espiral.»
  Lo he hecho yo, y sale bien.

## 3. Lo que he comprobado por mi cuenta

### 3.1 La ranura de emergencia (medida en la pieza): ahora sí llega

En `p2-aro-de-la-boca.3mf`, con líneas verticales desde debajo de la base:

- La ranura está libre de +6,5 a −22,6 mm y atraviesa los 4 mm del suelo. Mide 1,6 mm de
  ancho.
- El canto de abajo del panel está abierto de +7,5 a −15 mm (**medido** en
  `p1-panel.3mf`). El clip puede entrar a la derecha del pestillo y seguirlo hasta el final.
- El pestillo queda libre cuando su esquina llega a −13,8 mm. Para entonces el clip tiene
  que estar metido 4,2 mm o más (**calculado**). La guía dice 5.

**Sobre el papel, abre.** Es la primera versión en la que lo hace.

Una nota: la comprobación nueva mira que la ranura esté libre y que el pestillo quede a su
alcance. No gira el rotor ni tiene en cuenta el panel. Eso lo he mirado yo a mano y sale
bien.

### 3.2 El muelle con el tetón (calculado): conserva la carga

He recalculado la espiral con el taco articulado en el tetón, que es como queda ahora.

| Espiral | Par contra el tope | Par con la aguja a 50° | Deformación máxima |
| --- | --- | --- | --- |
| Fina (0,45 mm) | 0,13 mN·m | 0,46 a 0,53 | 0,5 % |
| Media (0,6 mm) | 0,31 mN·m | 1,1 a 1,25 | 0,7 % |
| Gruesa (0,8 mm) | 0,75 mN·m | 2,6 a 3,0 | 0,9 % |

- La aguja aguanta 5,0 mN·m: se queda girada con las tres.
- El taco gira sobre el tetón 3° con la precarga y hasta 12° con la aguja a tope, si nada
  lo para. Lo normal es que una esquina toque la pared del canal hacia los 4°. No pasa nada
  en ningún caso: las vueltas de la espiral no llegan a tocarse.
- La fuerza sobre el tetón no pasa de 0,25 N. El tetón mide 1,8 mm de diámetro y 1,3 de
  alto (**medido**): le sobra.
- El resalte de la tapa trasera deja al taco subir 0,25 a 0,55 mm. Para salirse del tetón
  necesita 1,0 (**calculado sobre medidas de las piezas**).

**Una cosa que no es fallo, pero hay que saber.** Con el panel tumbado, el rotor roza con
todo su peso: frena entre 0,2 y 0,4 mN·m si apoya en las puntas (**estimado**). La espiral
media empuja 0,31. Tumbado, el rotor puede no volver solo al tope. De pie vuelve siempre.
Como ahora se cierra girando la aguja de vuelta, no afecta al uso; afecta a cómo se lee la
prueba P1 (5).

### 3.3 La tapa trasera (medida en la pieza): la pestaña sí, el clip no

- **La pestaña está bien.** 18 mm de ancho, entra 2 mm bajo la banda de arriba, con 0,19 mm
  de juego. El labio que la retiene mide 0,81 mm de grueso.
- **El clip no retiene.** El resalte es un cilindro cuyo eje apunta hacia atrás, que es
  justo hacia donde la tapa se sale. Y su muesca en el panel es un canal abierto hasta la
  cara trasera: en ese punto no hay plástico entre la cara trasera y el fondo de la cámara.
- El resalte entra y sale de su canal deslizando, sin tocar nada. No hay nada que «salte».
- En reposo queda con 0,2 mm de holgura alrededor: la lengüeta no aprieta. Los 0,9 N del
  parche son la fuerza para doblarla de lado, no lo que sujeta la tapa.

**Resultado:** con la tarjeta fuera y el panel inclinado hacia atrás, el borde de abajo de
la tapa se abre, la pestaña se suelta y la tapa se cae. Igual que en la v4.

### 3.4 El retén de la funda (estimado): demasiado fuerte y siempre apretado

En la v4 estimé la rigidez de la pared de la funda con una cuenta de viga. Ahora la he
calculado como placa, con el borde de abajo libre y un nervio de 30 mm a 6 mm de ese borde.
Sale más rígida de lo que dije.

| | Rigidez de la pared | Retención con los dos nervios |
| --- | --- | --- |
| v4: nervio de 0,5 mm | 9 a 34 N/mm | 1,3 a 7,5 N |
| **v4.1: nervio de 0,8 mm** | 9 a 34 N/mm | **4,6 a 26 N** |
| v4.1 con la funda corta de P4 | 19 a 41 N/mm | 10 a 31 N |

El intervalo es ancho porque depende de cuánto sujeten las esquinas de la funda y del
rozamiento. El parche da de 2,5 a 10 N, con mi rigidez antigua.

- **El peso que cuelga es de unos 2,6 N.** En el caso más probable el retén aguanta tres o
  cuatro veces eso.
- **La funda cubre la caja entera: no hay de dónde coger la caja.** Si el retén aguanta más
  que el peso, al levantar la funda sube todo. Para soltarla hay que sacudir. Con 10 N, la
  sacudida es de casi 3 veces la gravedad, con un reloj dentro.
- **Ya asentada, la funda queda abierta 0,2 mm por lado** (**del modelo**): entre 2 y 7 N
  por lado, para siempre. El PLA cede con el tiempo bajo carga fija. Ese aprieto no añade
  retención: el máximo es el mismo sin él (**calculado**). Solo añade fluencia.
- **Al ponerla,** los últimos 6 mm bajan abriendo la funda 0,5 mm por lado: de 2 a 13 N de
  roce.

### 3.5 La lengüeta de la peana (calculado): la mitad de lo que dice el parche

La forma está bien: 12 × 1,2 mm, resalte redondo que sale 0,6, muesca con holgura
(**medido en la pieza**). El número, no.

- El parche da 0,7 N al flexar 0,4 mm y «unos 2,7 N para sacarla». Para llegar a 2,7 hay que
  juntar la fuerza del final del recorrido con la pendiente del principio. No coinciden: al
  empezar a salir la pendiente es fuerte pero la lengüeta aún no empuja, y al final empuja
  pero el resalte ya está casi fuera.
- Recorriendo el camino entero, la retención con las dos lengüetas es de **1,0 a 1,8 N**.
- Lo que carga: reloj, pinza y peana, unos 1,7 N (**estimado**, con un reloj de 150 g).

Con la boca de la caja hacia abajo, la peana aguanta justo o no aguanta. Si se suelta, el
reloj resbala 3 mm hasta tocar el panel por dentro. No se rompe nada, pero es la prueba que
yo mismo puse.

| Lengüeta | Retención | Deformación al pasar |
| --- | --- | --- |
| 1,2 mm (la del parche) | 1,0 a 1,8 N | 0,6 % |
| 1,5 mm | 1,9 a 3,6 N | 0,8 % |

### 3.6 Por dónde pasa el tirón (medido en la pieza y calculado)

Al tirar del panel con el pestillo echado, la caja para al rotor por las puntas y el panel
lo empuja por detrás.

- **En la v4** la cara de atrás del rotor era plana. Las bandas macizas tocaban las puntas a
  la vez que la tapa tocaba los brazos, o antes. El tirón iba a las bandas.
- **En la v4.1** las puntas están 0,4 mm más bajas que los brazos (**medido**). Lo primero
  que toca el rotor es la tapa trasera, junto a sus bordes de arriba y de abajo. Las bandas
  quedan 0,4 mm más lejos.
- Arriba, la tapa lo aguanta con su pestaña: unos 6 MPa con 1 kg por pestillo
  (**estimado**).
- Abajo no hay nada que la sujete (3.3). El borde de abajo de la tapa se abre 0,4 mm y solo
  entonces la banda recibe la punta.

No se rompe nada. Pero cada tirón fuerte deja la tapa trasera entreabierta, y las bandas se
pusieron en la v4 precisamente para que el tirón no pasara por la tapa.

### 3.7 La tira del suelo que deja la ranura (medido en la pieza y calculado)

La ranura pasante separa del resto del suelo la tira que retiene el pestillo de abajo.

- Queda una viga de 29 mm de largo y 2,4 mm de fondo, unida solo por los extremos. Antes
  estaba unida al suelo a todo lo largo.
- Con 1 kg en ese pestillo: cede 0,07 mm y trabaja a 17 MPa. Antes del parche, unos 6.
- Con 3 kg: 50 MPa, que es el límite del PLA. El punto débil es el extremo derecho de la
  ranura, que acaba en esquina viva.
- Al imprimir la base con la boca arriba, esa tira empieza como un puente de 29 mm.
- De esos 29 mm sobran 7: el pestillo abierto acaba en −13,8 y la ranura sigue hasta −22,6.

La prueba de los 2 kg de P2 (1 kg por pestillo) debería pasar. El margen es menor que
antes.

### 3.8 Lo que sigue saliendo bien

- **Imanes de esquina:** 0,69 N entre los dos (**calculado**; coincide con el parche). La
  aguja cogida por el centro aguanta 0,96 N: saca el panel con un margen de 1,4. Por la
  varilla, 0,56 N: no lo saca. La guía ya dice «por el centro o por la cola».
- **El chaflán de las guías** está: la boca pasa de 25,7 a 24,7 mm en 1,5 mm (**medido**).
- **Las puntas del rotor** están rebajadas 0,4 mm desde 34 mm del centro (**medido**).
- **Las alturas de pausa** de la guía están actualizadas: 63,0 y 4,8 mm.

## 4. Fallos importantes

### I1. El clip de la tapa trasera no sujeta

Apartado 3.3. Es el mismo fallo I5 de la v4, a medio arreglar. Además, el resalte que impide
que el taco se salga del tetón está en esa tapa: si la tapa se abre, esa garantía se va con
ella.

**Qué cambiar.** El resalte del clip tiene que ir tumbado, a lo largo del borde de la tapa,
y ocupar solo la mitad del grueso. Su muesca en el panel, cerrada por detrás, con un labio
de unos 0,6 mm. Así la lengüeta tiene que doblarse para pasar el labio y la tapa queda
cogida. Con la lengüeta actual y un resalte de 0,4 mm en rampa a 45°, saldría con 2 a 3 N
(**calculado**). Un resalte redondo que salga más de la mitad de su radio se acuña en vez
de soltar.

**Mientras tanto, en P1:** un trozo de cinta adhesiva sobre la tapa. La prueba de P1 es la
aguja, no la tapa.

### I2. El tirón pasa por la tapa trasera

Apartado 3.6.

**Qué cambiar.** Rebajar 0,4 mm toda la cara de atrás de los brazos del rotor, desde 13 mm
del centro, y no solo las puntas. En el generador es cambiar el arranque del rebaje
(`yr`) por `rotor_radio_brazo`. Brazos y puntas quedan a la misma altura y las bandas
vuelven a tocar primero. El cubo sigue haciendo de tope hacia atrás.

### I3. El retén de la funda

Apartado 3.4. Son dos problemas distintos.

**El aprieto permanente.** Tiene arreglo directo: rebaje de la funda de 0,55 mm en vez de
0,3. El nervio descansa sin apretar y retiene lo mismo.

**Cuánto debe retener.** Esto no lo arregla un número, porque el intervalo que sale del
cálculo es de 1 a 5, y la ventana buena es estrecha:

- Si retiene menos que el peso (2,6 N), al levantar la funda la caja se queda en la mesa.
  Es el gesto más limpio. Pero cogida por la funda, la caja se desliza y cae.
- Si retiene más, la caja no cae al cogerla por la funda. Pero no hay cómo soltarla sin
  sacudir.
- Para tener las dos cosas hace falta de dónde coger la caja: dos medias lunas de unos
  20 mm en el borde de abajo de la funda, delante y detrás. Entonces el valor del retén
  deja de ser crítico.

Es decisión tuya (8). En cualquiera de los casos:

- Nervio de partida de 0,6 mm, con rebaje de 0,35.
- **Ajustarlo con la funda entera, no con la corta.** La funda entera vale como definitiva
  si sale bien. Y dos o tres vasos de P4 con nervios de 0,5, 0,6 y 0,7 mm: cada vaso es una
  pieza pequeña.

### I4. La lengüeta de la peana retiene menos de lo que dice el parche

Apartado 3.5.

**Qué cambiar.** `lengueta_grosor` de 1,2 a 1,5 mm. Sale de 1,9 a 3,6 N. Lo demás, igual.
Lo confirma P3, que de todos modos no se imprime sin la medida del reloj.

### I5. La ranura pasante debilita la tira que retiene el pestillo

Apartado 3.7.

**Qué cambiar.** Acortar la ranura por la izquierda hasta −15,5 mm y redondear sus dos
extremos. La viga pasa de 29 a 22 mm. Si P2 aguanta los 2 kg tal como está, este punto baja
a detalle.

## 5. Detalles

- **El rotor solo entra bien entre 42° y 45°.** Por debajo de 42° las puntas tocan las
  bandas (**calculado**). Por encima de 45° el taco, que ahora es más ancho, pisa el
  arranque del canal (**medido**: a 50°, un 20 % del taco queda sobre plástico). Lo natural
  es girar el rotor hasta su tope de 50° y soltarlo. Se arregla empezando el canal 8° antes.
  Si no, la guía debe decir «45°, ni más ni menos, y empuja el taco al canal con el clip».
- **Montar el taco en el tetón** pide llevarlo 18°, levantarlo 1,3 mm y dejarlo caer con
  0,2 mm de holgura, con un muelle que tira de él 0,4 mm hacia dentro. Se puede, con
  paciencia. Un chaflán en la punta del tetón ayudaría. El parche ya lo marca como incierto.
- **La pestaña de la tapa trasera** vuela 1,1 mm sin apoyo al imprimirse, y entra en una
  ranura con 0,19 mm de juego. Si descuelga dos décimas, no entra sin lijar.
- **El juego de 0,65 mm del panel.** Al quitar la aguja con el pestillo echado, el panel
  sale 0,65 mm y los imanes lo devuelven con 0,49 N (**calculado**). Si en P2 el labio de la
  caja no descuelga, se puede bajar `holg_corte` a 0,2.
- **El roce de la aguja en su rebaje** sigue en 0,03 mm. El parche lo dice.
- **Plan de pruebas, P1:** «el rotor vuelve al tope en las tres posturas». Tumbado puede no
  volver con la espiral fina o la media (3.2). Que vuelva de pie; tumbado, basta con que la
  aguja lo devuelva.
- **Plan de pruebas, P4:** probar con la funda entera, no «si el filamento lo permite».

## 6. Fallos del parche, míos y del proceso

### 6.1 Del parche

- **«Sin choques» no es «funciona».** El clip de la tapa no choca con nada, y por eso mismo
  no sujeta. La comprobación del modelo no dice si una pieza retiene.
- **Los 2,7 N de la peana** (3.5) y **los 0,9 N del clip** (3.3) son fuerzas calculadas en
  una dirección y presentadas como retención en otra.
- **No hay fichero de cálculos del parche.** Las cifras nuevas están solo en el texto.
- **`contexto.md` se contradice.** La cabecera sigue fechada el 19 de noviembre, y el
  párrafo del parche acaba diciendo que «no está subido a GitHub» cuando dos líneas antes
  dice que sí.
- **El README sigue con las capturas de la v3.**

### 6.2 Míos, en el contra-reporte de la v4

- **«Nervio de 0,8 mm con el mismo rebaje.»** Esa frase crea el aprieto permanente de
  0,2 mm. Y la rigidez de la funda que di era baja: con la buena, 0,8 mm se pasa del
  objetivo de 6 N que yo mismo puse.
- **No pensé cómo se suelta la funda** si retiene más que el peso. Pedí «algo más del doble
  del peso» sin ver que no hay de dónde coger la caja.
- **«Rebajar 0,4 mm las puntas del rotor.»** Resolvía el roce bajo el puente y mandaba el
  tirón a la tapa trasera. Había que rebajar el brazo entero.
- **«Ranura pasante hasta la cara de arriba del suelo.»** Era más de lo necesario fuera de
  la zona del pestillo, y no miré lo que le quitaba a la tira que lo retiene.
- **«Una pestaña y un clip pequeño.»** Otra vez pedí una forma sin decir en qué dirección
  tenía que sujetar ni con cuánta fuerza. Es el mismo error que reconocí con los retenes de
  la v3.

### 6.3 Del proceso

- **Seis rondas. Nada impreso. Nada medido.**
- **El parche se hizo y se revisó en una mañana, y aun así aparecen cinco puntos.** Tres
  nacen de mis propias instrucciones. Corregir sobre el papel lo que otro corrige sobre el
  papel ya produce tantos errores como quita.
- **Lo siguiente que hace falta saber solo lo dicen las piezas:** si la aguja arrastra el
  rotor, cuánto descuelgan los puentes, cuánto retiene la funda de verdad.

## 7. Qué recomiendo

**Hoy, con los ficheros que ya están en `main`:**

1. Imprimir **P0**.
2. Imprimir **P1** (panel, tapa trasera, los tres rotores y la aguja de prueba) y el aro de
   **P2**. La tapa trasera, sujeta con cinta.
3. Medir el reloj, si está montado: contorno interior, y alto y fondo del lazo cerrado.

**Un segundo parche pequeño, junto con lo que salga de P1 y P2, y antes de P3 y P4:**

4. Clip de la tapa trasera con el resalte tumbado y la muesca cerrada por detrás (I1).
5. Rebaje de 0,4 mm en todo el brazo del rotor (I2).
6. Funda: rebaje de 0,55; nervio de partida de 0,6; vasos de P4 con tres nervios (I3).
7. Lengüeta de la peana de 1,5 mm (I4).
8. Ranura de emergencia hasta −15,5 mm, con los extremos redondos (I5).
9. Canal del taco 8° más largo en el arranque (5).

**No me mandes un report de ese segundo parche antes de tener P1 y P2 impresas.** Con las
piezas en la mano, la revisión siguiente será sobre lo que ha pasado, no sobre lo que podría
pasar.

**Los imanes siguen cuadrando:** 8 en la caja y 2 en la aguja de repuesto. Quedan 4.

## 8. Lo que solo puedes responder tú

1. **¿Qué día se entrega?**
2. **¿Está montado el reloj?** Si lo está, las tres medidas.
3. **¿Cómo quieres que salga la caja de la funda?** Que se quede en la mesa al levantar la
   funda, que aguante cogida por la funda, o las dos cosas con dos medias lunas para los
   dedos en el borde de la funda (I3).
4. **¿Aguja con pomo?** Ahora se puede tirar del centro de la aguja, pero es un disco de
   9 mm y 2,6 de alto pegado al panel: se coge con las uñas.
5. **¿Pongo yo en la web la pista de apertura y el aviso del imán?**
