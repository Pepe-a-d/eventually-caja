# Eventually, la caja: contra-reporte de la v4

Revisión crítica del prototipo v4 y lista de lo que hay que corregir antes de imprimir.

Escrito el 20 de noviembre de 2026 sobre el commit `4874e30` del repositorio. He leído
`reporte-v4/reporte-v4.md`, `guia-de-montaje.md`, `plan-de-pruebas.md`, `contexto.md`,
`generador_caja_v4.py` entero (1 169 líneas) y las dos capturas. Esta vez, además, he medido
sobre las piezas exportadas en `probetas-v4/`. No he abierto Fusion ni he impreso nada.

Cada cifra lleva su procedencia: **del modelo** (leída en el generador), **medida en la
pieza** (sobre el `.3mf` exportado), **calculada** (por mí), **estimada** (orden de magnitud)
o **juicio** (opinión de diseño).

---

## 1. Veredicto

La v4 hace caso al contra-reporte de la v3 casi punto por punto, y la base que eligió es la
buena: cerrar con la aguja puesta. Lo que queda ya no son errores de concepto. Son errores de
décimas de milímetro, y esos no se arreglan con otro modelo: se arreglan imprimiendo.

- **Dos fallos graves, los dos pequeños de arreglar:**
  - **La ranura de emergencia no llega al pestillo.** Entre la ranura y el pestillo queda
    plástico en casi todo el recorrido. Es la tercera versión seguida en la que la apertura
    de emergencia no abre (3.1).
  - **El diente no sujeta el taco del muelle.** Al cargar la espiral, su extremo se mete
    hacia dentro y se sale del diente. El muelle pierde la precarga, casi seguro al primer
    giro de la aguja (3.2).
- **Los retenes nuevos están dibujados, no calculados.** El de la peana es un aprieto de
  0,15 mm entre piezas rígidas: o no retiene o se clava. El de la funda sale del mismo orden
  que el peso que tiene que aguantar (3.3, 3.4).
- **Abrir tirando de la aguja y cerrar quitando la aguja se contradicen.** Si la aguja agarra
  más que el panel, al quitarla te llevas el panel (3.5).
- **Lo que sí está resuelto:** el rotor con tope, el tirón sobre una parte maciza, la pinza a
  medida, la peana que sale con el reloj, el frente liso, el orden de los imanes, la guía y
  el plan de pruebas.
- **Quinta versión modelada, cero piezas impresas, reloj sin medir.** Varios de los
  problemas que encuentro aquí son más pequeños que la tolerancia de la impresora. Otro
  contra-reporte sin una probeta en la mano ya no vale lo que cuesta.

Hay 2 fallos graves y 8 importantes. Uno de los graves y cuatro de los importantes vienen de
cosas que propuse yo sin precisar (6.3).

### Cómo queda cada punto del contra-reporte de la v3

| # | Pedía | En la v4 | Mi lectura |
| --- | --- | --- | --- |
| 1 | Rotor de un sentido, tope, precarga | Hecho | El tope, bien. La precarga no se sostiene (G2) |
| 2 | Cerrar con la aguja | Hecho | Bien. Falta decidir el gesto (I3) |
| 3 | Puente macizo y tapa trasera entera | Hecho | Bien de concepto. El puente, justo de holgura (I4). La tapa, suelta (I5) |
| 4 | Pinza a medida | Hecho | Bien. Falta la medida |
| 5 | Peana corredera | Hecho | Bien. El retén, no (I1) |
| 6 | Emergencia por la base | Hecho | **No funciona** (G1) |
| 7 | Retén de la funda | Hecho, sin calcular | Justo (I2) |
| 8 | Corregir guía y plan | Hecho | Bien. Cuatro retoques (6.2) |
| 9 | Medir el reloj | Depende de ti | **Sigue pendiente** |
| 10 | «Al derecho» por detrás | Hecho | Resuelto |
| 11 | Sujeción de 1,2 N | Hecho | Ver I3 |
| 12 | Pista y aviso en la web | No hecho | Es mío: lo hago cuando me digas |
| 13 | Retén de aguja y tarjeta | Hecho | Tarjeta, bien. Aguja: 0,03 mm, no es nada (I8) |
| 14 | Orden de impresión, prueba de calor | Hecho | Resuelto |
| 15 | Aire de arriba a 1,5 mm | Hecho | Ver I7 |
| 16–18 | A valorar contigo | Sin decidir | Siguen siendo tuyas |

