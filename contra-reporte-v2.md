# Eventually, la caja: contra-reporte de la v2

Revisión crítica del prototipo v2 y lista de lo que hay que cambiar para la v3.

Escrito el 19 de noviembre de 2026 sobre el commit `e340db5` del repositorio. He leído
`reporte-v2/reporte-v2.md`, `contexto.md`, `parametros-fusion-v2.csv`, `generador_caja_v2.py`
entero y las trece figuras. No he abierto el modelo en Fusion ni he impreso nada: lo que
sigue sale de leer la geometría en el generador y de cálculos propios.

Cada cifra lleva su procedencia: **del modelo** (leída en el generador), **calculada** (por
mí, con el método indicado) o **juicio** (opinión de diseño, sin número detrás).

---

## 1. Veredicto

La v2 es un buen concepto con un mecanismo que probablemente funciona, metido en una caja
que todavía no se puede usar.

- **Lo que más preocupaba al report está mejor de lo que dice.** Que el imán arrastre el
  rotor (R1) sale con margen en el cálculo. La magnetización del reloj, también.
- **Los problemas de verdad están donde el report no mira.** El reloj no se puede montar en
  el soporte. Cerrar la caja es torpe. No hay forma de abrirla si el pestillo se atasca. La
  tarjeta ni se ve ni se queda. La aguja vive fuera, al revés de lo que pediste.
- **Una idea del report no funciona:** el «cierre por gravedad». La gravedad no vence ni
  al rozamiento del rotor.
- **Se han modelado tres versiones sin imprimir una sola pieza.** La v3 no debería
  empezar en Fusion, sino en la impresora, con cinco probetas pequeñas.

- **La v2 no se puede montar con lo que hay**: pide 24 imanes y Pepe tiene 14, sin chapas
  de acero.

Hay 6 fallos graves, 11 importantes y una lista de defectos del propio report. Al final
va la especificación de la v3 y el plan de pruebas.

## 2. Lo que la v2 hace bien

Para no tirar lo que funciona:

- **Abrir por delante.** Convierte la caja en vitrina y arregla el acceso de la v1. Es la
  decisión correcta.
- **Sacar el imán central del eje del reloj.** En la v1 quedaba sobre el cristal.
- **La frase sale del fichero de fuente real de la web**, no de una parecida.
- **El generador.** Todo el modelo se reconstruye desde un script. Eso hará barata la v3.
- **La honestidad del report.** Separa lo comprobado de lo supuesto y dice que nada está
  impreso. El apartado «Lo que falta» es lo mejor del documento.

## 3. Lo que he comprobado por mi cuenta

El report no da ninguna fuerza. Las instrucciones del proyecto dicen «no inventar fuerzas
de imán», y se ha interpretado como «no calcularlas». Se pueden calcular.

**Método.** Dos discos de 5 × 1,6 mm imantados en el eje, modelo de cargas superficiales,
integración numérica. Remanencia 1,2 T (grado N35). Si tus imanes son N52, las fuerzas
suben un 45 %; los cocientes no cambian. Tómalo como ±30 %.

### 3.1 Fuerza entre dos imanes enfrentados (calculada)

| Separación | Fuerza | Dónde ocurre en la v2 |
| --- | --- | --- |
| 0,8 mm | 2,1 N | aguja guardada en la funda |
| 1,2 mm | 1,55 N | cubo de la aguja contra el imán central |
| 1,4 mm | 1,34 N | cada esquina del panel |
| 1,5 mm | 1,25 N | cola de la aguja contra el rotor |
| 2,0 mm | 0,89 N | |
| 3,0 mm | 0,48 N | |

El panel lo sujetan cuatro esquinas: **5,4 N en total**, medio kilo.

### 3.2 El arrastre del rotor: R1 (calculado)

Al girar la aguja, su imán se adelanta al del rotor y tira de él de lado.

| Dato | Valor |
| --- | --- |
| Arrastre lateral máximo, a 1,5 mm de separación | 0,59 N, con 2,5 mm de desfase |
| Par máximo sobre el rotor (brazo de 13,5 mm) | 8,0 mN·m |
| Cociente arrastre / fuerza axial con 0,5 mm de desfase | 0,18 |
| Con 1,5 mm de desfase | 0,57 |
| Con 2,5 mm de desfase | 1,20 |

