# Eventually, la caja: contra-reporte de la v3

Revisión crítica del prototipo v3 y lista de lo que hay que cambiar antes de imprimir la caja.

Escrito el 19 de noviembre de 2026 sobre el commit `21fb41d` del repositorio. He leído
`reporte-v3/reporte-v3.md`, `guia-de-montaje.md`, `plan-de-pruebas.md`, `calculos-v3.txt`,
`contexto.md`, `generador_caja_v3.py` entero (1 060 líneas) y las figuras y capturas. No he
abierto el modelo en Fusion ni he impreso nada: lo que sigue sale de leer la geometría en el
generador y de cálculos propios.

Cada cifra lleva su procedencia: **del modelo** (leída en el generador), **calculada** (por
mí, con el método indicado), **estimada** (orden de magnitud, con datos que no tengo) o
**juicio** (opinión de diseño, sin número detrás).

---

## 1. Veredicto

La v3 es mucho mejor caja que la v2 y arregla de verdad la mitad de lo que se pidió. Pero
cuatro de las soluciones nuevas no funcionan tal como están dibujadas, y eso se puede saber
hoy, sin imprimir.

- **El cierre de un empujón se acuña.** La boca empuja el pestillo casi en dirección al eje.
  Para que el rotor gire, el rozamiento tendría que ser de 0,06 al empezar; el PLA contra PLA
  ronda 0,2 a 0,4. No es cuestión de lijar: es la geometría (3.1).
- **La pinza del modelo no es la pinza real.** Se imprime para un brazalete de 200 mm y se
  dibuja montada como si midiera 180. En la realidad esos 20 mm se absorben doblando el
  brazo: la punta acaba encima del reloj y el PETG queda forzado para siempre (3.3).
- **El reloj no se puede meter como dice la guía, y sacarlo no es evidente.** La pinza
  necesita subir 22 mm para entrar en sus cunas y dentro de la caja hay 3 (3.4).
- **El taladro de emergencia no llega a soltar el pestillo.** El clip se sale del canto a
  mitad de recorrido (3.5).
- **Lo que sí aguanta:** la llave magnética, el muelle en espiral como idea, la funda con la
  frase, los 8 imanes y la magnetización del reloj. Esa parte es sólida.
- **La caja no queda inservible si falla el empujón.** Se puede cerrar con la aguja puesta, y
  eso ya funciona en la v3 sin tocar nada. Es mi recomendación como base (apartado 7).
- **Cuarta versión modelada, cero piezas impresas.** La tarjeta dice «diciembre de 2026» y
  hoy es 19 de noviembre. Lo siguiente es la impresora, no una v4 completa.

Hay 4 fallos graves, 10 importantes y una lista de defectos del report, del plan de pruebas y
de mi propio contra-reporte anterior: tres de los problemas de la v3 salen de cosas que pedí
yo (6.3).

### Cómo queda cada punto del contra-reporte de la v2

| Punto de la v2 | En la v3 | Mi lectura |
| --- | --- | --- |
| G1 Montar el reloj | Pinza y peana | **A medias.** La idea vale; la forma y el montaje, no (G2, G3) |
| G2 Cerrar es torpe | Resbalón | **No resuelto.** Se acuña (G1) |
| G3 Cierre por gravedad | Muelle en espiral | **Casi.** Falta un tope de reposo (I1) |
| G4 Si se atasca, no abre | Taladro y tapeta desmontable | **No resuelto.** El taladro no suelta (G4) |
| G5 Tarjeta | Carriles en el panel | **Resuelto**, con un pero (I3) |
| G6 Aguja fuera | Aguja en el techo, bajo la funda | **Resuelto** |
| I1 Apertura | Tope a 50°, bisel y ranura | **A medias.** Sigue acabando en una uña (I5) |
| I2 Tamaño | Fondo −17 mm, alto +11 | **A medias** (I8) |
| I3, I4, I6, I7, I8, I9, I10 | Funda, imanes, aguja, soportes, NFC, enganche | **Resueltos en el modelo** |
| I5 Piel | 1,4 mm | Pendiente de la probeta P0 |
| I11 Panel al derecho | Esquina achaflanada | **Resuelto, pero se ve** (I7) |