## 2. Lo que la v4 hace bien

- **Eligió el camino seguro.** Rotor rígido de base y el empujón como pieza opcional que
  cabe en el mismo panel. El calendario ya no depende de la pieza dudosa.
- **El tope y los puentes.** El rotor descansa contra una pared y cada pestillo tiene detrás
  una banda maciza. El tirón ya no pasa por una lámina.
- **La pinza se dibuja como se imprime.** Y el report me corrige con razón: los 5 mm que yo
  decía que sobraban eran de una pinza aplastada. Con la pinza a medida no sobran.
- **La peana corredera** cumple la decisión del proyecto: el soporte se saca entero.
- **El frente vuelve a ser un rectángulo liso.** El resalte por detrás hace lo mismo que la
  esquina cortada y no se ve.
- **El plan de pruebas es el mejor documento del proyecto.** Dice qué se puede hacer sin el
  reloj, y que P3 no se imprime sin la medida.
- **El report no esconde nada.** «Sin calcular», «no comprobado: el modelo no dobla piezas».
  De las siete dudas de su apartado 5, cuatro resultan ser problemas reales.

## 3. Lo que he comprobado por mi cuenta

### 3.1 La ranura de emergencia (medida en la pieza): no llega al pestillo

He trazado líneas verticales desde debajo de la base en `p2-aro-de-la-boca.3mf`, en el plano
del rotor. La ranura de emergencia sube 1,53 mm. La ranura del pestillo tiene el fondo curvo:
solo baja hasta ahí justo en el centro.

| Posición (mm desde el centro) | Plástico entre la ranura de emergencia y el pestillo |
| --- | --- |
| 0 | 0 (se tocan en una línea) |
| ±2 | 0,05 mm |
| ±5 | 0,29 mm |
| −8 | 0,73 mm |
| −10 | 1,13 mm |
| −14 | 2,25 mm |

- El pestillo ocupa de −4 a +4. La guía dice meter el clip a su derecha y arrastrarlo 2 cm a
  la izquierda. El pestillo tiene que llegar hasta −13,9 (**calculado**).
- A partir de −5 el clip choca con plástico. Ahí el rotor ha girado unos 12° de los 23°
  necesarios y el pestillo sigue entrando 1,7 mm.
- La causa es una línea del generador: la ranura se corta hasta la altura del punto más bajo
  de la ranura del pestillo, como si su fondo fuera plano.

**El arreglo es de una línea:** cortar la ranura de emergencia hasta la cara de arriba del
suelo. Queda dentro de la huella de la ranura del pestillo y la tapa el canto del panel.

### 3.2 El taco de la espiral (calculado): se sale del diente

En la v3 el taco entraba en una muesca cerrada. En la v4 corre por un canal y lo retiene un
diente de 0,7 mm, que lo pisa 0,4 mm. Nada lo sujeta hacia dentro.

Una espiral que se carga se aprieta: su extremo se acerca al centro. He calculado la forma
deformada, con el taco apoyado solo en el diente y sin rozamiento.

| Espiral | Giro de carga | El extremo se mete hacia dentro | Lo que el diente pisa el taco |
| --- | --- | --- | --- |
| 0,6 mm | 18° (solo la precarga) | 0,41 mm | −0,10 mm: ya está fuera |
| 0,6 mm | 68° (precarga y aguja a 50°) | 1,02 mm | −1,01 mm |
| 0,45 mm | 18° / 68° | 0,41 / 1,03 mm | −0,02 / −0,94 mm |
| 0,8 mm | 18° / 68° | 0,41 / 1,02 mm | −0,19 / −1,10 mm |