Lo que frena al rotor es el rozamiento contra la piel, y ese rozamiento lo crea la misma
atracción del imán. Por eso lo que importa es el **cociente**, no la fuerza. El plástico
contra plástico roza entre 0,3 y 0,5: el rotor echa a andar cuando el desfase llega a
1,0–1,4 mm, y el cociente sigue subiendo hasta 1,2.

**Conclusión: el rotor debería seguir a la aguja, con un retraso de 4° a 6°.** Hay margen
de 2 a 4 veces. Dos consecuencias:

- Apilar dos imanes, que el report propone como remedio, **no arregla nada**: sube el
  arrastre y el rozamiento a la vez. Lo que ayuda es bajar el rozamiento o alargar el brazo.
- Hay margen para **engordar la piel**, que hace falta por otros motivos (apartado 5).

### 3.3 El cierre por gravedad (calculado): no funciona

| Par | Valor |
| --- | --- |
| Gravedad sobre el imán del rotor, a 40° | 20 µN·m |
| A 10° | 5 µN·m |
| Rozamiento del rotor sobre su eje, solo por su peso (2 g, µ = 0,3) | 25 µN·m |
| Arrastre de la aguja, para comparar | 8 000 µN·m |

La gravedad es más débil que el rozamiento en todo el recorrido, y tiende a cero justo al
llegar a cerrado. El rotor **se queda donde lo dejes**. Además, con la caja tumbada no hay
gravedad que valga.

### 3.4 El enganche real (del modelo y calculado)

| Giro del rotor | Cuánto entra el pestillo |
| --- | --- |
| 0° a 4° | 1,30 mm |
| 10° | 1,25 mm |
| 15° | 0,93 mm |
| 20° | 0,33 mm |
| 22,1° | 0: libre |

El report dice «bloqueado de 0° a 20°». A 20° quedan 0,33 mm, menos que los juegos
sumados (0,2 del panel y 0,3 del eje del rotor). **El bloqueo fiable acaba hacia los 15°.**
Y la apertura empieza en 22,1°, no en 25°: la comprobación del generador prueba de 5 en 5
grados.

### 3.5 Imanes y reloj (calculado): riesgo bajo, con una excepción

Campo en el eje de un imán, frente al límite de la norma ISO 764 (4 800 A/m):

| Distancia | Campo | Frente al límite |
| --- | --- | --- |
| 4 mm | 31 000 A/m | 6,5 veces por encima |
| 8 mm | 6 300 A/m | por encima |
| 11 mm | 2 700 A/m | la mitad |
| 24 mm | 310 A/m | 15 veces por debajo |
| 52 mm | 32 A/m | despreciable |

- El imán central está a 23,7 mm del centro del movimiento (**del modelo**): 15 veces por
  debajo del límite, 8 veces con la aguja puesta.
- Los imanes de los patines están a 51,6 mm: despreciable.
- **La excepción es la aguja suelta.** Son dos imanes sin dueño. Si Pablo la apoya sobre
  el reloj, a 4 mm supera el límite seis veces. Hay que avisarlo en la tarjeta o en la web.

### 3.6 El soporte y el brazalete (calculado)

| Dato | Valor |
| --- | --- |
| Perímetro del anillo del soporte | 172,5 mm |
| Contorno mínimo que rodea anillo y patín | 212 mm |
| El reloj sobresale por delante del patín | 6,1 mm |
| Centro de gravedad de la cabeza, por detrás del frente del patín | 8,2 mm |
| Hueco tras el anillo con un cierre de 7 mm de grueso | 1,9 mm |

## 4. Fallos graves

Cualquiera de estos impide dar la caja por buena.

### G1. El reloj no se puede montar en el soporte