## 2. Lo que la v3 hace bien

Para no tirar lo que funciona:

- **La frase sin engordar, en las tres primeras capas de la funda.** Es la forma correcta de
  imprimirla y la que más se parece a la esfera.
- **De 24 imanes a 8, con una sola regla de orientación.** «Todos con la misma cara hacia el
  frente» es fácil de seguir y difícil de equivocar.
- **La espiral.** Reparte el giro en 76 mm y trabaja al 0,33 % (**calculado**; el report da
  0,35). Mi brazo recto de la v2 habría cedido. Fue buena corrección.
- **Haber visto que mi resbalón no funcionaba.** El report explica por qué un chaflán en un
  rotor centrado no gira. Tenía razón. Lo que hizo después se queda corto, pero el
  diagnóstico era correcto.
- **Hay plan de pruebas, guía de montaje y probetas listas.** En la v2 no había nada de eso.
- **La honestidad.** «Nada impreso ni probado», «ahora son cuatro versiones», y el apartado 7
  del report lista como dudas casi todo lo que aquí resulta ser un problema.
- **Los cálculos se pueden repetir.** `imanes.py` da los mismos números que mi script, con
  dos decimales.

## 3. Lo que he comprobado por mi cuenta

**Método general.** Mismas fórmulas que en el contra-reporte de la v2. Para el rozamiento uso
0,3 entre piezas de PLA y lo trato como un intervalo de 0,2 a 0,4 (**estimado**: con las
capas marcadas suele ser más, no menos). Para el PLA, un módulo de 3 000 MPa.

### 3.1 El cierre de un empujón (calculado): se acuña

Qué pasa al empujar el panel: el canto de la boca toca el pico del pestillo, que está 4 mm a
la izquierda del eje y 44 mm por encima. La boca es una arista horizontal, así que empuja el
pico **hacia abajo**. Para bajar, el pico tiene que apartarse **de lado**.

- Empujar hacia abajo un punto que está casi encima del eje apenas hace girar: el brazo de
  esa fuerza son los 4 mm de desfase.
- El rozamiento, en cambio, actúa de lado, con un brazo de 44 mm.
- Al empezar, el pico resbala 11 mm de lado por cada milímetro que entra el panel.

| Giro del rotor | Resbala de lado por mm de avance | Gira solo si el rozamiento es menor de… | …contando el roce del brazo contra la piel |
| --- | --- | --- | --- |
| 0° (primer contacto) | 11 mm | 0,06 | 0,04 |
| 4,5° | 5,8 mm | 0,12 | 0,07 |
| 8° | 4,3 mm | 0,17 | 0,10 |
| 13,7° (final) | 2,9 mm | 0,24 | 0,14 |

Con un rozamiento real de 0,2 a 0,4 no gira en ningún punto del recorrido. Y como la fuerza
que empuja y la que frena crecen juntas, **apretar más no lo arregla**: se clava más.

El report lo dejó escrito como duda: «la geometría pasa; el rozamiento del chaflán no está
calculado». La comprobación del generador (`check_resbalon`) solo mira si las piezas caben
al moverse, no si se mueven. La tabla de «giro que la boca le pide al rotor» es correcta como
geometría; lo que falta es que el rotor obedezca.

**Qué haría falta.** Que el punto de contacto esté tan lejos de la vertical del eje como por
encima de él, es decir, a unos 45°. Con el rotor de barra eso no existe. Se consigue con un
pico articulado corto (apartado 7).

### 3.2 Dónde descansa el rotor (calculado)

Para que el rotor pueda girar a los dos lados, la v3 le quita el tope. Queda donde lo deje el
muelle, y el muelle es muy blando cerca del centro.

| Espiral | Rigidez | Reposo con el panel de pie | Reposo con el panel tumbado |
| --- | --- | --- | --- |
| 0,45 mm | 8 µN·m por grado | ±5° | ±24° |
| **0,6 mm** (la del modelo) | 19 µN·m por grado | ±2° | ±10° |
| 0,8 mm | 45 µN·m por grado | ±1° | ±4° |