- Con la precarga sola, el resultado cae dentro de la tolerancia de impresión: puede
  aguantar o no. Al girar la aguja, no hay duda: se sale por un milímetro.
- Consecuencia: el taco vuelve atrás por el canal y el muelle se queda sin carga. Al quitar
  la aguja, el rotor no vuelve. La caja no se echa el pestillo sola.
- El plan de pruebas dice, si el rotor no vuelve, «muelle más grueso; subir la precarga».
  Las dos cosas lo empeoran.
- Lo que sí cuadra con el report: par contra el tope, 0,31 mN·m (da 0,34); par a 50°,
  1,1 mN·m (da 1,3). La espiral trabaja al 0,6 %.

**Qué hace falta.** Que el taco quede sujeto también hacia dentro: una muesca cerrada con
paredes bajas, a la que el taco salta por encima y cae; y un resalte de la tapa trasera que
no le deje volver a subir.

### 3.3 El retén de la peana (del modelo y calculado)

- Cada guía tiene un resalte de 0,35 mm y la base pasa con 0,20 de holgura. El aprieto es de
  0,15 mm por lado.
- Las dos piezas son rígidas ahí: una pared de 2 mm de grueso y 3,85 de alto, y una base
  maciza de 49 mm de ancho. Para ceder 0,15 mm hacen falta cientos de newtons
  (**estimado**).
- Con la tolerancia de la impresora, de una a dos décimas, el resultado es una lotería:
  o no hay clic, o la peana se clava.
- Si se clava, el gesto de sacar el reloj es tirar de él. La fuerza pasa por el cristal, las
  asas y el brazalete.

### 3.4 El retén de la funda (estimado)

Nervio que sobresale 0,5 mm, holgura de 0,30: la pared de la funda tiene que abrirse 0,2 mm
por lado. La retención depende de lo rígida que sea esa pared.

| Qué | Rigidez de la pared | Retención con los dos nervios |
| --- | --- | --- |
| Funda entera (pared de 76 × 95 mm) | 5 a 22 N/mm | **1,0 a 4,0 N** |
| Funda corta de la probeta P4 (76 × 40 mm) | 10 a 39 N/mm | 1,8 a 7,3 N |

- El peso a sostener es de unos 2,6 N (**estimado**). El retén sale del mismo orden: puede
  aguantar o no, y un tirón brusco lo suelta seguro.
- La funda corta de P4 es casi el doble de rígida que la entera. P4 puede dar por bueno un
  retén que en la funda real no aguante.

### 3.5 La aguja como tirador (calculado)

La aguja es una barra con dos imanes: 0,78 N en el centro y 0,89 N en la cola, a 16 mm. Lo
que aguanta antes de soltarse depende de dónde tires.

| Dónde se tira | La aguja se suelta con | ¿Saca el panel (1,22 N)? |
| --- | --- | --- |
| De la cola | 1,42 N | Sí, justo |
| Entre los dos imanes | 1,67 N | Sí |
| Del centro | 0,96 N | No |
| De la varilla, a media altura | 0,56 N | No |
| De la punta | 0,36 N | No |

- Solo funciona pellizcando la cola, que es una pala plana de 2,6 mm pegada al panel. Lo
  natural es coger la varilla, y de la varilla la aguja se queda en la mano.
- **El conflicto:** para cerrar, la guía dice «mete el panel, quita la aguja». En ese momento
  el pestillo aún no está echado. Si quitas la aguja tirando de donde agarra, te llevas el
  panel otra vez.

### 3.6 Los puentes y sus holguras (medido en la pieza y estimado)

El panel se imprime con la cara vista en la cama. Las dos bandas macizas quedan como puentes
sobre la cámara.

