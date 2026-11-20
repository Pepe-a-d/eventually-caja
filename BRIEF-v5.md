# Eventually, la caja v5: iris y ascensor

Escrito el 20 de noviembre de 2026 por la sesión del Mac, a partir de la conversación de diseño con Pepe de ese día. **Sustituye a la v4.1, que queda parada.** Nada de esto está modelado ni impreso.

Cada dato dice de dónde sale: **decidido** (lo eligió Pepe), **estimado** (cuenta a mano de la sesión del Mac, sin CAD) o **supuesto** (medida del reloj sin confirmar).

## 0. Para la sesión del PC: qué ha pasado y qué tienes que saber

**Este documento manda sobre `contexto.md`, `README.md` y todo lo de la v4.** El apartado 0 de `contexto.md` dice que manda la v4 y que el siguiente paso es imprimir P0 y P1: eso ya ocurrió y ya no vale.

**Qué pasó el 20 de noviembre de 2026, en orden:**

1. Pepe imprimió **P0** de `probetas-v4\`. Salió bien: 5,15 mm de alojamiento, holgura de 0,15 mm, piel de 0,8 mm. La imprimió con capa de 0,08 mm, no de 0,2.
2. Imprimió **P1 y P2** con capa de 0,2 mm, 7 capas inferiores y pared Aracne.
3. **P1 falló:** los imanes no mueven el rotor, «ni de cerca». La llave magnética, que era la idea central desde el brief original, no funciona con imanes de 5 × 1,6 mm.
4. Pepe decidió **volver a la fase de diseño**. No quiso arreglar la v4.1.
5. En una conversación larga con la sesión del Mac eligió, sector por sector, el diseño de este documento.

Los resultados de las probetas están en `resultados-probetas.md`.

**Qué se descartó en esa conversación, para no volver a proponerlo:**

- La aguja como llave, y la aguja en general: ya no hay aguja.
- Cualquier mecanismo que dependa de imanes.
- El trinquete.
- Números o grabados en el iris.
- La tarjeta bajo el reloj (no cabe por el hueco).
- Una corona en el costado y una cara plana en el cilindro, como marca del frente.
- Engranajes escondidos del todo, o del todo a la vista.
- Girar la base en vez del bisel.
- El reloj tumbado.
- Engranajes que giran en su sitio: Pepe quiere que los satélites orbiten.

Siguen descartados de antes: palabras en la tapa, piezas de acero, pestaña de arrancar.

**Qué se puede aprovechar de la v4:**

- Los contornos de la frase (`frase-v3.json`) y la idea de la funda de campana con colchón de aire. Ahora es cilíndrica.
- La pinza en C de PETG y la peana, adaptadas: la peana ya no desliza entre guías, apoya sobre un pedestal de unos 72 mm y se coloca con dos imanes.
- El rebaje del NFC.
- Las holguras de P0 y los ajustes de impresión.
- La manera de trabajar: generador en Python, parámetros en una lista, probetas ya orientadas, reporte con lo que es del modelo, lo calculado y lo supuesto. `instrucciones-de-trabajo.md` sigue valiendo.

**Qué te pido al empezar:**

1. Pon al día `contexto.md` con un apartado nuevo que mande, y deja la v4 como histórica.
2. Empieza por el apartado 11 de este documento. Nada más.
3. Sube el guion con el que generaste los fotogramas del tutorial de la web (`frames/caja/`). Solo existe en el PC, y con la caja nueva habrá que rehacer el tutorial.

**Lo que este documento no sabe:** por qué exactamente falló P1 (si el rotor rozaba, con qué espiral se probó) y el resultado de repetir P0 con capa de 0,2 mm. Si te hace falta, pregúntaselo a Pepe.

## 1. Por qué hay una v5

- La probeta P1 de la v4.1 falló: los imanes de 5 × 1,6 mm no mueven el mecanismo. Detalle en `resultados-probetas.md`.
- Los cálculos decían que sí. **Lección: ninguna fuerza calculada se da por buena sin una pieza impresa que lo confirme.**
- Se hicieron cinco versiones sobre el papel antes de imprimir nada. **Lección: primero la probeta del mecanismo, después la caja.**
- Pepe pidió volver a diseñar desde cero, por sectores: mecanismo, forma, estética, experiencia.

## 2. La idea

Una caja cilíndrica blanca. Se gira el bisel de arriba, como el de un reloj: unos engranajes se mueven a la vista, la tapa se abre como el diafragma de una cámara y el reloj sube entero desde dentro, de pie y mirando al frente.

Ya no hay llave. La aguja azul desaparece. Lo único azul de la caja es un engranaje.

## 3. Lo decidido por Pepe

| Tema | Decisión |
| --- | --- |
| Mecanismo | Iris que se abre y ascensor que sube el reloj, movidos por un solo giro |
| Qué se gira | El bisel de arriba |
| Engranajes | Sí, para dar aire de relojería. **Planetario de verdad: los satélites dan vueltas alrededor del hueco** |
| Trinquete | No |
| Reloj | De pie sobre su soporte, esfera al frente, como en la v4. Sube entero |
| Tamaño | No hace falta que sea pequeña. Vale un tamaño normal de estuche de reloj |
| Plazo | Más de un mes desde el 20 de noviembre de 2026 |
| Lo azul | Un solo engranaje azul. Todo lo demás, blanco |
| Engranajes a la vista | Parcialmente, tipo esqueleto: se ven entre puentes |
| Bisel | Grafilado (canto estriado) |
| Iris | Liso, sin números ni grabados |
| Frente | Un índice en relieve, blanco sobre blanco, en el cuerpo bajo el bisel |
| Tramo muerto | Sí: al empezar a girar, los engranajes se mueven y no pasa nada |
| Imanes | Solo para dar sensación de calidad. **Nada puede depender de ellos** |
| Funda | Se mantiene: mármol, con la frase en azul y el NFC dentro |
| Tarjeta | En la funda, o fuera de la caja. No va bajo el reloj (no cabe) |

Siguen en pie de antes: sin palabras en la tapa, sin piezas de acero, impresora Bambu Lab X1 Carbon con AMS, etiqueta NFC de 25 mm.

## 4. Cómo se usa

1. Se levanta la funda. Sale despacio, por el colchón de aire.
2. Queda un cilindro blanco. Arriba, el bisel, los engranajes entre puentes y el iris cerrado en el centro.
3. Se sujeta el cuerpo con una mano y se gira el bisel con la otra.
4. Primer tramo: no pasa nada. Los engranajes giran.
5. Segundo tramo: el iris se abre.
6. Resto del giro: el reloj sube. Arriba, un «clac» suave.
7. Se coge el reloj con su soporte. El soporte sirve solo en la mesilla.
8. Para cerrar, se gira al revés.

La caja queda pensada para usarse a diario como expositor: reloj arriba de día, guardado de noche.

## 5. Arquitectura propuesta (estimada, a comprobar en CAD)

De dentro afuera. Lo fijo va unido a la base por dentro; lo que gira lo envuelve.

| Pieza | Fija o gira | Qué hace |
| --- | --- | --- |
| Base con jaula | Fija | Disco de abajo con tres columnas verticales por dentro. Las columnas guían la plataforma y sostienen el iris arriba |
| Plataforma con pedestal | Sube y baja | Disco con tres muescas (corren por las columnas, así no gira) y tres tetones (entran en la rampa del tubo). Encima, un pedestal de unos 72 mm que tapa el hueco del iris cuando está arriba |
| Tubo | Gira | Rodea la jaula. Por dentro lleva la rampa en espiral, de tres entradas. Es un pintalabios grande. Arriba termina en una pestaña hacia dentro, que pasa por encima del iris y lleva los ejes de los satélites |
| Carcasa del iris | Fija | Sobre las columnas. Dos platos con las láminas y su aro en medio |
| Rueda central | Fija | Aro dentado alrededor del hueco, unido al plato de arriba del iris |
| Satélites | Giran y orbitan | Seis ruedas pequeñas sobre la pestaña del tubo, entre la rueda central y el bisel. Cinco blancas y una azul |
| Bisel | Gira (es lo que se toca) | Aro exterior de arriba, grafilado por fuera y dentado por dentro. Apoya y gira sobre el borde del cuerpo |
| Puentes | Por decidir | Lo que tapa a medias los engranajes. Puede ser un aro que orbita con los satélites y los retiene, o puentes fijos que salen de la rueda central |
| Cuerpo | Fijo | Piel exterior unida a la base. Tapa el tubo, retiene el bisel y lleva el índice del frente |
| Soporte del reloj | Suelto | Pinza en C y peana, como en la v4, sobre el pedestal |
| Funda | Suelta | Campana cilíndrica de mármol con la frase, el NFC y la tarjeta |

**Cómo llega el giro del bisel al tubo.** Es un planetario con el centro hueco. La rueda central está fija. El bisel, dentado por dentro, es la corona y es la entrada. Los satélites ruedan entre los dos y arrastran sus ejes, que están en el tubo: el tubo es el portasatélites y es la salida. Propuesta de partida, con módulo 1,5: rueda central de 60 dientes, satélites de 12, bisel de 84. El tubo gira a 0,58 veces la velocidad del bisel (84 / 144) y en el mismo sentido. Con 144 dientes entre central y bisel caben 3, 4, 6 u 8 satélites repartidos por igual.

**Los satélites orbitan a la velocidad del tubo.** En todo el recorrido dan casi una vuelta completa alrededor del hueco (345°). El azul puede salir del índice del frente y volver casi a él cuando el reloj llega arriba: una vuelta, como el segundero.

**Reparto del giro del tubo** (menos de una vuelta, con topes):

| Tramo del tubo | Qué pasa |
| --- | --- |
| 0° a 45° | Nada. La rampa es plana y el iris no se mueve |
| 45° a 105° | Un tetón del tubo arrastra el aro del iris y lo abre. Después lo suelta y el iris queda abierto |
| 105° a 335° | La rampa sube la plataforma |
| 335° a 345° | Rampa plana: el reloj descansa arriba y no puede bajar solo |

Con esa relación, el recorrido entero es de **algo más de una vuelta y media de bisel** (unos 590°). El tramo muerto es una quinta parte de vuelta.

**El orden lo fijan la forma de la rampa y el tetón, no el roce.** Al cerrar pasa lo mismo al revés: el reloj baja y, al final, el tetón cierra el iris.

### Sobre «planetario»

Una primera versión de este documento decía que los satélites no podían orbitar, porque el iris fijo del centro había que sujetarlo atravesando la zona de los engranajes. **Era un error de la sesión del Mac.** Pepe pidió que orbitaran y hay salida: el iris se sujeta por dentro, sobre las columnas de la jaula; la rueda central va fija encima del iris; y los ejes de los satélites van en la pestaña del tubo, que rodea a la rueda central sin tocarla. Nada fijo atraviesa nada que gire.

Lo que hay que comprobar en CAD: que la pestaña del tubo cabe entre el plato del iris y los satélites, y que la pared de la rueda central (entre el hueco de 75 mm y el pie de sus dientes) no queda demasiado fina.

## 6. Medidas (estimadas)

| Qué | Valor | De dónde sale |
| --- | --- | --- |
| Reloj: cabeza | 40 mm, 43,5 con corona, 11 de grueso | Supuesto: un 40 mm estándar. El reloj no está montado |
| Brazalete cerrado | Óvalo de unos 67 × 53 mm | Supuesto |
| Reloj de pie, visto desde arriba | Unos 44 × 53 mm | Estimado |
| Hueco libre del iris | 75 mm | Estimado: la diagonal anterior más 3 mm por lado |
| Carcasa del iris | Unos 125 a 130 mm de diámetro | Estimado: 1,6 a 1,7 veces el hueco. **Lo decide la probeta 1** |
| Caja sin funda | Unos 150 mm de diámetro y 135 de alto | Estimado |
| Recorrido del ascensor | Unos 88 mm | Estimado: alto del reloj más el grueso del iris |
| Pendiente de la rampa | Unos 18° | Estimado. Está en el límite de sujetarse sola por roce. **Lo decide la probeta 2** |

El reloj queda arriba dentro de un rebaje de unos 11 mm, rodeado por el aro de engranajes.

## 7. Imanes

Quedan 13 de 5 × 1,6 mm. Se usan 9, todos de adorno:

| Dónde | Qué se nota | Cuántos |
| --- | --- | --- |
| Final del recorrido | Un «clac» al llegar arriba y otro al cerrar del todo | 3 |
| Funda | Los últimos milímetros baja sola y se asienta | 4 |
| Soporte del reloj | Al devolverlo, se coloca solo y mirando al frente | 2 |

- Si se quitan los nueve, la caja tiene que funcionar igual.
- Ninguno a menos de 30 mm de la cabeza del reloj.
- Siempre imán contra imán: no hay piezas de acero.

## 8. Estética y acabados

- Blanco papel en todo, mármol en la funda, un satélite azul.
- La frase «Who cares, / I'm already late.» en azul, en la funda, con Reenie Beanie.
- Bisel grafilado. Iris liso. Índice del frente en relieve.
- Sin decidir: cuerpo liso o con estrías verticales; cuántos puentes y con qué forma; si va algo grabado bajo la base («Late Edition · 1 of 1»); si hay frase escondida bajo el soporte.

## 9. Puntos débiles conocidos

1. **El iris.** Láminas finas que rozan. Es lo más difícil y lo primero que hay que probar.
2. **Puede no cerrar del todo.** Suele quedar un agujero de pocos milímetros en el centro.
3. **La tapa es frágil.** La protege la funda.
4. **La rampa puede no sujetar el reloj a medio subir.** Arriba sí, por el tramo plano.
5. **Muchas piezas:** unas 25, frente a las 9 de la v4.
6. **Tamaño.** Es más grande que un estuche normal.
7. **Las medidas del reloj son supuestas.** El hueco del iris depende de ellas.
8. **La web.** El tutorial «¿Cómo se abre la caja?» describe la v4.1: fotogramas y textos hay que rehacerlos. La web también nombra la llave y sus imanes en «Por si acaso».

## 10. Orden de trabajo

No se modela la caja entera hasta que pasen las tres probetas.

| Orden | Probeta | Qué decide |
| --- | --- | --- |
| 1 | **Iris**, a tamaño real | Si el concepto vale, y el diámetro de la caja |
| 2 | **Ascensor**: tubo, jaula y plataforma con 150 g encima | Pendiente de la rampa, juego, si se sujeta sola |
| 3 | **Planetario**: bisel, satélites y rueda central | Tacto del giro, módulo, holguras |
| 4 | La caja entera | |

**Plan B:** si el iris no sale en dos rondas, dos compuertas correderas movidas por un piñón entre dos cremalleras. Aprovecha el mismo ascensor.

## 11. Encargo de la probeta 1: el iris

Para la sesión del PC, con Fusion.

**Qué se quiere saber.** Si un iris impreso en PLA, con 75 mm de hueco libre, abre y cierra suave girando un aro, y qué diámetro exterior necesita.

**Qué se modela.** Solo el iris, suelto: plato de abajo, láminas, aro que las mueve y plato de arriba. El aro saca una orejeta por el canto para moverlo con el dedo. Sin engranajes, sin tubo, sin caja.

**Requisitos.**

| Requisito | Valor |
| --- | --- |
| Hueco libre, abierto | 75 mm o más, redondo |
| Agujero central, cerrado | 8 mm o menos. Mejor cero |
| Giro del aro de cerrado a abierto | 60° o menos |
| Diámetro exterior de la carcasa | El menor posible. Objetivo: 130 mm o menos |
| Grueso total | 10 mm o menos |
| Láminas | 6 a 8, de 1,2 mm de grueso o más |
| Impresión | PLA blanco, capa de 0,2 mm, sin soportes, pared Aracne |
| Montaje | Sin pegamento ni tornillos. Boca abajo no se cae ninguna lámina |

**Holguras.** La P0 dio, con capa de 0,08 mm: a 0,10 mm por lado sujeta y a 0,15 pasa sin forzar. A 0,2 mm de capa no hay resultado todavía. Para piezas que se mueven, partir de 0,2 mm y decirlo en el reporte.

**Si sale barato, dos variantes** en la misma bandeja: una de 6 láminas y otra de 8.

**Comprobar en el modelo**, grado a grado, que ninguna lámina choca con otra ni con los platos en todo el giro. Y recordar que «sin choques» no es «funciona».

**Qué entregar.**

- Los `.3mf` ya orientados, en `probetas-v5\`.
- Una página con: diámetro exterior, hueco abierto, agujero cerrado y giro del aro, medidos en el modelo; qué es supuesto; y una tabla «vale si» para que Pepe pruebe la pieza.
- Antes de modelar: si algo de este encargo no se puede cumplir o tiene una forma mejor, decirlo primero.

**Vale si**, con la pieza en la mano: abre y cierra 20 veces con un dedo sin engancharse; abierta, pasa un cilindro de 75 mm; cerrada, no deja ver lo de dentro salvo el agujero central; boca abajo no se desmonta.