Rotor de unos 3,3 g (**estimado** del modelo). De pie roza en el eje; tumbado apoya de plano.

- El enganche pasa de 1 mm solo entre −8° y +18,5° (**del report**). Con la espiral de 0,6 y
  el panel tumbado, el rotor puede quedarse fuera de ese margen.
- El plan de pruebas dice «quédate con el muelle **más fino** que cumpla todo». Es al revés:
  el más fino es el que peor vuelve.
- Con un tope en cerrado y el muelle precargado 20°, la espiral de 0,6 empuja contra el tope
  con 380 µN·m, el doble del peor rozamiento, y a 50° pide 1,3 mN·m de los 5,0 que da la
  aguja. Vuelve siempre y sobra arrastre. Pero un tope solo cabe si el rotor gira hacia un
  único lado.

### 3.3 La pinza (calculado)

La pinza que se imprime tiene 199 mm de contorno y 82,9 mm de alto. El modelo, para dibujarla
«con el reloj puesto», no la dobla: le **acorta** el tramo recto 10 mm. Eso no es lo que hace
una pieza elástica. Lo que hace es doblar el brazo fino junto al talón.

| Brazalete | Giro del brazo | Alto real | Alto que supone el modelo | Dónde acaba la punta del brazo | PETG deformado |
| --- | --- | --- | --- | --- | --- |
| 200 mm | 0° | 82,9 | 82,9 | 5 mm por detrás de la cara plana | 0 % |
| 190 mm | 16° | 77,0 | 77,9 | 8 mm **por delante** | 0,6 % |
| **180 mm** (el supuesto) | 34° | 68,0 | 72,9 | 19 mm por delante: dentro del reloj | 1,2 % |
| 170 y 160 mm | no llega | — | — | — | cerca del 3 % |

Modelo simple: el brazo gira como una bisagra al final del talón. La forma real será algo
intermedio, pero no la del dibujo.

- Con 180 mm, la punta del brazo cae sobre el asa de arriba y la caja del reloj. Roza justo
  la zona pulida.
- El PETG queda al 1,2 % **de forma permanente**. A esa deformación sostenida el plástico
  cede en semanas (**estimado**): la pinza se queda con la forma cerrada y deja de tensar.
- El alto de la caja se calcula con la forma falsa. Con 180 mm sobran unos 5 mm.
- «La pinza vale para todos sin cambiarla» (apartado 5 del report) no es cierto.

### 3.4 Meter y sacar el reloj (del modelo)

- La guía dice: peana a la caja, luego reloj en la pinza, luego «déjala caer en las dos
  cunas». Para pasar la uña delantera de la cuna, la pinza tiene que subir **22 mm**. Sobre el
  brazalete hay **3 mm** de aire. No entra.
- El único orden posible es montar reloj, pinza y peana fuera y meter el bloque entero.
- La peana va encastrada 2,4 mm en el suelo, con un talón detrás y dientes delante. Para
  entrar tiene que pasar por encima del suelo: al bloque le quedan **0,6 mm** de margen de
  altura, sobre medidas que son supuestas, y por detrás 1 mm de aire.
- Para sacarlo hay que levantar el frente de una base que queda a ras del suelo, sin nada de
  donde cogerla. Tirar del reloj no sirve: la pinza sube 3 mm, toca el techo y no sale.

### 3.5 El taladro de emergencia (calculado)

El taladro está 3 mm a la izquierda del eje. El canto del pestillo mide 8 mm de ancho y, al
girar el rotor, se desplaza 10 mm hacia la izquierda.

- El clip se queda sin canto a los **9,6°** de los 13,7° necesarios. En ese momento el pico
  todavía entra 0,7 mm en el techo.
- No hay ninguna posición que valga: en reposo el canto ocupa de −4 a +4 mm, y al soltarse,
  de −14 a −6. No se solapan.
- Además es la misma geometría del resbalón: empujar hacia abajo casi sobre el eje.

### 3.6 La funda (calculado y estimado)