- **Banda del panel:** puente de 25 a 34 mm de luz (**medido en la pieza**), apoyado casi
  solo en los extremos. Debajo pasa la punta del rotor con 0,30 mm de juego en total.
- **Labio de la caja**, el que retiene el pestillo: 1,25 mm de grueso, vuela 2,5 mm sobre una
  cuerda de 29 mm. Holgura hacia el rotor: 0,15 mm.
- La primera capa de un puente de ese largo descuelga entre 0,2 y 0,4 mm (**estimado**). Es
  más que cualquiera de las dos holguras.

### 3.7 El pico articulado (calculado)

El report da un límite de rozamiento de 0,76. Yo di 0,6. Ninguno es el que manda.

- Al empujar, el rotor entero cede unos 4° a derechas, que es su sentido libre, y el pico
  baja casi recto. El roce de lado, que era el problema de la v3, desaparece. Eso es bueno.
- Lo que manda es otra cosa: el chaflán a 45° aprieta el pico contra la piel del panel, y
  ese roce frena la bajada.

| Rozamiento | Empuje total para cerrar |
| --- | --- |
| 0,2 | 2 N |
| 0,3 | 4 N |
| 0,35 | 8 N |
| 0,4 | 36 N |
| 0,41 o más | se acuña |

Funciona sobre el papel si el rozamiento no pasa de 0,35. Es una pieza opcional y el report
ya la marca como la de más riesgo. Solo corrijo el margen: es menor del que dice.

### 3.8 Lo que sigue saliendo bien

- **La apertura:** el pestillo se libera a 23,3° (**calculado**; el report dice 23). La aguja
  llega a 50°.
- **La aguja girada se queda:** 5,0 mN·m de rozamiento contra 1,1 del muelle.
- **El resalte «solo al derecho»:** con el panel del revés queda 1,6 mm fuera. Se ve.
- **La pinza con 6 mm de más:** al poner el brazalete, la punta del brazo se queda unos
  10 mm por encima del asa, sin tocar el reloj (**calculado**, con el brazalete supuesto).

## 4. Fallos graves

### G1. La apertura de emergencia sigue sin abrir

Apartado 3.1. En la v2 no existía, en la v3 el clip se salía del canto y en la v4 choca con
el suelo. En las tres versiones figura como hecha y en ninguna hay una comprobación en el
generador, que sí las tiene para el pestillo.

**Qué cambiar.**

- La ranura, pasante hasta la cara de arriba del suelo.
- Una comprobación en `main()`: que un cilindro de 1 mm, puesto junto al pestillo, pueda
  recorrer la ranura de un extremo a otro sin tocar la caja.

### G2. El muelle pierde la precarga

Apartado 3.2. No deja la caja inservible: el tope sigue ahí y el pestillo se puede echar
girando la aguja de vuelta. Pero se cae la frase central del report, «aguja fuera: el muelle
echa el pestillo», y la probeta P1 saldría mal por un motivo que no es el que quiere medir.

**Qué cambiar.** Muesca cerrada para el taco y resalte en la tapa trasera (3.2).

## 5. Fallos importantes

### I1. El retén de la peana es un aprieto entre piezas rígidas

Apartado 3.3.

**Qué cambiar.** Que algo flexe. Una lengüeta en la base de la peana, de unos 12 mm de largo
y 1 mm de grueso, con el resalte en la punta. Calculada para soltar con 2 o 3 N: tiene que
aguantar la peana boca abajo y salir tirando con un dedo.

### I2. El retén de la funda sale justo

Apartado 3.4.

**Qué cambiar.**

- Más aprieto: nervio de 0,8 mm con el mismo rebaje. Calcularlo para 6 N, algo más del doble
  del peso.
- En P4, imprimir la funda entera si el filamento lo permite, o saber que la corta retiene
  casi el doble.

### I3. Abrir y cerrar con la aguja: falta decidir el gesto

Apartado 3.5.