**Qué pasa.** El anillo lleva un patín pegado a cada lado. Un brazalete con cierre de
mariposa no se abre en línea: es siempre un aro. Para ponerlo hay que pasar el aro por
encima de un patín, y eso pide 212 mm de contorno. Un brazalete ajustado a una muñeca de
175 mm, con el cierre abierto, da unos 210–215 mm (**estimado**: depende del cierre). Pasa
rozando o no pasa.

**Y además el tamaño es fijo.** El anillo mide 172,5 mm de perímetro. Si la muñeca de
Pablo es de 165 mm, el brazalete ni cierra. Si es de 185, baila 12 mm y la cabeza se cae
hacia delante. El report trata el óvalo como «supuesto a medir», pero no depende del
reloj: depende de **la muñeca de Pablo**, que nadie ha preguntado.

**Para la v3.**
- Soporte en dos piezas: una **pinza en C** donde se abrocha el reloj y una **peana**
  donde encaja la pinza. El reloj se monta en la pinza suelta, sin patines que estorben.
- La pinza es elástica y vale para brazaletes de 160 a 200 mm.
- Imprimirla en PETG: el PLA cede con el tiempo bajo carga y la pinza se aflojaría.
- Perfil de extrusión pura, para imprimirla de lado **sin soportes**.
- Hueco para el cierre: 8 mm, no 4,5.

### G2. Cerrar la caja es torpe

**Qué pasa.** En reposo los pestillos asoman 1,3 mm por arriba y por abajo del panel. Con
el rotor así, el panel no entra. Para cerrar hay que poner la aguja, girarla, sujetarla
girada, meter el panel con la otra mano y devolverla. El report lo resume en una línea,
«panel dentro con la aguja girada», como si fuera trivial.

**Para la v3.** Un pestillo de resbalón, como el de cualquier puerta:
- Los extremos del rotor llevan un **chaflán** en la cara de entrada. Al empujar el panel,
  el borde de la boca empuja el chaflán y aparta el rotor solo.
- Algo lo devuelve a cerrado al llegar al fondo. Ver G3.
- Resultado: **cerrar es empujar; la aguja solo hace falta para abrir.**

### G3. El «cierre por gravedad» no existe

**Qué pasa.** Ver 3.3. Nada devuelve el rotor a cerrado ni lo mantiene ahí. En el
transporte queda donde caiga.

**Para la v3.** Un **muelle impreso**: un brazo fino de plástico, parte del propio rotor,
que apoya en un tetón del panel y lo empuja hacia cerrado. Ni acero ni imán.
- Par objetivo: en torno a 1 mN·m con el rotor abierto. Es 40 veces el rozamiento y la
  octava parte de lo que tira la aguja.
- Se ajusta con el grosor del brazo (0,6 a 1,0 mm). Va en la probeta P2.
- **En cerrado queda relajado.** El plástico solo trabaja mientras la aguja lo tiene
  abierto, así que no cede con el tiempo.
- La aguja puesta lo sujeta abierto: su rozamiento contra el panel es unas seis veces el
  par del muelle (**estimado**: 6,5 frente a 1 mN·m). Giras, sueltas y tiras del panel.
- **Al quitar la aguja, el pestillo vuelve solo a cerrado.** Quitar la llave echa el cierre.

### G4. Si el pestillo se atasca, la caja no se abre

**Qué pasa.** La tapeta es una chapa de 1 mm que entra «a presión o pegada»; sin rigidez
para sujetarse sola, acabará pegada, sobre un rotor con 0,3 mm de juego. Una rebaba, una
gota de pegamento que corra o un imán que se despegue, y el rotor se queda en cerrado con
el reloj dentro. La única salida es romper el panel.

**Para la v3.**
- **Apertura de emergencia**: un taladro de 1,5 mm en el techo de la caja, sobre el
  extremo del rotor, para empujarlo con un clip. Con la funda puesta no se ve.
- **Tapeta desmontable**: a presión con pestañas o con dos tornillos pequeños. Nada de
  pegamento junto a una pieza móvil.

### G5. La tarjeta ni se ve ni se queda

**No se ve.** La tarjeta hace de «telón de fondo», pero el soporte mide 46 mm de ancho y
va centrado delante. Tapa el centro y deja 19,5 mm a cada lado (**calculado**). El centro
es donde pone «Eventually».