La funda baja frenada por el aire que escapa por la rendija. Con caja y reloj en unos 260 g
(**estimado**), la presión que la sostiene es de 390 Pa.

| Holgura por lado | Tiempo en salirse la caja entera |
| --- | --- |
| 0,20 mm | 6 s |
| 0,25 mm | 3 s |
| **0,30 mm** (el modelo) | 1,8 s |
| 0,35 mm | 1,1 s |

- El tiempo va con el **cubo** de la holgura. Cinco centésimas lo doblan. En una pared impresa
  de 94 mm, con su costura, cinco centésimas no se controlan.
- La probeta P4 prueba un tramo corto y vacío. La caja real pesa varias veces más y baja en
  proporción más deprisa. P4 dirá «baja despacio» y la caja caerá.

### 3.7 El tirón sin aguja (calculado)

Lo primero que hará Pablo es tirar del panel. Ese tirón pasa del techo al pestillo, del
pestillo a la **tapeta** y de la tapeta al panel. La tapeta es una lámina de 1,2 mm, de
40 mm de ancho, sujeta solo por sus cantos en cola de milano.

- Con 10 N de tirón (1 kg), la tapeta se comba alrededor de 1 mm. Los cantos solapan 1,2.
- Es una cuenta de orden de magnitud (viga apoyada, 15 mm de ancho eficaz). Pero dice que un
  tirón normal puede sacar la tapeta de su guía, y con ella el rotor.

### 3.8 Lo que sigue saliendo bien (calculado)

- **Arrastre de la llave:** 6,9 mN·m, menos 1,9 de rozamiento, contra 1,0 del muelle. Coincido.
- **Aguja girada que se queda:** 5,0 mN·m de rozamiento contra 1,0. Aguanta incluso con la
  mitad de rozamiento.
- **Reloj:** 900 A/m en el movimiento, 1 400 con la aguja puesta. Límite de la norma: 4 800.
- **Golpes:** para abrir el pestillo de un golpe hace falta una caída de canto de casi medio
  metro. No es un riesgo real.

## 4. Fallos graves

### G1. El cierre de un empujón no va a funcionar

Apartado 3.1. No es un riesgo a comprobar: con esta geometría el rozamiento necesario es
entre tres y seis veces menor que el real.

**Consecuencias en cadena.** Para hacer sitio a este resbalón, la v3 deja el rotor sin tope
(I1), le da giro a los dos lados y pone el taladro de emergencia donde no sirve (G4). Si el
resbalón se cae, esas tres cosas se pueden deshacer.

**Qué cambiar.** Dos caminos, y recomiendo el primero como base:

1. **Cerrar con la aguja puesta.** La aguja se queda girada a 50°; se empuja el panel y se
   quita la aguja. El muelle echa el pestillo. Ya funciona en la v3. Es una mano y un gesto
   simétrico: la aguja abre y la aguja cierra.
2. **Pico articulado**, si quieres conservar el empujón. Detalle en el apartado 7. Se prueba
   en P2 y solo entra en la caja si pasa 20 de 20.

### G2. La pinza está dibujada con una forma que no va a tener

Apartado 3.3. De ahí salen tres errores: la punta del brazo sobre el reloj, el PETG forzado
y el alto de la caja.

**Qué cambiar.**

- Medir el contorno interior del brazalete cerrado. Es el dato que falta desde el primer día.
- Imprimir la pinza a esa medida más 6 mm. Así trabaja al 0,3 o 0,4 % y no cede.
- Olvidar la pinza universal de 160 a 200. La pinza es un parámetro: se regenera.
- Dibujar en el montaje la forma libre. Con 6 mm de diferencia, el error es despreciable.
- Calcular el alto del nicho con esa forma.

### G3. Meter y sacar el reloj

Apartado 3.4. La guía describe un montaje imposible, el real va con medio milímetro de margen
y a Pablo nadie le dice que hay que levantar una base que no se puede coger.

Además contradice una decisión cerrada del proyecto: «el soporte **se saca entero** y en la
mesilla presenta la esfera inclinada».

**Qué cambiar.** Peana corredera:

- Dos guías con labio sobre el suelo, de delante atrás. La peana entra y sale deslizando,
  con el reloj puesto. Sin levantar nada.
- Un resalte pequeño la retiene al fondo. Con el panel cerrado, además, no puede avanzar.
- Las guías con labio impiden que se levante boca abajo. Fuera talón, dientes y los «3 mm
  que sube el frente».
- Tirar del reloj hacia ti saca el soporte entero. Es el gesto natural.
- Las guías van de delante atrás: con la caja impresa de espaldas, salen verticales y sin
  soportes.

### G4. La apertura de emergencia no abre

Apartado 3.5. En la v2 era grave que un atasco obligara a romper la caja. Sigue igual.

Un atasco no es improbable. Basta con que algo empuje el panel hacia fuera desde dentro:
0,4 N sobre los pestillos ya frenan el rotor más de lo que la aguja puede arrastrar
(**calculado**: 0,3 × 0,4 N × 44 mm = 5,3 mN·m).

**Qué cambiar.**

- Empujar **de lado**, no hacia abajo. Una ranura corta sobre el recorrido del pico, por la
  que un clip lo arrastra.
- Ponerla en la **base** de la caja, sobre el pestillo de abajo. El rotor es una sola pieza:
  mover un pico mueve los dos. Y debajo no se ve.
- Para el caso «se ha perdido la aguja»: dos imanes sueltos pegados a un palito abren igual.
  Escribirlo en la guía.

## 5. Fallos importantes

### I1. El rotor no tiene posición de reposo

Apartado 3.2. Añado dos cosas:

- Con el expositor abierto, la aguja se queda en el panel a 50° y el muelle pasa días
  cargado. El PLA cede con el tiempo y el reposo se irá desplazando (**estimado**).
- La probeta P1 dice «al quitarla, el rotor vuelve solo». No dice adónde ni en qué postura.

**Qué cambiar.** Rotor de un solo sentido, tope en cerrado, muelle precargado 15 a 20°. Entre
los muelles que dejen la aguja girada, elegir el **más grueso**.

### I2. El tirón del panel pasa por la pieza más débil

Apartado 3.7. Además, el rotor lleva en el centro un alma de solo 0,8 mm.

**Qué cambiar.** Que cada punta del rotor, en posición de cerrado, tenga detrás un puente
macizo del propio panel. El rotor se monta girado a 50°, donde no hay puente, y se lleva a su
sitio. La tapeta pasa a ser una tapa de polvo. Como mínimo, si no se hace eso: tapeta de 2 mm.

### I3. El mecanismo queda a la vista por detrás

El report dice que las dos ventanas que deja la tapeta «las tapa la tarjeta». La tarjeta
mide 55 mm de alto y cubre hasta 27,5 mm del centro. Las ventanas llegan a 41,7
(**del modelo**).

- Con el panel en la mano se ve el brazo del rotor por encima de la tarjeta. El truco deja de
  ser un truco.
- Entra polvo y cabe un dedo.
- La piel de 1,4 mm queda sin apoyo en unos 34 mm. Apretando el frente con el dedo puede
  rozar el rotor, que tiene 0,3 mm de juego (**juicio**).
- En la cara vista se puede marcar el contorno de la cámara (**juicio**). P0 mira la sombra
  del imán, no esto.

**Qué cambiar.** Tapa trasera entera, sin ventanas. Un puente de 8 mm sobre la cámara lo
imprime la X1 sin problema; no hace falta dejarla abierta.

### I4. La funda deja caer la caja

Apartado 3.6. El gesto de levantar la funda y que la caja baje despacio es bueno. El problema
es otro: una caja se coge por los lados. Quien la levante así se queda con la funda en la
mano y, dos segundos después, la caja con el reloj cae.

**Qué cambiar.**

- Un retén: dos resaltes de 0,3 mm en la caja, cerca de la base, y dos rebajes en la funda.
  Tiene que aguantar el peso (2,6 N) y soltarse con un tirón suave.
- Probar P4 **lastrada** hasta el peso real, con monedas dentro del tramo.

### I5. Abrir sigue acabando en una uña