**Qué cambiar.** Un solo gesto, simétrico, que no depende del muelle ni de dónde se pellizque:

- **Abrir:** aguja al centro, girar a la derecha hasta el tope, tirar.
- **Cerrar:** panel dentro, **girar la aguja de vuelta** hasta arriba, quitarla. El pestillo
  lo echa la aguja; el muelle solo lo mantiene.

Y para tirar hace falta de dónde: o un pomo bajo entre los dos imanes (la pregunta de la
aguja con pomo lleva abierta desde la v2), o imanes de esquina más flojos, 0,7 N en total
bajo 1,8 mm de plástico, para que también valga tirar del centro.

### I4. Dos puentes con menos holgura de la que descuelgan

Apartado 3.6. Si la banda roza la punta del rotor, el rotor no gira y P1 falla por la
impresión, no por el imán.

**Qué cambiar.**

- Rebajar 0,4 mm las puntas del rotor por la cara de atrás. Es la cara de arriba al
  imprimirlo: no cuesta nada.
- Holgura del pestillo hacia el labio de la caja, de 0,15 a 0,35 mm.

### I5. La tapa trasera no se sujeta

Va «a presión» con 0,15 mm de holgura por lado: eso no aprieta. El report lo dice y añade
«la tarjeta la tapa». La tarjeta está para sacarla y leerla. Al sacarla, la tapa se cae y el
mecanismo queda a la vista.

**Qué cambiar.** Una pestaña que entre bajo una de las bandas y un clip pequeño en el lado
contrario. Sigue siendo desmontable y sin pegamento.

### I6. El margen del pico articulado

Apartado 3.7. No bloquea nada: es opcional. Pero la prueba P2 debe hacerse sabiendo que el
límite está en 0,4 y no en 0,76. Si se atasca, el remedio no es retocar el bracito: es que el
pico no roce la piel, o un chaflán más tendido.

### I7. Menos aire, sobre las mismas medidas supuestas

- Bajo el brazalete queda **1,0 mm** hasta el suelo (**del modelo**), con un grosor de
  brazalete de 3,5 mm que nadie ha medido. La peana se desliza con el brazalete colgando por
  el hueco del marco.
- Arriba, 1,5 mm. Lo pedí yo, y sigue apoyado en un contorno de 180 mm supuesto.
- **La forma del lazo tampoco se sabe.** La pinza obliga al brazalete a doblar con 15 mm de
  radio justo al salir de las asas. Un brazalete integrado suele tener los primeros
  eslabones casi rígidos. Si no dobla ahí, el lazo sale más ancho y el cierre toca la pared
  trasera (**juicio**).

**Qué cambiar.** Nada hasta medir. Y medir tres cosas, no una: el contorno interior, y el
alto y el fondo del lazo con el brazalete cerrado y apoyado en la mesa.

### I8. Detalles

- **Roce de la aguja en su rebaje:** 0,33 mm de resalte en 0,30 de holgura. Son 0,03 mm: no
  existe al imprimir. Un imán de los de reserva bajo el rebaje la sujetaría de verdad.
- **Guías de la peana sin entrada.** Empiezan en canto vivo, 6,7 mm detrás del panel, con
  0,2 mm de holgura y el reloj tapando la vista. Un chaflán de entrada.
- **Se ven:** los dos nervios en los costados de la caja, las cunas macizas a los lados del
  reloj y el rebaje redondo junto a la aguja. Es juicio estético, y es tuyo.

## 6. Fallos del report, del plan de pruebas y del proceso

### 6.1 Del report

- **`imprimir-v4/` no está en el repositorio.** La guía y el README lo citan. Solo se han
  subido las probetas, el `.f3d` y el `.step`.
- **No hay fichero de cálculos.** La v3 traía `calculos-v3.txt`. En la v4 los números están
  solo en el texto.