**No se queda.** Las guías la solapan 1,0 mm por lado y su cara de retención es una rampa
a 45° (**del modelo**). Una rampa en el lado que retiene no retiene: empuja la tarjeta
hacia el centro y la ayuda a saltar. El report lo deja como duda; con esa geometría, se
saldrá.

**Para la v3.** Dos opciones:
- En el interior del panel frontal, en dos carriles: al abrir, lo primero que tienes en
  la mano es la tarjeta.
- En el suelo de la caja, delante del soporte, inclinada como un cartel de museo.

En los dos casos, carriles en U con tope recto, no cuñas.

### G6. La aguja vive fuera, a la vista y expuesta

**Qué pasa.** La aguja va en el exterior de la funda, sobresaliendo 1 mm, sujeta por dos
imanes.
- **Contradice lo que pediste**: «la exterior podría poner algo escrito mientras que la
  interior tendría la aguja».
- **Estropea la sorpresa**: la llave se ve antes de saber que hay cerradura.
- **Es frágil y es única**: 1,2 mm de varilla, en el exterior de un paquete. Un roce en
  una bolsa y se pierde o se parte. Sin ella no hay regalo.

**Para la v3.** La aguja se guarda **en la caja interior**, en un rebaje a ras con su
silueta, en la cara de arriba. Al retirar la funda aparece un bloque blanco con una aguja
azul tumbada encima. Con la funda puesta queda protegida del todo.

## 5. Fallos importantes

### I1. Abrir no da ninguna señal y termina con una uña

Giras 40°, no suena nada, el panel no se mueve, y hay que hurgar con la uña en una muesca
lateral contra 5,4 N. Para una caja que quiere parecer cara, es el peor momento.

**Para la v3.**
- Un tope de final de recorrido que se note en la mano. La aguja se queda donde la dejes
  y mantiene el pestillo abierto (G3).
- Fuera la muesca lateral. En su lugar, un **bisel a todo lo ancho bajo el borde inferior
  del panel**, una línea de sombra donde entra la yema del dedo.
- Bajar la sujeción del panel de 5,4 N a unos 2 N: dos imanes en vez de cuatro, o más
  retirados.
- Opción a valorar: que el cubo de la aguja sea un pequeño pomo y la aguja sirva también
  de tirador. Gira y tira. Choca con tu petición de una aguja fina; decides tú.

### I2. Es grande: 98 × 92 × 83 mm para un reloj de 40

Tres cuartos de litro. Sale de poner de pie un óvalo de muñeca entero, más 5 mm de aire
por cada lado. Con la pinza en C aplanada y la tarjeta fuera del fondo, el objetivo
razonable es bajar el fondo de 92 a unos 75 mm. Es un objetivo, a confirmar con el
brazalete real.

### I3. La funda está pensada al revés para imprimirla

La frase va en una pared vertical. Eso obliga a:
- **Engordar la letra** 0,2 mm por lado. En la figura 1 ya no parece un boli: parece un
  rotulador gordo. Se pierde justo el trazo fino de la esfera.
- Cambiar de color en unas 110 capas, con su purga y sus horas.
- Pelearse con la textura de papel, que se aplica a las paredes y estropea el borde de las
  letras.

La otra orientación que propone el report deja un techo en puente de 79 mm con soportes
sobre una cara que desliza.

**Para la v3: funda de campana.** Abierta por abajo, se levanta en vertical, como la tapa
de una caja de móvil.
- La frase va en la **cara de arriba**, que es la que toca la cama: sale nítida, con
  cambio de color en 3 capas y sin engordar el trazo.
- Las cuatro paredes son verticales y sin texto: la textura de papel se aplica sin
  conflicto y el interior queda liso.
- Sin puentes ni soportes.
- Con 0,25–0,3 mm de holgura, la caja baja despacio por el colchón de aire.
- El NFC va bajo la frase: se toca donde se lee.

### I4. Hay 14 imanes y la v2 pide 24

- **No hay imanes para la v2.** Pepe los ha contado: tiene **14** (y alguno suelto más).
  La v2 usa 24, más 2 por cada aguja de repuesto. El `contexto.md` decía «tiene de
  sobra»: estaba mal. La v3 tiene que salir con 14 como máximo.