El panel se sujeta con 2,3 N. La aguja se sujeta al panel con 1,7 N (0,89 + 0,78). Si tiras
de la aguja, se suelta la aguja.

**Qué cambiar.** Bajar la sujeción del panel a 1,2 N, tapando los imanes de esquina con
1,3 mm en vez de 0,8 (**calculado**: 0,61 N cada uno a 2,6 mm). Entonces la aguja hace de
tirador. El margen es justo, 1,4 veces: hay que probarlo antes de creérselo. Si no sale, un
uñero de verdad, a todo lo ancho.

### I6. Nada le dice a Pablo cómo se abre

Recibe un bloque blanco con una aguja azul encima. No hay marca de dónde va, ni de que se
gira, ni hacia dónde. Además la aguja se pega en tres sitios que no son el bueno: el cubo
sobre el imán del rotor, la pala sobre el central, o centrada pero apuntando a otro lado.

**Qué cambiar.** No tocar la cara lisa. La pista va en la web, que es lo que abre el NFC de
la funda: una línea, «la aguja abre la caja: adelanta la hora». Lo puedo poner yo. O se lo
dices tú al dárselo.

### I7. La cara lisa ya no es lisa

La regla estética es «todo blanco y liso; la tapa, sin agujeros, ejes ni texto».

- **Esquina achaflanada de 6 mm**, arriba a la derecha del frente. Se ve en las capturas como
  un triángulo. Rompe la esfera en blanco.
- **Techo de la caja:** rebaje de la aguja, rebaje redondo para pellizcarla y un taladro.
- **Peana:** dientes de sierra a la vista y dos cunas macizas a los lados del reloj.

**Qué cambiar.** El «solo entra al derecho», por detrás: un resalte en el canto trasero del
panel y su muesca en la boca. El taladro se va a la base (G4). La peana corredera no lleva
dientes; las cunas, tan bajas como deje la pinza.

### I8. El tamaño y las holguras

- 94,4 mm de alto para un reloj de 40. Unos 5 son de la pinza mal dibujada (G2).
- Todas las holguras del interior son de 1 a 3 mm y todas se apoyan en medidas supuestas:
  contorno, grosor del brazalete, ancho de asas, corona, cierre.
- El report lo dice, pero la caja está dimensionada como si el supuesto fuera un dato.

**Qué cambiar.** Nada hasta medir. Con la peana corredera, el aire de arriba puede bajar de 3
a 1,5 mm.

### I9. Imanes embutidos

- Un imán embutido al revés obliga a tirar la pieza. Una de las piezas es la base, la
  impresión más larga, y su pausa llega casi al final.
- Los imanes pasan bajo una boquilla a más de 200 °C con 0,4 a 0,8 mm de plástico encima. Un
  disco fino es la forma que peor aguanta el calor. La pérdida será pequeña (**estimado**,
  sin dato), pero nadie la ha medido.

**Qué cambiar.**

- Orden: imprimir primero la base. Los imanes del panel se orientan después contra los de la
  base, comprobando con la torre. Así un error en la base no cuesta nada.
- En P0, embutir un imán con pausa y compararlo con uno suelto levantando clips.

### I10. Piezas sueltas

- La aguja va en su rebaje sin nada que la retenga. Sin la funda, al inclinar la caja se cae.
- La tarjeta sale sola de los carriles si se vuelca el panel. P1 pide que «no se salga al
  sacudir», pero no hay nada que la sujete.

**Qué cambiar.** Un punto de roce en el rebaje de la aguja y un resalte de 0,2 mm en un
carril.

## 6. Fallos del report, del plan de pruebas y del proceso

### 6.1 Del report

- **«Comprobado en el modelo»** se lee como «funciona». Para el resbalón significa «las piezas
  no se solapan al moverse». La duda del rozamiento está en el apartado 7, lejos de la tabla
  que dice «Hecho».
- **Tres frases que no son ciertas:** «las ventanas las tapa la tarjeta», «la pinza vale para
  todos sin cambiarla» y «la pinza se deja caer en las cunas».
- **G4 figura como «Modelado»** sin ninguna comprobación. Para el pestillo y el resbalón hay
  función de chequeo; para la emergencia, no.