- **«Del contra-reporte, la doy por buena sin repetirla.»** Mi rigidez del muelle estaba bien;
  mi límite del pico articulado, no. Los números ajenos se repiten.
- **G4 figura como «Modelado» sin comprobación**, por tercera vez.
- **El README sigue enseñando la v3**, y la cabecera de `contexto.md` dice a la vez que manda
  el apartado 0 y que manda el 1c.

### 6.2 Del plan de pruebas

| Dónde | Qué falla | Qué poner |
| --- | --- | --- |
| P1 | «El rotor vuelve al tope»: una vez | Después de 20 giros completos de la aguja |
| «Si falla» | Rotor que no vuelve: «subir la precarga» | Mirar primero si el taco sigue tras el diente |
| P2 | La emergencia, tal como está exportada, fallará | Regenerar el aro con la ranura pasante |
| P3 | «La peana hace clic» | Aguanta boca abajo y sale tirando con un dedo |
| P4 | Funda corta | Avisar de que retiene casi el doble que la entera |

### 6.3 Míos, en el contra-reporte de la v3

- **«Sobran unos 5 mm de alto.»** Era cierto para la pinza aplastada, no para la pinza a
  medida que yo mismo pedía. El report lo corrige bien.
- **El límite de 0,6 del pico articulado.** No conté el roce contra la piel. Es 0,41.
- **Los retenes.** Pedí «un resalte pequeño» y «dos resaltes de 0,3 mm» sin decir que algo
  tenía que flexar ni con qué fuerza. Se dibujaron tal cual.
- **La aguja como tirador.** Di el margen de 1,4 sin mirar de dónde se coge ni qué pasa al
  cerrar.
- **La precarga.** La pedí sin pensar cómo se ancla.

### 6.4 Del proceso

- **Cinco versiones, 165 parámetros, 17 probetas. Nada impreso. Nada medido.**
- **El método ha tocado techo.** En la v2 encontré fallos de centímetros. En la v3, de
  milímetros. En la v4, de décimas. Las décimas no se discuten sobre el papel: se miden en
  una pieza.
- **La fecha de entrega se ha preguntado cinco veces.** La tarjeta dice diciembre.

## 7. Qué recomiendo

**No una v5.** Un parche de cinco cambios en el generador de la v4, y a imprimir.

**Hoy, sin tocar nada:**

1. Imprimir **P0** de `probetas-v4/`. No depende de ninguno de estos fallos.
2. Medir el reloj, si está montado: contorno interior, y alto y fondo del lazo cerrado.

**Parche, antes de P1 y P2:**

3. Ranura de emergencia pasante, con su comprobación (G1).
4. Muesca cerrada para el taco y resalte en la tapa trasera (G2).
5. Puntas del rotor rebajadas 0,4 mm; holgura hacia el labio de 0,35 (I4).
6. Tapa trasera con pestaña y clip (I5).
7. Guía de montaje: cerrar girando la aguja de vuelta (I3).

**Si no quieres esperar al parche:** P1 se puede imprimir tal cual para probar lo principal,
que es si la aguja arrastra el rotor. Sujeta el taco con una gota de pegamento, solo en la
probeta, y lija las puntas del rotor si rozan.

**Después, con la medida:**

8. Retén de la peana con lengüeta, retén de la funda recalculado, chaflán de entrada en las
   guías (I1, I2, I8).
9. P3 y P4.

**Los imanes siguen cuadrando:** 8 en la caja, 2 en la aguja de repuesto y, si quieres, 1
bajo el rebaje de la aguja. 11 de 14.

## 8. Lo que solo puedes responder tú

1. **¿Qué día se entrega?**
2. **¿Está montado el reloj?** Si lo está, las tres medidas del apartado 7.
3. **¿Te vale cerrar girando la aguja de vuelta?** Es lo más robusto.
4. **¿Aguja con pomo?** Sin algo de donde coger, la aguja no puede sacar el panel.
5. **¿Pongo yo en la web la pista de apertura y el aviso del imán?**