- Seis quedan **desnudos en caras exteriores** de la caja blanca: cuatro en la trasera y
  dos en la pared izquierda. Rompen la regla «todo blanco y liso».
- 24 imanes con polaridad son 24 ocasiones de pegar uno al revés.

**Para la v3: presupuesto de 14, solo con imanes.** Pepe no tiene chapas de acero, así
que no se cuenta con ellas. Donde la v2 ponía un imán para sujetar algo, la v3 usa la
forma de la pieza.

| Función | Imanes | Cómo se resuelve |
| --- | --- | --- |
| Aguja: cubo y cola | 2 | |
| Panel: imán central fijo | 1 | centra la aguja |
| Rotor | 1 | en el brazo de abajo, como en la v2 |
| Sujeción del panel | 4 | dos parejas, en esquinas opuestas |
| Retorno del pestillo | 0 | muelle impreso (G3) |
| Aguja guardada | 0 | rebaje a ras en la cara de arriba; la funda la tapa |
| Funda de campana | 0 | baja por el colchón de aire |
| Peana del soporte | 0 | encaja por forma |
| Panel al derecho | 0 | una esquina achaflanada (I11) |
| **Caja completa** | **8** | |
| Aguja de repuesto | 2 | |
| **Total con un repuesto** | **10** | **quedan 4 de reserva** |

Con la reserva se puede, por orden de utilidad: dar un clic a la aguja guardada (1), hacer
el rotor simétrico (1) y dar un clic a la peana (2).

Dos parejas a 1,4 mm sujetan el panel con 2,7 N (**calculado**), cerca de los 2 N que
pide I1. Si queda duro, se retiran 0,3 mm más.

Nota: las monedas de 1, 2 y 5 céntimos de euro son de acero y se pegan a un imán. Si en
algún punto falta un imán, una moneda embutida hace de pareja. No se cuenta con ello.

Además:
- Los que queden en caras vistas, metidos con pausa de impresión bajo 0,4 mm de plástico.
- Una **guía de montaje** con el orden y la cara de cada imán.
- **En las probetas, los imanes no se pegan**: entran a presión y se recuperan. Un imán
  pegado con cianoacrilato es un imán gastado.

### I5. La piel de 1 mm

- **Se transparenta** (**juicio**, a comprobar): 1 mm de PLA blanco deja pasar luz. El
  imán central toca la piel por dentro y es oscuro. Lo probable es un punto gris en el
  centro de un panel que tenía que ser liso.
- **Flexa**: sobre la cámara del rotor la piel queda sin apoyo en vanos de más de 30 mm.

**Para la v3.** Piel de 1,4 mm con una capa de relleno opaco, y el imán central 0,4 mm
retirado. El cálculo de 3.2 dice que hay margen: a 2 mm de separación aún quedan 0,89 N.

### I6. La aguja

- **Los imanes van al aire por la cara que toca el panel.** Níquel contra PLA blanco
  mate: dejará marcas grises. Y un imán a presión puede quedarse pegado al panel.
- **La silueta.** Con un disco de 8,6 mm en la cola y un cubo de 9, lo que se lee son dos
  bolas y una flecha: una mancuerna. El segundero del reloj tiene cubo y **pala**.
- **Frágil**, como admite el report.

**Para la v3.** Imanes embutidos con pausa, 0,4 mm de plástico por debajo. Cola en forma
de pala, con el imán dentro. Varilla mínima de 1,6 mm. Imprimir tres.

### I7. El panel aparcado sobra

Pegado a la trasera es una losa que sobresale, con el pestillo asomando (figura 4). Cuesta
4 imanes desnudos. El panel puede guardarse dentro de la funda. **Fuera.**

### I8. El soporte necesita soportes para imprimirse

Lo admite el report. Con el perfil de G1, desaparece.

### I9. El NFC no dice dónde está y se va con la funda

Está en el techo, sin marca, mientras la frase está en el frente. Nadie sabrá dónde
acercar el móvil. Se resuelve con I3.