- **El montaje de Fusion enseña una pinza que no existe.** Las interferencias que comprueba
  `main()` se comprueban contra esa forma.
- **No hay calendario.** La fecha de entrega sigue sin constar en ningún documento.

### 6.2 Del plan de pruebas

| Probeta | Qué falla | Qué poner |
| --- | --- | --- |
| P1 | «El rotor vuelve solo»: no dice adónde | Vuelve a menos de 3° del cerrado con el panel de pie, tumbado y boca abajo |
| P2 | «Quédate con el muelle más fino» | El más grueso que deje la aguja girada |
| P2 | «No sale tirando de él sin aguja»: no dice cuánto | Aguanta 2 kg colgados del panel |
| P2 | «Subir `rotor_chaflan`» si se atasca | No lo arregla: el problema es el ángulo, no el chaflán |
| P3 | Solo imprime un trozo de suelo | Añadir techo y pared trasera: el problema es la altura |
| P3 | Necesita el reloj montado | Decir qué se puede probar sin él |
| P4 | Tramo vacío | Lastrado al peso real |
| P4 | NFC «solo con la caja completa» | Poner el reloj, o una cuchara, bajo el tramo |

### 6.3 Míos, en el contra-reporte de la v2

- **El resbalón** que pedí, un chaflán en los extremos del rotor, no funcionaba. La v3 lo vio.
- **La pinza universal de 160 a 200 mm** fue idea mía. Es el origen de G2.
- **La esquina achaflanada** la pedí yo, sin pensar en que se vería.
- **El taladro de emergencia vertical**, también. Con el rotor de la v2 tampoco habría girado.

Las cuatro tienen lo mismo en común: las describí sin hacer la cuenta. Las de este documento
están hechas.

### 6.4 Del proceso

- **Cuatro versiones, 135 parámetros, 9 piezas, 16 probetas. Nada impreso.** Las reglas del
  proyecto ya dicen «primero la impresora». Hay que cumplirlas.
- **P0 y P1 valen tal como están.** Lo que enseñan (piel, alojamientos, arrastre, que la
  espiral salga suelta) sirve para cualquier versión. Se pueden imprimir hoy.
- **La medida que más manda sigue sin tomarse.** Sin el contorno del brazalete, cualquier caja
  entera que se imprima es para tirar.

## 7. Otros enfoques

Una escalera de tres niveles. Se baja un peldaño solo si la probeta lo obliga.

**Nivel 1. Llave magnética y cierre de un empujón.** Lo que quiere ser la v3. Necesita el
pico articulado:

- El rotor gira solo a derechas y descansa en un tope, con el muelle precargado.
- Cada extremo acaba en un bracito de unos 15 mm, a 45°, unido al rotor por una lámina de
  0,6 × 6 mm. La boca empuja el pico y el bracito bascula.
- A 45° la fuerza sí tiene brazo: gira con rozamientos de hasta 0,6 (**calculado**, mismo
  método que 3.1).
- Baja los 2,2 mm doblando la lámina 11°: deformación del 1 %, solo durante el empujón.
- El tirón no puede pasar por la lámina: el pico tiene que apoyar en el puente macizo de I2.
- **Sin modelar ni probar.** Es la parte con más riesgo de todo el proyecto.

**Nivel 2. Llave magnética; se cierra con la aguja puesta (recomendado como base).** Rotor
rígido de un solo sentido, tope y muelle. Es la v3 con menos cosas. Depende solo de P1.

**Nivel 3. Sin pestillo.** Panel a imanes y la aguja como tirador. Solo si P1 falla, cosa
que el cálculo no espera. El plan C de la v2 (aguja con eje pasante) sigue disponible.

**Por qué el nivel 2 como base.** El rotor es una pieza pequeña y se cambia sin tocar la
caja. Si el panel admite los dos rotores, la caja se puede imprimir con el nivel 2 asegurado
y el empujón se añade después, si pasa P2. El calendario no queda colgado de la pieza más
dudosa.

## 8. Qué cambiar

**Imprescindible**

1. Rotor de un solo sentido, con tope en cerrado y muelle precargado 15 a 20°.
2. Cierre de base con la aguja puesta. El empujón, solo con un pico articulado que pase P2.
3. Puente macizo del panel detrás de cada punta del rotor. Tapa trasera entera, sin ventanas.
4. Pinza a la medida real del brazalete más 6 mm. Montaje y nicho con la forma libre.
5. Peana corredera con guías de labio y retén. Fuera talón y dientes.
6. Emergencia por la base, empujando de lado. Guía: dos imanes abren si se pierde la aguja.
7. Retén de la funda.
8. Corregir la guía de montaje y el plan de pruebas (6.2).
9. **Ninguna caja entera sin medir antes el reloj.**

**Recomendado**

10. «Solo entra al derecho» por detrás del panel. Fuera la esquina achaflanada.
11. Sujeción del panel de 1,2 N, para que la aguja haga de tirador. Probarlo.
12. Pista de apertura y aviso del imán en la web.
13. Retén de la aguja en su rebaje y de la tarjeta en su carril.
14. Orden de impresión de las piezas con imanes; prueba de calor en P0.
15. Aire de arriba de 3 a 1,5 mm, una vez haya peana corredera.

**A valorar contigo**

16. Quitar los cuatro imanes de esquina. Se pierde el «clic» de imán; se ganan dos pausas de
    impresión menos y un panel que sale solo con la aguja.
17. Rotor en PETG, si se hace el pico articulado: aguanta mejor las láminas.
18. Texto por dentro y aguja con pomo: siguen pendientes desde la v2.

**Los imanes siguen cuadrando.** 8 en la caja y 2 en la aguja de repuesto: 10 de 14. Si el
retén de la funda se hiciera con imanes, serían 14 justos; por eso lo propongo impreso.

## 9. Plan de pruebas corregido

| Orden | Qué | Con qué | Vale si |
| --- | --- | --- | --- |
| 1 | **Medir el reloj** | Tira de papel y calibre | Contorno interior del brazalete cerrado, ancho con corona, grosor del brazalete, ancho de asas, tipo y grosor del cierre |
| 2 | **P0**, tal como está | `probetas-v3/p0-*` | Como dice el plan. Añadir: un imán embutido con pausa levanta lo mismo que uno suelto |
| 3 | **P1**, tal como está | `probetas-v3/p1-*` | Como dice el plan. Añadir: el rotor vuelve a menos de 3° en las tres posturas; cerrar con la aguja puesta funciona 10 de 10 |
| 4 | **P2 tal como está**, una vez | `probetas-v3/p2-*` | Sirve para confirmar el acuñamiento. Cuesta poco y zanja la discusión |
| 5 | **P2 nueva** | Rotor con tope y pico articulado | Cierra de un empujón 20 de 20; aguanta 2 kg; abre por la ranura de la base |
| 6 | **P3 nueva** | Pinza a medida, peana corredera, suelo con guías, techo y pared trasera | El reloj real entra y sale tirando de él, con una mano, sin tocar el techo |
| 7 | **P4 lastrada** | Tramo de funda y de caja, con 260 g | La frase se lee. Cogida por la funda, la caja no cae. Con un tirón suave, baja en más de 2 s. El móvil lee el NFC con el reloj debajo |

Los pasos 1, 2 y 3 no necesitan tocar Fusion. Se pueden hacer hoy.

## 10. Lo que solo puedes responder tú

1. **¿Qué día se entrega?** Es la cuarta vez que se pregunta. Decide cuántos peldaños de la
   escalera da tiempo a probar.
2. **¿Está montado el reloj?** Si lo está: contorno interior del brazalete cerrado, con una
   tira de papel. Y si el brazalete ya está ajustado a la muñeca de Pablo.
3. **¿Te vale que la caja se cierre con la aguja puesta** si el empujón no sale?
4. **¿Quieres conservar el «clic» de imán del panel**, aunque obligue a abrir con la uña?
5. **¿Pongo yo en la web la pista de apertura y el aviso del imán?**
6. **¿De qué grado son los imanes?** Si no lo sabes, P1 lo dirá.