### I10. Enganche escaso y giro corto

1,3 mm nominales que se quedan en 0,8 con los juegos en contra. Y 40° de giro para un
gesto que tiene que notarse.

**Para la v3.** Enganche de 2 mm, juego del eje de 0,15 mm y giro de 50°. La apertura
pasa a unos 26°, con 24° de margen para el retraso de la aguja.

### I11. El panel se puede montar boca abajo

El report propone resolverlo invirtiendo polaridades, que añade riesgo al montaje y no
impide nada: solo hace que el panel no se pegue. Mejor por forma: **una esquina del panel
y de la boca achaflanada**, como una tarjeta SIM. Solo entra de una manera y no gasta imán.

Si sobra un imán de la reserva, la alternativa es un rotor simétrico, con imán en los dos
brazos: entonces da igual cómo se monte.

## 6. Fallos del report y del proceso

- **Las comprobaciones son más flojas de lo que parecen.** «Sin interferencias» solo dice
  que nada se solapa; no mide holguras. El pestillo se prueba cada 5°. «Cabe en la X1» y
  «el QR lleva a la web» no comprueban el diseño.
- **El reloj de referencia es un disco.** Sin corona, sin brazalete y sin cierre. Las
  cotas de «5 mm de aire» de la figura 10 se miden contra un objeto que no existe. El
  brazalete es la pieza más grande que hay dentro y no está dibujada.
- **No hay ni una fuerza.** Todo el riesgo principal se deja en «solo se sabe imprimiendo».
  Un cálculo de diez minutos lo acota.
- **No es «todo paramétrico».** La regla dice que ningún número va a mano en el modelo. El
  generador tiene más de veinte: el retranqueo de los imanes de esquina (4,5), los radios
  del eje (4,0 / 4,3 / 7,0 / 7,3), el margen de la cámara (0,3), el hueco de la tarjeta
  (0,6), los radios de las muescas (9 y 12) y del plato de la aguja (8,5), entre otros.
- **Sin plan de pruebas.** Se dice qué imprimir primero, pero no qué resultado vale.
- **Sin guía de montaje.** 24 imanes, una tapeta que se pega y un orden que importa (el
  imán central y el rotor entran antes que la tapeta), y nada escrito.
- **Sin probeta de tolerancias.** Las holguras de 0,15 / 0,2 / 0,3 mm son de libro, no de
  tu impresora.
- **Tres versiones sin imprimir.** El brief ya decía «primero la probeta». Se han hecho
  dos modelos completos, 75 parámetros y un report de 17 páginas antes de imprimirla.
- **Documentos que se contradicen.** `BRIEF.md` sigue en la raíz diciendo H2, tapa por
  arriba y seis piezas. El `README` dice X1 Carbon. Debería ir a una carpeta `archivo/`.

## 7. Otros enfoques

**A. Evolucionar la v2 (recomendado).** Mantener la apertura frontal y la llave magnética,
y cambiar funda, soporte, pestillo y sitio de la aguja y de la tarjeta. Es lo que detalla
el apartado 8.

**B. Parche mínimo, si el plazo aprieta.** La v2 con seis cambios: soporte en dos piezas
(G1), chaflán y muelle (G2, G3), taladro de emergencia (G4), aguja dentro (G6), tarjeta en
el panel (G5) e imanes de la aguja tapados (I6). Se queda grande y con la frase gorda,
pero se puede regalar.

**C. Plan B del mecanismo.** Solo si la probeta de la llave falla, cosa que el cálculo no
espera: la aguja con eje pasante y rampa helicoidal. Se pierde el panel sin agujeros.

## 8. Especificación de la v3

**Imprescindible**

1. Soporte en dos piezas: pinza en C elástica y peana. Hueco de 8 mm para el cierre.
2. Pestillo de resbalón: chaflán en los extremos del rotor y entrada guiada en la boca.
3. Muelle impreso que devuelve el pestillo a cerrado. Quitar el «cierre por gravedad».
4. Taladro de emergencia de 1,5 mm sobre el rotor. Tapeta desmontable, sin pegamento.
5. Aguja guardada en la cara superior de la caja interior, a ras.
6. Tarjeta en carriles en U: en el interior del panel o delante del soporte.
7. Imanes de la aguja embutidos; cola en pala; varilla de 1,6 mm como mínimo.
8. Enganche de 2 mm, juego del eje de 0,15 mm, giro de 50°.
9. Una esquina del panel achaflanada, para que solo entre al derecho.
10. Reloj de referencia completo: cabeza, corona, brazalete y cierre.

**Recomendado**

11. Funda de campana, con la frase en la cara de arriba y el NFC debajo.
12. Frase sin engordar, o con el mínimo que pida la primera capa.
13. Bisel de apertura a todo lo ancho. Fuera la muesca lateral.
14. Piel de 1,4 mm con relleno opaco.
15. Sujeción del panel en torno a 2 N.
16. **14 imanes como máximo, y solo imanes** (pasa a imprescindible): 8 en la caja, 2 en
    la aguja de repuesto y 4 de reserva. Ninguno a la vista.
17. Fuera el panel aparcado.
18. Redondeos: 1 mm en aristas exteriores, 0,5 mm en las de la boca.
19. Todos los números del generador, a `P_DEF`.
20. `BRIEF.md` y la v1, a una carpeta `archivo/`.

**A valorar contigo**

21. Aguja con pomo, que sirva de tirador.
22. Aviso en la tarjeta o en la web: «la aguja es un imán; no la apoyes en el reloj».
23. Algo escrito por dentro, como «Llegará. Cuando llegue.», pregunta abierta desde el brief.

## 9. Plan de pruebas, antes de modelar la v3

Cinco probetas pequeñas, cada una con su criterio.

| # | Probeta | Qué se imprime | Vale si |
| --- | --- | --- | --- |
| P0 | Tolerancias | Una tira con alojamientos de imán de 5,05 a 5,30 mm, encajes de 0,10 a 0,35 mm y chapas de 0,8 / 1,0 / 1,2 / 1,4 mm con un imán detrás | Se elige un alojamiento que entra a presión con el dedo, una holgura que desliza sin bailar y un grosor de piel que no deja ver el imán |
| P1 | Llave | Panel, rotor, tapeta y aguja de la v2, con la piel elegida en P0 | La aguja arrastra el rotor 10 de 10 veces, de pie, tumbada y boca abajo, con menos de 10° de retraso |
| P2 | Resbalón | Un aro de 15 mm de la boca de la caja, y el panel con rotor achaflanado y muelle impreso, en tres grosores de brazo | El panel cierra de un empujón 20 de 20 veces y no sale sin aguja. Agitado un minuto, sigue cerrado. Al quitar la aguja, el pestillo vuelve solo |
| P3 | Soporte | Pinza en C y peana | El reloj real se monta con una mano, no gira y no vuelca con un golpe en la mesa |
| P4 | Funda | Un tramo de 40 mm de campana, con la frase en la cara de cama y el NFC | La letra se lee fina. La funda baja sola y despacio. El móvil lee el NFC con el reloj dentro |

P0 y P1 se pueden imprimir hoy con lo que hay. P1 decide si se sigue por A o por C.

Las cinco probetas usan como mucho 8 imanes a la vez. Como no se pegan, son los mismos
que luego van a la caja.

## 10. Lo que solo puedes responder tú

1. **¿Cuándo se entrega el regalo?** Decide entre A y B.
2. **¿Cuánto mide la muñeca de Pablo, y está ya ajustado el brazalete?** Es la medida que
   más manda y no aparece en ningún documento.
3. **¿Tienes el reloj montado?** Hacen falta ancho con corona, grosor, tipo de cierre y
   contorno del brazalete cerrado y abierto.
4. **¿De qué grado son los imanes?** N35, N42 o N52. Si no lo sabes, P1 lo dirá.
   Cuántos hay, ya lo sabemos: 14.
5. **¿Funda de campana?** Cambia el gesto: levantar en vez de deslizar de lado.
6. **¿Aguja plana o con pomo?**
7. **¿La frase fina, como en la esfera, o gruesa, como ahora?**
